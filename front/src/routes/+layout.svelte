<script>
	import Header from '../lib/header/Header.svelte';
	import 'bulma/css/bulma.css';
	import '@fortawesome/fontawesome-free/css/all.css';
</script>

<Header />

<main>
	<slot />
</main>

<footer class="footer">
<<<<<<< HEAD
	<p>kukur@뻐꾸기</p>
=======
	<p>kuku@뻐꾸기kjs</p>
>>>>>>> 8265274f4aa6996cd3cce5d5a5a56fa885c44457
</footer>

<style>
	main {
		min-height: calc(100vh - 100px - 20px);
	}
	footer {
		width: 100%;
		text-align: center;
		font-size: small;
		color: darkgray;
		bottom: 0px;
		height: 20px;
	}
</style>
