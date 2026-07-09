# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
import logging
from random import randint
from datetime import datetime  # Importación vital para la fecha de publicación
from odoo import api, fields, models, SUPERUSER_ID, exceptions
from odoo.exceptions import UserError, ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO

def _default_color():
    return randint(1, 11)


_logger = logging.getLogger(__name__)


class RepositorioInstitucional(models.Model):
    _name = "sicpro.app.repo"
    _description = 'Repositorio Institucional'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence,id'
    _order = 'parent_id,sequence,id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # --- Valores por defecto ---
    def _get_default_stage_id(self):
        return self.env['sicpro.app.repo.estados'].search([], limit=1)

    # --- Campos Base y Jerarquía ---
    name = fields.Char(string='Título del Documento', required=True, tracking=True)
    doc_carpeta = fields.Selection(string='Carpeta o Documento', default='carpeta',
                                   selection=[('carpeta', 'Carpeta'), ('documento', 'Documento')], required=True)
    parent_path = fields.Char(index=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    full_name = fields.Char(string='Nombre completo', compute='_compute_full_name', store=True)
    description = fields.Char(string='Descripción de la carpeta')

    parent_id = fields.Many2one('sicpro.app.repo', "Carpeta", ondelete="cascade", index=True)
    parent_full_name = fields.Char(string="Directorio", related='parent_id.full_name')
    child_ids = fields.One2many('sicpro.app.repo', 'parent_id', string='Contenido')
    child_count = fields.Integer(compute='_compute_child_count', string='Cantidad', store=True)

    # --- Metadatos y Clasificación ---
    tipo = fields.Many2one('sicpro.app.repo.tipo', string='Tipo')
    autores_ids = fields.One2many('sicpro.app.repo.autores', 'repositorio_id', string='Autor(es)', tracking=True)
    resumen = fields.Text(string='Resumen')
    palabras_claves_ids = fields.Many2many('sicpro.app.repo.etiquetas', 'repo_etiqueta_rel', 'repositorio_id',
                                           'etiqueta_id', string='Palabras Clave')
    idioma_id = fields.Many2one('res.lang', string='Idioma')
    facultad_id = fields.Many2one('sicpro.app.repo.facultad', string='Facultad/Universidad')

    # --- Publicación y Tutoría ---
    tipo_tutor = fields.Selection([('interno', 'Interno'), ('externo', 'Externo'), ('ambos', 'Ambos')],
                                  string='Tipo de Tutor', default='interno')
    tutores_externos_ids = fields.One2many('sicpro.app.repo.tutor.externo', 'repositorio_id',
                                           string='Tutor(es) externos')
    tutores_internos_ids = fields.One2many('sicpro.app.repo.tutor.interno', 'repositorio_id',
                                           string='Tutor(es) internos')

    nombre_revista_libro = fields.Char(string='Nombre de la Revista/Libro')
    volumen = fields.Char(string='Volumen')
    numero = fields.Char(string='Número')
    paginas = fields.Char(string='Páginas')
    issn = fields.Char(string='ISSN/ISBN')
    identificador_objeto_digital = fields.Char(string='DOI', help='Identificador de Objeto Digital')

    # --- Archivos y Métricas ---
    attachment_ids = fields.Many2many('ir.attachment', 'repositorio_doc_rel', 'repositorio_id', 'attachment_id',
                                      string="Documentos")
    licencia_id = fields.Many2one('sicpro.app.repo.licencia', string='Licencia de Uso')
    download_count = fields.Integer(string='Total de Descargas', default=0, readonly=True, tracking=True)
    public_url = fields.Char(string='URL Pública', compute='_compute_public_url')

    # --- Flujo de Trabajo (Estados) ---
    fecha_publicacion = fields.Date(string='Fecha de Publicación', tracking=True)
    stage_id = fields.Many2one('sicpro.app.repo.estados', string='Estado', ondelete='restrict', tracking=True,
                               group_expand='_read_group_stage_ids', index=True, default=_get_default_stage_id)

    stage_id_is_inicial = fields.Boolean(related='stage_id.is_inicial')
    stage_id_is_revision = fields.Boolean(related='stage_id.is_revision')
    stage_id_is_won = fields.Boolean(related='stage_id.is_won')

    @api.constrains('name', 'parent_id')
    def _check_unique_name_per_parent(self):
        for record in self:
            domain = [('name', '=', record.name), ('parent_id', '=', record.parent_id.id),
                      ('id', 'not in', record.ids), ]

            if self.search(domain, limit=1):
                raise ValidationError(
                    "El nombre ya existe en esta carpeta o directorio. Los nombres deben ser únicos dentro de cada "
                    "nivel.\n\n" + MSG_SOPORTE_SICPRO)

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return stages.search([], order=order)

    @api.depends('child_ids', 'child_ids.active')
    def _compute_child_count(self):
        for record in self:
            record.child_count = self.search_count([('parent_id', '=', record.id)])

    def name_get(self):
        if self.env.context.get('display_full_name'):
            res = []
            for record in self:
                name = record.name
                p = record.parent_id
                while p:
                    name = f"{p.name} / {name}"
                    p = p.parent_id
                res.append((record.id, name))
            return res
        return super(RepositorioInstitucional, self).name_get()

    @api.depends('name', 'parent_id')
    def _compute_full_name(self):
        res_dict = dict(self.with_context({'display_full_name': True}).name_get())
        for record in self:
            record.full_name = res_dict.get(record.id, "")

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name="%s (copia)" % (self.name or ''))
        return super(RepositorioInstitucional, self).copy(default)

    def action(self):
        self.ensure_one()
        action_id = self.env.context.get('module_action_id')
        try:
            action_dict = self.env.ref(action_id).read()[0] if action_id else \
                self.env.ref('sicpro_app_repositorio_institucional.repositorio_institucional_carpetas_view_action').read()[0]
        except:
            return False
        action_dict["name"] = self.name
        new_ctx = dict(self.env.context)
        new_ctx.update({'default_parent_id': self.id, 'search_default_parent_id': self.id})
        action_dict['context'] = new_ctx
        return action_dict

    @api.depends('name')
    def _compute_public_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for item in self:
            item.public_url = f"{base_url}/repositorio/item/{item.id}" if item.id else False

    def action_liberar(self):
        self.ensure_one()
        if not self.autores_ids or not self.attachment_ids:
            raise exceptions.UserError("Debe especificar autores y un archivo digital.\n\n" + MSG_SOPORTE_SICPRO)
        estado = self.env['sicpro.app.repo.estados'].search([('is_revision', '=', True)], limit=1)
        if estado:
            self.stage_id = estado.id

    def action_revisado(self):
        self.ensure_one()
        estado = self.env['sicpro.app.repo.estados'].search([('is_won', '=', True)], limit=1)
        if estado:
            self.stage_id = estado.id
            self.fecha_publicacion = fields.Date.today()
            self.message_post(body="Documento publicado en el Repositorio.")

    def action_rechazada(self):
        self.ensure_one()
        estado = self.env['sicpro.app.repo.estados'].search([('is_inicial', '=', True)], limit=1)
        if estado:
            self.stage_id = estado.id


