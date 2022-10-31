<script>
	export let item;
	export let course_id;

	let children = item.children;
</script>

<div>
	<a href="/study/{course_id}/{item.no}" class="panel-block chapter-item">
		<span class="panel-icon">
			<i class="fas fa-book" aria-hidden="true" />
		</span>
		{item.title}
	</a>
	{#each children as child}
		<div class="ml-2"><svelte:self item={child} {course_id} /></div>
	{/each}
</div>

<style>
	.chapter-item {
		transition-duration: 0.3s;
	}
	.chapter-item:hover {
		background-color: azure;
	}
</style>
