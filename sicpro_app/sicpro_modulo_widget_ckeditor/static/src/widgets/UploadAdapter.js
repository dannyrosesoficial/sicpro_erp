/** @odoo-module **/

/**
 * Upload adapter for CKEditor 5 that works with Odoo
 * Replaces axios with native XMLHttpRequest for better Odoo integration
 */
export class UploadAdapter {
    constructor(loader, configuration) {
        // The file loader instance to use during the upload.
        this.loader = loader;
        this.validateConfig(configuration);
        this.configuration = configuration;
        this.xhr = null;
    }

    // Starts the upload process.
    upload() {
        return this.loader.file
            .then(file => new Promise((resolve, reject) => {
                // prepare form data
                const data = this.prepareFormData(file);
                // send request
                this.send(data, resolve, reject);
            }));
    }

    // Aborts the upload process.
    abort() {
        if (this.xhr) {
            this.xhr.abort();
        }
    }

    /**
     * Show validation error message
     * @param configuration
     */
    validateConfig(configuration) {
        if (typeof configuration !== 'object' || configuration === null) {
            console.info('La configuración del adaptador de carga debe ser un objeto.');
            console.error('La configuración del archivo de carga de CKEditor no es válida.');
        }
    }

    /**
     * Prepare form data
     * @param file
     * @returns {FormData}
     */
    prepareFormData(file) {
        const data = new FormData();
        data.append('ufile', file);

        // Add CSRF token to FormData for Odoo
        const {token, model, recordId} = this.configuration;
        if (token) {
            data.append('csrf_token', token);
        }

        // Add model and id parameters required by Odoo
        if (model) {
            data.append('model', model);
        }
        if (recordId) {
            data.append('id', recordId);
        }

        return data;
    }

    /**
     * Send upload request using XMLHttpRequest
     * @param data
     * @param resolve
     * @param reject
     */
    send(data, resolve, reject) {
        const loader = this.loader;
        const {uploadUrl} = this.configuration;

        if (!uploadUrl) {
            console.error('CKEditor5 Cargar FileAdapter: uploadUrl no está definido.');
            return reject('La URL de carga no está configurada');
        }

        const xhr = new XMLHttpRequest();
        this.xhr = xhr;

        // Configure request
        xhr.open('POST', uploadUrl, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        // Track upload progress
        xhr.upload.addEventListener('progress', (evt) => {
            if (evt.lengthComputable) {
                loader.uploadTotal = evt.total;
                loader.uploaded = evt.loaded;
            }
        });

        // Handle successful response
        xhr.addEventListener('load', () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    const response = JSON.parse(xhr.responseText);

                    // Odoo returns attachment info with 'id' field
                    // Build URL from attachment ID
                    let imageUrl;
                    if (response && response[0].id) {
                        imageUrl = `/web/content/${response[0].id}`;
                    }
                    console.log(imageUrl)
                    if (imageUrl) {
                        resolve({
                            default: imageUrl
                        });
                    } else {
                        console.error('Subir respuesta:', response);
                        reject('Respuesta no válida: no se devolvió ninguna URL ni ID');
                    }
                } catch (e) {
                    console.error('Failed to parse upload response:', xhr.responseText);
                    reject('Error de carga: respuesta JSON no válida');
                }
            } else if (xhr.status === 422) {
                // Unprocessable Entity
                try {
                    const response = JSON.parse(xhr.responseText);
                    const message = response.errors?.image?.[0] || 'Validation error';
                    reject(message);
                } catch (e) {
                    reject('Error de validación');
                }
            } else {
                reject(`La carga falló con el estado ${xhr.status}`);
            }
        });

        // Handle network errors
        xhr.addEventListener('error', () => {
            reject('Error de carga: error de red');
        });

        // Handle upload abort
        xhr.addEventListener('abort', () => {
            reject('Carga cancelada');
        });

        // Send the request
        xhr.send(data);
    }
}
