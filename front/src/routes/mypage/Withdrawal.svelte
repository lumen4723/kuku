<script>
	import { browser } from "$app/env";
	import Swal from "sweetalert2";

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
					Swal.fire({
						title: "회원탈퇴에 성공하였습니다.",
						icon: "success",
						confirmButtonText: "확인",
					}).then((result) => {
						if (result)
							if (browser) {
								window.sessionStorage.removeItem("user.email");
								window.sessionStorage.removeItem("user.id");
								window.sessionStorage.removeItem(
									"user.username"
								);
								window.location.href = "/";
							}
					});
				} else {
					Swal.fire({
						title: "회원탈퇴에 실패하였습니다.",
						icon: "error",
						confirmButtonText: "확인",
					});
				}
			})
			.catch((e) => {
				console.log(e);
				Swal.fire({
					title: "회원탈퇴에 실패하였습니다.",
					icon: "error",
					confirmButtonText: "확인",
				});
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
