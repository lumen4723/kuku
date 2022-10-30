<script>
	import "bulma/css/bulma.css";
	import "@fortawesome/fontawesome-free/css/all.css";
	import { page } from "$app/stores";
	import { browser } from "$app/env";

	let navbarStatus = false;

	let loginBtnStr = "Login";
	let loginBtnactivate = true;
	let username = null;
	if (browser) {
		username = window.localStorage.getItem("user.username");
		if (username != null) {
			loginBtnStr = username;
			loginBtnactivate = false;
		}
	}

	const logout = async () => {
		if (username != null) {
			await fetch(`//api.eyo.kr:8081/user/logout`, {
				method: "POST",
				headers: {
					Accept: "application/json",
				},
				mode: "cors",
				credentials: "include",
			})
				.then((res) => {
					if (res.ok == false) return Promise.reject(res);
				})
				.then(() => {
					if (browser) {
						window.localStorage.removeItem("user.email");
						window.localStorage.removeItem("user.id");
						window.localStorage.removeItem("user.username");
					}
					location.href = "/";
				})
				.catch((e) => {
					console.log(e);
				});
		}
	};
</script>

<header class="header">
	<nav class="navbar is-primary is-fixed-top">
		<div class="container">
			<div class="navbar-brand">
				<a
					class="navbar-item"
					sveltekit:prefetch
					on:click={() => (navbarStatus = false)}
					href="/">KUKU</a
				>
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
						class:is-active={$page.url.pathname.startsWith(
							"/board/free"
						)}
						sveltekit:prefetch
						href="/board/free/1"
						on:click={() => (navbarStatus = false)}>자유게시판</a
					>
					<a
						class="navbar-item"
						class:is-active={$page.url.pathname.startsWith(
							"/board/qna"
						)}
						sveltekit:prefetch
						href="/board/qna/1"
						on:click={() => (navbarStatus = false)}>질문게시판</a
					>
					<a
						class="navbar-item"
						class:is-active={$page.url.pathname.startsWith(
							"/study"
						)}
						sveltekit:prefetch
						href="/study"
						on:click={() => (navbarStatus = false)}>문제</a
					>
				</div>
				<div class="navbar-end">
					<a
						class="navbar-item"
						on:click={() => (navbarStatus = false)}
						sveltekit:prefetch
						href={loginBtnactivate ? "/account" : "/mypage"}
						>{loginBtnStr}</a
					>

					{#if !loginBtnactivate}
						<a
							class="navbar-item"
							sveltekit:prefetch
							href="/"
							on:click={logout}>Logout</a
						>
					{/if}
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
