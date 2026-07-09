# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models


class TransporteGeneral(models.Model):
    _name = 'sicpro.app.transporte.general'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Transporte'
    _order = 'matricula asc'

    def _get_default_state(self):
        return self.env['sicpro.app.transporte.estado'].search([], limit=1)

    transporte_id = fields.Many2one(
        comodel_name='sicpro.app.transporte.general', string='Transporte_id',
        required=False)
    company_id = fields.Many2one('res.company', 'Proceso',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    state_id = fields.Many2one('sicpro.app.transporte.estado', 'Estado',
                               default=_get_default_state,
                               group_expand='_read_group_stage_ids',
                               tracking=True,
                               help='Current state of the vehicle',
                               ondelete="set null")
    visual_fuerzas_medios = fields.Boolean(
        string="Visualizar Fuerzas y Medios", default=False)
    name = fields.Char(string='Nombre', tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True, index=True)

    unidadNombre = fields.Char(string='Unidad')
    unidadAcronimo = fields.Char(string='Acrónimo')

    areaNombre = fields.Char(string='Área')
    areaIdentificacion = fields.Char(string='Identificación')
    grupoEquipoNombre = fields.Char(string='Grupo')

    fechaRecibo = fields.Char(string='Fecha Recibido')
    annoFabricacion = fields.Char(string='Año Fabricación')

    tipoNombre = fields.Char(string='Tipo')
    marcaNombre = fields.Char(string='Marca')
    modeloNombre = fields.Char(string='Modelo')
    matricula = fields.Char(string='Matricula')
    color = fields.Char(string='color')

    especialidadNombre = fields.Char(string='Especialidad')
    actividadNombre = fields.Char(string='Actividad')
    actividadFundamentalNombre = fields.Char(string='Actividad Fund.')
    estadoTecnicoNombre = fields.Char(string='Estado Técnico')
    combustibleNombre = fields.Char(string='Combustible')

    choferNombre = fields.Char(string='Nombre Chofer')
    choferCi = fields.Char(string='Carnet ID Chofer')
    choferCargo = fields.Char(string='Cargo Chofer')
    choferDireccion = fields.Char(string='Dirección Chofer')
    choferLicencia = fields.Char(string='Licencia Chofer')
    choferEsChoferProfesional = fields.Char(string='Profecional Chofer')
    jefeChoferNombre = fields.Char(string='Nombre jefe')
    jefeChoferCi = fields.Char(string='Carnet ID Jefe')
    jefeChoferCargo = fields.Char(string='Cargo Jefe')
    jefeChoferDireccion = fields.Char(string='Dirección Jefe')
    jefeChoferLicencia = fields.Char(string='Licencia Jefe')
    jefeChoferEsChoferProfesional = fields.Char(string='Profecional Jefe')

    parqueoNombre = fields.Char(string='Nombre del parqueo')
    parqueoDireccion = fields.Char(string='Dirección de Parqueo')
    parqueoTipo = fields.Char(string='Tipo Parqueo')
    parqueoProvincia = fields.Char(string='Provincia')

    capacidadCargaNombre = fields.Char(string='Capacidad')
    codigoEquipo = fields.Char(string='Código')
    numeroCirculacion = fields.Char(string='No. Cirulación')
    numeroInventario = fields.Char(string='No. Inventario')

    vin = fields.Char(string='Vin')
    numeroSerie = fields.Char(string='No. Serie')
    numeroMotor = fields.Char(string='No. motor')
    marcaMotorNombre = fields.Char(string='Marca Motor')
    modeloMotorNombre = fields.Char(string='Modelo Motor')
    indiceConsumoNormado = fields.Char(string='IC Normado')
    indiceConsumoFabrica = fields.Char(string='IC Fabrica')

    tieneOdometro = fields.Char(string='Tiene Odometro')
    odometroOk = fields.Char(string='Estado Odometro')
    tieneHorametro = fields.Char(string='Tiene Horametro')
    horametroOk = fields.Char(string='Estado Horametro')

    esAlquilado = fields.Char(string='Alquilado')
    observacion = fields.Char(string='Observaciones')
    esParalizado = fields.Char(string='Paralizado')
    estaDefectuoso = fields.Char(string='Defectuoso')
    estaActivo = fields.Char(string='Activo')

    marca_id = fields.Many2one('sicpro.app.transporte.modelo',
                               'Marca del Vehículo')
    image_128 = fields.Image(related='marca_id.image_128', readonly=True)
    piquera = fields.Boolean(string='Servicio Piquera', required=False,
                             default=False)
    fecha_actualizado = fields.Datetime(string='Actualizado', required=False)
    chofer_trabajador_id = fields.Many2one(
        comodel_name='sicpro.app.trabajadores', string='Chofer Id')
    jefe_trabajador_id = fields.Many2one(
        comodel_name='sicpro.app.trabajadores', string='Jefe Id')
    piquera_count = fields.Integer(string='Piquera', compute='_compute_piquera_count')

    # Cuenta los servicios a piquera
    def _compute_piquera_count(self):
        for each in self:
            piquera_ids = self.env[
                'sicpro.app.transporte.piquera'].sudo().search(
                [('transporte_id', '=', each.id)])
            each.piquera_count = len(piquera_ids)

    # Abre la vista de piquera asociada al vehículo en el botón inteligente
    def action_piquera_view(self):
        self.ensure_one()
        domain = [('transporte_id', '=', self.id)]
        return {'name': 'Registros de la Piquera', 'domain': domain,
            'res_model': 'sicpro.app.transporte.piquera',
            'type': 'ir.actions.act_window', 'view_id': False,
            'view_mode': 'list,form',
            'help': '''<p class="oe_view_nocontent_create">Click para crear una nueva solicitud</p>''',
            'limit': 80, 'context': "{'default_transporte_id': %s}" % self.id}

    @api.onchange('marcaNombre')
    def _onchange_marcaNombre(self, ):
        if self.marcaNombre:
            marca = self.env['sicpro.app.transporte.modelo'].search(
                [('name', '=', self.marcaNombre)])
            self.marca_id = marca.id

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env['sicpro.app.transporte.estado'].search([],
                                                               order='id asc')
