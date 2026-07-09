/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { View } from "@web/views/view";
import { useState, onWillStart } from "@odoo/owl";

patch(ListController.prototype, {
    setup() {
        super.setup();
        // Ensure View is available in components for subclasses that might have copied components
        // before this module was loaded (e.g. SaleFileUploadListController).
        if (!this.constructor.components || !this.constructor.components.View) {
            this.constructor.components = {
                ...(this.constructor.components || {}),
                View,
            };
        }

        this.state = useState({
            ...this.state,
            splitViewEnabled: false,
            splitViewMode: 'horizontal', // 'horizontal' or 'vertical'
            selectedRecordId: null,
        });
        this.actionService = useService("action");
    },

    toggleSplitView() {
        this.state.splitViewEnabled = !this.state.splitViewEnabled;
        if (!this.state.splitViewEnabled) {
            this.state.selectedRecordId = null;
        }
    },

    setSplitMode(mode) {
        this.state.splitViewMode = mode;
        if (!this.state.splitViewEnabled) {
            this.state.splitViewEnabled = true;
        }
    },

    async openRecord(record) {
        if (this.state.splitViewEnabled) {
            this.state.selectedRecordId = record.resId;
        } else {
            super.openRecord(record);
        }
    },

    getSplitViewProps() {
        return {
            resModel: this.props.resModel,
            resId: this.state.selectedRecordId,
            type: "form",
            readonly: false,
            className: "o_split_view_form",
            display: { controlPanel: false },
        };
    },

    onResizeStart(ev) {
        // Implement resizing logic if needed
        console.log("Resize start");
    }
});
