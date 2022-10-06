<script>
  import { page } from "$app/stores";
  import List from "../../[page]/+page.svelte";

  const getArticle = async (article_id) => {
    const res = await fetch(
      `http://api.eyo.kr:8081/board/free/article_id/${article_id}`,
      {
        mode: "cors",
      }
    );
    const article = await res.json();
    if (res.ok) {
      return article;
    } else {
      throw new Error(article);
    }
  };
  let article = getArticle($page.params.id);

  const getComment = async (article_id) => {
    const res = await fetch(
      `http://api.eyo.kr:8081/board/free/comment/${article_id}`,
      {
        mode: "cors",
      }
    );
    const comment = await res.json();
    if (res.ok) {
      return comment;
    } else {
      throw new Error(comment);
    }
  };
  $: comments = getComment($page.params.id);

  const Like = async (article_id) => {
    const res = await fetch(
      `http://api.eyo.kr:8081/board/free/article/${article_id}/like`,
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        mode: "cors",
      }
    );
    const json = await res.json();
    postLikeResult = JSON.stringify(json);
  };

  const disLike = async (article_id) => {
    const res = await fetch(
      `http://api.eyo.kr:8081/board/free/article/${article_id}/dislike`,
      {
        method: "PUT",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        mode: "cors",
      }
    );
    const json = await res.json();
    disLikeResult = JSON.stringify(json);
  };

  let isClicked = false;
  const likeclick = () => {
    isClicked = !isClicked;
  };
  const alt = () => {
    alert("로그인이 필요합니다.");
  };
  let isLogin = true;
</script>

{#await article}
  <p class="has-text-centered">Loading in progress...</p>
{:then article}
  <header>
    <div style="padding: 16px">
      {#if isLogin}
        <div class="edit" style="float: right; margin-top: 16px">
          <a href="/board/free/write/update/{article.article_id}"
            ><button class="button is-rounded is-light"> 수정 </button></a
          >
          <a href="/board/free/1"
            ><button class="button is-rounded is-light"> 삭제 </button></a
          >
        </div>
      {/if}
      <div style="float:left;">
        <span class="is-size-3">{article.title}</span> <br />
        <div style="float: left;">
          <a
            class="author"
            href="/free/{article.username}"
            style="color: #4A4A4A;">{article.username}</a
          >
          <span style="color: #DBDBDB;">|</span>
          {article.created}
        </div>
      </div>
      <div style="clear:both" />
    </div>
  </header>

  <hr style="margin:0;" />

  <div class="content">{@html article.content}</div>

  <div style="margin: 0 auto; width: 100px; text-align: center">
    <span class="is-size-3">
      {#if isLogin}
        <i
          class={isClicked ? "fa-solid fa-heart" : "fa-regular fa-heart"}
          on:click={likeclick}
          on:submit={isClicked ? Like : disLike}
        />
      {:else}
        <i class="fa-regular fa-heart" on:click={alt} />
      {/if}
    </span>
    <div>추천 {article.like}</div>
  </div>
{/await}

<hr style="margin-top: 0;" />

<div class="comment" style="padding: 16px">
  <table class="table container is-fluid">
    <tbody>
      {#await comments then comments}
        {#if comments.list.length === 0}
          <tr>
            <td>댓글이 없습니다.</td>
          </tr>
        {:else}
          {#each comments["list"] as comment}
            <tr>
              <td>
                <a
                  class="author"
                  href="/free/{comment.username}"
                  style="color: #4A4A4A;">{comment.username}</a
                >
                <span style="color: #DBDBDB;">|</span>
                {comment.created}
              </td>
            </tr>
            <tr>
              <td>{comment.content}</td>
            </tr>
            {#if isLogin}
              <button
                class="button is-rounded
							is-link is-light is-small
							is-responsive
							"
              >
                수정
              </button>
              <button
                class="button is-rounded
							is-link is-light is-small
							is-responsive
							"
              >
                삭제
              </button>
            {/if}
          {/each}
        {/if}
      {/await}
    </tbody>
  </table>
  {#if isLogin}
    <textarea class="textarea" placeholder="댓글을 입력하세요" />
    <button class="button">등록</button>
  {/if}
</div>

<br /><br /><br />

<style>
  hr {
    border: 1px solid #dbdbdb;
  }
  span i {
    color: rgb(251, 106, 130);
  }
  .content {
    width: 100%;
    height: 300px;
    padding: 16px;
  }
  .comment table {
    width: 100%;
    background-color: rgba(239, 235, 235, 0.805);
  }
  textarea {
    width: 100%;
    height: 5.25em;
    resize: none;
  }
</style>
