<script>
	import { page } from '$app/stores';
	import BoadListQna from '$lib/boardListqna.svelte';

	const getBoardList = async (pageIdx, pageLimit) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/qna/list/${pageIdx}?limit=${pageLimit}`,
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

	let boardList = getBoardList($page.params.page || 1, 10);
</script>

<BoadListQna {boardList} />
