# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import os, time, sys
import re, shutil
import logging
_logger = logging.getLogger(__name__)


def ishostaccessible(details):
    response = dict(
        status=True,
        message='Success'
    )
    try:
        import paramiko
        ssh_obj = paramiko.SSHClient()
        ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _logger.info("Copia de seguridad de la base de datos en el script de verificación de conectividad en la línea {}".format(17))
        ssh_obj.connect(hostname = details['host'], username = details['user'], password = details['password'], port = details['port'])
        response['result'] = ssh_obj
        return response
    except ImportError:
        raise Exception("Módulo paramiko no encontrado. Instálelo usando pip: pip3 install paramiko")
    except Exception as e:
        _logger.info("No se pudo conectar el control remoto %r"%e)
        response['status'] = False
        response['message'] = e
    return response
