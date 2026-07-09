/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onWillDestroy, useState } from "@odoo/owl";

export class AutoUpdateServerInfo extends Component {
    static template = "sicpro_server_info.AutoUpdate";

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            stats: {},
            loading: true,
            isRefreshing: false,
            currentInterval: 5000
        });
        this.timer = null;

        onWillStart(async () => {
            await this._fetchStats();
            this._startTimer();
        });

        onWillDestroy(() => this._stopTimer());
    }

    _startTimer() {
        this._stopTimer();
        this.timer = setInterval(() => this._fetchStats(), this.state.currentInterval);
    }

    _stopTimer() {
        if (this.timer) clearInterval(this.timer);
    }

    onIntervalChange(ev) {
        this.state.currentInterval = parseInt(ev.target.value);
        this._startTimer();
    }

    formatBytes(bytes) {
        if (!bytes || isNaN(bytes)) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async manualUpdate() {
        this.state.isRefreshing = true;
        await this._fetchStats();
        setTimeout(() => { this.state.isRefreshing = false; }, 600);
    }

    async _fetchStats() {
        try {
            const data = await this.orm.call("ir.http", "session_info", [[]]);
            if (data && data.server_stats) {
                this.state.stats = data.server_stats;
                this.state.loading = false;
            }
        } catch (error) {
            console.error("Error en monitoreo SICPRO:", error);
        }
    }
}

registry.category("view_widgets").add("auto_update", { component: AutoUpdateServerInfo });