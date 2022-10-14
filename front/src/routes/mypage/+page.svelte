<script>
    let username ="";
    let useremail = "";

    const getuserdata = async () => {
        const res = await fetch('//api.eyo.kr:8081/user/whoami', {
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

    getuserdata();


</script>

<body>
</body>