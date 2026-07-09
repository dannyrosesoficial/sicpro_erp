# -*- coding: utf-8 -*-

from odoo import models, fields


class ApiConectorGitlabCommits(models.Model):
    _name = 'sicpro.modulo.api.conector.gitlab.commits'
    _description = "Registro de los commits del proyecto"
    _order = 'commit_creado desc'

    name = fields.Char(string='Commit', required=False)
    branch_nombre = fields.Char(string='Branch', required=False)
    branch_web_url = fields.Char(string='Url Branch', required=False)
    commit_id_largo = fields.Char(string='Commit ID Largo', required=False)
    commit_id_corto = fields.Char(string='Commit ID Corto', required=False)
    commit_creado = fields.Datetime(string='Creado', required=False)
    commit_mensaje = fields.Text(string='Mensaje', required=False)
    commit_autor = fields.Char(string='Autor', required=False)
    commit_web_url = fields.Char(string='Url Commit', required=False)
    active = fields.Boolean(string='Archivado', required=False, default=True)




