<script>
	import Swal from "sweetalert2";
	import { browser } from "$app/env";
	import { is_empty } from "svelte/internal";

	let username = "",
		email = "",
		password = "",
		passwordConf = "",
		passwordOrg = "";
	let valid_email =
		/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	let show_password = false;
	let show_passwordConf = false;
	function passwordShow_button() {
		show_password = !show_password;
	}
	function passwordConfShow_button() {
		show_passwordConf = !show_passwordConf;
	}
	let passwordThis;
	let passwordConfThis;
	let usernameFailed = true;
	let usernameExcepts = ["ㅅㅂ", "kuku"];

	/**checking user name is available
	이후 제한 사항들을 추가해야 합니다.
	*/
	const filterUsername = () => {
		if (is_empty(username)) {
			return false;
		} else if (
			usernameExcepts.filter((e) => {
				return username.includes(e);
			}).length > 0
		) {
			return false;
		} else {
			return true;
		}
	};

	const check_username = async () =>
		await fetch(`//api.eyo.kr:8081/user/check?username=${username}`, {
			method: "GET",
			headers: {
				Aceept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		})
			.then((res) => {
				if (res.ok) return res.json();
			})
			.then((data) => {
				if (data === true) {
					usernameFailed = false;
					isLoading = false;
				} else {
					usernameFailed = true;
					isLoading = false;
				}
			})
			.catch((err) => {
				console.log(err);
			});

	const checkUsername = () => {
		isLoading = true;
		if (filterUsername()) {
			check_username();
		} else {
			usernameFailed = true;
			isLoading = false;
		}
	};

	let isLoading = false;
	let message = "";

	const updateUser = async () => {
		isLoading = true;
		await fetch("//api.eyo.kr:8081/user/update", {
			method: "PUT",
			headers: {
				Aceept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				changeUser: {
					username,
					password,
					email,
				},
				originUser: {
					password: passwordOrg,
				},
			}),
			mode: "cors",
			credentials: "include",
		})
			.then((res) => {
				if (res.ok == false) return Promise.reject(res);
				return res.json();
			})
			.then((res) => {
				Swal.fire({
					title: "회원정보 변경에 성공하였습니다. 다시 로그인해주세요.",
					icon: "success",
					confirmButtonText: "확인",
				}).then((result) => {
					if (result)
						if (browser) {
							window.localStorage.removeItem("user.email");
							window.localStorage.removeItem("user.id");
							window.localStorage.removeItem("user.username");
							window.location.href = "/account";
						}
				});
			})
			.catch((e) => {
				Swal.fire({
					title: "회원정보 변경에 실패하였습니다." + e,
					icon: "error",
					confirmButtonText: "확인",
				});
			});
	};

	const emailcheck = async () => {
		await fetch("//api.eyo.kr:8081/user/sendEmailBySesson", {
			method: "POST",
			headers: {
				Aceept: "application/json",
			},
			mode: "cors",
			credentials: "include",
		})
			.then((res) => {
				if (res.ok == false) return Promise.reject(res);
				return res.json();
			})
			.then(() => {
				// 메세지
				message = "인증메일을 전송하였습니다.";
				isLoading = false;
			})
			.catch((e) => {
				e.json().then((json) => {
					message =
						"인증메일 전송에 실패하였습니다: " + json["detail"];
					isLoading = false;
				});
			});
	};
</script>

<article class="message is-warning">
	<div class="message-body">
		<p>이메일이 아직 검증되지 않았습니다.</p>
		<p>이메일을 검증해 주세요.</p>
	</div>
</article>
<div class="columns">
	<div class="column is-5 is-offset-2">
		<button class="button is-warning" on:click={emailcheck}>
			이메일 검증하기
		</button>
	</div>
