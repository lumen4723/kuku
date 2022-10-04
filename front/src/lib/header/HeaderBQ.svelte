<script>
<<<<<<< Updated upstream:front/src/lib/header/HeaderBQ.svelte
</script>

<header>
	<!-- 검색 -->
	<section class="hero is-small ">
		<div class="hero-body">
			<div class="container">
				<h1 class="title">질문</h1>
				<h2 class="subtitle">자유롭게 질문할 수 있는 게시판입니다.</h2>
			</div>
		</div>
	</section>
</header>
=======
	import { page } from '$app/stores';
	import Page from './[page]/+page.svelte';
</script>

{#if $page.url.pathname === '/board/qna/list/[page]'}
	<header>
		<!-- 검색 -->
		<section class="hero is-small ">
			<div class="hero-body">
				<div class="container">
					<h1 class="title">질문</h1>
					<h2 class="subtitle">자유롭게 질문할 수 있는 게시판입니다.</h2>
				</div>
			</div>
		</section>
	</header>
{/if}

<main class="container">
	<slot />
</main>
>>>>>>> Stashed changes:front/src/routes/board/qna/+layout.svelte
