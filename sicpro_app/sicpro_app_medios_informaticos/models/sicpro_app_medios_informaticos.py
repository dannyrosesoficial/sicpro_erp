# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class MediosInformaticos(models.Model):
    _name = 'sicpro.app.medios.informaticos'
    _description = "Inventario Medios Informáticos"

    name = fields.Char(string='No. inventario', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    archivado = fields.Boolean(string='Archivado', default=False)
    estado = fields.Selection(
        selection=[('funcionando', 'Funcionando'), ('reserva', 'Reserva TI'),
                   ('taller', 'En taller'), ('piezas', 'Pendiente por piezas'),
                   ('proceso_baja', 'Proceso de baja'), ('baja', 'Baja')],
        string='Estado', required=False, default='funcionando')
    fecha_archivado = fields.Date(string='Fecha de archivado')
    equipo = fields.Char(string='Equipo', required=True)
    tipo_equipo = fields.Many2one('sicpro.app.medios.informaticos.tipo.equipo',
                                  string='Tp.objeto', )
    denominacion = fields.Text(string='Denominación de objeto técnico', required=True)
    local = fields.Many2one('sicpro.nomenclador.locales', string='Local')
    centro_costo = fields.Many2one('sicpro.nomenclador.centro.costo',
                                   string='Ce.coste', related='local.centro_costo',
                                   store=True)
    are_id = fields.Many2one('sicpro.nomenclador.areas.empresa', string='ArE',
                             related='centro_costo.area_empresa_id',
                             store=True)
    emplazamiento = fields.Many2one('sicpro.nomenclador.emplazamientos',
                                    string='Emplaz.')
    centro_planificacion = fields.Many2one(
        'sicpro.nomenclador.centro.planificacion', string='CePl',
        related='emplazamiento.centro_planificacion', store=True)
    activo_fijo = fields.Char(string='Act.fijo', required=True)
    no_pieza_fab = fields.Char(string='No. pieza fabricante')
    responsable = fields.Char(string='Campo de clasificación', required=True)
    trabajador_id = fields.Many2one('sicpro.app.trabajadores',
                                    string='Trabajador')
