<script>
	let name, username, email, password, confirmpassword;
	let message = { success: null, display: '' };
</script>

<form>
	<div class="field">
		<label class="label" for="name">Name</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				name="name"
				type="text"
				placeholder="Your name"
				bind:value={name}
			/>
			<span class="icon is-small is-left">
				<i class="fa-regular fa-user" />
			</span>
			<span class="icon is-small is-right">
				<i class="fas fa-check" />
			</span>
		</div>
		<p class="help">Write your name</p>
	</div>
	<div class="field">
		<label class="label" for="username">Username</label>
		<div class="control">
			<input
				class="input"
				name="usernmae"
				type="text"
				placeholder="Your usernmae"
				bind:value={username}
			/>
		</div>
		<p class="help">Write your name to be shown to others</p>
	</div>
	<div class="field">
		<label class="label" for="email">Email</label>
		<div class="control">
			<input
				class="input"
				name="email"
				type="text"
				placeholder="Your email"
				bind:value={email}
			/>
		</div>
		<p class="help">Write your email</p>
	</div>
	<div class="field">
		<label class="label" for="password">Password</label>
		<div class="control">
			<input
				class="input"
				name="password"
				type="password"
				placeholder="Set your new password"
				bind:value={password}
			/>
		</div>
		<p class="help">Should contail at least 8 characters</p>
	</div>
	<div class="field">
		<label class="label" for="confirmpassword">Confirm Password</label>
		<input
			class="input"
			name="confirmpassword"
			type="password"
			placeholder="Confirm your new password"
			bind:value={confirmpassword}
		/>
	</div>
	<div class="field is-grouped">
		<div class="control">
			<button class="button is-link" type="submit">Signup</button>
		</div>
		<div class="control">
			<button class="button is-link is-light" type="submit">Cancel</button>
		</div>
	</div>
	{#if message.success != null}
		<div>
			{message.display}
		</div>
	{/if}
</form>
