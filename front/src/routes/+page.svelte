<script>
import Carousel from "$lib/carousel.svelte";
import { userIsLogged } from "$lib/user.js";
import gmttolocal from "$lib/time.js";

  const getBoardList = async (pageIdx, pageLimit) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/free/list/${pageIdx}?limit=${pageLimit}`,
      {
        mode: "cors",
        credentials: "include",
      }
    );
    const freeBoard = await res.json();
    if (res.ok) {
      return freeBoard;
    } else {
      throw new Error(freeBoard);
    }
  };
  const getNoticeList = async (pageLimit) => {
		const res = await fetch(
			`//api.eyo.kr:8081/board/free/notice/list?limit=${pageLimit}`,
			{
				mode: "cors",
  			credentials: "include",
			}
		);
		const freeBoard = await res.json();
		if (res.ok) {
    	return freeBoard;
		} else {
			throw new Error(freeBoard);
    }
	};
	const getqnalist = async (pageIdx, pageLimit) => {
    const res = await fetch(
			`//api.eyo.kr:8081/board/qna/list/${pageIdx}?limit=${pageLimit}`,
			{
				mode: "cors",
    		credentials: "include",
			}
		);
		const freeBoard = await res.json();
    if (res.ok) {
			return freeBoard;
		} else {
			throw new Error(freeBoard);
		}
  };
  let isLogged = userIsLogged();

	let boardList = getBoardList(1, 8);
	let NoticeList = getNoticeList(8);
	let qnaList = getqnalist(1, 8);
</script>

<section class="hero is-primary is-halfheight">
  <div class="hero-body">
    <div class="container">
      <div class="columns">
        <div
          class="column"
          style="align-items: center;
                justify-content: center;
                display: flex;
                padding-bottom: 5%;
				"
        >
          <div>
            <h1 class="title" style="word-break: keep-all;">
              차 한잔과 함께하는 코딩 사이트
            </h1>
            <div style="padding-left: 48px;">
              <h2 class="subtitle" style="line-height:1.4;">
                비전공자도 참여할 수 있는
                <br />
                쉬운 난이도를 통하여
                <br />
                여러분의 코딩실력을 향상시켜보세요!
              </h2>
              {#if !isLogged}
                <a
                  class="button
                            is-info is-dark
                            is-medium is-halfwidth"
                  sveltekit:prefetch
                  href="/account"
                >
                  시작하기
                </a>
              {/if}
            </div>
          </div>
        </div>
        <div class="column">
          <div style="padding-left: 30px; padding-top: 10px">
            <img src="https://via.placeholder.com/560x500" alt="" />
            <br />사진은 생각해놓음
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="hero-body">
  <div
    class="box"
    style="margin: 60px auto;
    border-radius: 20px;
    width: 80%;
    background-color: #fafafa;"
  >
    <div class="container block">
      <div class="columns" style="margin-bottom: 20px;">
        <div class="column" style="margin-top: 20px;">
          <h1
            class="title"
            style="word-break: keep-all; 
                    padding-left: 12%;"
          >
            기초 트랙들을 통해 코딩을 배워보세요!
          </h1>
        </div>
      </div>
      <Carousel />
    </div>
    <div class="container block">
      <div class="columns" style="margin-bottom: 20px;">
        <div class="column" style="margin-top: 20px;">
          <h1
            class="title"
            style="word-break: keep-all; 
                    padding-left: 12%;"
          >
            알고리즘 트랙들을 통해 실력을 향상시켜보세요!
          </h1>
        </div>
      </div>
      <Carousel />
    </div>
  </div>
</section>

<section class="hero-body">
  <div class="container">
    <div class="columns">
      <div class="column">
        <div class="table-container">
          <table
            class="table
					is-bordered
        			is-hoverable"
            style="
        			text-align: center;
        			table-layout: fixed;
        			"
          >
            <thead>
              <tr>
                <th colspan="2">새로운 내용</th>
              </tr>
            </thead>
            <tbody>
              {#await boardList then freeBoard}
                {#each freeBoard["list"] as free}
                  <tr>
                    <td
                      ><a href="/board/free/article/{free.article_id}"
                        >{free.title}</a
                      ></td
                    >
                    <td>{free.username}</td>
                  </tr>
                {/each}
              {:catch error}
                <tr>
                  <td colspan="2">{error.message}</td>
                </tr>
              {/await}
            </tbody>
          </table>
        </div>
      </div>
      <div class="column">
        <div class="table-container">
          <table
            class="table
					is-bordered
        			is-hoverable"
            style="
        			text-align: center;
        			table-layout: fixed;
        			"
					>
						<thead>
							<tr>
								<th colspan="2">공지사항</th>
							</tr>
						</thead>
						<tbody>
							{#await NoticeList then freenotice}
								{#each freenotice["list"] as free}
									<tr>
										<td
											><a
												href="/board/free/article/{free.article_id}"
												>{free.title}</a
											></td
										>
										<td>
											{gmttolocal(free.created)}
										</td>
									</tr>
								{/each}
							{:catch error}
								<tr>
									<td colspan="2">{error.message}</td>
								</tr>
							{/await}
						</tbody>
					</table>
				</div>
			</div>
			<div class="column">
				<div class="table-container">
					<table
						class="table
					is-bordered
        			is-hoverable"
            style="
        			text-align: center;
        			table-layout: fixed;
        			"
					>
						<thead>
							<tr>
								<th colspan="2">새로운 질문과 답변</th>
							</tr>
						</thead>
						<tbody>
							{#await qnaList then qnaBoard}
								{#each qnaBoard["list"] as qna}
									<tr>
										<td
											><a
												href="/board/qna/article/{qna.article_id}"
												>{qna.title}</a
											></td
										>
										<td>{qna.state}</td>
									</tr>
								{/each}
							{:catch error}
								<tr>
									<td colspan="2">{error.message}</td>
								</tr>
							{/await}
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</section>

<style>
	thead tr {
		background-color: #10e1c2;
	}
	thead th {
		text-align: center;
		color: #ffffff;
	}
	table.table {
		width: 100%;
	}
</style>
