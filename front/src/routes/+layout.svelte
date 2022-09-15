<script>
	import 'bulma/css/bulma.css';
	import '@fortawesome/fontawesome-free/css/all.css';
	import Header from '../lib/header/Header.svelte';
	import Footer from '../lib/footer/Footer.svelte';
</script>

<Header />

<main>
	<slot />
</main>

<Footer />

<style>
	/* main {
		min-height: calc(100vh - 100px - 20px);
	}
	footer {
		width: 100%;
		text-align: center;
		font-size: small;
		color: darkgray;
		bottom: 0px;
		height: 20px;
	} */
</style>
