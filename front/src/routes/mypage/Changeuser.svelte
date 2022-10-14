<script>
	let username, useremail, password;

	const user_change = async () => {
		await fetch("//api.eyo.kr:8081/user/change", {
			method: "POST",
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
	<form method="post">
		<div class="field">
			<label class="label">Username</label>
			<div class="control has-icons-left has-icons-right">
				<input
					class="input"
					type="text"
					placeholder="Username"
					bind:value={username}
				/>
				<span class="icon is-small is-left">
					<i class="fas fa-user" />
				</span>
			</div>
		</div>

		<div class="field">
			<label class="label">Email</label>
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
			<label class="label">Password</label>
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
			<label class="label">Confirm Password</label>
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
				<button class="button is-link" type="submit">Submit</button>
			</div>
		</div>
	</form>
</div>
