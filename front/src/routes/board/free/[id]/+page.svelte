<script>
	import { page } from '$app/stores';
	import List from '../+page.svelte';

	const likeclick = () => {
		isClicked = !isClicked;
	};
	const alt = () => {
		alert('로그인이 필요합니다.');
	};
	let isLogin = false;
	let isClicked = false;
	//let count;
	//count = isClicked? count+1 : count
</script>

<div class="header" style="padding: 16px">
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
		<div>
			<div class="icon is-medium" style="float: left;">
				<i class="fa-solid fa-tag" />
			</div>
			<a href="/board/free/tag/">
				<button
					class="button is-rounded is-link is-light is-small is-responsive"
				>
					태그
				</button>
			</a>
		</div>

		<div style="float: left;">
			<a class="author" href="/" style="color: #4A4A4A;"
				>가나다라마바사아자차카타파하</a
			>
			<span style="color: #DBDBDB;">|</span>
			2022-09-18 &nbsp; 20:46:24
		</div>
	</div>
	<div style="clear:both" />
</div>

<hr style="margin:0;" />

<div class="content">
	<div>
		{$page.params.id}
		skd df sfwewfs
	</div>
	<br />
</div>
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

<hr />

<!-- table 수정 -->
<div class="comment">
	<table class="table container is-fluid">
		<tbody>
			<tr>
				<td style="text-align: left;">ㅎ</td>
				<td style="width: 150px;">나다</td>
				<td style="width: 200px;">2022-09-19 &nbsp; 20:46:24</td>
				<td style="width: 150px;">
					{#if isLogin}
						<button
							class="button is-rounded is-link is-light is-small is-responsive"
						>
							수정
						</button>
						<button
							class="button is-rounded is-link is-light is-small is-responsive"
						>
							삭제
						</button>
					{/if}
				</td>
			</tr>
		</tbody>
	</table>
	{#if isLogin}
		<textarea class="textarea" placeholder="댓글을 입력하세요" />
		<button class="button">등록</button>
	{/if}
</div>

<br /><br /><br />
<List />

<style>
	hr {
		border: 1px solid #dbdbdb;
	}
	.content {
		width: 100%;
		height: 300px;
	}
	.comment table {
		width: 100%;

		background-color: rgba(239, 235, 235, 0.805);
	}
	span i {
		color: rgb(251, 106, 130);
	}
	textarea {
		width: 100%;
		height: 5.25em;
		resize: none;
	}
</style>
