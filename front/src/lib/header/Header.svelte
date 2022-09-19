<script>
	import { page } from '$app/stores';
	let navbarStatus = false;
</script>

<header>
	<section class="hero is-primary">
		<div class="hero-head">
			<nav class="navbar">
				<div
					class="container is-fluid"
					style="padding: 0px 6%;	position: fixed;"
				>
					>
					<div class="navbar-brand">
						<a class="navbar-item" sveltekit:prefetch href="/">KUKU</a>

						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							role="button"
							class="navbar-burger"
							aria-label="menu"
							aria-expanded="false"
							data-target="navbarMenuHeroA"
							on:click={() => (navbarStatus = !navbarStatus)}
						>
							<span aria-hidden="true" />
							<span aria-hidden="true" />
							<span aria-hidden="true" />
						</a>
					</div>
					<div
						id="navbarMenuHeroA"
						class="navbar-menu"
						class:is-active={navbarStatus}
					>
						<div class="navbar-start">
							<a
								class="navbar-item"
								class:is-active={$page.url.pathname === '/board/free'}
								sveltekit:prefetch
								href="/board/free">자유게시판</a
							>
							<a
								class="navbar-item"
								class:is-active={$page.url.pathname === '/board/qna'}
								sveltekit:prefetch
								href="/board/qna">질문게시판</a
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
		</div>
	</section>
</header>
