import { browser } from "$app/env";
import { writable } from "svelte/store";

function getUserObject() {
	if (browser == false) return null;
	const email = window.sessionStorage.getItem("user.email");
	const id = window.sessionStorage.getItem("user.id");
	const username = window.sessionStorage.getItem("user.username");

	if (email && id && username)
		return { email, id, username };

	return null;
}

export const user = writable(getUserObject());
export function userIsLogged() {
	return getUserObject() !== null;
}
