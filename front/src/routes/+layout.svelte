<script>
	import 'bulma/css/bulma.css';
	import '@fortawesome/fontawesome-free/css/all.css';
	import { page } from '$app/stores';
	let navbarStatus = false;
</script>

<header class="header">
	<nav class="navbar is-primary is-fixed-top">
		<div class="container">
			<div class="navbar-brand">
				<a class="navbar-item" sveltekit:prefetch href="/">KUKU</a>
				<!-- svelte-ignore a11y-missing-attribute -->
				<a
					role="button"
					class="navbar-burger"
					aria-label="menu"
					aria-expanded="false"
					data-target="navbarMenu"
					on:click={() => (navbarStatus = !navbarStatus)}
				>
					<span aria-hidden="true" />
					<span aria-hidden="true" />
					<span aria-hidden="true" />
				</a>
			</div>
			<div
				id="navbarMenu"
				class="navbar-menu"
				class:is-active={navbarStatus}
			>
				<div class="navbar-start">
					<a
						class="navbar-item"
						class:is-active={$page.url.pathname === '/board/free'}
						sveltekit:prefetch
						href="/board/free/1">자유게시판</a
					>
					<a
						class="navbar-item"
						class:is-active={$page.url.pathname === '/board/qna'}
						sveltekit:prefetch
						href="/board/qna/1">질문게시판</a
					>
					<a
						class="navbar-item"
						class:is-active={$page.url.pathname === '/study'}
						sveltekit:prefetch
						href="/study">문제</a
					>
					<!-- <div class="navbar-item has-dropdown">
								<a class="navbar-link">뭐하지</a>
								<div class="navbar-dropdown ">
									<a class="navbar-item"> Overview </a>
									<a class="navbar-item"> Modifiers </a>
									<a class="navbar-item"> Columns </a>
									<a class="navbar-item"> Layout </a>
									<a class="navbar-item"> Form </a>
									<hr class="navbar-divider" />
									<a class="navbar-item"> Elements </a>
									<a class="navbar-item"> Components </a>
								</div>
							</div> -->
				</div>
				<div class="navbar-end">
					<a class="navbar-item" sveltekit:prefetch href="/account"
						>Login</a
					>
				</div>
			</div>
		</div>
	</nav>
</header>

<main>
	<slot />
</main>

<footer class="footer">
	<div class="content has-text-centered"><p>kuku@뻐꾸기</p></div>
</footer>
