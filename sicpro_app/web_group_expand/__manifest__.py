# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Expandir Grupos Vistas de Lista',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Expandir Grupos Vistas de Lista",
    'description': "Este módulo se encarga de poder expandir los grupos en la vista de árbol o lista",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        "nucleo_sicpro_erp",
        "web"
    ],
    "assets": {
        "web.assets_backend": [
            "/web_group_expand/static/src/js/web_group_expand.esm.js",
        ],
        "web.assets_qweb": [
            "/web_group_expand/static/src/xml/expand_buttons.xml",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
