<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import Swal from "sweetalert2";
  let article_data = { title: "", content: "" };

  let ClassicEditor;
  let ckeditorInstance;
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
      `//api.eyo.kr:8081/board/free/article_id/${article_id}`,
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
      `//api.eyo.kr:8081/board/free/update/${article_id}`,
      {
        method: "PUT",
        headers: {
          Aceept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: article_data.title,
          content: ckeditorInstance.getData(),
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
        console.log(err);
      });

    // const json = await res.json();
    // putResult = JSON.stringify(json);
  };

  const upload = () => {
    console.log(
      JSON.stringify({
        title: article_data.title,
        content: ckeditorInstance.getData(),
      })
    );
    Swal.fire({
      title: "수정하시겠습니까?",
      text: "",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "rgb(067, 085, 189)",
      cancelButtonColor: "rgb(219, 224, 255)",
      confirmButtonText: "수정",
      cancelButtonText: "취소",
      preConfirm: () => {
        putArticle($page.params.id)
          .then((res) => {
            console.log(res);
          })
          .catch((err) => {
            console.log(err);
            err.text().then((text) => {
              console.log(text);
            });
          });
      },
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire("Motified!", "글이 수정되었습니다.", "success").then(
          (result) => {
            if (result.isConfirmed)
              location.href = "/board/free/article/" + $page.params.id;
          }
        );
      }
    });
  };
</script>

<br />

<form method="PUT" on:submit|preventDefault={upload}>
  <div class="contents">
    <input
      class="input mb-4"
      type="text"
      placeholder="제목을 입력해주세요"
      bind:value={article_data.title}
      required
    />
    <textarea
      class="textarea"
      id="editor"
      placeholder="내용을 입력하세요."
      required>{article_data.content}</textarea
    >
    <hr />
  </div>

  <button class="button is-link" type="submit" on:click={upload}>완료</button>
  <a href="/board/free/article/{$page.params.id}">
    <button class="button is-link is-light" type="button">취소</button>
  </a>
</form>
<br /> <br />

<style>
  textarea {
    width: 100%;
    height: 50em;
    resize: none;
  }
  :global(.ck-editor__editable_inline) {
    min-height: 400px;
  }
</style>