</div>
<form method="PUT" on:submit|preventDefault={updateUser}>
	{#if message != ""}
		{#if message.includes("인증메일을 전송하였습니다.")}
			<article class="message is-success">
				<div class="message-body">
					<p>{message}</p>
				</div>
			</article>
		{:else}
			<article class="message is-danger">
				<div class="message-body">
					<p>{message}</p>
				</div>
			</article>
		{/if}
	{/if}
	<div class="field">
		<label class="label" for="password">Password</label>
		<div class="control">
			<input
				class="input"
				type="password"
				placeholder="Your password"
				bind:value={passwordOrg}
				required
			/>
		</div>
	</div>
	<div class="field">
		<label class="label" for="username">New Username</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={usernameFailed && !is_empty(username)}
				class:is-success={!usernameFailed}
				name="username"
				type="text"
				placeholder="Set your new username"
				bind:value={username}
				on:input={checkUsername}
			/>
			<span class="icon is-small is-left ">
				<i
					class="fa-regular fa-user"
					class:has-text-danger={usernameFailed &&
						!is_empty(username)}
					class:has-text-success={!usernameFailed}
				/>
			</span>
			{#if isLoading}
				<span class="icon fa-sm is-right ">
					<i
						class="fa-solid fa-circle-notch fa-spin"
						class:has-text-danger={usernameFailed &&
							!is_empty(username)}
						class:has-text-success={!usernameFailed}
					/>
				</span>
			{:else}
				<span class="icon is-small is-right">
					<i
						class="fas fa-check"
						class:has-text-danger={usernameFailed &&
							!is_empty(username)}
						class:has-text-success={!usernameFailed}
					/>
				</span>

				{#if usernameFailed && !is_empty(username)}<p
						class="help has-text-danger"
					>
						{username} is not available
					</p>{/if}
			{/if}
		</div>
		<p class="help">Write your name to be shown to others</p>
	</div>
	<div class="field">
		<label class="label" for="email">New Email</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={!email.match(valid_email) && !is_empty(email)}
				class:is-success={email.match(valid_email)}
				name="email"
				type="text"
				placeholder="Set your new email"
				bind:value={email}
			/>
			<span class="icon is-small is-left">
				<i
					class="fa-regular fa-envelope"
					class:has-text-danger={!email.match(valid_email) &&
						!is_empty(email)}
					class:has-text-success={email.match(valid_email)}
				/>
			</span>
			<span class="icon is-small is-right">
				<i
					class="fas fa-check"
					class:has-text-danger={!email.match(valid_email) &&
						!is_empty(email)}
					class:has-text-success={email.match(valid_email)}
				/>
			</span>
		</div>
		<p class="help">Write your email</p>
	</div>

	<div class="field">
		<label class="label" for="password">New Password</label>
		<div class="control has-icons-left has-icons-right">
			<div class="control">
				<input
					class="input"
					class:is-danger={(!is_empty(password) &&
						password.length < 8) ||
						password.length > 128}
					class:is-success={password.length > 7 &&
						password.length < 129}
					name="password"
					type={show_password ? "text" : "password"}
					placeholder="Set your new password"
					bind:this={passwordThis}
					on:input={() => (password = passwordThis.value)}
				/>
				<span class="icon is-small is-left">
					<i
						class="fas fa-key"
						class:has-text-danger={(!is_empty(password) &&
							password.length < 8) ||
							password.length > 128}
						class:has-text-success={password.length > 7 &&
							password.length < 129}
					/>
				</span>
				<span class="icon is-small is-right">
					<i
						class={show_password
							? "fas fa-eye password_icon"
							: "fas fa-eye-slash password_icon"}
						on:click={passwordShow_button}
						class:has-text-danger={(!is_empty(password) &&
							password.length < 8) ||
							password.length > 128}
						class:has-text-success={password.length > 7 &&
							password.length < 129}
					/>
				</span>
			</div>
		</div>
		<p class="help">Should contain at least 8 ~ 128 characters</p>
	</div>

	<div class="field">
		<label class="label" for="passwordConf">Confirm New Password</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={!is_empty(passwordConf) &&
					password !== passwordConf}
				class:is-success={password === passwordConf &&
					password.length > 7 &&
					password.length < 129}
				name="passwordConf"
				type={show_passwordConf ? "text" : "password"}
				placeholder="Confirm your new password"
				bind:this={passwordConfThis}
				on:input={() => (passwordConf = passwordConfThis.value)}
			/>
			<span class="icon is-small is-left">
				<i
					class="fas fa-key"
					class:has-text-danger={!is_empty(passwordConf) &&
						password !== passwordConf}
					class:has-text-success={password === passwordConf &&
						password.length > 7 &&
						password.length < 129}
				/>
			</span>
			<span class="icon is-small is-right">
				<i
					class={show_passwordConf
						? "fas fa-eye passwordConf_icon"
						: "fas fa-eye-slash passwordConf_icon"}
					on:click={passwordConfShow_button}
					class:has-text-danger={!is_empty(passwordConf) &&
						password !== passwordConf}
					class:has-text-success={password === passwordConf &&
						password.length > 7 &&
						password.length < 129}
				/>
			</span>
		</div>
	</div>

	<div class="field is-grouped">
		<div class="control">
			<button
				class="button is-link"
				class:is-loading={isLoading}
				disabled={isLoading}
				type="submit">Update</button
			>
		</div>
	</div>
</form>

<style>
	.password_icon {
		pointer-events: all;
		cursor: pointer;
	}
	.passwordConf_icon {
		pointer-events: all;
		cursor: pointer;
	}
</style>
