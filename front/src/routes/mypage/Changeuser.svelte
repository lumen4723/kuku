<script>
	let username, useremail, password;

	const user_update = async () => {
		await fetch("//api.eyo.kr:8081/user/update", {
			method: "PUT",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username,
				useremail,
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
					// 병규가 얘쁘게 만들어줘야함
				} else {
					alert("회원정보 변경에 실패하였습니다.");
				}
			})
			.catch((e) => {
				alert("회원정보 변경에 실패하였습니다.");
			});
	};
</script>

<div class="container">
	<form method="PUT" on:submit|preventDefault={user_update}>
		<div class="field">
			<label class="label" for="username">Username</label>
			<div class="control has-icons-left has-icons-right">
				<input
					class="input"
					type="username"
					placeholder="Username"
					bind:value={username}
				/>
				<span class="icon is-small is-left">
					<i class="fas fa-user" />
				</span>
			</div>
		</div>

		<div class="field">
			<label class="label" for="email">Email</label>
			<div class="control has-icons-left has-icons-right">
				<input
					class="input"
					type="email"
					placeholder="Email"
					bind:value={useremail}
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
			<label class="label" for="confirmpassword">Confirm Password</label>
			<div class="control has-icons-left has-icons-right">
				<input
					class="input"
					type="confirmpassword"
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
				<button class="button is-link" type="submit">수정하기</button>
			</div>
		</div>
	</form>
</div>
