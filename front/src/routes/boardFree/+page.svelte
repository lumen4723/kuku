<script>
	import { page } from '$app/stores';
	import { listen } from 'svelte/internal';
	let data = [
		{
			created: '2021-01-01',
			title: '제목',
			author: '작성자',
			like: 123,
			id: 1
		},
		{
			created: '2021-01-02',
			title: '제목2',
			author: '작성자2',
			like: 123,
			id: 2
		},
		{
			created: '2021-01-03',
			title: '제목3',
			author: '작성자3',
			like: 123,
			id: 3
		}
	];
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
				<button class="button is-primary">글쓰기</button>
			</td>
		</tr>
	</tfoot>
	<tbody>
		{#each data as { created, title, author, id, like }}
			<tr>
				<td><a sveltekit:prefetch href="/boardFree/{id}">{title}</a></td>
				<td>{author}</td>
				<td>{created}</td>
				<td>{like}</td>
			</tr>
		{/each}
	</tbody>
</table>
