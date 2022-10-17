<script>
  import { onMount } from "svelte";

  let ClassicEditor;

  onMount(async () => {
    const module = await import("@ckeditor/ckeditor5-build-classic");
    ClassicEditor = module.default;
    ClassicEditor.create(document.querySelector("#editor"))
      .then((editor) => {
        console.log(editor);
      })
      .catch((error) => {
        console.error(error);
      });
  });
</script>

<!-- 글작성 페이지-->
<div class="content">
  <div class="write__title" style="text-align: left; font-size: 30px;" />
  <form>
    <div class="write__form__title" style="margin-top: 2px;">
      <h1>A</h1>
      <div class="write__form__content">
        <textarea
          class="textarea"
          id="editor"
          placeholder="답변을 입력해주세요."
        />
      </div>
    </div>
  </form>
</div>

<br /><br /><br />

<div class="buttons">
  <a href="/board/qna/article/1">
    <button class="button is-success">작성</button>
  </a>
  <a href="/board/qna/1">
    <button class="button is-danger">삭제</button>
  </a>
</div>

<br /><br />

<style>
  :global(.ck-editor__editable_inline) {
    min-height: 400px;
  }
</style>
