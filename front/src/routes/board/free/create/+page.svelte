<script>
	import { onMount } from 'svelte';
	let ClassicEditor;
	onMount(async () => {
		const module = await import('@ckeditor/ckeditor5-build-custom');
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

<br />
<div>
	<form action="" method="POST">
		<input
			class="input is-medium mb-4"
			type="text"
			placeholder="제목을 입력해주세요"
		/>
		<textarea
			class="textarea is-medium"
			id="editor"
			placeholder="내용을 입력하세요."
		/>
	</form>
	<hr />
</div>
<div class="file has-name">
	<label class="file-label">
		<input class="file-input" type="file" name="resume" />
		<span class="file-cta">
			<span class="file-icon">
				<i class="fas fa-upload" />
			</span>
			<span class="file-label"> Choose a file… </span>
		</span>
		<span class="file-name"> file-name </span>
	</label>
</div>
<br />
<button class="button is-info">완료</button>
<br /> <br />

<style>
	textarea {
		width: 100%;
		height: 50em;
		resize: none;
	}
	/* 
	:global(.ck-editor__editable_inline > *) {
		padding: 0 2em 0 2em;
	} */
	:global(.ck-editor__editable_inline) {
		min-height: 400px;
	}
</style>
