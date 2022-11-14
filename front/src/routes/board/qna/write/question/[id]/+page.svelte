<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { is_empty } from "svelte/internal";
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
        console.log(editor);
      })
      .catch((error) => {
        console.error(error);
      });
  });

  const getArticle = async (article_id) => {
    if (isNaN(article_id)) return false;
    const res = await fetch(
      `//api.eyo.kr:8081/board/qna/list/article/${article_id}`,
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
    let tagArr = article_data.tags.map(x=>x.slug);
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
          tags: tagArr,
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
  };
  const getTags = async () => {
    const res = await fetch(`//api.eyo.kr:8081/board/tag/list`, {
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

  const upload = () => {
    console.log(
      JSON.stringify({
        title: article_data.title,
        content: ckeditorInstance.getData(),
        tags: article_data.tags,
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
              location.href = "/board/qna/article/" + $page.params.id;
          }
        );
      }
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
<form method="PUT" on:submit|preventDefault={upload}>
  <div class="content">
    <h1>Q</h1>
    <input
      class="input mb-4"
      id="title"
      placeholder="제목을 입력해주세요."
      bind:value={article_data.title}
      required
    />
    <textarea
      class="textarea"
      id="editor"
      placeholder="내용을 입력해주세요."
      required>{article_data.content}</textarea
    >
  </div>

  <div class="dropdown is-hoverable" on:click={(e)=>e.preventDefault()}>
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
        {#await boardtags then picktags}
          {#each picktags as tag}
                <div
                  class="dropdown-item"
                  on:click={() => {
                    console.log(article_data.tags.filter((x)=>x==tag.slug).length);
                    if(article_data.tags.filter((x)=>x.slug==tag.slug).length > 0) {
                      return;
                    }
                    article_data.tags[article_data.tags.length] = tag;
                  }}
                >
                  {tag.name}
                </div>
          {/each}
        {:catch error}
          <p>태그를 불러오는데 실패했습니다.</p>
        {/await}
      </div>
    </div>

    <div class="tags has-addons tag-add">
      {#each article_data.tags as tag}
        <span class="tag is-info">{tag.name}</span>
        <div
          class="tag is-delete"
          on:click={() => {
            article_data.tags = article_data.tags.filter((x) => x != tag);
          }}
        />
      {/each}
    </div>
  </div>
  <br /><br /><br />

  <div>
    <button
      class="button is-success"
      type="submit"
      on:click={is_empty(article_data.title) ? alt : upload}>완료</button
    >
    <a href="/board/qna/article/{$page.params.id}">
      <button class="button is-danger">취소</button>
    </a>
  </div>
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
