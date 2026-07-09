# -*- coding: utf-8 -*-


from odoo import fields, models, api


class Users(models.Model):
    _inherit = 'res.users'

    trabajador = fields.Many2one(comodel_name="sicpro.app.trabajadores.general",
                                 string="Trabajador", required=False, )
    departamento = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                   string="Area",
                                   related="trabajador.department_id",
                                   required=False, store=True)
    job_id = fields.Many2one('sicpro.app.trabajadores.trabajos',
                             'Puesto de trabajo', related="trabajador.job_id",
                             required=False, store=True)
    jefe_id = fields.Many2one('sicpro.app.trabajadores.general',
                              'Jefe Inmediato', related="trabajador.parent_id",
                              required=False, store=True)
    plaza_id = fields.Char(string="Número de Plaza",
                           related="trabajador.plaza_id", required=False,
                           store=True)
    identification_id = fields.Char(string='Carnet de identidad',
                                    related="trabajador.identification_id",
                                    required=False, store=True)
    notas = fields.Text('Notas', required=False)
    work_phone = fields.Char('Teléfono trabajo',
                             related="trabajador.work_phone", required=False,
                             store=True)
    mobile_phone = fields.Char('Móvil del trabajo',
                               related="trabajador.mobile_phone",
                               required=False, store=True)
    tipo = fields.Selection(string="Tipo", selection=[('interno', 'Interno'),
                                                      ('externo', 'Externo'), ],
                            required=True, default="interno")

    # bloqueo campo trabajadores si el usuario es externo
    @api.onchange('tipo')
    def _onchange_tipo(self, ):
        if self.tipo == 'externo':
            self.trabajador = None

    # agrega el id de usuario al trabajador
    @api.onchange('trabajador')
    def _onchange_trabajador(self,):
        if self.trabajador:
            # actualizo el id del usuario y el identificador
            usuario = self._origin.id
            data = self.env['sicpro.app.trabajadores.general'].search(
                [('id', '=', self.trabajador.id)])
            for item in data:
                item.user_id = usuario
                item.pin = self.company_id.identificador_corto + " - " + str(usuario)
