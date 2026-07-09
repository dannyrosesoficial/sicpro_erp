# -*- coding: utf-8 -*-

from odoo import fields, models, api


class TransferenciasGastosImportar(models.Model):
    _name = 'sicpro.app.transferencias.gastos.importar'
    _description = "Sincronizar Transferencias de Gastos"
    _order = 'id asc'

    name = fields.Selection(selection=[('pendiente', 'Pendiente'), ('error', 'Error'), ], string='Estado',
                            required=False, )
    active = fields.Boolean('Activo', default=True)
    per = fields.Integer(string='Período', required=False)
    anio = fields.Char(string='Ejercicio', required=False)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses', string='Mes', required=False)
    fecha_contable = fields.Date(string='Fe.contabilización', required=False)
    fecha_doc = fields.Date(string='Fecha de documento', required=False)
    objeto = fields.Char(string='Objeto', required=False)
    denominacion_objeto = fields.Char(string='Denominación del objeto', required=False)
    valor_var = fields.Monetary(currency_field='company_currency', string='Valor variable/MonO', required=False)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id',
                                       readonly=True)
    monO = fields.Char(string='Moneda del objeto', required=False)
    cl_coste = fields.Char(string='Clase de coste', required=False)
    denom_cl_coste = fields.Char(string='Denom.clase de coste', required=False)
    cta_cp = fields.Char(string='Cta.contrapartida', required=False)
    denomctacp = fields.Char(string='Denominacion cuenta contrapartida', required=False)
    n_doc = fields.Char(string='Número de documento', required=False)
    n_doc_ref = fields.Char(string='Nº docum.refer.', required=False)
    denominacion = fields.Char(string='Denominación', required=False)
    usuario = fields.Char(string='Usuario', required=False)
    texto_cabecera_documento = fields.Char(string='Texto de cabecera de documento', required=False)
    material = fields.Char(string='Material', required=False)
    texto_breve_material = fields.Char(string='Texto breve de material', required=False)
    ud_cantidad_contab = fields.Char(string='Ud. cantidad contab.', required=False)
    cantidad_total_reg = fields.Char(string='Cantidad total reg.', required=False)
    orden = fields.Many2one(comodel_name='sicpro.app.ordenes.trabajo', string="Orden de Trabajo", required=False)

    @api.model
    def create(self, vals):
        res = super(TransferenciasGastosImportar, self).create(vals)
        # agregar la orden automáticamente
        orden = self.env['sicpro.app.ordenes.trabajo'].search([('name', '=', res['objeto'])])
        if orden:
            for value in orden:
                if value:
                    res['orden'] = value.id
                    res['name'] = 'pendiente'
        else:
            res['orden'] = None
            res['name'] = 'error'

        # agregar el mes automáticamente
        nombre_mes = self.env['sicpro.nomenclador.meses'].search([('codigo_mes', '=', res['per'])])
        res['mes'] = nombre_mes

        # # convertir el valor del gasto a float
        # if res['valor_var']:
        #     res['valor_var_compute'] = float(str(res['valor_var']))
        # else:
        #     res['valor_var_compute'] = None

        # Elimino los registro que no tengan mes (debe ser el último registro con el valor total de la cj74)
        if not res['per']:
            res.unlink()

        return res