# Autores
class RepositorioInstitucionalAutores(models.Model):
    _name = 'sicpro.app.repo.autores'
    _order = "id asc"
    _description = 'Autores del repositorio'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Autor(es)', required=True,
                           tracking=True)
    user_id = fields.Many2one('res.users', related='name.user_id')
    user_partner_id = fields.Many2one(related_sudo=False, related='name.user_partner_id')
    autor_estudio_titulo = fields.Char(string="Nombre del Título", related='name.estudio_titulo')
    autor_ocupacion_titulo = fields.Many2one(comodel_name='sicpro.app.trabajadores.ocupacion', string="Cargo",
                                             related='name.ocupacion_titulo')
    autor_area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento', related='name.area_id')
    autor_company_id = fields.Many2one('res.company', string='Proceso', related='name.company_id')
    repositorio_id = fields.Many2one('sicpro.app.repo', 'Repositorio', required=False, index=True)

# Tutores externos
class RepositorioInstitucionalTutorExterno(models.Model):
    _name = 'sicpro.app.repo.tutor.externo'
    _order = "id asc"
    _description = 'Tutores Externos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tutor(es) Externo', required=True, tracking=True)
    tutor_nivel_escolar = fields.Selection(
        [('primaria', 'Primaria'), ('secundaria', 'Secundaria Básica'), ('sintitulo', 'Sin Título'),
         ('tecnico', 'Técnico Medio'), ('medio', 'Medio'), ('mediosuperior', 'Medio Superior'),
         ('superior', 'Superior'), ], 'Nivel Escolar', required=True, tracking=True)
    tutor_estudio_titulo = fields.Char(string="Nombre del Título", required=True, tracking=True)
    tutor_company_id = fields.Char(string='Institución', required=True, tracking=True)
    repositorio_id = fields.Many2one('sicpro.app.repo', 'Repositorio', required=False, index=True)

# Tutores internos
class RepositorioInstitucionalTutorInterno(models.Model):
    _name = 'sicpro.app.repo.tutor.interno'
    _order = "id asc"
    _description = 'Tutores Internos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Tutor(es) internos', required=True,
                           tracking=True)
    tutor_estudio_titulo = fields.Char(string="Nombre del Título", related='name.estudio_titulo')
    tutor_ocupacion_titulo = fields.Many2one(comodel_name='sicpro.app.trabajadores.ocupacion', string="Cargo",
                                             related='name.ocupacion_titulo')
    tutor_area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento', related='name.area_id')
    tutor_company_id = fields.Many2one('res.company', string='Proceso', related='name.company_id')
    repositorio_id = fields.Many2one('sicpro.app.repo', 'Repositorio', required=False, index=True)
