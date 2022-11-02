<script>
  import { onMount } from "svelte";
  import { append, hasContext, is_empty } from "svelte/internal";
  import Swal from "sweetalert2";

  let title = "",
    content = "",
    picktags = [];
  let ClassicEditor;
  let ckeditorInstance;

  onMount(async () => {
    const module = await import("@ckeditor/ckeditor5-build-classic");
    ClassicEditor = module.default;
    ClassicEditor.create(document.querySelector("#editor"))
      .then((editor) => {
        ckeditorInstance = editor;
        console.log(editor);
      })
      .catch((error) => {
        console.error(error);
      });
  });

  const postArticle = () => 
    fetch(`//api.eyo.kr:8081/board/qna/question`, {
      method: "POST",
      headers: {
        Aceept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        content: ckeditorInstance.getData(),
        tags,
      }),
      mode: "cors",
      credentials: "include",
    })
      .then((res) => {
        if (res.ok == false) return Promise.reject(res);
        return res.json();
      })
      .then((json) => {
        postResult = JSON.stringify(json);
      })
      .catch((err) => {
        console.log(err);
      });

  const upload = () => {
    console.log(title);
    console.log(
      JSON.stringify({
        title,
        content: ckeditorInstance.getData(),
        tags,
      })
    );
    postArticle()
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
        err.text().then((text) => {
          console.log(text);
        });
      });
  };

  const alt = () => {
    Swal.fire({
      title: "제목을 입력해주세요",
      icon: "error",
      confirmButtonText: "확인",
    });
  };

  // 태그 가져오기
  const getTags = async() => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/tag/list`,
      {
      mode: "cors",
      credentials: "include",
    });
    const article = await res.json();
    if (res.ok) {
      return article;
    } else {
      throw new Error(article);
    }
  };
  $: boardtags = getTags();
</script>

<!-- 글작성 페이지-->
<form action="POST" on:submit|preventDefault={upload}>
  <div class="content">
    <h1>Q</h1>
    <input
      class="input mb-4"
      id="title"
      placeholder="제목을 입력해주세요."
      bind:value={title}
      required
    />
    <textarea
      class="textarea"
      id="editor"
      placeholder="내용을 입력해주세요."
      required>{content}</textarea
    >
  </div>

  <div class="dropdown is-hoverable">
    <div class="dropdown-trigger">
      <button
        class="button"
        aria-haspopup="true"
        aria-controls="dropdown-menu4"
      >
        <span>태그 선택</span>
        <span class="icon is-medium">
          <i class="fas fa-angle-down" aria-hidden="true" />
        </span>
      </button>
    </div>
    <div class="dropdown-menu" id="dropdown-menu4" role="menu">
      <div class="dropdown-content">
        {#await boardtags then tags}
          {#each tags as tag}
            {#if picktags.includes(tag.slug)}
            <div class="dropdown-item">
              {tag.slug}
            </div>
            {:else}
            <div class="dropdown-item" on:click={() => {picktags[picktags.length] = tag.slug}}>
              {tag.slug}
            </div>
            {/if}
          {/each}
        {:catch error}
          <p>태그를 불러오는데 실패했습니다.</p>
        {/await}
      </div>
    </div>

    <div class="tags has-addons tag-add">
      {#each picktags as tag}
        <span class="tag is-info">{tag}</span>
        <div class="tag is-delete" on:click={() => {picktags = picktags.filter(x => x != tag)}} />
      {/each}
      <!--{#each picktags as tag}
        <span class="tag is-info" on:click={console.log(picktags.has(tag))}>{tag}</span>
        <div class="button tag is-delete" style="margin-right: 5px;" on:click={() => {}}/>
      {/each} -->
    </div>
  </div>

  <br /><br /><br />

  {#if is_empty(title)}
    <button class="button is-success" on:click={alt}>작성</button>
  {:else}
    <a href="/board/qna/1">
      <button class="button is-success" type="submit" on:click={upload}>
        작성
      </button>
    </a>
  {/if}
  <a href="/board/qna/1">
    <button class="button is-danger">삭제</button>
  </a>
</form>
<br /><br />

<style>
  :global(.ck-editor__editable_inline) {
    min-height: 400px;
  }
  .tag-add {
    margin-left: 10px;
    padding: 5px;
  }
</style>
