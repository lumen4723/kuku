<script>
	import { page } from '$app/stores';
</script>

<header>
	<section class="hero is-primary">
		<div class="hero-head">
			<nav class="navbar">
				<div class="container">
					<div class="navbar-brand">
						<a class="navbar-item" sveltekit:prefetch href="/">KUKU</a>
					</div>
					<div class="navbar-menu">
						<div class="navbar-start">
							<a
								class="navbar-item"
								class:active={$page.url.pathname === '/boardFree'}
								sveltekit:prefetch
								href="/boardFree">자유게시판</a
							>
							<a
								class="navbar-item"
								class:active={$page.url.pathname === '/boardQna'}
								sveltekit:prefetch
								href="/boardQna">질문게시판</a
							>
							<a
								class="navbar-item"
								class:active={$page.url.pathname === '/study'}
								sveltekit:prefetch
								href="/study">문제</a
							>
							<div class="navbar-item has-dropdown is-active">
								<a class="navbar-link">뭐하지</a>
								<div class="navbar-dropdown">
									<a class="navbar-item">Overview</a>
									<a class="navbar-item">Elements</a>
									<a class="navbar-item">Components</a>
									<hr class="navbar-divider" />
									<div class="navbar-item">Version 0.9.4</div>
								</div>
							</div>
						</div>
						<div class="navbar-end">
							<a class="navbar-item" sveltekit:prefetch href="/account"
								>Login</a
							>
						</div>
					</div>
				</div>
			</nav>
		</div>
	</section>
</header>
