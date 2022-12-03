<script>
	import { onDestroy, onMount } from "svelte";
	import env from "$lib/env.js";

	export let run_id;

	class OutputLine {
		constructor(msg, color = "white", direction = ">>", id = null) {
			this.id = id;
			this.msg = msg;
			this.color = color;
			this.direction = direction;
		}
	}

	let output_lines = []; // list of OutputLine
	let output_html = ">> 실행 버튼을 눌려주세요";
	let input_text = "";
	let clearIntervalToken = null;

	onDestroy(() => {
		if (clearIntervalToken != null) {
			clearInterval(clearIntervalToken);
		}
	});

	onMount(() => {
		poll_run(run_id);
	});
	$: poll_run(run_id);

	function poll_run(run_id) {
		console.log(["polling run", run_id]);
		if (run_id == null || run_id == "") {
			return clearOutput();
		}

		if (clearIntervalToken != null) {
			clearInterval(clearIntervalToken);
		}

		output_lines = [];
		output_lines.push(new OutputLine("실행 준비중", "#9ab2ff", ">>"));

		var is_started = false;
		var try_count = 0;
		var localIntervalToken = setInterval(() => {
			if (try_count++ >= 10) clearInterval(localIntervalToken);

			fetch(`${env.baseUrl}/run/${run_id}/`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
			})
				.then((res) => res.json())
				.then((res) => {
					// output == Null 이면 아직 준비중
					// output != Null 이면 실행은 시작된 상태임.
					// 그러므로, output 상태를 추적해서, output이 최초로 non-null이 되면 "프로그램 시작됨" 메세지 표시
					if (res.output != null && !is_started) {
						is_started = true;
						output_lines.push(
							new OutputLine("프로그램 시작됨", "#9ab2ff", ">>")
						);
					}

					for (let rcv_line of res.output) {
						let found = false;
						for (let i = 0; i < output_lines.length; i++) {
							if (
								output_lines[i].id != null &&
								output_lines[i].id == rcv_line.id
							) {
								output_lines[i].msg = rcv_line.data;
								found = true;
								break;
							}
						}

						if (found) continue;
						output_lines.push(
							new OutputLine(
								rcv_line.data,
								"white",
								">>",
								rcv_line.id
							)
						);
					}

					if (res.error != "") {
						// find index of error
						let idx = output_lines.findIndex((line) => {
							return line.id == res.error;
						});

						if (idx != -1) {
							output_lines[idx].msg = res.error;
						} else {
							output_lines.push(
								new OutputLine(
									res.error,
									"red",
									">> 오류 발생:",
									"error"
								)
							);
						}

						clearInterval(localIntervalToken);
					}

					if (res.status == "done") {
						output_lines.push(
							new OutputLine("프로그램 종료됨", "#9acd32", ">>")
						);
						clearInterval(localIntervalToken);
					}

					return Promise.resolve(output_lines);
				})
				.then(printOuput);
		}, 800);

		clearIntervalToken = localIntervalToken;

		printOuput(output_lines);
	}

	function input_text_act() {
		if (run_id == null || run_id == "") {
			return;
		}

		const input = input_text;
		input_text = "";

		if (input == null || input == "") {
			alert("입력값을 적어주세요.");
			return;
		}

		output_lines.push(new OutputLine(input, "white", "<<"));

		fetch(`${env.baseUrl}/run/${run_id}/input`, {
			method: "PUT",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			mode: "cors",
			credentials: "include",
			body: JSON.stringify({
				input: input,
			}),
		});
	}

	function escapeHtml(str) {
		var map = {
			"&": "&amp;",
			"<": "&lt;",
			">": "&gt;",
			'"': "&quot;",
			"'": "&#039;",
		};

		return str.replace(/[&<>"']/g, function (m) {
			return map[m];
		});
	}

	function printOuput(outputLines) {
		let output_html_builder = "";
		for (let line of outputLines) {
			output_html_builder += `<div class="output-line"><span class="output-line-direction">${
				line.direction
			}</span><span class="output-line-msg" style="color: ${
				line.color
			}">${escapeHtml(line.msg)}</span></div>`;
		}

		output_html = output_html_builder;
	}
	function clearOutput() {
		output_lines = [];
		output_html = ">> 실행 버튼을 눌려주세요";
	}
</script>

<section id="run-console" class="is-family-code">
	<div id="run-output" class="p-2" style="padding-bottom: 20px">
		{@html output_html}
	</div>
	<form id="run-input" on:submit|preventDefault={input_text_act}>
		<input type="text" bind:value={input_text} />
	</form>
</section>

<style>
	#run-console {
		border-top: 1px solid white;
		height: 180px;
	}
	#run-output {
		overflow-y: scroll;
		white-space: pre;
		height: 156px;
		font-size: 13px;
	}
	#run-input {
		height: 24px;
		color: white;
	}
	#run-input::before {
		line-height: 1.8;
		content: "　<<";
		position: absolute;
		font-size: 13px;
	}
	#run-input input {
		padding-left: 40px;
		background-color: black;
		color: white;
		border: none;
		display: inline-flex;
		width: 100%;
	}
</style>
