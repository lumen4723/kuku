<script>
    let username ="asd";
    let useremail = "dsa";

    const getuserdata = async () => {
        const res = await fetch('//127.0.0.1:8081/user/whoami', {
            method: 'GET',
            headers: {
                Accept: "application/json",
            },
            mode: "cors",
			credentials: "include",
        })
        .then((res) => {
            if (res.ok == false) throw new Error();
            return res.json();
        })
        .then((json) => {
            console.log(json);
            username = json["username"];
            useremail = json["email"];
        });
    };

    //유저의 이름 변경 요청
    //유저의 이메일 변경 요청
    //유저의 비밀번호 변경 요청
    //모든 변경 요청은 비밀번호 입력 후 가능하도록 한다.

</script>

<body>
    <!-- 자신의 이름 이메일을 보여주고 오른쪽 버튼을 누르면 변경 입력창이 뜨는 구조 -->
    <div>
        <h1>이름</h1>
        <h2>{username}</h2>
        <button>변경</button>
    </div>
    <div>
        <h1>이메일</h1>
        <h2>{useremail}</h2>
        <button>변경</button>
    </div>
    <div>
        <h1>비밀번호</h1>
        <h2>********</h2>
        <button>변경</button>
    </div>



    <div class="column is-4"
    style="margin: auto;">
        <div class="box">
            <div class="column is-10">
                <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                        <input class="input" type="text" placeholder="Text input">
                    </div>
                </div>
            </div>
            <div class="column is-10">
                <div class="field">
                    <label class="label">Email</label>
                    <div class="control">
                        <input class="input" type="email" placeholder="Email input">
                    </div>
                </div>
            </div>
            <div class="column is-10">
                <div class="field">
                    <label class="label">Password</label>
                    <div class="control">
                        <input class="input" type="password" placeholder="Password input">
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>