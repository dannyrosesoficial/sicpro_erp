/** @odoo-module **/

import {UploadAdapter} from './UploadAdapter';

/**
 * Upload adapter plugin for CKEditor 5
 * Compatible with CKEditor 5 UMD build used in Odoo
 */
export function UploadAdapterPlugin(editor) {
    const configuration = editor.config.get('uploadAdapter');

    if (!configuration) {
        console.warn('CKEditor5 Cargar FileAdapter: la configuración no está definida.');
        console.warn('Configurar uploadAdapter en la configuración de CKEditor: { uploadAdapter: { uploadUrl: "/your/upload/url", token: "csrf-token" } }');
        return;
    }

    // Create upload adapter factory
    editor.plugins.get('FileRepository').createUploadAdapter = (loader) => {
        return new UploadAdapter(loader, configuration);
    };
}
