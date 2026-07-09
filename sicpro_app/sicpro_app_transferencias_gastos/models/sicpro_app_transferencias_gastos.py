# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TransferenciasGastos(models.Model):
    _name = 'sicpro.app.transferencias.gastos'
    _description = "Transferencias de Gastos"
    _order = 'id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='sicpro.app.ordenes.trabajo',
                           string="Orden de Trabajo", required=True,
                           tracking=True, ondelete='restrict')
    active = fields.Boolean(string='Activo', default=True, tracking=True,
                            index=True)
    user_id = fields.Many2one('res.users', string='Solícita la Orden',
                              index=True, tracking=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True, related='name.company_id')
    company_currency = fields.Many2one("res.currency", string='Moneda',
                                       related='company_id.currency_id')
    company_abreviatura = fields.Char(string='Abreviatura', required=False,
                                      related='company_id.identificador_corto',
                                      store=True)

    # Se corrige la clave 'Validacion_inversionista' a minúsculas para mantener consistencia snake_case
    estado = fields.Selection(string='Estados', required=True, tracking=True,
                              index=True, copy=False, selection=[
            ('revision_economica', 'Revisión Económica'),
            ('revision_dtp', 'Revisión Técnico'),
            ('validacion_ejecutor', 'Validación Ejecutor'),
            ('rechazado_ejecutor', 'Rechazado Ejecutor'),
            ('validacion_inversionista', 'Validación Inversionista'),
            ('rechazado_inversionista', 'Rechazado Inversionista'),
            ('espera_contabilizar', 'En Espera por Contabilizar'),
            ('pendiente_contabilizar', 'Pendiente a Transferir'),
            ('contabilizado', 'Contabilizado'), ],
                              default='revision_economica')
    contabilizado = fields.Boolean(string='Contabilizado', required=False,
                                   default=False)
    gasto_id = fields.Many2one('sicpro.app.transferencias.gastos.ordenes',
                               'Orden', required=False, index=True)
    motivo_rechazo = fields.Text(string="Motivo del Rechazo", required=False,
                                 tracking=True)

    ############### CAMPOS CJ47## ######################################################################################
    per = fields.Integer(string='Período', required=False)
    anio = fields.Char(string='Ejercicio', required=False)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses',
                          string='Mes', required=False)
    fecha_contable = fields.Date(string='Fe.contabilización', required=False)
    fecha_doc = fields.Date(string='Fecha de documento', required=False)
    objeto = fields.Char(string='Objeto', required=False)
    denominacion_objeto = fields.Char(string='Denominación del objeto',
                                      required=False)
    valor_var = fields.Monetary(currency_field='company_currency',
                                string='Valor variable/MonO', required=False)
    monO = fields.Char(string='Moneda del objeto', required=False)
    cl_coste = fields.Char(string='Clase de coste', required=False)
    denom_cl_coste = fields.Char(string='Denom.clase de coste', required=False)
    cta_cp = fields.Char(string='Cta.contrapartida', required=False)
    denomctacp = fields.Char(string='Denominacion cuenta contrapartida',
                             required=False)
    n_doc = fields.Char(string='Número de documento', required=False)
    n_doc_ref = fields.Char(string='Nº docum.refer.', required=False)
    denominacion = fields.Char(string='Denominación', required=False)
    usuario = fields.Char(string='Usuario', required=False)
    texto_cabecera_documento = fields.Char(
        string='Texto de cabecera de documento', required=False)
    material = fields.Char(string='Material', required=False)
    texto_breve_material = fields.Char(string='Texto breve de material',
                                       required=False)
    ud_cantidad_contab = fields.Char(string='Ud. cantidad contab.',
                                     required=False)
    cantidad_total_reg = fields.Char(string='Cantidad total reg.',
                                     required=False)

    ####################################################################################################################
    ############### INVERSIONISTA ######################################################################################
    cliente_id = fields.Many2one('sicpro.app.clientes', string='Cliente',
                                 related='name.cliente_id', required=True)
    cliente_territorio_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.territorios", string="UO",
        related='cliente_id.territorio', required=False)
    cliente_provincia_id = fields.Many2one(comodel_name="res.country.state",
                                           string="Provincia Cliente",
                                           related='cliente_id.provincias_id',
                                           required=False)
    cliente_cargo = fields.Char(string="Cargo", related='cliente_id.cargo',
                                required=False)
    cliente_telefono_fijo = fields.Char(string="Teléfono",
                                        related='cliente_id.telefono_fijo',
                                        required=False)
    cliente_telefono_movil = fields.Char(string="Móvil",
                                         related='cliente_id.telefono_movil',
                                         required=False)
    cliente_correo = fields.Char(string="Correo electrónico",
                                 related='cliente_id.correo', required=False)

    ####################################################################################################################

    # btn sin función para mostrar el botón con el nombre del estado
    def btn_contabilizar_sin_funcion(self):
        l = 'l'
        return l

    # llamar al wizard para realizar ajuste de gastos
    def ajustar_gastos_cj74(self):
        self.ensure_one()
        # Se optimiza utilizando la función nativa de Odoo _for_xml_id en lugar de .read()[0]
        return self.env["ir.actions.actions"]._for_xml_id(
            'sicpro_app_transferencias_gastos.transferencias_ajustar_gastos_wizard_action')
