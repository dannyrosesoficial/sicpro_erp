# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import UserError


class TrabajadoresDocumentos(models.Model):
    _name = 'sicpro.app.trabajadores.documentos'
    _description = 'Documentos de los trabajadores'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.constrains('fecha_expira')
    def check_expr_date(self):
        for each in self:
            if each.fecha_expira:
                exp_date = fields.Date.from_string(each.fecha_expira)
                if exp_date < fields.Date.context_today(self):
                    raise UserError(
                        'El documento a expirado.' + MSG_SOPORTE_SICPRO)

    name = fields.Char(string='Número Doc.', required=True, copy=False)
    descripcion = fields.Text(string='Descripción', copy=False)
    fecha_expira = fields.Date(string='Fecha Expiración', copy=False)
    trabajadores_id = fields.Many2one('sicpro.app.trabajadores', copy=False)
    fecha_agregado = fields.Date(string='Fecha Agregado',
                                 default=fields.Datetime.now, copy=False)
    tipo_documento = fields.Many2one(
        'sicpro.app.trabajadores.documentos.tipos', string="Tipo de Documento")
    active = fields.Boolean(string='Activo', default=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)

    # desactivo la certificación del trabajador y envío notificación y correo
    def send_expira_documento_mail(self):
        expira = fields.Datetime.now()
        trabajador = self.env['sicpro.app.trabajadores.documentos'].search(
            ['&', ('active', '=', True), ('fecha_expira', '=', expira)])
        if trabajador:
            for emp in trabajador:
                # busco el líder del grupo de atención al trabajador
                lider = emp.trabajadores_id.equipo_tecnico.lider.user_id
                # busco los técnicos que atienden al trabajador
                tecnicos = emp.trabajadores_id.tecnicos.user_id
                # busco los responsables de la aplicación de trabajadores
                group_responsables = self.env.ref(
                    'sicpro_app_trabajadores.grupo_app_trabajador_responsable',
                    raise_if_not_found=False)
                responsables = self.env['res.users']
                if group_responsables:
                    responsables = group_responsables.user_ids
                # creo la lista de seguidores
                seguidores = tecnicos + lider + responsables
                # agrego los seguidores al modelo
                emp.message_subscribe(partner_ids=seguidores.partner_id.ids)
                # envió la notificación a los seguidores
                emp.message_post(
                    body='Expiró una documentación del trabajador',
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                    author_id=self.env.user.partner_id.id)
                # desactivo el registro
                emp.active = False

                for participante in emp.message_partner_ids:
                    # envío el correo electrónico
                    participantes = participante.email_formatted
                    email_values = {'email_to': participantes}
                    template = self.env.ref(
                        'sicpro_app_trabajadores.trabajadores_documentacion_expira')
                    template.send_mail(emp.id, force_send=True,
                                       email_values=email_values, )
