# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api


class TransferenciasGastosImportar(models.Model):
    _name = 'sicpro.app.transferencias.gastos.importar'
    _description = "Sincronizar Transferencias de Gastos"
    _order = 'id asc'

    name = fields.Selection(
        selection=[('pendiente', 'Pendiente'), ('error', 'Error'), ],
        string='Estado', required=False)
    active = fields.Boolean(string='Activo', default=True, index=True)
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
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Moneda',
                                       related='company_id.currency_id',
                                       readonly=True)
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
    orden = fields.Many2one(comodel_name='sicpro.app.ordenes.trabajo',
                            string="Orden de Trabajo", required=False)

    @api.model_create_multi
    def create(self, vals_list):
        if not vals_list:
            return self.env['sicpro.app.transferencias.gastos.importar']

        # 2. Recolectamos todos los 'objeto' y 'per' únicos
        lista_objetos = list(
            set(vals['objeto'] for vals in vals_list if vals.get('objeto')))
        lista_periodos = list(
            set(vals['per'] for vals in vals_list if vals.get('per')))

        # 3. Mapeamos las órdenes existentes
        ordenes_map = {}
        if lista_objetos:
            ordenes = self.env['sicpro.app.ordenes.trabajo'].search(
                [('name', 'in', lista_objetos)])
            ordenes_map = {ord_obj.name: ord_obj.id for ord_obj in ordenes}

        # 4. Mapeamos los meses
        meses_map = {}
        if lista_periodos:
            meses = self.env['sicpro.nomenclador.meses'].search(
                [('codigo_mes', 'in', lista_periodos)])
            meses_map = {mes.codigo_mes: mes.id for mes in meses}

        # 5. Inyectamos las relaciones
        for vals in vals_list:
            objeto = vals.get('objeto')
            if objeto and objeto in ordenes_map:
                vals['orden'] = ordenes_map[objeto]
                vals['name'] = 'pendiente'
            else:
                vals['orden'] = False
                vals['name'] = 'error'

            periodo = vals.get('per')
            if periodo in meses_map:
                vals['mes'] = meses_map[periodo]

        # 6. Insert masivo respetando la longitud original de vals_list
        return super(TransferenciasGastosImportar, self).create(vals_list)
