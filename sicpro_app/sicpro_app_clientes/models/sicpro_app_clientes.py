# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.tools import UserError


class AppClientes(models.Model):
    _name = 'sicpro.app.clientes'
    _order = "id asc"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _description = 'Aplicación de Clientes'

    name = fields.Char(required=True, string='Nombre', tracking=True, )
    es_entidad = fields.Boolean(string="es_entidad", )
    entidad = fields.Many2one(comodel_name="sicpro.app.clientes",
                              string="Entidad", required=False, )
    jefe_entidad = fields.Many2one(comodel_name='sicpro.app.clientes',
                                   string='Jefe Entidad', readonly=True)
    tipo_registro = fields.Selection(string="", selection=[
        ('persona', 'Persona'), ('entidad', 'Entidad'), ], default='entidad', )
    hijos_ids = fields.One2many("sicpro.app.clientes", "entidad",
                                string="Inversionistas")
    firma_acuerdo_servicio = fields.Boolean(string='Firma Acuerdo de Servicio',
                                            default=False, required=False)
    etiquetas = fields.Many2many(comodel_name="sicpro.app.clientes.etiquetas",
                                 string="Etiquetas", )
    territorio = fields.Many2one(comodel_name="sicpro.nomenclador.territorios",
                                 string="Territorio",
                                 required=True, tracking=True, )
    provincia = fields.Many2one(comodel_name="sicpro.nomenclador.provincia",
                                string="Provincia",
                                required=True, default="", tracking=True, )
    cargo = fields.Char(string="Cargo", required=False, tracking=True, )
    telefono_fijo = fields.Char(string="Teléfono", required=False,
                                tracking=True, )
    telefono_movil = fields.Char(string="Móvil", required=False,
                                 tracking=True, )
    correo = fields.Char(string="Correo electrónico", required=False,
                         tracking=True, )
    pagina_web = fields.Char(string="Pagína Web", required=False,
                             tracking=True, )
    observaciones = fields.Text(string="Observaciones", required=False, )
    active = fields.Boolean(string="Activo", default=True, tracking=True, )
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920",
                             max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920",
                             max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920",
                             max_width=128, max_height=128, store=True)
    user_id = fields.Many2one('res.users', 'Usuario', store=True,
                              readonly=False)
    pin = fields.Char(string="ID Usuario", help="Identificador del usuario.")
    id_user_cliente = fields.Integer(string="id usuario clientes")

    # verifico la existencia del jefe de la entidad
    @api.onchange('firma_acuerdo_servicio')
    def _onchange_firma_acuerdo_servicio(self):
        if self.firma_acuerdo_servicio:
            jefe = self.env['sicpro.app.clientes'].search(
                [('id', '=', self.entidad.id)])
            if jefe.jefe_entidad:
                self.firma_acuerdo_servicio = False
                raise UserError(
                    _('ERROR: La entidad ya tiene un jefe configurado.'))
            else:
                self.env['sicpro.app.clientes'].search(
                    [('id', '=', self.entidad.id)]).update(
                    {'jefe_entidad': self._origin.id})
        else:
            self.env['sicpro.app.clientes'].search(
                [('id', '=', self.entidad.id)]).update(
                {'jefe_entidad': False})

    # agrega el id de usuario al cliente y marca como cliente en el res.users
    @api.onchange('user_id')
    def _onchange_user_id(self, ):
        if self.user_id:
            self.env['res.users'].search([('id', '=', self.id_user_cliente)]). \
                update({'user_inversionista': False})
            self.env['res.users'].search([('id', '=', self.user_id.id)]). \
                update({'user_inversionista': True})
            self.id_user_cliente = self.user_id.id

            data = self.env['res.users'].search(
                [('id', '=', self.user_id.id), ])
            self.pin = data.company_id.identificador_corto + " - " + str(
                self.user_id.id)

    # Seleccionó entre entidad y persona
    @api.onchange('tipo_registro')
    def _onchange_tipo_registro(self):
        if self.tipo_registro == 'entidad':
            self.es_entidad = True
        else:
            self.es_entidad = False

    # devuelve nuevos valores a provincia cuando el territorio ha cambiado
    def _onchange_territorio_values(self, territorio):
        if territorio:
            partner = self.env['sicpro.nomenclador.territorios'].browse(
                territorio)
            return {'provincia': partner.provincia}
        return {}

    # Al cambiar campo territorio
    @api.onchange('territorio')
    def _onchange_territorio(self):
        values = self._onchange_territorio_values(
            self.territorio.id if self.territorio else False)
        self.update(values)

    @api.onchange('entidad')
    def _onchange_entidad(self):
        self.territorio = self.entidad.territorio
        self.provincia = self.entidad.provincia
