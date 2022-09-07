<script>
	import { is_empty } from 'svelte/internal';

	let name = '',
		username,
		email ='',
		password,
		confirmpassword;
	let message = { success: null, display: '' };

	let valid_email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
</script>

<form>
	<div class="field">
		<label class="label" for="name">Name</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={is_empty(name)}
				class:is-success={!is_empty(name)}
				name="name"
				type="text"
				placeholder="Your name"
				bind:value={name}
			/>
			<span class="icon is-small is-left">
				<i
					class="fa-regular fa-user"
					class:has-text-danger={is_empty(name)}
					class:has-text-success={!is_empty(name)}
				/>
			</span>
			<span class="icon is-small is-right">
				<i
					class="fas fa-check"
					class:has-text-danger={is_empty(name)}
					class:has-text-success={!is_empty(name)}
				/>
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
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={!email.match(valid_email)}
				class:is-success={email.match(valid_email)}
				name="email"
				type="text"
				placeholder="Your email"
				bind:value={email}
			/>
			<span class="icon is-small is-left">
				<i
					class="fa-regular fa-envelope"
					class:has-text-danger={!email.match(valid_email)}
					class:has-text-success={email.match(valid_email)}
				/>
			</span>
			<span class="icon is-small is-right">
				<i
					class="fas fa-check"
					class:has-text-danger={!email.match(valid_email)}
					class:has-text-success={email.match(valid_email)}
				/>
			</span>
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
</form>
