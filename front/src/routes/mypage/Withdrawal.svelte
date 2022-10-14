<script>
	let email, password;

	const user_delete = async () => {
		await fetch("//api.eyo.kr:8081/user/delete", {
			method: "DELETE",
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
				if (res == 0) {
					location.href = "/";
				} else {
					alert("회원탈퇴에 실패하였습니다.");
				}
			})
			.catch((e) => {
				console.log(e);
				alert("회원탈퇴에 실패하였습니다.");
			});
	};
</script>

<div class="withdraw">
	<form method="DELETE" on:submit|preventDefault={user_delete}>
		<div class="field">
			<label class="label" for="email">Email</label>
			<div class="control has-icons-left has-icons-right">
				<input
					class="input"
					type="email"
					placeholder="Email"
					bind:value={email}
				/>
				<span class="icon is-small is-left">
					<i class="fas fa-envelope" />
				</span>
			</div>
		</div>

		<div class="field">
			<label class="label" for="password">Password</label>
			<div class="control has-icons-left has-icons-right">
				<input
					class="input"
					type="password"
					placeholder="Password"
					bind:value={password}
				/>
				<span class="icon is-small is-left">
					<i class="fas fa-lock" />
				</span>
			</div>
		</div>

		<div class="field">
			<div class="control">
				<button class="button is-danger" type="submit">회원탈퇴</button>
			</div>
		</div>
	</form>
</div>

<style>
	.withdraw {
		margin-bottom: 264px;
	}
</style>
