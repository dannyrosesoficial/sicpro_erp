# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)


class MediosInformaticosBajas(models.Model):
    _name = 'sicpro.app.medios.informaticos.bajas'
    _description = "Baja de Medios Informáticos"
    _inherit = ['mail.thread']

    name = fields.Many2one('sicpro.app.medios.informaticos.taller',
                           string='No. de Inventario', required=True,
                           domain="[('tique_cerrado', '=', False)]", )
    active = fields.Boolean(string='Activo', default=True, index=True)
    denominacion = fields.Text(string='Denominación del Equipo',
                               related='name.denominacion', store=True, )
    no_orden_mtto_taller = fields.Char(string='No. de Orden de Mantenimiento Taller',
                                       required=True, )
    dictamen_tec = fields.Char(string='Dictamen Técnico de SERTOD No. de Orden de Trabajo', required=True, )
    unidad_org = fields.Many2one('sicpro.app.trabajadores.areas',
                                 string='Unidad Organizativa',
                                 related='name.unidad_org', store=True, )
    fecha_ent_exp_economia = fields.Date(string='Fecha de Entrega del Expediente a Economía', )
    no_acta_acuerdo_consejo_dir = fields.Char(string='No. de Acta y Acuerdo del Consejo de Dirección', )
    fecha_acta_destino_final = fields.Date(string='Fecha del Acta de Destino Final', )
    acta_entrega_sertod = fields.Char(string='Acta de Entrega a SERTOD', )
    no_exp_economia = fields.Char(string='No. de Expediente de Economía', )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)

    def _enviar_notificaciones_generico(self, template_xmlid,
                                        mensaje_seguidores):
        """Método auxiliar centralizado para Odoo 19 usando user_ids"""
        template = self.env.ref(template_xmlid, raise_if_not_found=False)
        if not template:
            return

        # 1. Correo al usuario que ejecuta la acción
        if self.env.user.email:
            template.send_mail(self.id, force_send=True, email_values={
                'email_to': self.env.user.email_formatted})

        # 2. Correo a los responsables del grupo usando user_ids y exists()
        grupo_responsable = self.env.ref(
            'sicpro_app_medios_informaticos.grupo_app_medios_informaticos_responsable',
            raise_if_not_found=False)

        if grupo_responsable and grupo_responsable.exists():
            for responsable in grupo_responsable.user_ids:
                if responsable.email:
                    template.send_mail(self.id, force_send=True, email_values={
                        'email_to': responsable.email_formatted})

            # Registro en el chatter para seguidores
            self.message_post(body=mensaje_seguidores,
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

        # 3. Correo al responsable del equipo y su jefe
        # Accedemos a través de la relación: taller -> medio_informatico -> trabajador
        if self.name.name and self.name.name.trabajador_id:
            trabajador = self.name.name.trabajador_id
            if trabajador.correo_trabajo:
                template.send_mail(self.id, force_send=True, email_values={
                    'email_to': trabajador.correo_trabajo})
            if trabajador.parent_id and trabajador.parent_id.correo_trabajo:
                template.send_mail(self.id, force_send=True, email_values={
                    'email_to': trabajador.parent_id.correo_trabajo})

    def notificar_nuevo_registro(self):
        self._enviar_notificaciones_generico(
            'sicpro_app_medios_informaticos.medios_informaticos_baja',
            'Baja de medio informático registrada')

    @api.model_create_multi
    def create(self, vals_list):
        records = super(MediosInformaticosBajas, self).create(vals_list)

        for res in records:
            if res.name and res.name.name:
                # Localizamos el medio informático base y el registro de taller
                medio_id = res.name.name.id

                # Actualizamos el medio base: se archiva y cambia estado
                medio_informatico = self.env[
                    'sicpro.app.medios.informaticos'].browse(medio_id)
                if medio_informatico.exists():
                    medio_informatico.sudo().write(
                        {'archivado': True, 'active': False, 'estado': 'baja'})

                # El registro actual de taller se desactiva (ya es una baja definitiva)
                res.name.sudo().write({'active': False})

            # Disparamos notificaciones
            res.notificar_nuevo_registro()

        return records