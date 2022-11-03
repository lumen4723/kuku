<script>
	import { page } from "$app/stores";
	import { browser } from "$app/env";
	import Swal from "sweetalert2";
	import Changeuser from "./Changeuser.svelte";
	import Withdrawal from "./Withdrawal.svelte";

	let currentPage = "Changeuser";
	const isSignup = $page.url.searchParams.has("msg");
	const afterSignup = () => {
		Swal.fire({
			title: "회원정보 변경이 완료되었습니다.	변경된 정보로 다시 로그인 해주세요.",
			icon: "success",
			confirmButtonText: "확인",
		});
		logout();
	};

	const logout = async () => {
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
					window.location.href = "/account";
				}
			})
			.catch((e) => {
				console.log(e);
			});
	};

	$: if (isSignup) afterSignup();
</script>

<div class="container">
	<div class="columns">
		<div class="column is-2">
			<aside class="menu">
				<p class="menu-label">ADMINISTRATION</p>
				<ul class="menu-list">
					<li>
						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							class:is-active={currentPage == "Changeuser"}
							on:click={() => (currentPage = "Changeuser")}
						>
							정보수정
						</a>
					</li>
					<li>
						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							class:is-active={currentPage == "Withdrawal"}
							on:click={() => (currentPage = "Withdrawal")}
						>
							회원탈퇴
						</a>
					</li>
				</ul>
			</aside>
		</div>
		<div class="column is-8">
			{#if currentPage == "Changeuser"}
				<Changeuser />
			{:else if currentPage == "Withdrawal"}
				<Withdrawal />
			{:else}
				ERROR!@!
			{/if}
		</div>
	</div>
</div>

<style>
	.container {
		margin-top: 1rem;
		margin-bottom: 2rem;
	}
	.menu {
		border-right: 1px solid #eaecef;
	}
</style>
