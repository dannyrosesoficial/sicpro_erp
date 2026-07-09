# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models, api


class Users(models.Model):
    _inherit = 'res.users'

    user_inversionista = fields.Boolean(string="¿Es inversionista?")
    nombre_inversionista = fields.Many2one('sicpro.app.clientes',
                                           string='Nombre',
                                           domain="['&', ('es_entidad', '=', False), ('user_id', '=', False)]")
    nombre_inversionista_2 = fields.Many2one('sicpro.app.clientes',
                                             string='nombre_inversionista_2')
    inversionista_jefe_entidad = fields.Many2one(
        comodel_name='sicpro.app.clientes', string='Jefe Entidad', store=True,
        related='nombre_inversionista.jefe_entidad')
    inversionista_etiquetas = fields.Many2many(
        comodel_name="sicpro.app.clientes.etiquetas", string="Etiquetas",
        related='nombre_inversionista.etiquetas')
    inversionista_territorio = fields.Many2one(
        comodel_name="sicpro.nomenclador.territorios",
        string="Unidad Organizativa", store=True,
        related='nombre_inversionista.territorio')
    inversionista_provincia = fields.Many2one(comodel_name="res.country.state",
                                              string="Provincia", store=True,
                                              related='nombre_inversionista.provincias_id')
    inversionista_cargo = fields.Char(string="Cargo",
                                      related='nombre_inversionista.cargo')
    inversionista_telefono_fijo = fields.Char(string="Teléfono", store=True,
                                              related='nombre_inversionista.telefono_fijo')
    inversionista_telefono_movil = fields.Char(string="Móvil", store=True,
                                               related='nombre_inversionista.telefono_movil')
    inversionista_nivel_escolar = fields.Selection(
        string='Nivel Escolar Inversionista',
        related='nombre_inversionista.nivel_escolar')

    # agrega el id de usuario al cliente
    @api.onchange('nombre_inversionista')
    def _onchange_nombre_inversionista(self, ):
        usuario = self._origin.id
        if self.nombre_inversionista:
            # Elimino el registro existente del cliente al usuario
            data = self.env['sicpro.app.clientes'].search(
                [('id', '=', self.nombre_inversionista_2.id)])
            for item in data:
                item.user_id = None
                item.pin = None
            self.nombre_inversionista_2 = ''

            # creo nuevo registro del cliente al usuario
            self.nombre_inversionista_2 = self.nombre_inversionista
            self.user_inversionista = True
            # actualizo el, id del usuario y el identificador
            data = self.env['sicpro.app.clientes'].search(
                [('id', '=', self.nombre_inversionista.id)])
            for item in data:
                item.user_id = usuario
                item.pin = self.company_id.identificador_corto + " - " + str(
                    usuario)
        else:
            self.user_inversionista = False
            # actualizo el, id del usuario y el identificador
            data = self.env['sicpro.app.clientes'].search(
                [('id', '=', self.nombre_inversionista_2.id)])
            for item in data:
                item.user_id = None
                item.pin = None
            self.nombre_inversionista_2 = ''
