<script>
	import { page } from '$app/stores';

	const load = async () => {
		const res = await fetch('http://localhost:8080');
		const data = await res.json();
		return data;
	};

	let boardFree = load();
	console.log(boardFree);
</script>

<table class="table container is-fluid">
	<thead>
		<tr>
			<th>제목</th>
			<th>작성자</th>
			<th>작성일자</th>
			<th>추천</th>
		</tr>
	</thead>
	<tfoot>
		<tr>
			<td colspan="4">
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
			</td>
		</tr>
	</tfoot>
	<tbody>
		{#await boardFree}
			<h2>Loading....</h2>
		{:then data}
			{#each data as { created, title, author, id, like }}
				<tr>
					<td><a sveltekit:prefetch href="/boardFree/{id}">{title}</a></td>
					<td>{author}</td>
					<td>{created}</td>
					<td>{like}</td>
				</tr>
			{/each}
		{/await}
	</tbody>
</table>
