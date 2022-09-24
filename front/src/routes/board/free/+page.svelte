<script>
	import { page } from '$app/stores';
	import BoadList from '$lib/BoardList.svelte';

	const getBoardList = async ({ params }) => {
		const res = await fetch('http://localhost:8089/board_free/getAll', {
			mode: 'cors'
		});
		const freeBoard = await res.json();
		if (res.ok) {
			return freeBoard;
		} else {
			throw new Error(freeBoard);
		}
	};

	$: boardList = getBoardList($page.params);
</script>

<BoadList {boardList} />
