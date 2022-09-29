<script>
	import { onMount } from 'svelte';
	export let boardList;
	let rows = [];
	let page = 0;
	let totalPages = [];
	let currentPageRows = [];
	let itemsPerPage = 10;
</script>

<div class="container">
	<table class="table container is-fluid has-text-centered">
		<thead>
			<tr>
				<th class="has-text-centered">제목</th>
				<th class="has-text-centered">작성자</th>
				<th class="has-text-centered">작성일자</th>
				<th class="has-text-centered">추천</th>
				<th class="has-text-centered">조회수</th>
			</tr>
		</thead>
		<tfoot>
			<tr>
				<td colspan="5">
					{#await boardList}
						<tr>
							<td colspan="5">Loading...</td>
						</tr>
					{:then boardList}
						<!-- svelte-ignore a11y-no-redundant-roles -->
						<nav
							class="pagination is-centered"
							role="navigation"
							aria-label="pagination"
						>
							<ul class="pagination-list" />
						</nav>
					{/await}
				</td>
			</tr>
		</tfoot>
		<tbody>
			{#await boardList}
				<tr>
					<td colspan="5">Loading...</td>
				</tr>
			{:then qnaBoard}
				{#each qnaBoard['list'] as qna}
					<tr>
						<td><a href="../article/{qna.article_id}">{qna.title}</a></td>
						<td>{qna.username}</td>
						<td>{qna.created}</td>
						<td>{qna.like}</td>
						<td>{qna.views}</td>
					</tr>
				{/each}
			{:catch error}
				<tr>
					<td colspan="5">{error.message}</td>
				</tr>
			{/await}
		</tbody>
	</table>
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
