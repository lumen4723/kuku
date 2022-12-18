<script>
	export let language;
	export let code;
	export let getData;

	import { onMount } from "svelte";
	import { browser } from "$app/env";
	import { initialize as editorWorker } from "monaco-editor/esm/vs/editor/editor.worker?worker";

	let divEl = null;
	let editor;
	let Monaco;

	$: {
		if (browser && editor != undefined) {
			Monaco.editor.setModelLanguage(
				editor.getModel(),
				language.toLocaleLowerCase()
			);
		}
	}
	$: {
		if (browser && editor != undefined) {
			editor.getModel().setValue(code);
		}
	}
	getData = () => {
		return editor.getModel().getValue();
	};

	onMount(async () => {
		// @ts-ignore
		self.MonacoEnvironment = {
			getWorker: function (_moduleId, label) {
				return new editorWorker();
			},
		};

		Monaco = await import("monaco-editor");
		editor = Monaco.editor.create(divEl, {
			theme: "vs-dark",
			value: code,
			language: language.toLocaleLowerCase(),
		});

		return () => {
			editor.dispose();
		};
	});
</script>

<div bind:this={divEl} class="h-screen" />

<style>
	.h-screen {
		height: calc(100vh - 282px);
	}
</style>
