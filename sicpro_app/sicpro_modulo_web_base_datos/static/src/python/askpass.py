#!/usr/bin/env python
#
# Script para actualizar las credenciales de git.
# Requiere las variables GIT_USERNAME y GIT_PASSWORD,
# El script es llamado desde el propio sicpro GIT_ASKPASS.
#

from os import environ
from sys import argv

if argv[1] == "Username for 'https://gitlab.etecsa.cu': ":
    print environ['GIT_USERNAME']
    exit()

if argv[1] == "Password for 'https://%(GIT_USERNAME)s@gitlab.etecsa.cu': " % environ:
    print environ['GIT_PASSWORD']
    exit()

exit(1)
