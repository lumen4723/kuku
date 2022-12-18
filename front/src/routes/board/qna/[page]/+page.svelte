<script>
	import { userIsLogged } from "$lib/user.js";

	const pageLimits = [
		{ value: 10, label: "10개씩 보기" },
		{ value: 15, label: "15개씩 보기" },
		{ value: 20, label: "20개씩 보기" },
	];
	const searchTypes = [
		{ value: "title", label: "제목" },
		{ value: "content", label: "내용" },
		{ value: "username", label: "작성자" },
	];

	let searchT = "";
	let isLogged = userIsLogged();
	let currentPage = 1;
	let currentLimit = pageLimits[0].value;
	let currentST = searchTypes[0].value;
	let boardList;

	const getBoardList = async (pageIdx, pageLimit) => {
		const res = await fetch(
			`//api.eyo.kr/board/qna/list/${pageIdx}?limit=${pageLimit}`,
			{
				mode: "cors",
				credentials: "include",
			}
		);
		const qnaBoard = await res.json();
		if (res.ok) {
			qnaBoard.cntDiv10 = Math.round(Math.abs(qnaBoard["cnt"]) / 10);
			qnaBoard.cntDiv15 = Math.round(Math.abs(qnaBoard["cnt"]) / 15);
			qnaBoard.cntDiv20 = Math.round(Math.abs(qnaBoard["cnt"]) / 20);
			return qnaBoard;
		} else {
			throw new Error(qnaBoard);
		}
	};
	const searchTitle = async (title, pageIdx, pageLimit) => {
		const res = await fetch(
			`//api.eyo.kr/board/qna/search/title/${title}?page=${pageIdx}&limit=${pageLimit}`,
			{
				mode: "cors",
				credentials: "include",
			}
		);
		const qnaBoard = await res.json();
		if (res.ok) {
			qnaBoard.cntDiv10 = Math.round(Math.abs(qnaBoard["cnt"]) / 10);
			qnaBoard.cntDiv15 = Math.round(Math.abs(qnaBoard["cnt"]) / 15);
			qnaBoard.cntDiv20 = Math.round(Math.abs(qnaBoard["cnt"]) / 20);
			return qnaBoard;
		} else {
			throw new Error(qnaBoard);
		}
	};
	const searchUser = async (user, pageIdx, pageLimit) => {
		const res = await fetch(
			`//api.eyo.kr/board/qna/search/username/${user}?page=${pageIdx}&limit=${pageLimit}`,
			{
				mode: "cors",
				credentials: "include",
			}
		);
		const qnaBoard = await res.json();
		if (res.ok) {
			qnaBoard.cntDiv10 = Math.round(Math.abs(qnaBoard["cnt"]) / 10);
			qnaBoard.cntDiv15 = Math.round(Math.abs(qnaBoard["cnt"]) / 15);
			qnaBoard.cntDiv20 = Math.round(Math.abs(qnaBoard["cnt"]) / 20);
			return qnaBoard;
		} else {
			throw new Error(qnaBoard);
		}
	};
	const searchContent = async (content, pageIdx, pageLimit) => {
		const res = await fetch(
			`//api.eyo.kr/board/qna/search/content/${content}?page=${pageIdx}&limit=${pageLimit}`,
			{
				mode: "cors",
				credentials: "include",
			}
		);
		const qnaBoard = await res.json();
		if (res.ok) {
			qnaBoard.cntDiv10 = Math.round(Math.abs(qnaBoard["cnt"]) / 10);
			qnaBoard.cntDiv15 = Math.round(Math.abs(qnaBoard["cnt"]) / 15);
			qnaBoard.cntDiv20 = Math.round(Math.abs(qnaBoard["cnt"]) / 20);
			return qnaBoard;
		} else {
			throw new Error(qnaBoard);
		}
	};
	const searchRun = () => {
		if (currentST === "title") {
			boardList = searchTitle(searchT, currentPage, currentLimit);
		} else if (currentST === "content") {
			boardList = searchContent(searchT, currentPage, currentLimit);
		} else if (currentST === "username") {
			boardList = searchUser(searchT, currentPage, currentLimit);
		}
	};
	const changeList = () => {
		searchT == ""
			? (boardList = getBoardList(currentPage, currentLimit))
			: searchRun();
	};

	changeList();
