# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields, api


class MediosInformaticosPdtesPiezas(models.Model):
    _name = 'sicpro.app.medios.informaticos.pdtes.piezas'
    _description = "Medios Informáticos Pendiente por Piezas"
    _inherit = ['mail.thread']

    name = fields.Many2one('sicpro.app.medios.informaticos.taller',
                           string='No. de Inventario', required=True,
                           domain="[('tique_cerrado', '=', False)]", )
    active = fields.Boolean(string='Activo', default=True, index=True)
    equipo = fields.Char(string='Equipo', related='name.equipo', store=True, )
    no_orden = fields.Char(string='No. de Orden', required=True)
    no_tique = fields.Char(string='Tique', related='name.no_tique', store=True, )
    denominacion = fields.Text(string='Denominación del Equipo',
                               related='name.denominacion', store=True, )
    usuario_ant = fields.Many2one('sicpro.app.trabajadores',
                                  string='Usuario anterior', )
    pieza_orden_trabajo = fields.Char(string='Pieza en la orden del Trabajo', )
    observaciones_glpi = fields.Text(string='Observaciones GLPI', )
    area = fields.Many2one('sicpro.app.trabajadores.areas', string='Área',
                           related='name.unidad_org', store=True, )
    pieza_a_utilizar = fields.Char(string='Pieza a utilizar', )
    observaciones = fields.Text(string='Observaciones', )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)

    def _enviar_notificaciones_generico(self, template_xmlid,
                                        mensaje_seguidores):
        """Método auxiliar centralizado para Odoo 19 usando user_ids y exists()"""
        template = self.env.ref(template_xmlid, raise_if_not_found=False)
        if not template:
            return

        # 1. Correo al usuario que ejecuta la acción
        if self.env.user.email:
            template.send_mail(self.id, force_send=True, email_values={
                'email_to': self.env.user.email_formatted})

        # 2. Correo a los responsables del grupo usando user_ids (Corrección crítica)
        grupo_responsable = self.env.ref(
            'sicpro_app_medios_informaticos.grupo_app_medios_informaticos_responsable',
            raise_if_not_found=False)

        if grupo_responsable and grupo_responsable.exists():
            for responsable in grupo_responsable.user_ids:
                if responsable.email:
                    template.send_mail(self.id, force_send=True, email_values={
                        'email_to': responsable.email_formatted})

            # Notificación en el chatter para seguidores
            self.message_post(body=mensaje_seguidores,
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

        # 3. Correo al responsable del equipo y su jefe
        # Acceso: taller (name) -> medio_base (name) -> trabajador_id
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
            'sicpro_app_medios_informaticos.medios_informaticos_pdtes_piezas',
            'Medio informático pendiente por piezas')

    @api.model_create_multi
    def create(self, vals_list):
        """Creación optimizada para Odoo 19 con gestión de estados"""
        records = super(MediosInformaticosPdtesPiezas, self).create(vals_list)

        for res in records:
            if res.name and res.name.name:
                # Localizamos el medio informático base directamente por ID
                medio_id = res.name.name.id
                medio_informatico = self.env[
                    'sicpro.app.medios.informaticos'].browse(medio_id)

                if medio_informatico.exists():
                    medio_informatico.sudo().write({'estado': 'piezas'})

            # Disparamos notificaciones
            res.notificar_nuevo_registro()

        return records