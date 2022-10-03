<script>
    import Carousel from '$lib/carousel.svelte';
    import { page } from '$app/stores';

    const getBoardList = async (pageIdx, pageLimit) => {
		const res = await fetch(
			`http://127.0.0.1:8000/board/free/list/${pageIdx}?limit=${pageLimit}`,
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

<section class="hero is-primary is-halfheight">
    <div class="hero-body">
        <div class="container">
            <div class="columns">
                <div class="column"
                style="align-items: center;
                justify-content: center;
                display: flex;
                padding-bottom: 5%;">
                    <div>
                        <h1 class="title" style="word-break: keep-all;">
                            차 한잔과 함께하는 코딩 사이트
                        </h1>
                        <div style="padding-left: 48px;">
                            <h2 class="subtitle"
                            style="line-height:1.4;">
                                비전공자도 참여할 수 있는
                                <br>
                                쉬운 난이도를 통하여
                                <br>
                                여러분의 코딩실력을 향상시켜보세요!
                            </h2>
                            <a class="button
                            is-info is-dark
                            is-medium is-halfwidth"
                            sveltekit:prefetch href="/account"
                            >
                                시작하기
                            </a>
                        </div>
                    </div>
                </div>
                <div class="column">
                    <div style="padding-left: 30px; padding-top: 10px">
                        <img src="https://via.placeholder.com/560x500" alt="">
                        <br>사진은 생각해놓음
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<section class="hero-body">
    <div class="box"
    style="margin: 60px auto;
    border-radius: 20px;
    width: 80%;
    background-color: #fafafa;"
    >
        <div class="container block">
            <div class="columns"
            style="margin-bottom: 20px;"
            >
                <div class="column"
                style="margin-top: 20px;"
                >
                    <h1 class="title" 
                    style="word-break: keep-all; 
                    padding-left: 12%;"
                    >
                        기초 트랙들을 통해 코딩을 배워보세요!
                    </h1>
                </div>
            </div>
            <Carousel />
        </div>
        <div class="container block">
            <div class="columns"
            style="margin-bottom: 20px;"
            >
                <div class="column"
                style="margin-top: 20px;"
                >
                    <h1 class="title" 
                    style="word-break: keep-all; 
                    padding-left: 12%;"
                    >
                        알고리즘 트랙들을 통해 실력을 향상시켜보세요!
                    </h1>
                </div>
            </div>
            <Carousel />
        </div>
    </div>
</section>

<section class="hero-body">
    <div style="margin: 0px auto;
    width: 80%;
    ">
        <div class="columns">
            <div class="column"
            style="padding: 12px 0px;
            ">
                <div class="table-container">
                    <table class="table
                    is-bordered
                    is-hoverable"
                    style="
                    text-align: center;
                    table-layout: fixed;
                    width: -webkit-fill-available;
                    "
                    >
                        <thead>
                            <tr>
                                <th colspan="3">새로운 내용</th>
                            </tr>
                        </thead>
                        <tbody>
                            <td colspan="2">여기 제목 들어감</td>
                            <td colspan="1">여기 이름 들어감</td>
                            {#await boardList}
                                <tr>
                                    <td colspan="3">Loading...</td>
                                </tr>
                            {:then freeBoard}
                                {#each freeBoard['list'] as free}
                                    <tr>
                                        <td colspan="2"><a href="../article/{free.article_id}">{free.title}</a></td>
                                        <td colspan="1">{free.username}</td>
                                    </tr>
                                {/each}
                            {:catch error}
                                <tr>
                                    <td colspan="5">{error.message}</td>
                                </tr>
                            {/await}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="column"
            style="padding: 12px 0px;
            ">
                <div class="table-container">
                    <table class="table
                    is-bordered
                    is-hoverable"
                    style="
                    text-align: center;
                    table-layout: fixed;
                    width: -webkit-fill-available;
                    ">
                        <thead>
                            <tr>
                                <th colspan="3">공지사항</th>
                            </tr>
                        </thead>
                        <tbody>
                            <td colspan="2">여기 제목 들어감</td>
                            <td colspan="1">여기 시간 들어감</td>
                            <!-- boardfree 의 state가 다른 애들 == 공지인 애들만 호출로 변경해야함 -->
                            {#await boardList}
                                <tr>
                                    <td colspan="3">Loading...</td>
                                </tr>
                            {:then freeBoard}
                                {#each freeBoard['list'] as free}
                                    <tr>
                                        <td colspan="2"><a href="../article/{free.article_id}">{free.title}</a></td>
                                        <td colspan="1">
                                            {#each [2,3,4,5,6,7,8,9] as i}
                                                {free.created[i]}
                                            {/each}
                                        </td>
                                    </tr>
                                {/each}
                            {:catch error}
                                <tr>
                                    <td colspan="5">{error.message}</td>
                                </tr>
                            {/await}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="column"
            style="padding: 12px 0px;
            ">
                <div class="table-container">
                    <table class="table
                    is-bordered
                    is-hoverable"
                    style="
                    text-align: center;
                    table-layout: fixed;
                    width: -webkit-fill-available;
                    ">
                        <thead>
                            <tr>
                                <th colspan="3">새로운 질문과 답변</th>
                            </tr>
                        </thead>
                        <tbody>
                            <td colspan="2">여기 제목 들어감</td>
                            <td colspan="1">여기 분류 들어감</td>
                            <!-- qnaboard 제목이랑 분류로 변경해야함 -->
                            {#await boardList}
                                <tr>
                                    <td colspan="3">Loading...</td>
                                </tr>
                            {:then freeBoard}
                                {#each freeBoard['list'] as free}
                                    <tr>
                                        <td colspan="2"><a href="../article/{free.article_id}">{free.title}</a></td>
                                        <td colspan="1">{free.state}</td>
                                    </tr>
                                {/each}
                            {:catch error}
                                <tr>
                                    <td colspan="5">{error.message}</td>
                                </tr>
                            {/await}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</section>

<style>
    thead tr {
        background-color: #00d1b2;
    }
    thead th {
        text-align: center;
        color: #ffffff;
    }
</style>