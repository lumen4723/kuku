<script>
	import { page } from '$app/stores';
	let navbarStatus = false;
</script>

<header>
	<section class="hero is-primary">
		<div class="hero-head">
			<nav class="navbar">
				<div class="container is-fluid">
					<div class="navbar-brand">
						<a class="navbar-item" sveltekit:prefetch href="/">KUKU</a>

						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							role="button"
							class="navbar-burger"
							class:is-active={navbarStatus}
							aria-label="menu"
							aria-expanded="false"
							data-target="navbarMenuHeroA"
							on:clickic={() => (navbarStatus = !navbarStatus)}
							on:clickic={() => console.log('click')}
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
							<div class="navbar-item has-dropdown is-hoverable">
								<a class="navbar-link">뭐하지</a>
								<div class="navbar-dropdown is-boxed">
									<a class="navbar-item"> Overview </a>
									<a class="navbar-item"> Modifiers </a>
									<a class="navbar-item"> Columns </a>
									<a class="navbar-item"> Layout </a>
									<a class="navbar-item"> Form </a>
									<hr class="navbar-divider" />
									<a class="navbar-item"> Elements </a>
									<a class="navbar-item is-active"> Components </a>
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
