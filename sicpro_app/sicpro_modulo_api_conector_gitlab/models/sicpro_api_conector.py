# -*- coding: utf-8 -*-

from datetime import datetime

import gitlab

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ApiConector(models.Model):
    _inherit = 'sicpro.modulo.api.conector'

    name = fields.Selection(selection_add=[('sicpro.api.gitlab', 'APLICACIÓN GITLAB ETECSA')],
                            ondelete={'sicpro.api.gitlab': 'cascade'})

    # IMPORTANTE: El nombre de la acción debe ser 'api_test_' + el nombre del valor del campo name
    def conector_api_test_sicpro_api_gitlab(self):
        app = self.env['sicpro.modulo.api.conector'].sudo().search([('name', '=', 'sicpro.api.gitlab')])
        token = app.token
        proyecto = app.url_config_data
        url_data = app.url_data

        try:
            if token and proyecto:
                # llamo a la conexión api
                gl = gitlab.Gitlab(url_data, oauth_token=token, ssl_verify=False)
                gl.auth()
                raise ValidationError(_('Conexión establecida con éxito.'))
            else:
                raise ValidationError(_('El campo Token o Dato Variable están vacíos, verifíquelo'))

        except gitlab.GitlabAuthenticationError as e:
            raise ValidationError(_('Conexión reusada en el Url Login o el Token de acceso. '
                                    'Descripción del error: ' + str(e) + ', Verifíquelo'))

    # IMPORTANTE: El nombre de la acción debe ser 'api_cron_' + el nombre del valor del campo name
    def conector_api_cron_sicpro_api_gitlab(self):
        # compruebo que esté creada la configuración de la aplicación api
        global app_id, fecha_inicio, seguidores
        app = self.env['sicpro.modulo.api.conector'].sudo().search([('name', '=', 'sicpro.api.gitlab')])
        try:
            if app:
                app_id = app.app_id
                token = app.token
                proyecto = app.url_config_data
                url_data = app.url_data
                dic_commits = []
                dic_commit_id_corto = []
                fecha_inicio = datetime.today()
                registros_creados = 0
                registros_actualizados = 0
                registros_archivados = 0

                # Busco todos los commits almacenados
                todos_commits = self.env['sicpro.modulo.api.conector.gitlab.commits'].sudo().search([('active', '=', True)])

                # llamo a la conexión api
                gl = gitlab.Gitlab(url_data, oauth_token=token, ssl_verify=False)
                gl.auth()
                # busco el proyecto específico en gitlab, debe ser el usuario/proyecto
                # ej: daniel.borrero/sicpro-erp
                proyecto_git = gl.projects.get(proyecto)
                # busco los branches del proyecto seleccionado
                branches_git = proyecto_git.branches.list()
                # busco los commits por cada branch
                for branch in branches_git:
                    branch_nombre = branch.name
                    branch_web_url = branch.web_url
                    # busco los commits del proyecto seleccionado
                    commits_git = proyecto_git.commits.list(ref_name=branch_nombre)
                    for commit in commits_git:
                        commit_id_largo = commit.id
                        commit_id_corto = commit.short_id
                        commit_titulo = commit.title
                        commit_creado = datetime.strptime(
                            str(commit.created_at[0:10]) + ' ' + str(commit.created_at[11:19]), '%Y-%m-%d %H:%M:%S')
                        commit_mensaje = commit.message
                        commit_autor = commit.author_name
                        commit_web_url = commit.web_url
                        # creo listado con los registros
                        data = {
                            'name': commit_titulo, 'branch_nombre': branch_nombre,
                            'branch_web_url': branch_web_url, 'commit_id_largo': commit_id_largo,
                            'commit_id_corto': commit_id_corto, 'commit_creado': commit_creado,
                            'commit_mensaje': commit_mensaje, 'commit_autor': commit_autor,
                            'commit_web_url': commit_web_url,
                        }
                        # agrego listado al diccionario
                        dic_commits.append(data)

                # Busco los usuarios para el envío del correo de notificación de la ejecución.
                seguidores = self.env.ref('sicpro_app_administracion.grupo_app_administracion_notificaciones').users

                # verífico que el id_corto del registro no exista en el diccionario para archivarlo
                for id_corto in dic_commits:
                    dic_commit_id_corto.append(id_corto['commit_id_corto'])
                # realizo la comparación
                for item1 in todos_commits:
                    estado = item1.commit_id_corto in dic_commit_id_corto
                    if not estado:
                        item1.active = False
                        # actualizo la cantidad de registros archivados
                        registros_archivados += 1

                # voy a realizar la acción de crear o actualizar en dependencia del caso necesario
                for item in dic_commits:
                    # verífico que exista el commit en el registro sicpro
                    data = self.env['sicpro.modulo.api.conector.gitlab.commits'].sudo().search(
                        [('commit_id_corto', '=', item['commit_id_corto'])])

                    if data.commit_id_corto:
                        # actualizo registros de los commits desde el api gitlab
                        data.sudo().write({
                            'name': item['name'], 'branch_nombre': item['branch_nombre'],
                            'branch_web_url': item['branch_web_url'], 'commit_id_largo': item['commit_id_largo'],
                            'commit_creado': item['commit_creado'],
                            'commit_mensaje': item['commit_mensaje'], 'commit_autor': item['commit_autor'],
                            'commit_web_url': item['commit_web_url'], })
                        # actualizo la cantidad de registros actualizados
                        registros_actualizados += 1
                    else:
                        # creo los registros de los commits desde el api gitlab
                        self.env['sicpro.modulo.api.conector.gitlab.commits'].sudo().create({
                            'name': item['name'], 'branch_nombre': item['branch_nombre'],
                            'branch_web_url': item['branch_web_url'], 'commit_id_largo': item['commit_id_largo'],
                            'commit_creado': item['commit_creado'], 'commit_id_corto': item['commit_id_corto'],
                            'commit_mensaje': item['commit_mensaje'], 'commit_autor': item['commit_autor'],
                            'commit_web_url': item['commit_web_url'], })
                        # actualizo la cantidad de registros creados
                        registros_creados += 1

                # actualizo el historial de conexiones
                self.env['sicpro.modulo.api.conector.historial'].sudo().create(
                    {'name': 'APLICACIÓN GITLAB ETECSA', 'app_externa': app_id, 'fecha_inicio': fecha_inicio,
                     'fecha_fin': datetime.today(), 'registros_creados': registros_creados, 'estado': 'exito',
                     'registros_actualizados': registros_actualizados, 'registros_archivados': registros_archivados, })

                # envío el correo electrónico
                for participante in seguidores:
                    email_values = {'email_to': participante.email_formatted, }
                    local_context = self.env.context.copy()
                    template = self.env.ref('sicpro_modulo_api_conector_gitlab.gitlab_conector_rest_api_exito')
                    template.with_context(local_context).send_mail(app.id, force_send=True, email_values=email_values)
            else:
                print("No se ha configurado el servicio para la APLICACIÓN DE GITLAB ETECSA - app_id:gitlab, "
                      "no será ejecutado el cron: 'conector_api_cron_sicpro_api_gitlab' ")

        except gitlab.GitlabAuthenticationError as e:
            # actualizo el historial de conexiones
            self.env['sicpro.modulo.api.conector.historial'].sudo().create(
                {'name': 'APLICACIÓN GITLAB ETECSA', 'app_externa': app_id, 'fecha_inicio': fecha_inicio,
                 'fecha_fin': datetime.today(), 'registros_creados': 0, 'registros_actualizados': 0,
                 'registros_archivados': 0, 'estado': 'fallido', })

            # envío el correo electrónico
            for participante in seguidores:
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_modulo_api_conector_gitlab.gitlab_conector_rest_api_fallida')
                template.with_context(local_context).send_mail(app.id, force_send=True, email_values=email_values)