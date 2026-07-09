# -*- coding: utf-8 -*-


from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import pytz

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
                    raise Warning('El documento a expirado.')

    name = fields.Char(string='Número Doc.', required=True,
                       copy=False)
    descripcion = fields.Text(string='Descripción', copy=False)
    fecha_expira = fields.Date(string='Fecha Expiración', copy=False)
    trabajadores_id = fields.Many2one('sicpro.app.trabajadores', invisible=1,
                                      copy=False)
    doc_attachment_id = fields.Many2many(
        'ir.attachment', 'doc_attach_rel', 'doc_id', 'attach_id3',
        string="Adjunto", copy=False)
    fecha_agregado = fields.Date(string='Fecha Agregado',
                                 default=fields.datetime.now(), copy=False)
    tipo_documento = fields.Many2one('sicpro.app.trabajadores.documentos.tipos',
                                     string="Tipo de Documento")
    active = fields.Boolean('Activo', default=True)
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    fecha_agregado_formated = fields.Char(compute='_fecha_agregado_formated')
    fecha_expira_formated = fields.Char(compute='_fecha_expira_formated')

    def _fecha_agregado_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.fecha_agregado_formated = datetime.strftime(
                pytz.utc.localize(part.fecha_agregado).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    def _fecha_expira_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.fecha_expira_formated = datetime.strftime(
                pytz.utc.localize(part.fecha_expira).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    # desactivo la certificación del trabajador y envío notificación y correo
    def send_expira_documento_mail(self):
        date = str(datetime.now().date().strftime('%d/%m/%Y'))
        trabajador = self.env['sicpro.app.trabajadores.documentos'].search(
            ['&', ('active', '=', True), ('fecha_expira', '=', date)])
        if trabajador:
            for emp in trabajador:
                # busco el lider del grupo de atención al trabajador
                lider = emp.trabajadores_id.equipo_tecnico.lider.user_id
                # busco los técnicos que atienden al trabajador
                tecnicos = emp.trabajadores_id.tecnicos.user_id
                # busco los responsables de la aplicación de trabajadores
                responsables = self.env.ref(
                    'sicpro_app_trabajadores.grupo_app_trabajador_responsable').users
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
                # mantiene actualizado el correo de los seguidores del registro
                correos = ''
                for follower in emp.message_partner_ids:
                    correos = str(correos) + str(follower.email_formatted)
                emp.correo_seguidores = correos
                # envío el correo a los implicados
                template = self.env.ref(
                    'sicpro_app_trabajadores.trabajadores_documentacion_expira')
                template.send_mail(emp.id, force_send=True)
