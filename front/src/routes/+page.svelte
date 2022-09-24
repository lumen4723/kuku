<script>
    import Carousel from '$lib/carousel.svelte';
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
    <div class="table-container"
    style="
    margin: 0px auto;
    width: 80%;
    ">
        <table class="table
        is-bordered
        is-striped
        is-hoverable
        is-fullwidth"
        style="
        text-align: center;
        table-layout: fixed;
        "
        >
            <thead>
                <tr>
                    <th style="text-align: center;">새로운 내용</th>
                    <th style="text-align: center;">공지사항</th>
                    <th style="text-align: center;">새로운 질문과 답변</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>추가 어캐함</td>
                    <td>추가 어캐함</td>
                    <td>추가 어캐함</td>
                </tr>
                <tr>
                    <td>추가 어캐함</td>
                    <td>추가 어캐함</td>
                    <td>추가 어캐함</td>
                </tr>
                <tr>
                    <td>추가 어캐함</td>
                    <td>추가 어캐함</td>
                    <td>추가 어캐함</td>
                </tr>
            </tbody>
        </table>
    </div>
</section>

<style>
</style>