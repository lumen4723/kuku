<script>
	import { page } from '$app/stores';
	import BoadList from '$lib/BoardList.svelte';

	const getBoardList = async ({ params }) => {
		const res = await fetch('http://localhost:8089/board_qna/getAll', {
			mode: 'cors'
		});
		const qnaBoard = await res.json();
		if (res.ok) {
			return qnaBoard;
		} else {
			throw new Error(qnaBoard);
		}
	};

	$: boardList = getBoardList($page.params);
</script>

<BoadList {boardList} />
