<script>
	// export let article;
	let isLogin = true;
</script>

<header>
	<div style="padding: 16px">
		{#if isLogin}
			<div class="edit" style="float: right; margin-top: 16px">
				<a href="/"
					><button class="button is-rounded is-light"> 수정 </button></a
				>
				<button class="button is-rounded is-light"> 삭제 </button>
			</div>
		{/if}

		<div style="float:left;">
			<span class="is-size-3">title</span> <br />
			<div style="float: left;">
				<a class="author" href="/" style="color: #4A4A4A;">author</a>
				<span style="color: #DBDBDB;">|</span>
				created
			</div>
		</div>
		<div style="clear:both" />

		<div style="float:left;">
			<div>
				<div class="icon is-medium" style="float: left;">
					<i class="fa-solid fa-tag" />
				</div>
				<a href="/board/qna/tag/">
					<button
						class="button is-rounded is-link is-light is-small is-responsive"
					>
						태그
					</button>
				</a>
			</div>
		</div>
	</div>
</header>
