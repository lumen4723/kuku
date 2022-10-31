<script>
  import { onMount } from "svelte";
  import { is_empty } from "svelte/internal";
  import Swal from "sweetalert2";

  let title = "",
    content = "",
    tags = [];
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
        <a href="#" class="dropdown-item">1tag</a>
        <a href="#" class="dropdown-item">2tag</a>
        <a href="#" class="dropdown-item">3tag</a>
        <a href="#" class="dropdown-item">4tag</a>
        <a href="#" class="dropdown-item">5tag</a>
      </div>
    </div>

    <div class="tags has-addons tag-add">
      <span class="tag is-info">1tag</span>
      <a href="#" class="tag is-delete" />
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
    margin: 0, 0, 0, 10px;
    padding: 5px;
  }
</style>
