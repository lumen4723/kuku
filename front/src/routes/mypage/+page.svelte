<script>
	import Changeuser from "./Changeuser.svelte";
	import Withdrawal from "./Withdrawal.svelte";

	let currentPage = "Changeuser";
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
