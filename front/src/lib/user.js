import { browser } from "$app/env";
import { writable } from "svelte/store";

export function userIsLogged() {
	return browser && sessionStorage.getItem("user.username") !== null;
}
