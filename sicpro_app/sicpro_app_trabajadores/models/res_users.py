# -*- coding: utf-8 -*-


from odoo import fields, models, api


class Users(models.Model):
    _inherit = 'res.users'

    trabajador = fields.Many2one(comodel_name="sicpro.app.trabajadores",
                                 string="Trabajador", required=False,
                                 domain="[('user_id', '=', False)]")
    departamento = fields.Many2one('sicpro.app.trabajadores.areas',
                                   string="Area", required=False,
                                   related="trabajador.area_id")
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                   'Puesto de trabajo', required=False,
                                   related="trabajador.ocupacion_id")
    jefe_id = fields.Many2one('sicpro.app.trabajadores', 'Jefe Inmediato',
                              required=False, related="trabajador.parent_id")
    plaza_id = fields.Char(string="Número de Plaza",
                           related="trabajador.plaza_id", required=False)
    identification_id = fields.Char(string='Carnet de identidad',
                                    related="trabajador.identification_id",
                                    required=False)
    notas = fields.Text('Notas', required=False)
    telefono_trabajo = fields.Char('Teléfono trabajo',
                                   related="trabajador.telefono_trabajo",
                                   required=False)
    movil_trabajo = fields.Char('Móvil del trabajo',
                                related="trabajador.telefono_trabajo",
                                required=False)
    tipo = fields.Selection(string="Tipo de usuario", required=True,
                            default="externo",
                            selection=[('interno', 'Interno'),
                                       ('externo', 'Externo'), ], )
    resume_line_ids = fields.One2many(related='trabajador.resume_line_ids',
                                      readonly=False)
    employee_skill_ids = fields.One2many(
        related='trabajador.employee_skill_ids', readonly=False)
    fecha_incorporacion = fields.Date(string="Fecha de Incorporación",
                                      related='trabajador.fecha_incorporacion',
                                      required=False)
    ubicacion_laboral = fields.Text(string="Ubicación Laboral",
                                    related='trabajador.ubicacion_laboral',
                                    required=False)
    inicio_contrato = fields.Date(string="Inicio del contrato",
                                  related='trabajador.inicio_contrato',
                                  required=False)
    bloquear = fields.Boolean(default=False)
    # protege las acciones sobre la selección de trabajadores
    seguridad = fields.Boolean(default=True)

    # agrega el id de usuario al trabajador
    @api.onchange('trabajador')
    def _onchange_trabajador(self, ):
        if not self.seguridad:
            usuario = self._origin.id
            data = self.env['sicpro.app.trabajadores'].search(
                [('user_id', '=', usuario)])
            for item in data:
                item.user_id = None
                item.pin = None

            if self.trabajador:
                self.bloquear = True
                # actualizo el id del usuario y el identificador
                data = self.env['sicpro.app.trabajadores'].search(
                    [('id', '=', self.trabajador.id)])
                for item in data:
                    item.user_id = usuario
                    item.pin = self.company_id.identificador_corto + " - " + str(
                        usuario)

    def liberar_trabajador(self, ):
        usuario = self._origin.id
        data = self.env['sicpro.app.trabajadores'].search(
            [('user_id', '=', usuario)])
        for item in data:
            item.user_id = None
            item.pin = None
        self.trabajador = None
        self.bloquear = False
        self.tipo = 'externo'

    @api.onchange('tipo')
    def _onchange_tipo(self, ):
        if not self.seguridad:
            if self.tipo == 'externo':
                self.liberar_trabajador()
