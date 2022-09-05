<script>
	import { page } from '$app/stores';
</script>

<header>
	<nav class="navbar">
		<div class="navbar-brand">
			<a sveltekit:prefetch href="/" class="navbar-item">KUKU</a>
		</div>

		<ul>
			<li class:active={$page.url.pathname === '/board'}>
				<a sveltekit:prefetch href="/board">게시판</a>
			</li>
			<li class:active={$page.url.pathname === '/study'}>
				<a sveltekit:prefetch href="/study">문제</a>
			</li>
		</ul>
	</nav>

	<div class="corner"><a sveltekit:prefetch href="/account">Login</a></div>
</header>

<style>
	header {
		display: flex;
		justify-content: space-between;
	}

	.corner {
		width: 3em;
		height: 3em;
	}

	nav {
		display: flex;
		justify-content: center;
	}

	ul {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
	}

	li {
		position: relative;
	}

	nav a {
		display: flex;
		align-items: center;
		padding: 0 1em;
		font-size: 1rem;
		letter-spacing: 0.1em;
		color: black;
		text-decoration: none;
	}
</style>
