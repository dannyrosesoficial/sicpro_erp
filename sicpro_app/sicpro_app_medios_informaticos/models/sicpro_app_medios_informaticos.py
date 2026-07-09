# -*- coding: utf-8 -*-

from odoo import models, fields


class MediosInformaticos(models.Model):
    _name = 'sicpro.app.medios.informaticos'
    _description = "Inventario Medios Informáticos"

    name = fields.Char('No. inventario', required=True)
    active = fields.Boolean('Activo', default=True)
    archivado = fields.Boolean('Archivado', default=False)
    estado = fields.Selection(selection=[('funcionando', 'Funcionando'), ('reserva', 'Reserva TI'),
                                         ('taller', 'En taller'), ('piezas', 'Pendiente por piezas'),
                                         ('proceso_baja', 'Proceso de baja'), ('baja', 'Baja')],
                              string='Estado', required=False, default='funcionando')
    fecha_archivado = fields.Date('Fecha de archivado')
    equipo = fields.Char('Equipo', required=True)
    tipo_equipo = fields.Many2one('sicpro.app.medios.informaticos.tipo.equipo', 'Tp.objeto', )
    denominacion = fields.Text('Denominación de objeto técnico', required=True)
    local = fields.Many2one('sicpro.nomenclador.locales', 'Local')
    centro_costo = fields.Many2one('sicpro.nomenclador.centro.costo', 'Ce.coste', related='local.centro_costo',
                                   store=True)
    are_id = fields.Many2one('sicpro.nomenclador.areas.empresa', 'ArE', related='centro_costo.area_empresa_id',
                             store=True)
    emplazamiento = fields.Many2one('sicpro.nomenclador.emplazamientos', 'Emplaz.')
    centro_planificacion = fields.Many2one('sicpro.nomenclador.centro.planificacion', 'CePl',
                                           related='emplazamiento.centro_planificacion', store=True)
    activo_fijo = fields.Char('Act.fijo', required=True)
    no_pieza_fab = fields.Char('No. pieza fabricante')
    responsable = fields.Char('Campo de clasificación', required=True)
    trabajador_id = fields.Many2one('sicpro.app.trabajadores', string='Trabajador')