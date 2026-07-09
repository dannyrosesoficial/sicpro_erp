# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes
#    CONTACTO: daniel.borrero@etecsa.cu
##############################################################################

import logging
from random import randint
from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


_logger = logging.getLogger(__name__)


class GestorDocumentos(models.Model):
    _name = "sicpro.app.gestor.documental"
    _description = 'Gestor Documental'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence,id'
    _order = 'parent_id,sequence,id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    parent_path = fields.Char(index=True)
    active = fields.Boolean(default=True, index=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    name = fields.Char(string='Nombre', required=True, index=True)
    full_name = fields.Char(string='Nombre completo', compute='_compute_full_name',
                            store=True, recursive=True)
    description = fields.Char(string='Descripción')
    content = fields.Html(string='Contenido')

    parent_id = fields.Many2one('sicpro.app.gestor.documental', "Carpeta",
                                ondelete="cascade", index=True)
    parent_full_name = fields.Char(string="Directorio", related='parent_id.full_name')

    child_ids = fields.One2many('sicpro.app.gestor.documental', 'parent_id',
                                string='Elementos hijos')

    # Almacenado para que el Kanban pueda ordenar por cantidad de archivos
    child_count = fields.Integer(compute='_compute_child_count',
                                 string='Cantidad', store=True)

    @api.constrains('parent_id', 'name')
    def _check_unique_name_per_parent(self):
        for record in self:
            if record.name:
                name_clean = record.name.strip()
                domain = [('name', '=ilike', name_clean),
                          ('parent_id', '=', record.parent_id.id),
                          ('id', '!=', record.id)]
                if self.search_count(domain) > 0:
                    parent_name = record.parent_id.name or "el nivel raíz"
                    raise ValidationError(
                        f"Ya existe un registro con el nombre '{name_clean}' en '{parent_name}'.\n\n" + MSG_SOPORTE_SICPRO)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(
                "Error: No se puede asignar una carpeta como hija de sí misma.\n\n" + MSG_SOPORTE_SICPRO)

    @api.depends('child_ids')
    def _compute_child_count(self):
        for record in self:
            # search_count es eficiente con índices en parent_id
            record.child_count = len(record.child_ids)

    @api.depends('name', 'parent_id.full_name')
    def _compute_full_name(self):
        for record in self:
            if record.parent_id:
                record.full_name = f"{record.parent_id.full_name} / {record.name}"
            else:
                record.full_name = record.name

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=f"{self.name} (copia)")
        return super(GestorDocumentos, self).copy(default)

    def action_open_folder(self):
        """Acción para navegar dentro de una carpeta en el Kanban"""
        self.ensure_one()
        # Buscamos la acción principal del gestor documental
        action = self.env.ref(
            'sicpro_app_gestor_documental.documental_carpetas_view_action').read()[
            0]

        # Filtramos para que muestre los hijos de la carpeta actual
        action['domain'] = [('parent_id', '=', self.id)]

        # Seteamos el contexto para nuevos registros
        context = dict(self.env.context)
        context.update({'default_parent_id': self.id,
            'search_default_parent_id': self.id, })
        action['context'] = context
        action['name'] = self.name
        return action