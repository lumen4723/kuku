<script>
	let loading = false;
	let email, password;

	const login = async () => {
		const res = await fetch('http://api.eyo.kr:8081/user/login', {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				username: email,
				password
			}),
			mode: 'cors'
		});
		const json = await res.json();
		console.log(json);
		localStorage.setItem('username', json.username);
	};
</script>

<form method="post" on:submit|preventDefault={login}>
	<div class="field">
		<label class="label" for="email">Email Address</label>
		<div class="control">
			<input
				class="input"
				type="text"
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
			<button class="button is-link" disabled={loading}
				>{loading ? 'Loading' : 'Login'}</button
			>
		</div>
	</div>
</form>
