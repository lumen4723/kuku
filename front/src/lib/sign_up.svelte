<script>
	import { is_empty } from 'svelte/internal';

	let name = '',
		username = '',
		email = '',
		password = '',
		confirmpassword = '';
	let message = { success: null, display: '' };

	let valid_email =
		/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

	let show_password = false;
	let show_confirmpassword = false;
	function passwordShow_button() {
		show_password = !show_password;
	}
	function confirmpasswordShow_button() {
		show_confirmpassword = !show_confirmpassword;
	}
	let passwordThis;
	let confirmpasswordThis;
	let usernameFailed = true;
	let usernameExcepts = ['ㅅㅂ', 'kuku'];

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

	let timer = 0;
	let loading = false;
	/*backend api 생성 후 이걸로 변경*/
	//sleep 함수 제거 후
	// await sleep(1000).then((value)=>{
	//		usernameFailed = false;
	//		loading = false;
	//	}) 이걸 await fetch ('http://~') 이걸로 변경하면 됩니다.
	const sleep = (ms) => {
		return new Promise((resolve, reject) => {
			setTimeout(function () {
				resolve(true);
			}, ms);
		});
	};
	const setTimeoutFun = async () => {
		await sleep(1000).then((value) => {
			usernameFailed = false;
			loading = false;
		});
	};
	/**
	 * Checking user name is exist
	 */
	const checkUsername = () => {
		clearTimeout(timer);
		loading = true;
		if (filterUsername()) {
			timer = setTimeout(setTimeoutFun, 2000);
		} else {
			usernameFailed = true;
			loading = false;
		}
	};
	//
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
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={usernameFailed && !is_empty(username)}
				class:is-success={!usernameFailed}
				name="username"
				type="text"
				placeholder="Your username"
				bind:value={username}
				on:input={checkUsername}
			/>
			<span class="icon is-small is-left ">
				<i
					class="fa-regular fa-user"
					class:has-text-danger={usernameFailed && !is_empty(username)}
					class:has-text-success={!usernameFailed}
				/>
			</span>
			{#if loading}
				<span class="icon fa-sm is-right ">
					<i
						class="fa-solid fa-circle-notch fa-spin"
						class:has-text-danger={usernameFailed && !is_empty(username)}
						class:has-text-success={!usernameFailed}
					/>
				</span>
			{:else}
				<span class="icon is-small is-right">
					<i
						class="fas fa-check"
						class:has-text-danger={usernameFailed && !is_empty(username)}
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
		<label class="label" for="email">Email</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={!email.match(valid_email) && !is_empty(email)}
				class:is-success={email.match(valid_email)}
				name="email"
				type="text"
				placeholder="Your email"
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
		<label class="label" for="password">Password</label>
		<div class="control has-icons-left has-icons-right">
			<div class="control">
				<input
					class="input"
					class:is-danger={(!is_empty(password) && password.length < 8) ||
						password.length > 128}
					class:is-success={password.length > 7 && password.length < 129}
					name="password"
					type={show_password ? 'text' : 'password'}
					placeholder="Set your new password"
					bind:this={passwordThis}
					on:input={() => (password = passwordThis.value)}
				/>
				<span class="icon is-small is-right">
					<i
						class={show_password
							? 'fas fa-eye password_icon'
							: 'fas fa-eye-slash password_icon'}
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
		<p class="help">Should contail at least 8 ~ 128 characters</p>
	</div>

	<div class="field">
		<label class="label" for="confirmpassword">Confirm Password</label>
		<div class="control has-icons-left has-icons-right">
			<input
				class="input"
				class:is-danger={!is_empty(confirmpassword) &&
					password !== confirmpassword}
				class:is-success={password === confirmpassword &&
					password.length > 7 &&
					password.length < 129}
				name="confirmpassword"
				type={show_confirmpassword ? 'text' : 'password'}
				placeholder="Confirm your new password"
				bind:this={confirmpasswordThis}
				on:input={() => (confirmpassword = confirmpasswordThis.value)}
			/>
			<span class="icon is-small is-right">
				<i
					class={show_confirmpassword
						? 'fas fa-eye confirmpassword_icon'
						: 'fas fa-eye-slash confirmpassword_icon'}
					on:click={confirmpasswordShow_button}
					class:has-text-danger={!is_empty(confirmpassword) &&
						password !== confirmpassword}
					class:has-text-success={password === confirmpassword &&
						password.length > 7 &&
						password.length < 129}
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
</form>

<style>
	.password_icon {
		pointer-events: all;
		cursor: pointer;
	}
	.confirmpassword_icon {
		pointer-events: all;
		cursor: pointer;
	}
</style>
