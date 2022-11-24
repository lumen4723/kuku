<script>
	import { browser } from "$app/env";
	import { writable } from "svelte/store";
	import { user } from "$lib/user.js";
	import { page } from "$app/stores";
	import { goto } from "$app/navigation";

	let isLoading = false;
	let email, password;
	let message = "";
	if ($page.url.searchParams.has("msg")) {
		message = $page.url.searchParams.get("msg");
	} else {
		message = "";
	}
	const login = async () => {
		isLoading = true;
		await fetch("https://api.eyo.kr/user/login", {
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
			.then((json) => {
				writable(null).subscribe(function (value) {
					if (browser) {
						window.sessionStorage.setItem(
							"user.email",
							json["email"]
						);
						window.sessionStorage.setItem(
							"user.id",
							json["userid"]
						);
						window.sessionStorage.setItem(
							"user.username",
							json["username"]
						);
					}
				});

				user.set({
					email: json.email,
					id: json.id,
					username: json.username,
				});

				goto("/");
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
				placeholder="Your password"
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
