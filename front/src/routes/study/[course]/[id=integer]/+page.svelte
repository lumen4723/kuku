<script>
	import { afterUpdate, beforeUpdate, onDestroy, tick } from "svelte";
	import { page } from "$app/stores";
	import { goto } from "$app/navigation";
	import env from "$lib/env.js";

	import prism from "prismjs";
	import "prismjs/plugins/custom-class/prism-custom-class.js";
	import "prismjs/components/prism-c.min.js";
	import "prismjs/components/prism-cpp.min.js";
	import "prismjs/components/prism-java.min.js";
	import "prismjs/components/prism-python.min.js";

	// import "$lib/prism/themes/prism.css";
	import "$lib/prism/themes/prism-tomorrow.css";

	import "$lib/ckeditor/styles.css";
	import ChapterListItem from "./chapterListItem.svelte";
	import CodeEditor from "$lib/codeEditor.svelte";

	prism.manual = true;
	prism.plugins.customClass.map({ number: "prism-number", tag: "prism-tag" });

	let element_chapter_select;
	let element_article;

	const course_id = $page.params.course;
	let chapter_id = $page.params.id.match(/\d+/);

	let articles = [];
	let supported_language = [];
	let selected_language = "";

	let run_token = "";
	let run_output = " >> 실행 버튼을 눌려주세요";

	let chapter_tree = [];
	let chapter_kv = {};

	let cancelation_token = null;
	let get_editor_code = () => "";

	onDestroy(() => {
		if (cancelation_token != null) {
			cancelation_token.cancel();
		}
	});
	beforeUpdate(() => {
		if (cancelation_token != null) {
			cancelation_token.cancel();
		}
	});

	async function async_chapter_list(course_id) {
		console.log(chapter_tree.length);
		if (chapter_tree.length != 0) return Promise.resolve("already loaded");

		return fetch(`${env.baseUrl}/study/${course_id}/list`, {
			method: "GET",
			headers: {
				Accept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		}).then((resp) =>
			resp
				.json()
				.then(function (data) {
					chapter_tree = data;

					function traverse(node) {
						chapter_kv[node.no] = node;

						node.children.forEach((child) => {
							traverse(child);
						});
					}
					data.forEach((data) => traverse(data));

					Promise.resolve(data);
				})
				.then((data) => {
					element_chapter_select.value = chapter_id;
					element_chapter_select.querySelector(
						`option[value="${chapter_id}"]`
					).selected = true;

					return Promise.resolve(data);
				})
		);
	}

	async function async_chapter_article(course_id, chapter_id) {
		return fetch(`${env.baseUrl}/study/${course_id}/${chapter_id}/`, {
			method: "GET",
			headers: {
				Accept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		})
			.then((resp) => {
				if (resp.ok) return resp.json();
				return Promise.reject(resp);
			})
			.then((data) => {
				articles = data;
				supported_language = data.map((article) => article.language);

				return Promise.resolve(data);
			})
			.then((data) => {
				if (data.length > 0) {
					selected_language = data[0].language;
				}

				return Promise.resolve(data);
			})
			.catch((err) => {
				console.log(err);
			});
	}

	function run_code() {
		const code = get_editor_code();
		const language = selected_language;

		return fetch(`${env.baseUrl}/run/`, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			mode: "cors",
			credentials: "include",
			body: JSON.stringify({
				code: code,
				language: language,
			}),
		})
			.then((resp) => {
				console.log(resp);

				if (!resp.ok) return Promise.reject(resp);
				return resp.json();
			})
			.then((data) => {
				run_token = data;

				return Promise.resolve(data);
			})
			.then((token) => {
				const max_count = 10;
				let try_count = 0;
				cancelation_token = setInterval(() => {
					// 기본적으로 카운트를 까되, pending 상태면 보상을 하는 방식으로 구현
					if (try_count++ > max_count) {
						clearInterval(cancelation_token);
						return;
					}

					if (token != run_token) {
						clearInterval(cancelation_token);
						return;
					}

					fetch(`${env.baseUrl}/run/${token}/`, {
						method: "GET",
						headers: {
							Accept: "application/json",
						},
						mode: "cors",
						credentials: "include",
					})
						.then((resp) => resp.json())
						.then((data) => {
							run_done = data.done;
							run_output = data.output;

							if (run_done) {
								clearInterval(cancelation_token);
							}
						});
				}, 1000);
			})
			.catch((err) => {
				console.log(err);
			});
	}

	function get_article(chapter_id, language) {
		if (chapter_id == null) {
			return "";
		}

		return articles.filter((article) => article.language == language)[0]
			.content;
	}
	function get_code(chapter_id, language) {
		if (chapter_id == null || articles == null) {
			return "";
		}

		let article = articles.filter(
			(article) => article.language == language
		);

		if (article.length == 0) {
			return "";
		}

		return article[0].code;
	}

	async function highlight_code() {
		await tick();
		if (element_article) {
			prism.highlightAllUnder(element_article);
		}

		return "";
	}
	afterUpdate(() => {
		highlight_code();
	});

	function change_chapter(e) {
		goto(`/study/${course_id}/${e.target.value}`);
	}
</script>

<main class="columns mt-0 mb-0">
	<aside class="column is-three-fifths pt-0 pr-0">
		<header class="p-2">
			<select
				bind:this={element_chapter_select}
				bind:value={chapter_id}
				on:change={change_chapter}
				style="display: block; width: 100%"
			>
				{#each chapter_tree as item}
					<ChapterListItem
						{item}
						{course_id}
						selected_id={chapter_id}
					/>
				{/each}
			</select>
		</header>
		<article
			class="content p-2 pb-4 ck-content"
			bind:this={element_article}
		>
			{#await Promise.all( [async_chapter_list(course_id), async_chapter_article(course_id, chapter_id)] )}
				<div class="p-6">
					<progress class="progress is-small is-primary" max="100"
						>Loading in progress</progress
					>
				</div>
			{:then}
				{@html get_article(chapter_id, selected_language)}
				{highlight_code() === null || ""}
			{/await}
		</article>
	</aside>
	<section id="editor" class="column is-two-fifths pt-0 pr-0 pl-0">
		<header class="container is-fluid">
			<select name="language" bind:value={selected_language}>
				{#each supported_language as language}
					<option value={language}>{language}</option>
				{/each}
			</select>
			<button class="button is-info" on:click={run_code}
				>Run <i class="fa-solid fa-play ml-3 is-size-7" />
			</button>
		</header>
		<CodeEditor
			bind:getData={get_editor_code}
			language={selected_language}
			code={get_code(chapter_id, selected_language, articles)}
		/>
		<section id="output" class="p-2 is-family-code">{run_output}</section>
	</section>
</main>

<style>
	aside {
		/* width: calc(100% - 700px);
		height: calc(100vh - 52px);
		float: left; */
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
		/* width: 700px;
		float: right; */
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
