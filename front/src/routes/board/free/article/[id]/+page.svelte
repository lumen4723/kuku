<script>
	import { page } from '$app/stores';
	import List from '../../[page]/+page.svelte';
	import Header from '$lib/header/HeaderBC.svelte';

	const getArticle = async (article_id) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/free/article/${article_id}`,
			{
				mode: 'cors'
			}
		);

		const article = await res.json();
		if (res.ok) {
			return article;
		} else {
			throw new Error(article);
		}
	};

	let article = getArticle($page.params.id);

	//let count;
	//count = isClicked? count+1 : count
	let isClicked = false;
	const likeclick = () => {
		isClicked = !isClicked;
	};
	const alt = () => {
		alert('로그인이 필요합니다.');
	};
	let isLogin = false;
</script>

{#await article}
	<p class="has-text-centered">Loading in progress...</p>
{:then article}
	<Header {article} />

	<hr style="margin:0;" />

	<div class="content">{@html article.content}</div>

	<div style="margin: 0 auto; width: 100px; text-align: center">
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
		<div>추천 {article.like}</div>
	</div>
{/await}

<hr style="margin-top: 0;" />

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
	span i {
		color: rgb(251, 106, 130);
	}
	.content {
		width: 100%;
		height: 300px;
	}
	.comment table {
		width: 100%;

		background-color: rgba(239, 235, 235, 0.805);
	}
	textarea {
		width: 100%;
		height: 5.25em;
		resize: none;
	}
</style>
