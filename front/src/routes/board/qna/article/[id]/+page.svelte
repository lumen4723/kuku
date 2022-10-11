<script>
	import { page } from "$app/stores";
	import List from "../../[page]/+page.svelte";
	// import Header from '$lib/header/HeaderBQC.svelte';

	const getArticle = async (article_id) => {
		const res = await fetch(
			`//api.eyo.kr:8081/board/qna/article/${article_id}?article_id=${article_id}`,
			{
				mode: "cors",
				credentials: "include",
			}
		);

		const qnaboard = await res.json();
		if (res.ok) {
			return qnaboard;
		} else {
			throw new Error(qnaboard);
		}
	};

	let article = getArticle($page.params.id);

	const like_qna = async (article_id) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/qna/article/${article_id}/like`,
			{
				method: "POST",
				mode: "cors",

				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					article_id: article_id,
				}),
			}
		);
		const like = await res.json();
		if (res.ok) {
			return like;
		} else {
			throw new Error(like);
		}
	};

	//dislike_qna fetch 함수
	const dislike_qna = async (article_id) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/qna/article/${article_id}/dislike`,
			{
				method: "POST",
				mode: "cors",

				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					article_id: article_id,
				}),
			}
		);
		const dislike = await res.json();
		if (res.ok) {
			return dislike;
		} else {
			throw new Error(dislike);
		}
	};

	let isClicked = false;
	const likeclick = () => {
		isClicked = !isClicked;
		if (isClicked) {
			like_qna($page.params.id);
		} else {
			dislike_qna($page.params.id);
		}
	};
	const alt = () => {
		alert("로그인이 필요합니다.");
	};

	let isClicked2 = false;
	const likeclick2 = () => {
		isClicked2 = !isClicked2;
	};
	const alt2 = () => {
		alert("로그인이 필요합니다.");
	};

	let isLogin = true;
</script>

{#await article then article}
	<header>
		<div style="padding: 16px">
			{#if isLogin}
				<div class="edit" style="float: right; margin-top: 16px">
					<a href="/"
						><button class="button is-rounded is-light">
							수정
						</button></a
					><a href="/board/qna/1">
						<button class="button is-rounded is-light">
							삭제
						</button>
					</a>
				</div>
			{/if}
			<div style="float:left;">
				<span class="is-size-3">{article.title}</span>
				{#if article.answers == true}
					<span style="float: inline-end;">
						<span class="icon is-large ">
							<i
								class="fas fa-check-circle fas fa-2x"
								style="color: greenyellow"
							/>
						</span>
					</span>
				{:else}
					<span style="float: inline-end;">
						<span class="icon is-large">
							<i
								class="fas fa-check-circle fas fa-2x"
								style="color: #4A4A4A;"
							/>
						</span>
					</span>
				{/if}
				<br />
				<div style="float: left;">
					<a class="author" href="/" style="color: #4A4A4A;"
						>{article.username}</a
					>
					<span style="color: #DBDBDB;">|</span>
					{article.created}
				</div>
			</div>
			<div style="clear:both" />
			<div style="float:left;">
				<div>
					<div class="icon is-medium" style="float: left;">
						<i class="fa-solid fa-tag" />
					</div>
					<a href="/">
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

	<div style="clear:both" />

	<hr style="margin:0;" />

	<div class="content">
		{@html article.content}
		<!--이 부분은 질문의 내용 부분입니다. <br />
	양식에 맞게 질문을 작성해주세요. <br /><br />
	ex) 여기 링크가 있습니다. <a href="/">기술 블로그</a> <br />
	,등등-->
	</div>

	<div
		style="margin: 0 0 0 100%; width: auto%; text-align: center; float: right"
	>
		<span class="is-size-3">
			{#if isLogin}
				<i
					class={isClicked
						? "fa-solid fa-heart"
						: "fa-regular fa-heart"}
					on:click={likeclick}
				/>
			{:else}
				<i class="fa-regular fa-heart" on:click={alt} />
			{/if}
		</span>
		<span>추천 {article.like}</span>
	</div>
{/await}

<hr style="margin-top: 0;" />

<div style="padding: 5px ">
	<div style="float: left;">
		<a href="/board/qna/1"
			><button class="button is-rounded is-light">목록</button></a
		>
	</div>
	<div style="float: right;">
		<a href="/board/qna/write/answer"
			><button class="button is-rounded is-light">답글 작성</button></a
		>
	</div>
</div>
<br /><br />
<div style="padding: 16px">
	<div style="float: left;">
		<div class="icon is-medium" style="float: left;">
			<i class="fa-solid fa-comment" />
		</div>
		<span class="is-size-4">답변</span>
	</div>
	<div style="clear:both" />
</div>

{#await article}
	<p class="has-text-centered">Loading in progress...</p>
{:then article}
	{#each article["answers"] as answer}
		<div class="comment">
			<table class="table container is-fluid comment_table">
				<tbody>
					<tr>
						<td
							style="text-align: left; width: 100px; border-right: 2px solid #dbdbdb; padding: 10px;"
						>
							<a
								class="comment_author"
								href="/"
								style="color: #4A4A4A;">{answer.author}</a
							>
						</td>
						<td style="width: 900px;">{answer.created}</td>
						<td style="left: 100%;">
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
											? "fa-solid fa-heart"
											: "fa-regular fa-heart"}
										on:click={likeclick2}
									/>
								{:else}
									<i
										class="fa-regular fa-heart"
										on:click={alt}
									/>
								{/if}
							</span>
							<span>추천 {answer.like}</span>
						</div>
					</tr>
				</tbody>
			</table>

			<div class="comment_WordStyle">
				<div class="comment_content">
					{@html answer.content}<br />
				</div>
			</div>

			<hr style="margin: 0;" />
		</div>
	{/each}
{/await}

<br /><br />
<!--
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
-->
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
		height: 100px;
		padding: 16px;
	}
	.comment table {
		width: 100%;
		border: 1px solid #dbdbdb;
		background-color: rgba(239, 235, 235, 0.805);
		margin: 0 0 0 0;
	}
	.comment_WordStyle {
		padding: 0 100px 0 100px;
		height: 100px;
		border-left: solid 2px #dbdbdb;
		border-right: solid 2px #dbdbdb;
		/*		border-bottom-right-radius: 10px;
		border-bottom-left-radius: 10px; */
	}
</style>
