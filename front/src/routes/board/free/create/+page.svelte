<script>
	import { beforeUpdate, afterUpdate, onMount } from 'svelte';
	onMount(() => {
		ClassicEditor.create(document.querySelector('#editor'), {
			language: 'ko',
			height: '800px'
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
	<script
		src="https://cdn.ckeditor.com/ckeditor5/35.1.0/classic/ckeditor.js"></script>
	<script
		src="https://cdn.ckeditor.com/ckeditor5/35.1.0/classic/translations/ko.js"></script>
	<script>
	</script>
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
<button class="button is-info" style="float: right;">글쓰기</button>
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
