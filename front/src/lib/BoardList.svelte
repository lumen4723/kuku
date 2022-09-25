<script>
	export let boardList;
	// 	{
	//     "article_id": 1,
	//     "userid": 1,
	//     "state": 1,
	//     "views": 0,
	//     "title": "test",
	//     "content": "test",
	//     "created": "2022-09-19T19:29:49",
	//     "like": 0
	//   }
</script>

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
				<!-- svelte-ignore a11y-missing-attribute -->
				<nav class="pagination is-centered" aria-label="pagination">
					<a class="pagination-previous">Previous</a>
					<a class="pagination-next">Next page</a>
					<ul class="pagination-list">
						<li>
							<a class="pagination-link">1</a>
						</li>
						<li><span class="pagination-ellipsis">&hellip;</span></li>
						<li>
							<a class="pagination-link">45</a>
						</li>
						<li>
							<a
								class="pagination-link is-current"
								aria-label="Page 46"
								aria-current="page">46</a
							>
						</li>
						<li>
							<a class="pagination-link" aria-label="Goto page 47">47</a>
						</li>
						<li><span class="pagination-ellipsis">&hellip;</span></li>
						<li>
							<a class="pagination-link" aria-label="Goto page 86">86</a>
						</li>
					</ul>
				</nav>
			</td>
		</tr>
	</tfoot>
	<tbody>
		{#await boardList}
			<tr>
				<td colspan="5">Loading...</td>
			</tr>
		{:then freeBoard}
			{#each freeBoard['list'] as free}
				<tr>
					<td><a href="./{free.article_id}">{free.title}</a></td>
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
