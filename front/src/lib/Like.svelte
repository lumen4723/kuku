<script>
	let isClicked = false;
	const likeclick = () => {
		isClicked = !isClicked;
	};
	const alt = () => {
		alert('로그인이 필요합니다.');
	};
	let isLogin = false;
</script>

<div style="bottom: 0;">
	<span class="is-size-3">
		{#if isLogin}
			<i
				class={isClicked ? 'fa-solid fa-heart' : 'fa-regular fa-heart'}
				on:click={likeclick}
			/>
		{:else}
			<i class="fa-regular fa-heart" on:click={alt} />
		{/if}
	</span>
	추천 count
</div>

<style>
	span i {
		color: rgb(251, 106, 130);
	}
</style>
