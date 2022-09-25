<script>
	import { page } from '$app/stores';
	import BoadList from '$lib/BoardList.svelte';

	const getBoardList = async (pageIdx) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/free/list?start_page=${pageIdx}`,
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

	let boardList = getBoardList($page.url.searchParams.get('page') || 1);
</script>

<BoadList {boardList} />
