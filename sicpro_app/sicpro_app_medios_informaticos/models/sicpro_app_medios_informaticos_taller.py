# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import date
from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import UserError


class MediosInformaticosTaller(models.Model):
    _name = 'sicpro.app.medios.informaticos.taller'
    _description = "Medios Informáticos Enviados a Taller"
    _inherit = ['mail.thread']

    name = fields.Many2one('sicpro.app.medios.informaticos',
                           string='No. Inventario', )
    no_tique = fields.Char(string='Tique', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    fecha_entrada = fields.Date(string='Fecha de Entrada', required=True)
    fecha_recogida = fields.Date(string='Fecha Recogida', )
    responsable = fields.Char(string='Responsable en PM', related='name.responsable',
                              store=True, )
    equipo = fields.Char(string='Equipo', related='name.equipo', store=True, )
    denominacion = fields.Text(string='Denominación de objeto técnico',
                               related='name.denominacion', store=True, )
    unidad_org = fields.Many2one('sicpro.app.trabajadores.areas',
                                 string='Unidad Organizativa', required=True)
    tramite = fields.Many2one('sicpro.app.medios.informaticos.tramites',
                              string='Trámite')
    dictamen_tec = fields.Char(string='Dictamen Técnico', )
    no_orden_taller = fields.Char(string='No. Orden Taller')
    tique_cerrado = fields.Boolean(string='Tique cerrado')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)

    def _enviar_notificaciones_generico(self, template_xmlid,
                                        mensaje_seguidores):
        """Método auxiliar para centralizar el envío de correos y evitar duplicar código"""
        template = self.env.ref(template_xmlid, raise_if_not_found=False)
        if not template:
            return

        # 1. Correo al usuario que ejecuta la acción
        if self.env.user.email:
            template.send_mail(self.id, force_send=True, email_values={
                'email_to': self.env.user.email_formatted})

        # 2. Correo a los responsables del grupo (Corrección del AttributeError)
        grupo_responsable = self.env.ref(
            'sicpro_app_medios_informaticos.grupo_app_medios_informaticos_responsable',
            raise_if_not_found=False)
        if grupo_responsable:
            for responsable in grupo_responsable.user_ids:
                if responsable.email:
                    template.send_mail(self.id, force_send=True, email_values={
                        'email_to': responsable.email_formatted})

            # Notificación en el chatter para seguidores
            self.message_post(body=mensaje_seguidores,
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

        # 3. Correo al responsable del equipo y su jefe
        if self.name.trabajador_id:
            trabajador = self.name.trabajador_id
            # Al trabajador
            if trabajador.correo_trabajo:
                template.send_mail(self.id, force_send=True, email_values={
                    'email_to': trabajador.correo_trabajo})
            # Al jefe
            if trabajador.parent_id and trabajador.parent_id.correo_trabajo:
                template.send_mail(self.id, force_send=True, email_values={
                    'email_to': trabajador.parent_id.correo_trabajo})

    def notificar_nuevo_registro(self):
        self._enviar_notificaciones_generico(
            'sicpro_app_medios_informaticos.medios_informaticos_envio_taller',
            'Nuevo envío a taller registrado')

    @api.model_create_multi
    def create(self, vals_list):
        # Odoo 19 utiliza api.model_create_multi por defecto para optimización
        records = super(MediosInformaticosTaller, self).create(vals_list)
        for res in records:
            if res.name:
                res.name.sudo().write({'estado': 'taller'})
            res.notificar_nuevo_registro()
        return records

    def cerrar_tique(self):
        self.ensure_one()
        if self.name:
            self.name.estado = 'funcionando'
        self.tique_cerrado = True

        self._enviar_notificaciones_generico(
            'sicpro_app_medios_informaticos.medios_informaticos_cerrar_tique',
            'Se ha cerrado el tique de taller')

    @api.constrains('fecha_recogida', 'fecha_entrada')
    def _check_fechas_taller(self):
        today = date.today()
        for record in self:
            if record.fecha_entrada and record.fecha_entrada > today:
                raise UserError(
                    "La fecha de entrada no puede ser mayor al día de hoy.\n\n" + MSG_SOPORTE_SICPRO)

            if record.fecha_recogida and record.fecha_entrada:
                if record.fecha_recogida < record.fecha_entrada:
                    raise UserError(
                        "La fecha de recogida no puede ser menor que la fecha de entrada.\n\n" + MSG_SOPORTE_SICPRO)