<script>
	import { page } from '$app/stores';
	import BoadList from '$lib/BoardList.svelte';

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

	let boardList = getBoardList($page.params.page || 1, 10);
</script>

<BoadList {boardList} />
