/** @odoo-module **/

// Danny: Constantes necesarias para el manejo de coordenadas de Cropper 🌹
const cropperDataFields = ['x', 'y', 'width', 'height', 'rotate', 'scaleX', 'scaleY'];
const modifierFields = [
    'filter', 'quality', 'mimetype', 'glFilter',
    'originalId', 'originalSrc', 'resizeWidth', 'aspectRatio'
];

/**
 * Carga una imagen de forma asíncrona devolviendo una Promesa
 */
export function loadImage(src, img = new Image()) {
    return new Promise((resolve, reject) => {
        img.addEventListener('load', () => resolve(img), {once: true});
        img.addEventListener('error', reject, {once: true});
        img.src = src;
    });
}

/**
 * Activa la instancia de Cropper sobre un elemento imagen
 * Danny: Esta es la función motor que usamos en los widgets 🌹
 */
export async function activateCropper(image, aspectRatio, dataset) {
    if (image.cropperInstance) {
        image.cropperInstance.destroy();
    }

    // Danny: En Odoo 19 offline, evitamos el crossorigin si usamos DataURLs 🌹
    if (!image.src.startsWith('data:')) {
        image.setAttribute('crossorigin', 'anonymous');
    }

    const cropper = new window.Cropper(image, {
        viewMode: 1,
        dragMode: 'move',
        autoCropArea: 0.8,
        aspectRatio: aspectRatio || 1,
        checkOrientation: false,
        checkCrossOrigin: false, // Danny: Falso para mejor compatibilidad offline 🌹
        responsive: true,
        // Danny: Mapeamos los datos del dataset si existen (posiciones previas)
        data: Object.fromEntries(
            Object.entries(dataset || {})
                .filter(([key]) => cropperDataFields.includes(key))
                .map(([key, value]) => [key, parseFloat(value)])
        ),
    });

    image.cropperInstance = cropper;

    // Devolvemos la promesa cuando la rejilla esté lista para interactuar
    return new Promise(resolve => {
        image.addEventListener('ready', () => {
            resolve(cropper);
        }, {once: true});
    });
}

/**
 * Danny: He comentado esta función porque para SICPRO usamos binarios directos
 * y no necesitamos consultar adjuntos de web_editor (evitamos errores de RPC) 🌹
 */
/*
export async function loadImageInfo(img, rpc, attachmentSrc = '') {
    // ... lógica de Odoo nativa que no usaremos para credenciales ...
}
*/

export { cropperDataFields, modifierFields };
export const removeOnImageChangeAttrs = [...cropperDataFields, ...modifierFields, 'aspectRatio'];