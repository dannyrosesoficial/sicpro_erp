/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { useState, useRef, onMounted } from "@odoo/owl";
import { SearchPanel } from "@web/search/search_panel/search_panel";
import { SearchBar } from "@web/search/search_bar/search_bar";
import { user } from "@web/core/user";


function getSearchPanelWidthKey(env) {
    const model = env.searchModel?.resModel || "unknown_model";
    const view = env.config?.viewType || "unknown_view";
    const uid = user.userId;
    return `searchPanelWidth:${model}:${view}:${uid}`;
}
function getSearchPanelKey(env) {
    const model = env.searchModel?.resModel || "unknown_model";
    const view = env.config?.viewType || "unknown_view";
    const uid = user.userId;
    return `searchPanelVisible:${model}:${view}:${uid}`;
}

patch(SearchPanel.prototype, {
    setup() {
        super.setup(...arguments);

        const widthKey = getSearchPanelWidthKey(this.env);
        const storedWidth = window.localStorage.getItem(widthKey);

        this.width = storedWidth;

        const key = getSearchPanelKey(this.env);
        const stored = window.localStorage.getItem(key);
        const visible = stored === null ? true : stored === "1";
        this.state = useState({
            ...this.state,
            visible: visible,
        });
        this.root = useRef("root");

        this.env.bus.addEventListener("advance_search:toggle", () => {
            this.state.visible = !this.state.visible;
            window.localStorage.setItem(key, this.state.visible ? "1" : "0");
            if (this.state.visible) {
                setTimeout(() => {
                    if (this.root.el) {
                        this.root.el.style["min-width"] = this.width;
                    }
                }, 0);
            }
        });

        onMounted(() => {
            if (this.root.el) {
                this.root.el.style["min-width"] = this.width;
            }
        });

        if (typeof onPatched === "function") {
            onPatched(() => {
                if (this.state.visible && this.root.el) {
                    this.root.el.style["min-width"] = this.width;
                }
            });
        }
    },

    _onStartResize(ev) {
        if (ev.button !== 0) return;
        const initialX = ev.pageX;
        const initialWidth = this.root.el.offsetWidth;
        const resizeStoppingEvents = ["keydown", "pointerdown", "pointerup"];
        const widthKey = getSearchPanelWidthKey(this.env);

        const resizePanel = (ev) => {
            ev.preventDefault();
            ev.stopPropagation();
            const maxWidth = Math.max(0.5 * window.innerWidth, initialWidth);
            const delta = ev.pageX - initialX;
            const newWidth = Math.min(maxWidth, Math.max(10, initialWidth + delta));
            this.width = `${newWidth}px`;
            this.root.el.style["min-width"] = this.width;
        };
        document.addEventListener("pointermove", resizePanel, true);

        const stopResize = (ev) => {
            if (ev.type === "pointerdown" && ev.button === 0) return;
            ev.preventDefault();
            ev.stopPropagation();
            document.removeEventListener("pointermove", resizePanel, true);
            resizeStoppingEvents.forEach((event) => {
                document.removeEventListener(event, stopResize, true);
            });
            document.activeElement.blur();
            window.localStorage.setItem(widthKey, this.width);
        };
        resizeStoppingEvents.forEach((event) => {
            document.addEventListener(event, stopResize, true);
        });
    },
});

patch(SearchBar.prototype, {
    onToggleSearchPanel() {
        this.env.bus.trigger("advance_search:toggle");
    }
});