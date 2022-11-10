<script>
	import { page } from "$app/stores";
	import ChapterListItem from "./chapter_list_item.svelte";

	const course_id = $page.params.course;
	$: chapter_id = $page.params.id.match(/\d+/)[0];

	let article_tree = [];
	let article_list = {};
	const async_chapter_list = fetch(
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
		resp.json().then(function (data) {
			article_tree = data;

			function traverse(node) {
				article_list[node.no] = node;

				node.children.forEach((child) => {
					traverse(child);
				});
			}
			data.forEach((data) => traverse(data));

			return data;
		})
	);

	function print_article(chapter_id) {
		if (chapter_id == null) {
			return article_tree[0].content;
		}

		return article_list[chapter_id].content;
	}
</script>

{#await async_chapter_list}
	<div class="p-6">
		<progress class="progress is-small is-primary" max="100"
			>Loading in progress</progress
		>
	</div>
{:then list}
	<main>
		<aside>
			{#each list as item}
				<ChapterListItem {item} {course_id} />
			{/each}
		</aside>
		<article class="p-2">
			<div class="content">
				{@html print_article(chapter_id)}
			</div>
		</article>
	</main>
{/await}

<style>
	aside {
		width: 250px;
		float: left;
		max-height: calc(100vh - 52px);
		overflow-y: scroll;
	}
	article {
		width: calc(100% - 250px);
		float: right;
		background: white;
		min-height: calc(100vh - 220px);
	}
	article .content {
		max-width: 768px;
		margin: 0 auto;
	}

	main {
		min-height: calc(100vh - 220px);
		background-color: whitesmoke;
	}
	:global(body > div > main) {
		min-height: calc(100vh - 220px);
	}
</style>
