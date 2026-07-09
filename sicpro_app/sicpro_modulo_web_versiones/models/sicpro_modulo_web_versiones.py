# -*- coding: utf-8 -*-
import json

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SicproWebVersiones(models.Model):
    _name = 'sicpro.modulo.web.registro.versiones'
    _description = 'Detalles de las versiones del sistema'
    _order = "sequence, id desc"

    @api.model
    def _default_version(self):
        version_activo = self._context.get('version_id')
        return version_activo

    name = fields.Many2one(comodel_name='sicpro.modulo.web.registro.version', string='Versión', required=True,
                           default=_default_version)
    fecha_liberacion = fields.Date(string='Fecha Liberación', related='name.fecha_liberacion')
    aplicaciones_ids = fields.Many2many(comodel_name='sicpro.app.soporte.aplicaciones',
                                        relation='sicpro_app_soporte_versiones_web_rel', string='Aplicaciones',
                                        related='name.aplicaciones_ids')
    modulos_no_usados = fields.Char(compute="_modulos_no_usados", readonly=True, store=False,)
    modulo_nombre = fields.Many2one(comodel_name='sicpro.app.soporte.aplicaciones', string='Nombre del Módulo',
                                    required=True,)
    modulo_app = fields.Selection(string='Módulo o Aplicación', related='modulo_nombre.tipo')
    descripcion = fields.Html(string='Descripción', required=True)
    tickets_ids = fields.Html(string='Descripciones', required=False)
    sequence = fields.Integer('Secuencia', default=1, )
    active = fields.Boolean(string='Archivado', default=True)

    # verífico que no se repita el módulo o aplicación en la version
    @api.constrains('modulo_nombre')
    def _check_modulo_app_unico(self):
        uniq = self.env['sicpro.modulo.web.registro.versiones'].search(
            ['&', '&', ("active", "=", True), ("modulo_nombre", "=", self.modulo_nombre.name),
             ("name", "=", self.name.name.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El módulo o aplicación introducida ya existe para esta versión!. "
                                    "Si cree que es un error contacte al administrador"))

    # busco los módulos no registrados de la version
    @api.model
    @api.onchange('name', 'modulo_nombre')
    def _modulos_no_usados(self):
        for rec in self:
            ticket_ids = []
            ticket = self.env['sicpro.app.soporte'].search(
                ['&', '&', ("active", "=", True), ("version_id", "=", rec.name.name.name),
                 ("aplicaciones", "=", rec.modulo_nombre.name), ])

            if ticket:
                for value in ticket:
                    data = '<ul style="margin:0px 0 12px 0;box-sizing:border-box;line-height:inherit;' \
                           'font-weight:inherit;font-size:inherit;"><li style="box-sizing:border-box;' \
                           'line-height:inherit;font-weight:inherit;font-size:inherit;"><span ' \
                           'style="box-sizing:border-box;line-height:inherit;font-weight: bolder; font-size: 14px;">'\
                           + value.name + '</span></li></ul>'
                    ticket_ids.append(data)
            else:
                data = '<span style="font-weight: bolder; font-size: 20px;"><font style="color: rgb(156, 0, 0);">' \
                       'NO EXISTEN TICKETS RELACIONADOS</font></span><br>'
                ticket_ids.append(data)
            rec.tickets_ids = ticket_ids

            # módulos usados
            mod = self.env['sicpro.modulo.web.registro.versiones'].search(
                ['&', ("active", "=", True), ("name", "in", rec.name.name.name), ]).modulo_nombre.ids
            # todos los módulos
            domain = rec.name.aplicaciones_ids.ids
            # elimino los módulos ya usados
            for item in mod:
                domain.remove(item)
            # envío el json con el dominio creado
            rec.modulos_no_usados = json.dumps([('id', 'in', domain), ])


