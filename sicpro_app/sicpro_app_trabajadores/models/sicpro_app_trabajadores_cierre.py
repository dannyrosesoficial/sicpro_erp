# -*- coding: utf-8 -*-

from odoo import models, fields


class TrabajadoresCierre(models.Model):
    _name = 'sicpro.app.trabajadores.cierre'
    _description = "Cierres mensuales de Capital Humano"
    _inherit = ['mail.thread']
    _order = "codigo_mes desc, name asc"

    name = fields.Many2one('sicpro.app.trabajadores.areas', string='Área')
    direccion = fields.Many2one('res.company', string='Proceso', related='name.company_id', store=True, )
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses', string='Mes', )
    codigo_mes = fields.Integer(string="Código Mes", related='mes.codigo_mes', )
    anio = fields.Char(string='Año', default=fields.Datetime.now().strftime("%Y"))
    total = fields.Integer('Total de trabajadores', )
    altas = fields.Integer('Cantidad de altas', )
    bajas = fields.Integer('Cantidad de bajas', )
    active = fields.Boolean('Activo', default=True)
    estado = fields.Selection(selection=[('ok', 'Correcto'), ('error', 'Error')], string='Estado', default='ok')
    company_id = fields.Many2one('res.company', string='Procesos', required=True, default=lambda self: self.env.company)

    def notificar_nuevo_cierre(self):
        # Lista de correo de los trabajadores a notificar
        list_trabajadores = self.env['sicpro.app.trabajadores.notificacion.cierre'].search([('active', '=', True)])
        for trabajador in list_trabajadores:
            # Envío del correo 
            email_values = {'email_to': trabajador.name.correo_trabajo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_trabajadores.trabajadores_cierre')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envío de la notificación 
            self.message_notify(body='Nuevo envío a taller', subtype_xmlid='mail.mt_comment',
                                author_id=self.env.user.partner_id.id)

        # Lista de correo de los tecnicos
        list_tecnicos = self.env.ref('sicpro_app_trabajadores.grupo_app_trabajador_ejecutor').users
        for tecnico in list_tecnicos:
            # Envío del correo
            email_values = {'email_to': tecnico.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_trabajadores.trabajadores_cierre')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envío de la notificación
            self.message_notify(body='Nuevo envío a taller', subtype_xmlid='mail.mt_comment',
                                author_id=self.env.user.partner_id.id)

        # Lista de correo de los responsables
        list_responsable = self.env.ref('sicpro_app_trabajadores.grupo_app_trabajador_responsable').users
        for responsable in list_responsable:
            # envío del correo 
            email_values = {'email_to': responsable.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_trabajadores.trabajadores_cierre')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envío de la notificación
            self.message_notify(body='Nuevo envío a taller', subtype_xmlid='mail.mt_comment',
                                author_id=self.env.user.partner_id.id)
