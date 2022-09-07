<script>
	import { is_empty } from 'svelte/internal';

	let name = '',
		username,
		email,
		password= '',
		confirmpassword = '';
	let message = { success: null, display: '' };
	let show_password = false;
	function passwordShowHide() {
		show_password = !show_password;
	}

	var show_eye = document.getElementsByClassName("fas fa-eye-slash");
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
		<div class="control has-icons-left has-icons-right">
			<div class="control">
				<input
					class="input"
						class:is-danger={!is_empty(password)
						&& password.length < 8
						|| password.length > 128}
						class:is-success={password.length > 7}
						name="password"
						type ={show_password ? "text" : "password"}
						placeholder="Set your new password"
						bind:this={password}
				/>
				<span class="icon is-small is-right">
					<i
						
						class="fas fa-eye-slash password_icon"
						on:click={passwordShowHide}
						class:has-text-danger={!is_empty(password)
							&& password.length < 8
							|| password.length > 128}
						class:has-text-success={password.length > 7}
					/>
				</span>
			</div>
		</div>
		<p class="help">
			Should contail at least 8 ~ 128 characters
		</p>
	</div>

	<div class="field">
		<label class="label" for="confirmpassword">Confirm Password</label>
		<div class="control has-icons-left has-icons-right">
			<input		
				class="input"
				class:is-danger={!is_empty(confirmpassword)
					&& password !== confirmpassword}
				class:is-success={password === confirmpassword &&
				password.length > 7}
				name="confirmpassword"
				type="password"
				placeholder="Confirm your new password"
				bind:this={confirmpassword}
			/>
			<span class="icon is-small is-right">
				<i
				class="fas fa-eye-slash"
				class:has-text-danger={!is_empty(confirmpassword)
					&& password !== confirmpassword}
				class:has-text-success={password === confirmpassword &&
					password.length > 7}
				/>
			</span>
		</div>
	</div>

	<div class="field is-grouped">
		<div class="control">
			<button class="button is-link" type="submit">Signup</button>
		</div>
		<div class="control">
			<button class="button is-link is-light" type="submit">Cancel</button>
		</div>
	</div>
	<button type="button" on:click="{passwordShowHide}">{show_password ? 'Hide' : 'Show'}</button>
</form>

<style>
	.password_icon {
		pointer-events: all;
		cursor : pointer;
	}
</style>