<script>
	const user_delete = async () => {
		await fetch("//api.eyo.kr:8081/user/delete", {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				email,
				password,
			}),
			mode: "cors",
			credentials: "include",
		})
			.then((res) => {
				if (res.ok == false) return Promise.reject(res);
				return res.json();
			})
			.then((res) => {
				if (res["status"] == "success") {
					location.href = "/";
				} else {
					alert("회원탈퇴에 실패하였습니다.");
				}
			})
			.catch((e) => {
				alert("회원탈퇴에 실패하였습니다.");
			});
	};
</script>

<div class="withdraw">
	<form method="post" on:submit|preventDefault={user_delete}>
		<div class="field">
			<label class="label" for="repeat"
				>KUKU 탈퇴를 원하시면 "탈퇴하겠습니다." 를 입력해주세요.</label
			>
			<div class="control">
				<input
					class="input"
					type="repeat"
					placeholder="탈퇴하겠습니다."
				/>
			</div>
			<button class="button is-danger" type="submit">회원탈퇴</button>
		</div>
	</form>
</div>

<style>
	.withdraw {
		margin-bottom: 264px;
	}
</style>
