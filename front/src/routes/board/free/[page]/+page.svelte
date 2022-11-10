<script>
	import { userIsLogged } from "$lib/user.js";

	let currentPage = 1;
	let isLogged = userIsLogged();
	const pageLimits = [
		{ value: 10, label: "10개씩 보기" },
		{ value: 15, label: "15개씩 보기" },
		{ value: 20, label: "20개씩 보기" },
	];
	let currentLimit = pageLimits[0].value;

	const getBoardList = async (pageIdx, pageLimit) => {
		const res = await fetch(
			`//api.eyo.kr:8081/board/free/list/${pageIdx}?limit=${pageLimit}`,
			{
				mode: "cors",
				credentials: "include",
			}
		);
		const freeBoard = await res.json();
		if (res.ok) {
			return freeBoard;
		} else {
			throw new Error(freeBoard);
		}
	};

	$: boardList = getBoardList(currentPage, currentLimit);
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
			{#await boardList then freeBoard}
				{#each freeBoard["list"] as free}
					<tr>
						<td
							><a href="/board/free/article/{free.article_id}"
								>{free.title}</a
							></td
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
	{#await boardList then freeBoard}
		<nav class="pagination is-centered" aria-label="pagination">
			<ul class="pagination-list">
				{#each Array(Math.ceil(Math.abs(freeBoard["cnt"]) / currentLimit)) as n, i}
					<li>
						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							class="pagination-link"
							class:is-current={i + 1 === currentPage}
							sveltekit:prefetch
							on:click={() => (currentPage = i + 1)}>{i + 1}</a
						>
					</li>
				{/each}
			</ul>
		</nav>
	{:catch error}
		{error.message}
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
				<p class="control ml-2">
					<button class="button is-info"> 검색 </button>
				</p>
			</div>
			{#if isLogged}
				<a href="/board/free/write" class="button is-primary">글쓰기</a>
			{/if}
			<div class="select">
				<select bind:value={currentLimit}>
					{#each pageLimits as pl}
						<option value={pl.value}>
							{pl.label}
						</option>
					{/each}
				</select>
			</div>
		</div>
	</div>
	<br />
</div>
