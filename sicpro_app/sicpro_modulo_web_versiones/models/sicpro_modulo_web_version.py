# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SicproWebVersion(models.Model):
    _name = 'sicpro.modulo.web.registro.version'
    _description = 'Versiones del sistema vinculadas con Soporte'
    _order = "sequence, id asc"

    name = fields.Many2one(comodel_name='sicpro.app.soporte.versiones', string='Versión', required=True,
                           domain="[('estado_final', '=', True)]", )
    fecha_liberacion = fields.Date(string='Fecha Liberación', required=True)
    active = fields.Boolean(default=True)
    paquetes_ids = fields.One2many(comodel_name='sicpro.app.soporte.paquetes', inverse_name='version_id',
                                   string='Paquetes Linux', related='name.paquetes_ids')
    aplicaciones_ids = fields.Many2many(comodel_name='sicpro.app.soporte.aplicaciones',
                                        relation='sicpro_app_soporte_versiones_web_rel', string='Aplicaciones',
                                        related='name.aplicaciones_ids')
    tickets_ids = fields.One2many(comodel_name='sicpro.app.soporte', inverse_name='version_id',
                                  string='Ticket de Soporte', related='name.tickets_ids')
    sequence = fields.Integer('Secuencia', default=1, )
    versiones_no_usados = fields.Char(compute="_versiones_no_usados", readonly=True, store=False, )

    @api.constrains('name')
    def _check_version_unico(self):
        uniq = self.env['sicpro.modulo.web.registro.version'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡La versión introducida ya existe!. "
                                    "Si cree que es un error contacte al administrador"))

    # llamar al action para buscar las tareas ejecutadas en la versión
    def action_tareas_versiones(self):
        version_activo = self._context.get('version_id')
        action = self.env['ir.actions.act_window']._for_xml_id('sicpro_modulo_web_versiones.web_versiones_action')
        action['domain'] = [('name', '=', version_activo), ('active', '=', True)]
        return action

    # busco las versiones no registrados
    @api.model
    @api.onchange('name')
    def _versiones_no_usados(self):
        for rec in self:
            # todas las versiones
            versiones_ids = []
            versiones = self.env['sicpro.app.soporte.versiones'].search(
                ['&', ("active", "=", True), ('estado_final', '=', True)])
            for value in versiones:
                data = value.id
                versiones_ids.append(data)

            # versiones usadas
            domain_ids = []
            domain = self.env['sicpro.modulo.web.registro.version'].search([("active", "=", True)])
            for values in domain:
                datas = values.name.id
                domain_ids.append(datas)

            # elimino las versiones ya usados
            for item in domain_ids:
                versiones_ids.remove(item)
            # envío el json con el dominio creado
            rec.versiones_no_usados = json.dumps([('id', 'in', versiones_ids), ])

    # organizar las secciones de las versiones
    def organizar_orden_versiones(self):
        list_ids = []
        versiones = self.env['sicpro.modulo.web.registro.version'].search([("active", "=", True)], order='sequence ASC')

        # creo la lista con los ids del registro de versiones
        for item in versiones:
            data = item.id
            list_ids.append(data)
        # half = len(list_ids)//2
        # lista_1 = list_ids[:half]
        # lista_2 = list_ids[half:]
        return list_ids

    # extrae datos de las versiones sector izquierdo
    def versiones_izq(self):
        # busco los ids del sector izquierdo
        lista_ids = self.organizar_orden_versiones()
        half = len(lista_ids) // 2
        lista_izq = lista_ids[:half]
        return lista_izq

    # extrae datos de las versiones sector izquierdo
    def versiones_der(self):
        # busco los ids del sector derecho
        lista_ids = self.organizar_orden_versiones()
        half = len(lista_ids) // 2
        lista_der = lista_ids[half:]
        return lista_der
