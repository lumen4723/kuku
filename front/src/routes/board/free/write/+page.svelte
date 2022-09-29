<script>
	import { onMount } from 'svelte';
	let title = '',
		content = '';

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

	const postArticle = async () => {
		const res = await fetch(`http://api.eyo.kr:8081/board/free/article`, {
			method: 'POST',
			headers: {
				Aceept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				title,
				content
			}),
			mode: 'cors'
		});
		const json = await res.json();
		postResult = JSON.stringify(json);
	};

	const upload = () => {
		alert('업로드가 완료되었습니다.');
	};
	const alt = () => {
		alert('제목 또는 내용을 입력해주세요.');
	};
</script>

<br />
<form method="POST" on:submit|preventDefault={postArticle}>
	<div class="contents">
		<input
			class="input mb-4"
			type="text"
			placeholder="제목을 입력해주세요"
			bind:value={title}
			required
		/>
		<textarea
			class="textarea"
			id="editor"
			placeholder="내용을 입력하세요."
			bind:value={content}
			required
		/>
		<hr />
	</div>
	<!-- <div class="file has-name">
		<label class="file-label">
			<input class="file-input" type="file" name="resume" />
			<span class="file-cta">
				<span class="file-icon">
					<i class="fas fa-upload" />
				</span>
				<span class="file-label"> Choose a file… </span>
			</span>
			<span class="file-name" />
		</label>
	</div>
	<br /> -->
	<!-- {#if title != '' && content != ''}
		<button class="button is-link" type="submit" on:click={alt}
			>완료</button
		>
	{:else}
		<a href="/board/free/1"
			><button class="button is-link" type="submit" on:click={upload}
				>완료</button
			>
		</a>
	{/if} -->
	<a href="/board/free/1"
		><button class="button is-link" type="submit" on:click={upload}
			>완료</button
		>
	</a>
	<button class="button is-link is-light" type="button">취소</button>
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
