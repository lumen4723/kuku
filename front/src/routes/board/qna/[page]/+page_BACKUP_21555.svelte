<script>
	import { page } from '$app/stores';
<<<<<<< HEAD
	import BoadList from '$lib/BoardList.svelte';

	const getBoardList = async (pageIdx) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/qna/list?start_page=${pageIdx}`,
=======
	import BoadListQna from '$lib/boardListqna.svelte';

	const getBoardList = async (pageIdx, pageLimit) => {
		const res = await fetch(
			`http://api.eyo.kr:8081/board/qna/list/${pageIdx}?limit=${pageLimit}`,
>>>>>>> dev-backend
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

<<<<<<< HEAD
	let boardList = getBoardList($page.params.page || 1);
</script>

<BoadList {boardList} />
=======
	let boardList = getBoardList($page.params.page || 1, 10);
</script>

<BoadListQna {boardList} />
>>>>>>> dev-backend
