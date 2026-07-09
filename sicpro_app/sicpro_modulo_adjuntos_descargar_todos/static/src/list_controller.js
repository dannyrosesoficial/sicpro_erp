/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { download } from "@web/core/network/download";

patch(ListController.prototype, {
    getStaticActionMenuItems() {
        const menuItems = super.getStaticActionMenuItems(...arguments);

        menuItems["download_attachments"] = {
            isAvailable: () => true,
            sequence: 25,
            icon: "fa fa-download",
            description: _t("Descargar archivos adjuntos"),
            callback: () => this.downloadAttachments(),
        };

        return menuItems;
    },

    async downloadAttachments() {
     /**
         * Descargue todos los archivos adjuntos vinculados a los registros seleccionados en la vista de lista.
         *
         * Este método se activa desde una acción personalizada en el menú de la barra lateral de la vista de lista.
         * Recopila todos los ID de registros seleccionados actualmente, recupera sus relacionados
         * Entradas `ir.attachment` y genera un archivo ZIP para descargar.
     **/
        const root = this.model.root;
        const active_ids = root.selection.map(record => record.resId);
        const model = root.resModel;
        debugger;
        this.attachmentList = await this.orm.searchRead(
                "ir.attachment",
                [
                    ["res_model", "=", model],
                    ["res_id", "in", active_ids],
                ],
                ["id", "res_id"]
        );

        if (!this.attachmentList.length) {
            this.env.services.notification.add(
                _t("No se encontraron archivos adjuntos para los registros seleccionados.!"),
                { type: "warning" }
            );
            return;
        }

        const recordWithNoAttachments = active_ids.filter(id => {
            return !this.attachmentList.some(att => Number(att.res_id) === Number(id));
        });

        if (recordWithNoAttachments.length) {
            this.env.services.notification.add(
                _t("Algunos registros seleccionados no tienen archivos adjuntos. Descargando archivos disponibles."),
                { type: "warning" }
            );
        }
        const modelName = model.includes(".") ? model.replace(/\./g, "_") : model;
        const zipName = `${modelName}_attachments.zip`;
        const attachment_ids = this.attachmentList.map(record => record.id);
        download({
            data: {
                file_ids: attachment_ids,
                zip_name: zipName,
            },
            url: "/mail/attachment/zip",
        });
    },
});

