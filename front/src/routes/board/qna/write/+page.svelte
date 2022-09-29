<script>
	import { onMount } from 'svelte';

	let ClassicEditor;

	onMount(async () => {
		const module = await import('@ckeditor/ckeditor5-build-classic');
		ClassicEditor = module.default;
		ClassicEditor.create(document.querySelector('#editor'))
			.then((editor) => {
				console.log(editor);
			})
			.catch((error) => {
				console.error(error);
			});
	});
</script>

<!-- 글작성 페이지-->
<div class="write">
	<div class="write__title" style="text-align: left; font-size: 30px;">
		<h1>글쓰기</h1>
	</div>
	<div class="write__form">
		<form>
			<div class="write__form__title">
				<input
					class="input mb-4"
					id="title"
					placeholder="제목을 입력해주세요."
				/>
			</div>
			<div class="write__form__content">
				<textarea
					class="textarea"
					id="editor"
					placeholder="내용을 입력해주세요."
				/>
			</div>
			<div class="write__form__submit">
				<button type="submit">작성</button>
			</div>
		</form>
	</div>
</div>

<style>
	:global(.ck-editor__editable_inline) {
		min-height: 400px;
	}
</style>
