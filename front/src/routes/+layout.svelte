<script>
	import 'bulma/css/bulma.css';
	import '@fortawesome/fontawesome-free/css/all.css';
	import Header from '$lib/header/Header.svelte';
	import Footer from '$lib/footer/Footer.svelte';
</script>

<Header />

<main>
	<slot />
</main>

<Footer />
