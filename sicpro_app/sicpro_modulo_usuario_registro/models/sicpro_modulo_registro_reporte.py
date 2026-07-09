# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class LoginUserReport(models.Model):
    _name = 'sicpro.modulo.registro.usuarios.reporte'
    _description = 'Reportes del Registro de usuarios'

    start_date = fields.Datetime(required=True, string="Fecha Inicial",
                                 default=fields.Datetime.now())
    end_date = fields.Datetime(required=True, string="Fecha Final",
                               default=fields.Datetime.now())
    type = fields.Selection(
        [('all', 'Todos los Usuarios'), ('selected', 'Seleccionar Usuario')],
        default='all', required=True, string="Tipo")
    user_id = fields.Many2many('res.users', string="Usuario")

    def gathering_user_details(self):
        user = self.env['res.users'].search([])
        users = []
        login_users = []
        for rec in user:
            users.append(rec.name)
        if self.type == 'all':
            records = self.env['sicpro.modulo.registro.usuarios'].search(
                [('name', 'in', users), ('date_time', '>=', self.start_date),
                 ('date_time', '<=', self.end_date)])
            for obj in records:
                data = {'name': obj.name, 'date_time': obj.date_time,
                    'ip_address': obj.ip_address,
                    'navegador_web': obj.navegador_web,
                    'sistema_operativo': obj.sistema_operativo,
                    'vpn': obj.vpn, }
                login_users.append(data)
            return login_users
        else:
            for rec in self.user_id:
                records = self.env['sicpro.modulo.registro.usuarios'].search(
                    [('name', '=', rec.name),
                     ('date_time', '>=', self.start_date),
                     ('date_time', '<=', self.end_date)])
                for obj in records:
                    data = {'name': obj.name, 'date_time': obj.date_time,
                        'ip_address': obj.ip_address,
                        'navegador_web': obj.navegador_web,
                        'sistema_operativo': obj.sistema_operativo,
                        'vpn': obj.vpn, }
                    login_users.append(data)
                return login_users

    def generar_reporte(self):
        return self.env.ref(
            'sicpro_modulo_usuario_registro.reporte_registro_usuario_report').report_action(
            [], )
