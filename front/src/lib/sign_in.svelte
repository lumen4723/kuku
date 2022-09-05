<script>
	let loading = false;
	let email, password;
	let message = { success: null, display: '' };
</script>

<form>
	<div class="field">
		<label class="label" for="email">Email Address</label>
		<div class="control">
			<input
				class="input"
				id="email"
				type="email"
				placeholder="Your email"
				bind:value={email}
			/>
		</div>
	</div>
	<div class="field">
		<label class="label" for="password">Password</label>
		<div class="control">
			<input
				class="input"
				id="password"
				type="password"
				placeholder="Set your new password"
				bind:value={password}
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
	{#if message.success != null}
		<div>
			{message.display}
		</div>
	{/if}
</form>

<style>
</style>
