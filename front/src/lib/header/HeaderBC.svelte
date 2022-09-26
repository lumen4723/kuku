<script>
	export let article;
	let isLogin = false;
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
			<span class="is-size-3">Title</span> <br />
			<div style="float: left;">
				<a class="author" href="/" style="color: #4A4A4A;"
					>{article.title}</a
				>
				<span style="color: #DBDBDB;">|</span>
				{article.created}
			</div>
		</div>
		<div style="clear:both" />
	</div>
</header>
