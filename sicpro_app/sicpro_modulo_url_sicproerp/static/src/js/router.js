/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { router, routerBus } from "@web/core/browser/router";
import { patch } from "@web/core/utils/patch";


const SICPRO_PREFIX = "/sicpro";
const ODOO_PREFIX = "/odoo";


function normalizeSicproUrl(url) {
    const normalizedUrl = new URL(url.href);

    if (normalizedUrl.pathname === SICPRO_PREFIX) {
        normalizedUrl.pathname = ODOO_PREFIX;
    } else if (normalizedUrl.pathname.startsWith(`${SICPRO_PREFIX}/`)) {
        normalizedUrl.pathname =
            `${ODOO_PREFIX}${normalizedUrl.pathname.slice(SICPRO_PREFIX.length)}`;
    }

    return normalizedUrl;
}


function toSicproUrl(url) {
    if (url === ODOO_PREFIX) {
        return SICPRO_PREFIX;
    }

    if (url.startsWith(`${ODOO_PREFIX}/`)) {
        return `${SICPRO_PREFIX}${url.slice(ODOO_PREFIX.length)}`;
    }

    return url;
}


patch(router, {
    stateToUrl(state) {
        return toSicproUrl(super.stateToUrl(state));
    },

    urlToState(url) {
        return super.urlToState(normalizeSicproUrl(url));
    },
});


function synchronizeInitialRoute() {
    const currentUrl = new URL(browser.location.href);

    if (
        currentUrl.pathname !== SICPRO_PREFIX &&
        !currentUrl.pathname.startsWith(`${SICPRO_PREFIX}/`)
    ) {
        return;
    }

    const currentState = router.urlToState(currentUrl);

    router.replaceState(currentState, {
        replace: true,
        sync: true,
    });
}


browser.addEventListener("click", (ev) => {
    if (
        ev.defaultPrevented ||
        ev.button !== 0 ||
        ev.metaKey ||
        ev.ctrlKey ||
        ev.shiftKey ||
        ev.altKey ||
        ev.target.closest("[contenteditable]")
    ) {
        return;
    }

    const anchor = ev.target.closest("a");

    if (!anchor || anchor.target === "_blank") {
        return;
    }

    const href = anchor.getAttribute("href");

    if (!href || href.startsWith("#")) {
        return;
    }

    let url;

    try {
        url = new URL(anchor.href);
    } catch {
        return;
    }

    if (
        browser.location.host !== url.host ||
        (
            url.pathname !== SICPRO_PREFIX &&
            !url.pathname.startsWith(`${SICPRO_PREFIX}/`)
        )
    ) {
        return;
    }

    ev.preventDefault();

    router.pushState(router.urlToState(url));
});


synchronizeInitialRoute();
