<script>
	import HeaderBF from '$lib/header/HeaderBF.svelte';
	import HeaderBQ from '$lib/header/HeaderBQ.svelte';
	import { page } from '$app/stores';
</script>

{#if $page.url.pathname === '/board/free'}
	<HeaderBF />
{:else if $page.url.pathname === '/board/qna'}
	<HeaderBQ />
{/if}

<main class="container is-max-desktop">
	<slot />
</main>
