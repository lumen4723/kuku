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
<div class="content">
	<div class="write__title" style="text-align: left; font-size: 30px;" />
	<form>
		<div class="write__form__title" style="margin-top: 2px;">
			<h1>Q</h1>
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
	.tag-add {
		margin: 0, 0, 0, 10px;
		padding: 5px;
	}
</style>
