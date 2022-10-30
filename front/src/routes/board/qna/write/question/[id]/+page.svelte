<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import Swal from "sweetalert2";

  let ClassicEditor;
  let ckeditorInstance;
  let article_data = { title: "", content: "", tags: [] };

  onMount(async () => {
    const module = await import("@ckeditor/ckeditor5-build-classic");
    ClassicEditor = module.default;
    ClassicEditor.create(document.querySelector("#editor"))
      .then((editor) => {
        ckeditorInstance = editor;
      })
      .catch((error) => {
        console.error(error);
      });
  });

  const getArticle = async (article_id) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/qna/article/${article_id}?article_id=${article_id}`,
      {
        mode: "cors",
        credentials: "include",
      }
    );
    const article = await res.json();
    article_data = article;
    if (ckeditorInstance != undefined)
      ckeditorInstance.setData(article_data.content);

    if (res.ok) {
      return article;
    } else {
      throw new Error(article);
    }
  };
  let article = getArticle($page.params.id);

  const putArticle = async (article_id) => {
    const res = await fetch(
      `//api.eyo.kr:8081/board/qna/article/${article_id}`,
      {
        method: "PUT",
        headers: {
          Aceept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: article_data.title,
          content: ckeditorInstance.getData(),
          tags: article_data.tags,
        }),
        mode: "cors",
        credentials: "include",
      }
    )
      .then((res) => {
        if (res.ok == false) return Promise.reject(res);
        return res.json();
      })
      .then((json) => {
        putResult = JSON.stringify(json);
      })
      .catch((err) => {
        putResult = JSON.stringify(err);
      });
  };
  const upload = () => {
    console.log(
      JSON.stringify({
        title: article_data.title,
        content: ckeditorInstance.getData(),
        tags: article_data.tags,
      })
    );
    putArticle($page.params.id)
      .then((res) => {
        console.log(res);
      })
      .then(
        Swal.fire({
          title: "수정하시겠습니까?",
          text: "",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "RGB(067, 085, 189)",
          cancelButtonColor: "RGB(219, 224, 255)",
          confirmButtonText: "수정",
          cancelButtonText: "취소",
        }).then((result) => {
          if (result.isConfirmed) {
            Swal.fire("Motified!", "글이 수정되었습니다.", "success").then(
              (result) => {
                if (result.isConfirmed)
                  location.href = "/board/qna/article/" + $page.params.id;
              }
            );
          }
        })
      )
      .catch((err) => {
        console.log(err);
        // err.text().then((text) => {
        //   console.log(text);
        // });
      });
  };
</script>

<!-- 글작성 페이지-->
<form action="PUT" on:submit|preventDefault={upload}>
  <div class="content">
    <div class="write__title" style="text-align: left; font-size: 30px;" />
    <form>
      <div class="write__form__title" style="margin-top: 2px;">
        <h1>Q</h1>
        <input
          class="input mb-4"
          id="title"
          placeholder="제목을 입력해주세요."
          bind:value={article_data.title}
          required
        />
      </div>
      <div class="write__form__content">
        <textarea
          class="textarea"
          id="editor"
          placeholder="내용을 입력해주세요."
          required>{article_data.content}</textarea
        >
      </div>
    </form>
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

  <button class="button is-success" type="submit" on:click={upload}>작성</button
  >
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
