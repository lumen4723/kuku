<script>
	import { page } from '$app/stores';
	import BoadList from '$lib/BoardList.svelte';

	const getBoardList = async (pageIdx) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/qna/list?start_page=${pageIdx}`,
			{
				mode: 'cors'
			}
		);
		const qnaBoard = await res.json();
		//const freeBoard = await res.json();
		if (res.ok) {
			return qnaBoard;
			//return freeBoard;
		} else {
			throw new Error(qnaBoard);
			//throw new Error(freeBoard);
		}
	};

	let boardList = getBoardList($page.params.page || 1);
</script>

<BoadList {boardList} />