</script>

<div class="container">
	{#await boardList then qnaBoard}
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
				{#each qnaBoard["list"] as qna}
					<tr>
						<td>
							<a href="/board/qna/article/{qna.article_id}">
								{qna.title}
							</a>
						</td>
						<td>{qna.username}</td>
						<td>{qna.created}</td>
						<td>{qna.like}</td>
						<td>{qna.views}</td>
					</tr>
				{/each}
			</tbody>
			<tfoot>
				<tr>
					<td colspan="5" />
				</tr>
			</tfoot>
		</table>
		<nav class="pagination is-centered" aria-label="pagination">
			<ul class="pagination-list">
				{#if currentPage > 3}
					<li>
						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							class="pagination-link"
							on:click={() => {
								currentPage = 1;
								changeList();
							}}
						>
							1
						</a>
					</li>
					<li>
						<span class="pagination-ellipsis">&hellip;</span>
					</li>
				{/if}
				{#if currentPage <= 3}
					{#each [1, 2, 3, 4, 5] as n}
						<li>
							<!-- svelte-ignore a11y-missing-attribute -->
							<a
								class="pagination-link"
								class:is-current={n === currentPage}
								on:click={() => {
									currentPage = n;
									changeList();
								}}
							>
								{n}
							</a>
						</li>
					{/each}
				{:else}
					{#each ((s, e) => [...Array(e - s + 1)].map((_, i) => s + i))(currentPage >= qnaBoard["cntDiv" + currentLimit] - 2 ? qnaBoard["cntDiv" + currentLimit] - 4 : currentPage - 2, currentPage >= qnaBoard["cntDiv" + currentLimit] - 2 ? qnaBoard["cntDiv" + currentLimit] : currentPage + 2) as n}
						<li>
							<!-- svelte-ignore a11y-missing-attribute -->
							<a
								class="pagination-link"
								class:is-current={n === currentPage}
								on:click={() => {
									currentPage = n;
									changeList();
								}}
							>
								{n}
							</a>
						</li>
					{/each}
				{/if}
				{#if currentPage + 2 < qnaBoard["cntDiv" + currentLimit]}
					<li>
						<span class="pagination-ellipsis">&hellip;</span>
					</li>
					<li>
						<!-- svelte-ignore a11y-missing-attribute -->
						<a
							class="pagination-link"
							on:click={() => {
								currentPage = qnaBoard["cntDiv" + currentLimit];
								changeList();
							}}
						>
							{qnaBoard["cntDiv" + currentLimit]}
						</a>
					</li>
				{/if}
			</ul>
		</nav>
	{:catch error}
		{error.message}
	{/await}
	<div class="container">
		<form method="get" on:submit|preventDefault={changeList}>
			<div class="field is-horizontal">
				<div class="field-body">
					<div class="select">
						<select bind:value={currentST}>
							{#each searchTypes as st}
								<option value={st.value}>
									{st.label}
								</option>
							{/each}
						</select>
					</div>
					<div class="control is-expanded has-icons-left">
						<input
							class="input"
							type="text"
							placeholder="검색어를 입력하세요."
							bind:value={searchT}
						/>
						<span class="icon is-small is-left">
							<i class="fas fa-search" />
						</span>
					</div>
					<button class="button is-info" type="submit"> 검색 </button>
				</div>
				{#if isLogged}
					<a
						sveltekit:reload
						href="/board/qna/write/question"
						class="button is-primary"
					>
						글쓰기
					</a>
				{/if}
				<div class="select">
					<select
						bind:value={currentLimit}
						on:change={() => {
							currentPage = 1;
							changeList();
						}}
					>
						{#each pageLimits as pl}
							<option value={pl.value}>
								{pl.label}
							</option>
						{/each}
					</select>
				</div>
			</div>
		</form>
	</div>
	<br />
</div>
