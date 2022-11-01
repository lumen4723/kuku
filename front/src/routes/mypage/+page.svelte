<script>
	import Myprofile from "./Myprofile.svelte";
	import Changeuser from "./Changeuser.svelte";
	import Withdrawal from "./Withdrawal.svelte";
	let currentPage = "Myprofile";
	
</script>

<div class="container">
	<div class="columns">
		<div class="column is-2">
			<aside class="menu">
				<p class="menu-label">General</p>
				<ul class="menu-list">
					<li>
						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							class:is-active={currentPage == "Dashboard"}
							on:click={() => (currentPage = "Dashboard")}
							>대쉬보드</a
						>
					</li>
				</ul>
				<p class="menu-label">ADMINISTRATION</p>
				<ul class="menu-list">
					<li>
						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							class:is-active={currentPage == "Myprofile"}
							on:click={() => (currentPage = "Myprofile")}
						>
							프로필
						</a>
					</li>
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
			{#if currentPage == "Myprofile"}
				<Myprofile />
			{:else if currentPage == "Changeuser"}
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
