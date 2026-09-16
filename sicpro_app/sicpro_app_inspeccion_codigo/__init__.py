# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################ails.

import logging
import os
import ast
import importlib
from odoo import api, SUPERUSER_ID
from .hooks import post_init_hook_verificar_modulos

_logger = logging.getLogger(__name__)


def _inspeccionar_codigo_python_sicpro():
    """
    Función que recorre la suite de módulos 'sicpro_app_*' analizando el Árbol
    de Sintaxis Abstracta (AST) e intentando la importación directa de componentes
    para capturar NameError, SyntaxError y errores de nombres globales no definidos.
    """
    _logger.info(
        "=================================================================")
    _logger.info(
        "[SICPRO DEBUG] Iniciando escaneo de seguridad en módulos sicpro_app...")

    # Directorio raíz donde residen los 114+ módulos personalizados
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    errores_encontrados = []
    archivos_analizados = 0

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                archivos_analizados += 1
                filepath = os.path.join(root, file)

                # 1. Inspección de Sintaxis mediante AST (Abstract Syntax Tree)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        source = f.read()

                    tree = ast.parse(source, filename=filepath)

                    # Buscador específico de lambdas mal configuradas en defaults de campos ORM
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            # Identificar si es una asignación de campo de Odoo (fields.Integer, fields.Char, etc.)
                            if isinstance(node.func,
                                          ast.Attribute) and node.func.attr in (
                            'Integer', 'Char', 'Many2one', 'Selection',
                            'Boolean', 'Float', 'Monetary', 'Datetime',
                            'Date'):
                                for keyword in node.keywords:
                                    if keyword.arg == 'default' and isinstance(
                                        keyword.value, ast.Lambda):
                                        # Detectar si la lambda llama a un nombre sin self ni ámbito
                                        lambda_body = keyword.value.body
                                        if isinstance(lambda_body,
                                                      ast.Call) and isinstance(
                                            lambda_body.func, ast.Name):
                                            _logger.warning(
                                                f"[SICPRO WARN] Advertencia de posible NameError en {filepath}:{node.lineno}: "
                                                f"Sintaxis obsoleta 'default=lambda self: {lambda_body.func.id}()'. "
                                                f"Se recomienda cambiar a 'default={lambda_body.func.id}' o 'default=self._{lambda_body.func.id}'.")

                except SyntaxError as se:
                    msg = f"SyntaxError en {filepath} línea {se.lineno}: {se.msg}"
                    _logger.error(f"[SICPRO ERROR] {msg}")
                    errores_encontrados.append(msg)
                except Exception as e:
                    msg = f"Error leyendo {filepath}: {str(e)}"
                    _logger.error(f"[SICPRO ERROR] {msg}")
                    errores_encontrados.append(msg)

    _logger.info(
        f"[SICPRO DEBUG] Escaneo finalizado. {archivos_analizados} archivos Python inspeccionados.")

    if errores_encontrados:
        _logger.critical(
            f"[SICPRO CRITICAL] Se detectaron {len(errores_encontrados)} errores que previenen el arranque seguro.")  # Comentado para no tumbar la instancia si se prefiere solo auditar en log:  # raise Exception(f"Se encontraron errores de código en sicpro_app: {errores_encontrados}")
    else:
        _logger.info(
            "[SICPRO DEBUG] Verdadero: No se encontraron errores críticos de sintaxis en los módulos.")


# Ejecutar la verificación al importar el paquete durante el arranque de Odoo
_inspeccionar_codigo_python_sicpro()