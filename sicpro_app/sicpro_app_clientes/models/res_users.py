# -*- coding: utf-8 -*-


from odoo import fields, models, api


class Users(models.Model):

    _inherit = 'res.users'

    user_inversionista = fields.Boolean("¿Es inversionista?")

    nombre_inversionista = fields.Many2one(
        'sicpro.app.clientes', string='Nombre',
        domain="['&', ('es_entidad', '=', False), ('user_id', '=', False)]")
    nombre_inversionista_2 = fields.Many2one('sicpro.app.clientes',
                                             string='nombre_inversionista_2')
    inversionista_jefe_entidad = fields.Many2one(comodel_name='sicpro.app.clientes',
                                   string='Jefe Entidad',
                                   related='nombre_inversionista.jefe_entidad')
    inversionista_etiquetas = fields.Many2many(comodel_name="sicpro.app.clientes.etiquetas",
                                 string="Etiquetas",
                                 related='nombre_inversionista.etiquetas')
    inversionista_territorio = fields.Many2one(comodel_name="sicpro.nomenclador.territorios",
                                 string="Territorio",
                                 related='nombre_inversionista.territorio' )
    inversionista_provincia = fields.Many2one(comodel_name="sicpro.nomenclador.provincia",
                                string="Provincia",
                                related='nombre_inversionista.provincia')
    inversionista_cargo = fields.Char(string="Cargo", related='nombre_inversionista.cargo' )
    inversionista_telefono_fijo = fields.Char(string="Teléfono",
                                related='nombre_inversionista.telefono_fijo')
    inversionista_telefono_movil = fields.Char(string="Móvil",
                                 related='nombre_inversionista.telefono_movil')

    # agrega el id de usuario al cliente
    @api.onchange('nombre_inversionista')
    def _onchange_nombre_inversionista(self, ):
        usuario = self._origin.id
        if self.nombre_inversionista:
            # elimino el registro existente del cliente al usuario
            data = self.env['sicpro.app.clientes'].search(
                [('id', '=', self.nombre_inversionista_2.id)])
            for item in data:
                item.user_id = None
                item.pin = None
            self.nombre_inversionista_2 = ''

            # creo nuevo registro del cliente al usuario
            self.nombre_inversionista_2 = self.nombre_inversionista
            self.user_inversionista = True
            # actualizo el id del usuario y el identificador
            data = self.env['sicpro.app.clientes'].search(
                [('id', '=', self.nombre_inversionista.id)])
            for item in data:
                item.user_id = usuario
                item.pin = self.company_id.identificador_corto + " - " + str(
                    usuario)
        else:
            self.user_inversionista = False
            # actualizo el id del usuario y el identificador
            data = self.env['sicpro.app.clientes'].search(
                [('id', '=', self.nombre_inversionista_2.id)])
            for item in data:
                item.user_id = None
                item.pin = None
            self.nombre_inversionista_2 = ''