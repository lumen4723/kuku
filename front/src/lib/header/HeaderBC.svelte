<script>
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
					>가나다라마바사아자차카타파하</a
				>
				<span style="color: #DBDBDB;">|</span>
				2022-09-18 &nbsp; 20:46:24
			</div>
			<div class="tags" style="float:left; clear:both; margin-top:1em">
				<div class="icon is-medium" style="float: left;">
					<i class="fa-solid fa-tag" />
				</div>
				<a href="/board/free/tag/tag">
					<button
						class="button is-rounded is-link is-light is-small is-responsive"
					>
						태그
					</button>
				</a>
			</div>
		</div>
		<div style="clear:both" />
	</div>
</header>
