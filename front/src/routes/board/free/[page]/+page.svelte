<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { each } from 'svelte/internal';
	import Layout from '../../../+layout.svelte';

	let current_page = 1;
	let pageLimit = 10;

	const getBoardList = async (pageIdx, pageLimit) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/free/list/${pageIdx}?limit=${pageLimit}`,
			{
				mode: 'cors'
			}
		);
		const freeBoard = await res.json();
		if (res.ok) {
			return freeBoard;
		} else {
			throw new Error(freeBoard);
		}
	};

	const changePage = (p) => {
		console.log('changePage');
		current_page = p + 1;
	};

	// let boardList = getBoardList(
	// 	$page.params.page || current_page,
	// 	pageLimit
	// );
	let boardList = getBoardList(current_page, pageLimit);
</script>

<div class="container">
	<table
		class="table container is-fluid has-text-centered"
		style="margin-bottom: 0;"
	>
		<thead>
			<tr>
				<th class="has-text-centered">제목</th>
				<th class="has-text-centered">작성자</th>
				<th class="has-text-centered">작성일자</th>
				<th class="has-text-centered">추천</th>
				<th class="has-text-centered">조회수</th>
			</tr>
		</thead>
		<tbody>
			{#await boardList}
				<tr>
					<td colspan="5">Loading...</td>
				</tr>
			{:then freeBoard}
				{#each freeBoard['list'] as free}
					<tr>
						<td><a href="../article/{free.article_id}">{free.title}</a></td
						>
						<td>{free.username}</td>
						<td>{free.created}</td>
						<td>{free.like}</td>
						<td>{free.views}</td>
					</tr>
				{/each}
			{:catch error}
				<tr>
					<td colspan="5">{error.message}</td>
				</tr>
			{/await}
		</tbody>
		<tfoot>
			<tr>
				<td colspan="5" />
			</tr></tfoot
		>
	</table>
	{#await boardList}
		<div class="container is-fluid has-text-centered">
			<div class="buttons is-centered">
				<button class="button is-primary" disabled>이전</button>
				<button class="button is-primary" disabled>다음</button>
			</div>
		</div>
	{:then freeBoard}
		<nav class="pagination is-centered" aria-label="pagination">
			<ul class="pagination-list">
				{#each Array(Math.ceil(freeBoard['cnt'] / pageLimit)) as n, i}
					<li>
						<!-- svelte-ignore a11y-missing-attribute -->
						<a class="pagination-link" on:click={changePage(i)}>{i + 1}</a>
					</li>
				{/each}
			</ul>
		</nav>
	{/await}

	<div class="container">
		<div class="field is-horizontal">
			<div class="field-body">
				<div class="select">
					<select>
						<option>제목</option>
						<option>작성자</option>
						<option>내용</option>
					</select>
				</div>
				<div class="control is-expanded has-icons-left">
					<input
						class="input"
						type="text"
						placeholder="검색어를 입력하세요."
					/>
					<span class="icon is-small is-left">
						<i class="fas fa-search" />
					</span>
				</div>
				<p class="control">
					<button class="button is-info"> 검색 </button>
				</p>
			</div>
		</div>
	</div>
</div>
