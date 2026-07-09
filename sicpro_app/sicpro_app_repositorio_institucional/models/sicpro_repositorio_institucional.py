# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from random import randint

from odoo import fields, models, api, exceptions, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


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

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.repo.estados'].search([], limit=1)

    name = fields.Char(string='Título del Documento', required=True, tracking=True)
    doc_carpeta = fields.Selection(string='Carpeta o Documento', default='carpeta',
                                   selection=[('carpeta', 'Carpeta'), ('documento', 'Documento'), ], required=True, )
    parent_path = fields.Char(index=True)
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=0)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    full_name = fields.Char('Nombre completo', compute='_compute_full_name')
    description = fields.Char('Descripción de la carpeta')
    parent_id = fields.Many2one('sicpro.app.repo', "Carpeta", ondelete="cascade", index=True)
    parent_full_name = fields.Char("Directorio", related='parent_id.full_name')
    child_ids = fields.One2many('sicpro.app.repo', 'parent_id', string='Crear Carpetas')
    child_count = fields.Integer(compute='_compute_child_count', string='Cantidad')

    # === CAMPOS DE IDENTIFICACIÓN Y METADATOS ===
    tipo = fields.Many2one(comodel_name='sicpro.app.repo.tipo', string='Tipo', required=False)
    autores_ids = fields.One2many(comodel_name='sicpro.app.repo.autores',
                                           inverse_name='repositorio_id', copy=False, string='Autor(es)',
                                           required=False, tracking=True)
    resumen = fields.Text(string='Resumen')
    palabras_claves_ids = fields.Many2many(comodel_name='sicpro.app.repo.etiquetas',
                                           relation='repo_etiqueta_rel', column1='repositorio_id',
                                           column2='etiqueta_id', string='Palabras Clave')
    idioma_id = fields.Many2one('res.lang', string='Idioma')

    # === CAMPOS DE FILIACIÓN Y PUBLICACIÓN ===
    facultad_id = fields.Many2one('sicpro.app.repo.facultad', string='Facultad/Universidad')
    tipo_tutor = fields.Selection(string='Tipo de Tutor',
        selection=[('interno', 'Interno'), ('externo', 'Externo'), ('ambos', 'Ambos'), ], required=False,
        default='interno')
    tutores_externos_ids = fields.One2many(comodel_name='sicpro.app.repo.tutor.externo',
                                           inverse_name='repositorio_id', copy=False, string='Tutor(es) externos',
                                           required=False, tracking=True)
    tutores_internos_ids = fields.One2many(comodel_name='sicpro.app.repo.tutor.interno',
                                           inverse_name='repositorio_id', copy=False, string='Tutor(es) internos',
                                           required=False, tracking=True)
    nombre_revista_libro = fields.Char(string='Nombre de la Revista/Libro')
    volumen = fields.Char(string='Volumen')
    numero = fields.Char(string='Número')
    paginas = fields.Char(string='Páginas')
    issn = fields.Char(string='ISSN/ISBN')
    identificador_objeto_digital = fields.Char(string='DOI', help='Identificador de Objeto Digital')

    # === ARCHIVO Y DERECHOS ===
    attachment_ids = fields.Many2many('ir.attachment', 'repositorio_doc_rel', 'repositorio_id',
                                      'attachment_id', string="Documentos")
    licencia_id = fields.Many2one('sicpro.app.repo.licencia', string='Licencia de Uso')

    # === FINANCIAMIENTO Y MÉTRICAS ===
    download_count = fields.Integer(string='Total de Descargas', default=0, readonly=True, tracking=True)

    # === FLUJO DE TRABAJO ===
    fecha_publicacion = fields.Date(string='Fecha de Publicación Original', required=False, tracking=True)
    stage_id = fields.Many2one('sicpro.app.repo.estados', string='Estados', ondelete='restrict',
                               tracking=True, group_expand='_read_group_stage_ids', index=True, copy=False,
                               default=_get_default_stage_id)
    stage_id_is_inicial = fields.Boolean(related='stage_id.is_inicial')
    stage_id_is_revision = fields.Boolean(related='stage_id.is_revision')
    stage_id_is_won = fields.Boolean(related='stage_id.is_won')

    # Campo Computado para la URL (Solo ejemplo, la URL real requiere un Controller)
    public_url = fields.Char(string='URL Pública', compute='_compute_public_url')

    @api.constrains('name', 'parent_id')
    def _check_unique_name_per_parent(self):
        for record in self:
            domain = [('name', '=', record.name), ('parent_id', '=', record.parent_id.id),
                      ('id', 'not in', record.ids), ]

            if self.search(domain, limit=1):
                raise ValidationError(
                    'El nombre ya existe en esta carpeta o directorio. Los nombres deben ser únicos dentro de cada '
                    'nivel. Si cree que es un error contacte al administrador')

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _compute_child_count(self):
        relative_field = self._fields.get("child_ids")
        comodel_name = relative_field.comodel_name
        inverse_name = relative_field.inverse_name
        count_data = self.env[comodel_name].read_group([(inverse_name, 'in', self.ids)], [inverse_name], [inverse_name])
        mapped_data = dict(
            [(count_item[inverse_name][0], count_item['%s_count' % inverse_name]) for count_item in count_data])
        for record in self:
            record.child_count = mapped_data.get(record.id, 0)

    def name_get(self):
        if self.env.context.get('display_full_name'):
            def get_names(record):
                res = []
                while record:
                    res.append(record.name or '')
                    record = record.parent_id
                return res

            return [(record.id, " / ".join(reversed(get_names(record)))) for record in self]

        # Comportamiento por defecto
        return super(RepositorioInstitucional, self).name_get()

    def _compute_full_name(self):
        res_dict = dict(self.with_context({'display_full_name': True}).name_get())
        for record in self:
            record.full_name = res_dict.get(record.id, "")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=_("%s (copy)") % (self.name or ''))
        return super(RepositorioInstitucional, self).copy(default)

    def action(self):
        self.ensure_one()
        context = self.env.context
        action_id = context.get('module_action_id')
        if action_id:
            action_dict = self.env.ref(action_id).read(["type", "res_model", "view_mode", "domain"])[0]
            action_dict["name"] = self.name
        return action_dict

    @api.depends('name')
    def _compute_public_url(self):
       base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
       for item in self:
           item.public_url = f"{base_url}/repossitorio/item/{item.id}" if item.id else False

    def action_liberar(self):
       self.ensure_one()
       if not self.autores_ids or not self.attachment_ids:
           raise exceptions.UserError("Debe especificar autores y un archivo digital.")
       estado = self.env['sicpro.app.repo.estados'].search([('is_revision', '=', True)]).id
       self.stage_id = estado

    def action_revisado(self):
       self.ensure_one()
       estado = self.env['sicpro.app.repo.estados'].search([('is_won', '=', True)]).id
       self.stage_id = estado
       self.fecha_publicacion = datetime.now()
       self.message_post(body="Documento publicado en el Repositorio.")

    def action_rechazada(self):
       self.ensure_one()
       estado = self.env['sicpro.app.repo.estados'].search([('is_inicial', '=', True)]).id
       self.stage_id = estado


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
    autor_estudio_titulo = fields.Char("Nombre del Título", related='name.estudio_titulo')
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
    tutor_estudio_titulo = fields.Char("Nombre del Título", required=True, tracking=True)
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
    tutor_estudio_titulo = fields.Char("Nombre del Título", related='name.estudio_titulo')
    tutor_ocupacion_titulo = fields.Many2one(comodel_name='sicpro.app.trabajadores.ocupacion', string="Cargo",
                                             related='name.ocupacion_titulo')
    tutor_area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento', related='name.area_id')
    tutor_company_id = fields.Many2one('res.company', string='Proceso', related='name.company_id')
    repositorio_id = fields.Many2one('sicpro.app.repo', 'Repositorio', required=False, index=True)
