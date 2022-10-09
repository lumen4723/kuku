<script>
	import { browser } from "$app/env";
	import { writable } from "svelte/store";

	let isLoading = false;
	let email, password;
	let message = "";

	if (browser) {
		let msg = new URLSearchParams(location.search).get("msg");
		if (msg != null) {
			message = url;
		}
	}

	const login = async () => {
		isLoading = true;
		const res = await fetch("http://api.eyo.kr:8081/user/login", {
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
		})
			.then((res) => {
				if (res.ok == false) throw new Error();
				return res.json();
			})
			.then((json) => {
				writable(null).subscribe(function (value) {
					if (browser) {
						window.localStorage.setItem(
							"user.email",
							json["email"]
						);
						window.localStorage.setItem("user.id", json["userid"]);
						window.localStorage.setItem(
							"user.username",
							json["username"]
						);
					}
				});

				location.href = "/";
				isLoading = false;
			})
			.catch((e) => {
				message = "로그인에 실패하였습니다.";
				isLoading = false;
			});
	};
</script>

<form method="post" on:submit|preventDefault={login}>
	{#if message != ""}
		<article class="message is-danger">
			<div class="message-body">
				{message}
			</div>
		</article>
	{/if}
	<div class="field">
		<label class="label" for="email">Email Address</label>
		<div class="control">
			<input
				class="input"
				type="email"
				placeholder="Your email"
				bind:value={email}
				required
			/>
		</div>
	</div>
	<div class="field">
		<label class="label" for="password">Password</label>
		<div class="control">
			<input
				class="input"
				type="password"
				placeholder="Set your new password"
				bind:value={password}
				required
			/>
		</div>
	</div>
	<div class="field">
		<div class="control">
			<button
				class="button is-link"
				class:is-loading={isLoading}
				disabled={isLoading}>{isLoading ? "Loading" : "Login"}</button
			>
		</div>
	</div>
</form>
