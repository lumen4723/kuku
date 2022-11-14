<script>
	import { page } from "$app/stores";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import ChapterListItem from "./chapterListItem.svelte";
	import CodeEditor from "$lib/codeEditor.svelte";

	let chapter_select_element;
	const course_id = $page.params.course;

	$: chapter_id = $page.params.id.match(/\d+/)[0];

	let supported_language = ["Java", "Python"];
	let selected_language = supported_language[0];

	let run_output =
		"\n\n    Anyone know how to change the language according to code file extension or first line like '#!/usr/bin/env python'?\n\n  setLanguage(node: any) {\n    if (node) {\n      const languages = {\n        'js': 'javascript',\n        'ts': 'typescript',\n        'html': 'html',\n        'htm': 'html',\n        'txt': 'text',\n        'css': 'css'\n      }\n      const ext = node.name.match(/([^.])+$/g)[0];\n\n      // this.editorComponent.instance.options.language = languages[ext];\n\n      (window as any).monaco.editor.setModelLanguage((window as any).monaco.editor.getModels()[0], languages[ext]);\n\n      return node;\n    }\n  }\n\n";

	let article_tree = [];
	let article_list = {};
	let async_chapter_list = fetch(
		`//api.eyo.kr:8081/study/${course_id}/list`,
		{
			method: "GET",
			headers: {
				Accept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		}
	).then((resp) =>
		resp
			.json()
			.then(function (data) {
				article_tree = data;

				function traverse(node) {
					article_list[node.no] = node;

					node.children.forEach((child) => {
						traverse(child);
					});
				}
				data.forEach((data) => traverse(data));

				Promise.resolve(data);
			})
			.then((data) => {
				chapter_select_element.value = chapter_id;
				chapter_select_element.querySelector(
					`option[value="${chapter_id}"]`
				).selected = true;

				return data;
			})
	);

	function print_article(chapter_id) {
		if (chapter_id == null) {
			return article_tree[0].content;
		}

		return article_list[chapter_id].content;
	}

	function change_chapter(e) {
		goto(`/study/${course_id}/${e.target.value}`);
	}
</script>

<main>
	<aside>
		<header class="p-2">
			<select
				bind:this={chapter_select_element}
				bind:value={chapter_id}
				on:change={change_chapter}
				style="display: block; width: 100%"
			>
				{#each article_tree as item}
					<ChapterListItem
						{item}
						{course_id}
						selected_id={chapter_id}
					/>
				{/each}
			</select>
		</header>
		<article class="content">
			{#await async_chapter_list}
				<div class="p-6">
					<progress class="progress is-small is-primary" max="100"
						>Loading in progress</progress
					>
				</div>
			{:then}
				{@html print_article(chapter_id)}
			{/await}
		</article>
	</aside>
	<section id="editor">
		<header>
			<select name="language" bind:value={selected_language}>
				{#each supported_language as language}
					<option value={language}>{language}</option>
				{/each}
			</select>
			<button class="button is-info"
				>Run <i class="fa-solid fa-play ml-3 is-size-7" />
			</button>
		</header>
		<CodeEditor language={selected_language} />
		<section id="output" class="p-2 is-family-code">{run_output}</section>
	</section>
</main>

<style>
	aside {
		width: calc(100% - 700px);
		height: calc(100vh - 52px);
		float: left;
		background-color: #eee;
	}

	aside header {
		background-color: #e2e2e2;
		border-bottom: 2px solid #d5d5d5;
		height: 50px;
	}
	aside select {
		height: 36px;
	}
	aside article.content {
		padding: 8px;
		height: calc(100vh - 52px - 1em - 36px);
		max-height: calc(100vh - 52px);
		overflow-y: scroll;
	}
	#editor #output {
		height: 150px;
		overflow-y: scroll;
		white-space: pre;
	}
	#editor {
		width: 700px;
		float: right;
		background: #1a1a1a;
		height: calc(100vh - 52px);
	}
	#editor header {
		height: 50px;
		background: #1a1a1a;
		border: 2px solid #343434;
		text-align: right;
		padding: 4px;
	}
	#editor header > * {
		height: 36px;
	}
	main {
		height: calc(100vh - 52px);
	}
	:global(body > div > main) {
		height: calc(100vh - 52px);
	}
	:global(body > div > footer.footer) {
		display: none;
	}
</style>
