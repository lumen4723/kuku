const MYSQL_SERVER_URL: &'static str = "mysql://kukudev:rhdqngofk!%40%23@127.0.0.1:20022/kuku_dev";

mod language;
use std::collections::HashMap;

use language::*;
use mysql_async::prelude::*;
use mysql_async::Conn;
use rayon::prelude::*;
use tokio;

#[derive(Debug)]
enum Job {
    CPlusPlus(language::CPlusPlus),
    Java(language::Java),
    Python(language::Python),
    Unknwon(u64),
}
impl Job {
    pub fn run(mut self) -> RunResult {
        let result = match self {
            Job::CPlusPlus(mut c) => c.run(),
            Job::Java(mut j) => j.run(),
            Job::Python(mut p) => p.run(),
            Job::Unknwon(id) => RunResult::error(id, "Unknown language".to_string()),
        };

        println!("--> result {:?}", result);
        return result;
    }
}

#[derive(Debug)]
enum ControlType {
    Input(String),
    Stop,
}
struct Control {
    cmd_id: usize,
    id: usize,
    data: ControlType,
}

fn main() {
    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(main_loop());
}

async fn main_loop() {
    let new_job_notifier = tokio::sync::mpsc::unbounded_channel::<(
        usize,
        Option<tokio::sync::mpsc::UnboundedSender<ControlType>>,
    )>();

    tokio::spawn(check_controls(new_job_notifier.1));
    let new_job_receiver = new_job_notifier.0;

    loop {
        let jobs = list_jobs().await;

        println!("--> code_jobs return {:?}", jobs);
        if let Ok(mut jobs) = jobs {
            println!("--> select code_jobs {:?}", jobs);

            if jobs.len() == 0 {
                continue;
            }

            let results: Vec<RunResult> = jobs.par_drain(..).map(|job| job.run()).collect();

            tokio::spawn(update_jobs(results));
        }
    }
}

// 동시성 문제가 있긴 할 듯 함. (프로그램이 종료된 직후에 취소 요청이 올 경우... 또는 프로그램이 실행되기 전에 명령이 올 경우)
async fn check_controls(
    mut rx: tokio::sync::mpsc::UnboundedReceiver<(
        usize,
        Option<tokio::sync::mpsc::UnboundedSender<ControlType>>,
    )>,
) {
    let mut job_ongoing: usize = 0;
    let mut job_controller: HashMap<usize, tokio::sync::mpsc::UnboundedSender<ControlType>> =
        HashMap::with_capacity(128);

    loop {
        tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;

        loop {
            match rx.try_recv() {
                Ok((id, Some(control))) => {
                    job_ongoing = id;
                    job_controller.insert(id, control);
                }
                Ok((id, None)) => {
                    job_controller.remove(&id);
                }
                Err(_) => {
                    break;
                }
            }
        }

        if let Ok(mut controls) = list_controls().await {
            let completed_commands = controls
                .drain(..)
                .filter(|ctrl| ctrl.id <= job_ongoing)
                .map(|ctrl| {
                    match (job_controller.get(&ctrl.id), ctrl.data) {
                        (Some(sender), ControlType::Stop) => {
                            sender.send(ControlType::Stop).unwrap();
                        }
                        (Some(sender), cmd) => {
                            sender.send(cmd).unwrap();
                        }
                        _ => (),
                    };

                    return ctrl.cmd_id;
                });

            update_control_status(completed_commands.collect(), 1).await;
        }
    }
}

async fn list_controls() -> Result<Vec<Control>, &'static str> {
    let pool = mysql_async::Pool::new(MYSQL_SERVER_URL);
    let mut conn = pool.get_conn().await.map_err(|_| "DB 연결 실패")?;

    let result = conn
        .query_map::<(usize, usize, String, String), _, _, _>(
            "SELECT id, data FROM code_controls WHERE status = 0",
            |(cmd_id, id, ctrl, data)| -> Control {
                let ctrl = match ctrl.as_str() {
                    "input" => ControlType::Input(data),
                    "stop" => ControlType::Stop,
                    _ => ControlType::Stop,
                };

                Control {
                    cmd_id,
                    id,
                    data: ctrl,
                }
            },
        )
        .await
        .map_err(|_| "query error")?;

    Ok(result)
}

async fn list_jobs() -> Result<Vec<Job>, Box<dyn std::error::Error>> {
    let pool = mysql_async::Pool::new(MYSQL_SERVER_URL);
    let mut conn = pool.get_conn().await?;

    println!("select code_jobs");

    Ok("select * from code_jobs"
        .with(())
        .map::<(u64, String, String, String, mysql_async::Value), Job, _, &mut Conn>(
            &mut conn,
            |(id, langauge, code, status, status_updated)| {
                let submission = Submission::new(id, langauge, status, code, status_updated);

                match submission.language.to_lowercase().as_str() {
                    "cpp" => Job::CPlusPlus(language::CPlusPlus::new(submission)),
                    "python" => Job::Python(language::Python::new(submission)),
                    "java" => Job::Java(language::Java::new(submission)),
                    _ => Job::Unknwon(submission.id),
                }
            },
        )
        .await
        .unwrap_or(vec![]))
}

async fn update_jobs(mut results: Vec<RunResult>) {
    loop {
        let pool = mysql_async::Pool::new(MYSQL_SERVER_URL);
        let conn = pool.get_conn().await;

        if conn.is_err() {
            pool.disconnect().await;
            continue;
        }

        let insert_result =
            r"INSERT INTO jobs_result (id, output, error) VALUES (:id, :output, :error)"
                .with(results.drain(..).map(|result| {
                    if result.result.is_ok() {
                        params! {
                            "id" => result.id,
                            "output" => result.result.unwrap(),
                            "error" => "",
                        }
                    } else {
                        params! {
                            "id" => result.id,
                            "output" => result.result.unwrap(),
                            "error" => "",
                        }
                    }
                }))
                .batch(&mut conn.unwrap())
                .await;

        if insert_result.is_ok() {
            pool.disconnect().await;
            break;
        }
    }
}
async fn update_control_status(cmd_id: Vec<usize>, status: usize) {
    loop {
        let pool = mysql_async::Pool::new(MYSQL_SERVER_URL);
        let conn = pool.get_conn().await;

        if conn.is_err() {
            pool.disconnect().await;
            continue;
        }

        let update_result = r"UPDATE code_controls SET status = :status WHERE id IN (:id)"
            .with(cmd_id.iter().map(|cmd_id| {
                params! {
                    "id" => cmd_id,
                    "status" => status,
                }
            }))
            .batch(&mut conn.unwrap())
            .await;

        if update_result.is_ok() {
            pool.disconnect().await;
            break;
        }
    }
}
