odoo.define('sicpro_modulo_mapas.solmap_common', function () {
    "use strict";
    var SolMapMixin = {
        cssLibs: [
            '/sicpro_modulo_mapas/static/lib/ol-6.4.3/ol.css',
            '/sicpro_modulo_mapas/static/lib/ol-ext/ol-ext.min.css',
        ],
        jsLibs: [
            '/sicpro_modulo_mapas/static/lib/ol-6.4.3/ol.js',
            '/sicpro_modulo_mapas/static/lib/ol-ext/ol-ext.min.js',
        ],
    };

    return {
        SolMapMixin: SolMapMixin,
    };
});