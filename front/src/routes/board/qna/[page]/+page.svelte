<script>
  import { userIsLogged } from "$lib/user.js";
  import { onMount } from "svelte";

  let currentPage = 1;
  let pageLimit = 10;
  let label = 1;
  const isLogged = userIsLogged();
  let message = "message";

  const getBoardList = async (pageIdx, pageLimit) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/qna/list/${pageIdx}?limit=${pageLimit}`,
      {
        method: "GET",
        mode: "cors",
        credentials: "include",
      }
    ).catch((err) => {
      console.log(err);
    });
    const qnaBoard = await res.json();
    if (res.ok) {
      return qnaBoard;
    } else {
      throw new Error(qnaBoard);
    }
  };

  $: boardList = getBoardList(currentPage, pageLimit);
</script>

<div class="container">
  <table
    class="table container is-fluid has-text-centered"
    style="margin-bottom: 0;"
  >
    <thead>
      <tr>
        <th class="has-text-centered">제목</th>
        <th class="has-text-centered">작성자</th>
        <th class="has-text-centered">작성일자</th>
        <th class="has-text-centered">추천</th>
        <th class="has-text-centered">조회수</th>
      </tr>
    </thead>
    <tbody>
      {#await boardList then qnaBoard}
        {#each qnaBoard["list"] as qna}
          <tr>
            <td
              ><a href="/board/qna/article/{qna.article_id}">{qna.title}</a></td
            >
            <td>{qna.username}</td>
            <td>{qna.created}</td>
            <td>{qna.like}</td>
            <td>{qna.views}</td>
          </tr>
        {/each}
      {:catch error}
        <tr>
          <td colspan="5">{error.message}</td>
        </tr>
      {/await}
    </tbody>
    <tfoot>
      <tr>
        <td colspan="5" />
      </tr></tfoot
    >
  </table>
  {#await boardList then qnaBoard}
    <nav class="pagination is-centered" aria-label="pagination">
      <ul class="pagination-list">
        {#each Array(Math.ceil(qnaBoard["cnt"] / pageLimit)) as n, i}
          <li>
            <!-- svelte-ignore a11y-missing-attribute -->
            <a
              class="pagination-link"
              class:is-current={i + 1 === currentPage}
              sveltekit:prefetch
              on:click={() => (currentPage = i + 1)}>{i + 1}</a
            >
          </li>
        {/each}
      </ul>
    </nav>
  {:catch error}
    {error.message}
  {/await}

  <div class="container">
    <div class="field is-horizontal">
      <div class="field-body">
        <div class="select">
          <select>
            <option>제목</option>
            <option>작성자</option>
            <option>내용</option>
          </select>
        </div>
        <div class="control is-expanded has-icons-left">
          <input class="input" type="text" placeholder="검색어를 입력하세요." />
          <span class="icon is-small is-left">
            <i class="fas fa-search" />
          </span>
        </div>
        <p class="control">
          <button class="button is-info"> 검색 </button>
        </p>
      </div>
      {#if isLogged}
        <a href="/board/qna/write/question" class="button is-primary">글쓰기</a>
      {/if}
      <div class="select">
        <select>
          <option>10개씩 보기</option>
          <option>15개씩 보기</option>
          <option>20개씩 보기</option>
        </select>
      </div>
    </div>
  </div>
  <br />
</div>
