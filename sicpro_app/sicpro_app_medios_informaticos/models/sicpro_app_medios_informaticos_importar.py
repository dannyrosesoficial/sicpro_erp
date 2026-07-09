# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api


class MediosInformaticosImportar(models.Model):
    _name = 'sicpro.app.medios.informaticos.importar'
    _description = "Sincronizar Medios Informáticos"
    _order = 'id asc'

    def _default_tipo_equipo(self):
        return self.env['sicpro.app.medios.informaticos.tipo.equipo'].search([('name', '=', 'SIN DEFINIR')], limit=1).id

    name = fields.Selection(selection=[('actualizar', 'Actualizar'), ('nuevo', 'Nuevo')], string='Estado',
                            required=False)
    active = fields.Boolean(string='Activo', default=True, index=True)
    medio_informatico = fields.Char(string='No. inventario')
    equipo = fields.Char(string='Equipo')
    tipo_equipo = fields.Many2one('sicpro.app.medios.informaticos.tipo.equipo', 'Tp.objeto', )
    denominacion = fields.Text(string='Denominación de objeto técnico')
    local = fields.Many2one('sicpro.nomenclador.locales', string='Local')
    emplazamiento = fields.Many2one('sicpro.nomenclador.emplazamientos', string='Emplaz.')
    activo_fijo = fields.Char(string='Act.fijo', required=True)
    no_pieza_fab = fields.Char(string='No. pieza fabricante', default='')
    responsable = fields.Char(string='Campo de clasificación', required=True)
    trabajador_id = fields.Many2one('sicpro.app.trabajadores', string='Trabajador', )

    @api.model
    def create(self, vals):
        res = super(MediosInformaticosImportar, self).create(vals)

        medio_informatico = self.env['sicpro.app.medios.informaticos'].search([('name', '=', res['medio_informatico'])])
        if medio_informatico:
            for value in medio_informatico:
                if value:
                    res['name'] = 'actualizar'
        else:
            res['name'] = 'nuevo'

        if not res['tipo_equipo']:
            res['tipo_equipo'] = self._default_tipo_equipo()

        if res['responsable']:
            trabajadores = self.env['sicpro.app.trabajadores'].search([('active', '=', True)])
            for trabajador in trabajadores:
                if trabajador.correo_trabajo:
                    user = trabajador.correo_trabajo.split("@", 1)
                    user = user[0].upper()
                    if user == res.responsable:
                        res.trabajador_id = trabajador.id
        return res
