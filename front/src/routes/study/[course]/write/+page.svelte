<script>
	import { onMount } from "svelte";
	import { browser } from "$app/env";
	import { is_empty } from "svelte/internal";
	import Swal from "sweetalert2";
	import CodeEditor from "$lib/codeEditor.svelte";

	let title = "",
		content = "";

	let course = [];
	let chapter = [{ id: "", title: "(최상위)" }];
	let language = [
		{
			name: "Cpp",
			code: '#include <stdio.h>\n\nint main() {\n\tint a = 0;\n\tscanf("%d", &a);\n\tprintf("%d", a);\n\n\treturn 0;\n}',
		},
		{
			name: "Python",
			code: "a = int(input())\nprint(a)",
		},
		{
			name: "Java",
			code: "import java.util.Scanner;\n\npublic class Main {\n\tpublic static void main(String[] args) {\n\t\tScanner sc = new Scanner(System.in);\n\t\tint a = sc.nextInt();\n\t\tSystem.out.println(a);\n\t}\n}",
		},
	];

	let selected_course = "";
	let selected_chapter = "";
	let selected_language = language[0].name;
	let getCodeData;

	if (browser) {
		// get chapter list

		fetch(`//api.eyo.kr:8081/study/list`, {
			method: "GET",
			headers: {
				Accept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		})
			.then((resp) => resp.json())
			.then((data) => {
				course = data;
			});
	}

	$: {
		if (selected_course != "") {
			fetch(`//api.eyo.kr:8081/study/${selected_course}/list`, {
				method: "GET",
				headers: {
					Accept: "application/json",
				},
				mode: "cors",
				credentials: "include",
			})
				.then((resp) => resp.json())
				.then((data) => {
					chapter = [{ id: "", title: "(최상위)" }];
					data.forEach((item) => {
						chapter.push(item);
					});
				});
		}
	}

	let ckeditorInstance;
	// let ClassicEditor;
	onMount(async () => {
		if (browser)
			ClassicEditor.create(document.querySelector("#editor"), {
				simpleUpload: {
					// The URL that the images are uploaded to.
					uploadUrl: "//api.eyo.kr:8081/upload/",

					// Enable the XMLHttpRequest.withCredentials property.
					withCredentials: true,
				},
			})
				.then((editor) => {
					ckeditorInstance = editor;
				})
				.catch((error) => {
					console.error(error);
				});
	});

	const postArticle = () => console.log(getCodeData());
</script>

<svelte:head>
	<script src="/ckeditor.js"></script>
</svelte:head>

<br />
<div class="editor">
	<form method="POST" on:submit|preventDefault={postArticle}>
		<div class="contents">
			<header class="control is-flex">
				<div class="select">
					<select bind:value={selected_course}>
						<option value="" disabled selected>강의</option>
						{#each course as c}
							<option value={c.id}>{c.title}</option>
						{/each}
					</select>
				</div>
				<div class="select">
					<select bind:value={selected_chapter}>
						<option value="" disabled selected>상위 챕터</option>
						{#each chapter as c}
							<option value={c.id}>{c.title}</option>
						{/each}
					</select>
				</div>
				<div class="select">
					<select bind:value={selected_language}>
						<option value="" disabled selected>언어</option>
						{#each language as lang}
							<option value={lang.name}>{lang.name}</option>
						{/each}
					</select>
				</div>
				<input
					class="mb-4 input"
					type="text"
					placeholder="챕터 명을 입력해주세요"
					bind:value={title}
					required
				/>
			</header>
			<textarea
				class="textarea"
				id="editor"
				placeholder="내용을 입력하세요."
				required>{content}</textarea
			>
			<hr />
			<h2 class="title">기본 예제코드</h2>
			<CodeEditor
				language={selected_language}
				code={language.find((lang) => lang.name == selected_language)
					.code}
				bind:getData={getCodeData}
			/>
			<br /><br /><br />
		</div>
		<a href="/board/free/1"
			><button class="button is-link" type="submit" on:click={postArticle}
				>완료</button
			>
		</a>
		<a href="/board/free/1"
			><button class="button is-link is-light" type="button">취소</button
			></a
		>
	</form>
</div>
<br /> <br />

<style>
	header.control select {
		margin-right: 4px;
		width: 155px;
	}
	header.control input {
		width: calc(100% - 479px);
	}
	.editor {
		width: calc(100% - 400px - 8px);
		margin: 0 auto;
	}
	textarea {
		width: 100%;
		height: 80em;
		resize: none;
	}

	CodeEditor {
		height: 80em;
	}

	:global(.ck-editor__editable_inline) {
		min-height: 600px;
	}
</style>
