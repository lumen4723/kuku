<script>
	import { page } from '$app/stores';
	import List from '../../[page]/+page.svelte';
	import Header from '$lib/header/HeaderBQC.svelte';

	// const getArticle = async (article_id) => {
	// 	const res = await fetch(
	// 		`http://api.eyo.kr:8081/board/qna/list?start_page=${article_id}`,
	// 		{
	// 			mode: 'cors'
	// 		}
	// 	);

	// 	const article = await res.json();
	// 	if (res.ok) {
	// 		return article;
	// 	} else {
	// 		throw new Error(article);
	// 	}
	// };

	// let article = getArticle($page.params.id || 1);

	let isClicked = false;
	const likeclick = () => {
		isClicked = !isClicked;
	};
	const alt = () => {
		alert('로그인이 필요합니다.');
	};

	let isClicked2 = false;
	const likeclick2 = () => {
		isClicked2 = !isClicked2;
	};
	const alt2 = () => {
		alert('로그인이 필요합니다.');
	};

	let isLogin = true;
</script>

<Header />

<div style="clear:both" />

<hr style="margin:0;" />

<div class="content">
	이 부분은 질문의 내용 부분입니다. <br />
	양식에 맞게 질문을 작성해주세요. <br /><br />
	ex) 여기 링크가 있습니다. <a href="/">기술 블로그</a> <br />
	,등등
</div>

<div style="margin: 0 0 0 870px; width: 100px; text-align: center; 	">
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
	<div>추천 count</div>
</div>

<hr style="margin-top: 0;" />

<div class="comment">
	<table class="table container is-fluid">
		<tbody>
			<tr>
				<td style="text-align: left; width: 100px;"
					><a href="/">댓글이름</a></td
				>
				<td style="width: 600px;">2022-09-15 &nbsp; 19:29:50</td>
				<td>
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

				<div style="text-align: center; float: right;">
					<span class="is-size-4">
						{#if isLogin}
							<i
								class={isClicked2
									? 'fa-solid fa-heart'
									: 'fa-regular fa-heart'}
								on:click={likeclick2}
							/>
						{:else}
							<i class="fa-regular fa-heart" on:click={alt} />
						{/if}
					</span>
					<span>추천 count</span>
				</div>
			</tr>
		</tbody>
	</table>
	{#if isLogin}
		<textarea class="textarea" placeholder="댓글을 입력하세요." />
		<button class="button">댓글 쓰기</button>
	{:else}
		<textarea
			class="textarea"
			placeholder="댓글을 쓰려면 로그인이 필요합니다."
		/>
		<button class="button" on:click={alt}>댓글 쓰기</button>
	{/if}
</div>

<br /><br /><br />
<List />

<style>
	hr {
		border: 1px solid #dbdbdb;
	}
	span i {
		position: static;
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
