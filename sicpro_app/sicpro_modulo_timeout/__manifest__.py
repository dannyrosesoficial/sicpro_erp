# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Timeout',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'El módulo se encarga de cerrar la session después del tiempo '
               'predeterminado por la configuración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp', "base"],
    "data": ["data/ir_config_parameter_data.xml"],

    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}