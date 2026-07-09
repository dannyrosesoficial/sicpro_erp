# -*- coding: utf-8 -*-


from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression


class TransporteGeneral(models.Model):
    _name = 'sicpro.app.transporte.general'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Transporte'
    _order = 'license_plate asc, acquisition_date asc'

    @api.returns('self')
    def _get_default_state(self):
        return self.env['sicpro.app.transporte.estado'].search([], limit=1)

    name = fields.Char(compute="_compute_vehicle_name", store=True)
    active = fields.Boolean('Active', default=True, tracking=True)
    company_id = fields.Many2one('res.company', 'Proceso',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    license_plate = fields.Char(string="Matrícula", tracking=True,
                                help='License plate number of the vehicle (i = plate number for a car)')
    vin_sn = fields.Char('Número de bastidor',
                         help='Unique number written on the vehicle motor (VIN/SN number)',
                         copy=False)
    driver_id = fields.Many2one('sicpro.app.trabajadores.general', 'Chofer',
                                tracking=True,
                                help='Driver of the vehicle', copy=False)
    cargo_chofer = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.trabajos',
        string="Cargo del chofer", required=False, )
    jefe_chofer = fields.Many2one('sicpro.app.trabajadores.general',
                                  'Jefe del chofer', tracking=True, copy=False)
    cargo_jefe = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.trabajos',
        string="Cargo del jefe", required=False, )
    location = fields.Char(string="Área", help='Área del vehículo')
    future_driver_id = fields.Many2one(
        'sicpro.app.trabajadores.general', 'Próximo Chofer', tracking=True,
        help='Next Conductor of the vehicle', copy=False,
        domain="['|', ('company_id', '=', False), "
               "('company_id', '=', company_id)]")
    model_id = fields.Many2one('sicpro.app.transporte.modelo', 'Modelo',
                               tracking=True, required=True,
                               help='Model of the vehicle')
    clase = fields.Char(string="Clase", required=True, )
    manager_id = fields.Many2one('res.users', related='model_id.manager_id')
    brand_id = fields.Many2one('sicpro.app.transporte.modelo.brand', 'Brand',
                               related="model_id.brand_id", store=True,
                               readonly=False)
    log_drivers = fields.One2many('sicpro.app.transporte.historial',
                                  'vehicle_id', string='Assignation Logs')
    log_fuel = fields.One2many('sicpro.app.transporte.combustible',
                               'vehicle_id', 'Fuel Logs')
    log_services = fields.One2many('sicpro.app.transporte.servicios',
                                   'vehicle_id', 'Services Logs')
    log_contracts = fields.One2many('sicpro.app.transporte.contratos',
                                    'vehicle_id', 'Contrato')
    cost_count = fields.Integer(compute="_compute_count_all", string="Costes")
    contract_count = fields.Integer(compute="_compute_count_all",
                                    string='Contract Count')
    service_count = fields.Integer(compute="_compute_count_all",
                                   string='Servicios')
    fuel_logs_count = fields.Integer(compute="_compute_count_all",
                                     string='Fuel Log Count')
    odometer_count = fields.Integer(compute="_compute_count_all",
                                    string='Odómetro')
    history_count = fields.Integer(compute="_compute_count_all",
                                   string="Drivers History Count")
    next_assignation_date = fields.Date('Fecha de asignación',
                                        help='This is the date at which the car will be available, '
                                             'if not set it means available instantly')
    acquisition_date = fields.Date('Fecha de registro', required=False,
                                   default=fields.Date.today,
                                   help='Date when the vehicle has been immatriculated')
    first_contract_date = fields.Date(string="Primera fecha del contrato",
                                      default=fields.Date.today)
    color = fields.Char(help='Color of the vehicle')
    state_id = fields.Many2one('sicpro.app.transporte.estado', 'Estado',
                               default=_get_default_state,
                               group_expand='_read_group_stage_ids',
                               tracking=True,
                               help='Current state of the vehicle',
                               ondelete="set null")
    seats = fields.Integer('Nº de asientos',
                           help='Number of seats of the vehicle')
    model_year = fields.Char('Año del modelo',
                             help='Year of the model')
    doors = fields.Integer('Nº de puertas',
                           help='Number of doors of the vehicle', default=5)
    tag_ids = fields.Many2many('sicpro.app.transporte.etiqueta',
                               'sicpro_app_transporte_vehicle_tag_rel', 'vehicle_tag_id',
                               'tag_id', 'Etiquetas', copy=False)
    odometer = fields.Float(compute='_get_odometer', inverse='_set_odometer',
                            string='Último odómetro',
                            help='Odometer measure of the vehicle at the moment of this log')
    '''odometer_unit = fields.Selection([('kilometros', 'Kilómetros'), ('millas', 'Millas')], 'Unidad Odómetro',
                                     default='Kilómetros', help='Unit of the odometer ', required=True, )'''

    odometer_unit = fields.Selection([
        ('kilometers', 'Kilómetros'),
        ('millas', 'Millas')
    ], 'Odometer Unit', default='kilometers', help='Unit of the odometer ',
        required=True)

    transmission = fields.Selection(
        [('manual', 'Manual'), ('automatica', 'Automatica')], 'Transmisión',
        help='Transmission Used by the vehicle')
    indice_consumo_fabrica = fields.Float(string="Indice consumo fabrica",
                                          required=False, )
    indice_consumo_real = fields.Float('Indice consumo real', required=True, )
    power = fields.Integer('Potencia', help='Power in kW of the vehicle')
    co2 = fields.Float('Emisiones de CO2', help='CO2 emissions of the vehicle')
    image_128 = fields.Image(related='model_id.image_128', readonly=False)
    contract_renewal_due_soon = fields.Boolean(
        compute='_compute_contract_reminder',
        search='_search_contract_renewal_due_soon',
        string='Has Contracts to renew', multi='contract_info')
    contract_renewal_overdue = fields.Boolean(
        compute='_compute_contract_reminder',
        search='_search_get_overdue_contract_reminder',
        string='Has Contracts Overdue', multi='contract_info')
    contract_renewal_name = fields.Text(
        compute='_compute_contract_reminder',
        string='Name of contract to renew soon',
        multi='contract_info')
    contract_renewal_total = fields.Text(
        compute='_compute_contract_reminder',
        string='Total of contracts due or overdue minus one',
        multi='contract_info')
    car_value = fields.Float(string="Valor de compra",
                             help='Valor de compra del vehículo')
    rotulo = fields.Char(string="Rotulo", required=False, )
    circulacion = fields.Char(string="Circulación", required=True, )
    inventario = fields.Char(string="Inventario", required=False, )
    combustible = fields.Many2one(
        comodel_name="sicpro.app.transporte.tipo.combustible",
        string="Combustible",
        required=True, )
    actividad_fundamental = fields.Selection(
        string="Actividad Principal", required=True,
        selection=[('operacion', 'Operación'),
                   ('administrativa', 'Administrativa'), ])
    visual_fuerzas_medios = fields.Boolean(
        string="Visualizar Fuerzas y Medios",
        default=False, )
    notas = fields.Text('Notas')
    paqueo_tipo = fields.Selection(
        string="Tipo de Parqueo", selection=[('etecsa', 'ETECSA'),
                                             ('estatal', 'EMPRESA ESTATAL'),
                                             ('particular', 'PARTICULAR'),
                                             ('otros', 'Otros'), ],
        required=True, )
    parqueo_nombre = fields.Char(string="Nombre del Lugar", required=False, )
    parqueo_direccion = fields.Text(string="Dirección de Parqueo",
                                    required=False, )
    parqueo_observaciones = fields.Char(string="Observaciones",
                                        required=False, )
    denominacion = fields.Selection(
        string="Denominación", selection=[('especializado', 'Especializado'),
                                          ('no_especializado',
                                           'No Especializado'), ],
        required=True, )

    @api.onchange('driver_id')
    def _onchange_driver_id(self):
        self.cargo_chofer = self.driver_id.job_id
        self.jefe_chofer = self.driver_id.parent_id
        self.location = self.driver_id.department_id.name

    @api.onchange('jefe_chofer')
    def _onchange_jefe_chofer(self):
        self.cargo_jefe = self.jefe_chofer.job_id

    @api.onchange('model_id')
    def _onchange_model_id(self):
        if self.model_id:
            self.clase = self.model_id.clase_id.name

    @api.depends('model_id.brand_id.name', 'model_id.name', 'license_plate')
    def _compute_vehicle_name(self):
        for record in self:
            record.name = (record.model_id.brand_id.name or '') + '/' + \
                          (record.model_id.name or '') + '/' + (
                                  record.license_plate or _('No Plate'))

    def _get_odometer(self):
        FleetVehicalOdometer = self.env['sicpro.app.transporte.odometro']
        for record in self:
            vehicle_odometer = FleetVehicalOdometer.search(
                [('vehicle_id', '=', record.id)], limit=1, order='value desc')
            if vehicle_odometer:
                record.odometer = vehicle_odometer.value
            else:
                record.odometer = 0

    def _set_odometer(self):
        for record in self:
            if record.odometer:
                date = fields.Date.context_today(record)
                data = {'value': record.odometer, 'date': date,
                        'vehicle_id': record.id}
                self.env['sicpro.app.transporte.odometro'].create(data)

    def _compute_count_all(self):
        Odometer = self.env['sicpro.app.transporte.odometro']
        LogFuel = self.env['sicpro.app.transporte.combustible']
        LogService = self.env['sicpro.app.transporte.servicios']
        LogContract = self.env['sicpro.app.transporte.contratos']
        Cost = self.env['sicpro.app.transporte.costo']
        for record in self:
            record.odometer_count = Odometer.search_count(
                [('vehicle_id', '=', record.id)])
            record.fuel_logs_count = LogFuel.search_count(
                [('vehicle_id', '=', record.id)])
            record.service_count = LogService.search_count(
                [('vehicle_id', '=', record.id)])
            record.contract_count = LogContract.search_count(
                [('vehicle_id', '=', record.id), ('state', '!=', 'closed')])
            record.cost_count = Cost.search_count(
                [('vehicle_id', '=', record.id), ('parent_id', '=', False)])
            record.history_count = self.env[
                'sicpro.app.transporte.historial'].search_count(
                [('vehicle_id', '=', record.id)])

    @api.depends('log_contracts')
    def _compute_contract_reminder(self):
        params = self.env['ir.config_parameter'].sudo()
        delay_alert_contract = int(
            params.get_param('hr_fleet.delay_alert_contract', default=30))
        for record in self:
            overdue = False
            due_soon = False
            total = 0
            name = ''
            for element in record.log_contracts:
                if element.state in ('open', 'diesoon', 'expired') and \
                        element.expiration_date:
                    current_date_str = fields.Date.context_today(record)
                    due_time_str = element.expiration_date
                    current_date = fields.Date.from_string(current_date_str)
                    due_time = fields.Date.from_string(due_time_str)
                    diff_time = (due_time - current_date).days
                    if diff_time < 0:
                        overdue = True
                        total += 1
                    if diff_time < delay_alert_contract:
                        due_soon = True
                        total += 1
                    if overdue or due_soon:
                        log_contract = self.env[
                            'sicpro.app.transporte.contratos'].search([
                            ('vehicle_id', '=', record.id),
                            ('state', 'in', ('open', 'diesoon', 'expired'))
                        ], limit=1, order='expiration_date asc')
                        if log_contract:
                            # we display only the name of the oldest
                            # overdue/due soon contract
                            name = log_contract.cost_subtype_id.name

            record.contract_renewal_overdue = overdue
            record.contract_renewal_due_soon = due_soon
            record.contract_renewal_total = total - 1  # we remove 1 from the
            # real total for display purposes
            record.contract_renewal_name = name

    def _search_contract_renewal_due_soon(self, operator, value):
        params = self.env['ir.config_parameter'].sudo()
        delay_alert_contract = int(
            params.get_param('hr_fleet.delay_alert_contract', default=30))
        res = []
        assert operator in ('=', '!=', '<>') and value in (True, False), \
            'Operation not supported'
        if (operator == '=' and value is True) or (operator in ('<>', '!=') and
                                                   value is False):
            search_operator = 'in'
        else:
            search_operator = 'not in'
        today = fields.Date.context_today(self)
        datetime_today = fields.Datetime.from_string(today)
        limit_date = fields.Datetime.to_string(datetime_today + relativedelta(
            days=+delay_alert_contract))
        self.env.cr.execute("""SELECT cost.vehicle_id,
                        count(contract.id) AS contract_number
                        FROM fleet_vehicle_cost cost
                        LEFT JOIN fleet_vehicle_log_contract contract ON contract.cost_id = cost.id
                        WHERE contract.expiration_date IS NOT NULL
                          AND contract.expiration_date > %s
                          AND contract.expiration_date < %s
                          AND contract.state IN ('open', 'diesoon', 'expired')
                        GROUP BY cost.vehicle_id""", (today, limit_date))
        res_ids = [x[0] for x in self.env.cr.fetchall()]
        res.append(('id', search_operator, res_ids))
        return res

    def _search_get_overdue_contract_reminder(self, operator, value):
        res = []
        assert operator in ('=', '!=', '<>') and value in (True, False), \
            'Operation not supported'
        if (operator == '=' and value is True) or (operator in ('<>', '!=') and
                                                   value is False):
            search_operator = 'in'
        else:
            search_operator = 'not in'
        today = fields.Date.context_today(self)
        self.env.cr.execute('''SELECT cost.vehicle_id,
                        count(contract.id) AS contract_number
                        FROM fleet_vehicle_cost cost
                        LEFT JOIN fleet_vehicle_log_contract contract ON contract.cost_id = cost.id
                        WHERE contract.expiration_date IS NOT NULL
                          AND contract.expiration_date < %s
                          AND contract.state IN ('open', 'diesoon', 'expired')
                        GROUP BY cost.vehicle_id ''', (today,))
        res_ids = [x[0] for x in self.env.cr.fetchall()]
        res.append(('id', search_operator, res_ids))
        return res

    @api.model
    def create(self, vals):
        res = super(TransporteGeneral, self).create(vals)
        if 'driver_id' in vals and vals['driver_id']:
            res.create_driver_history(vals['driver_id'])
        return res

    def write(self, vals):
        if 'driver_id' in vals and vals['driver_id']:
            driver_id = vals['driver_id']
            self.filtered(
                lambda v: v.driver_id.id != driver_id).create_driver_history(
                driver_id)

        if 'future_driver_id' in vals and vals['future_driver_id']:
            pass

        res = super(TransporteGeneral, self).write(vals)
        if 'active' in vals and not vals['active']:
            self.mapped('log_contracts').write({'active': False})
        return res

    def _close_driver_history(self):
        self.env['sicpro.app.transporte.historial'].search([
            ('vehicle_id', 'in', self.ids),
            ('driver_id', 'in', self.mapped('driver_id').ids),
            ('date_end', '=', False)
        ]).write({'date_end': fields.Date.today()})

    def create_driver_history(self, driver_id):
        for vehicle in self:
            self.env['sicpro.app.transporte.historial'].create({
                'vehicle_id': vehicle.id,
                'driver_id': driver_id,
                'date_start': fields.Date.today(),
            })

    def action_accept_driver_change(self):
        vehicles = self.search(
            [('driver_id', 'in', self.mapped('future_driver_id').ids)])
        vehicles.write({'driver_id': False})
        vehicles._close_driver_history()

        for vehicle in self:
            vehicle.driver_id = vehicle.future_driver_id
            vehicle.future_driver_id = False
            self.cargo_chofer = self.driver_id.job_id
            self.jefe_chofer = self.driver_id.parent_id
            self.location = self.driver_id.department_id.name
            self.cargo_jefe = self.jefe_chofer.job_id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['sicpro.app.transporte.estado'].search([], order=order)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100,
                     name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name),
                      ('driver_id.name', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit,
                           access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

    def return_action_to_open(self):
        """ This opens the xml view specified in xml_id
         for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id(
                'sicpro_app_transporte', xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id,
                             group_by=False),
                domain=[('vehicle_id', '=', self.id)]
            )
            return res
        return False

    def act_show_log_cost(self):
        """ This opens log view to view and add new log for this vehicle,
        groupby default to only show effective costs
            @return: the costs log view
        """
        self.ensure_one()
        copy_context = dict(self.env.context)
        copy_context.pop('group_by', None)
        res = self.env['ir.actions.act_window'].for_xml_id(
            'sicpro_app_transporte', 'fleet_vehicle_costs_action')
        res.update(
            context=dict(copy_context, default_vehicle_id=self.id,
                         search_default_parent_false=True),
            domain=[('vehicle_id', '=', self.id)]
        )
        return res

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'driver_id' in init_values:
            return self.env.ref(
                'sicpro_app_transporte.mt_fleet_driver_updated')
        return super(TransporteGeneral, self)._track_subtype(init_values)

    def open_assignation_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assignation Logs',
            'view_mode': 'tree',
            'res_model': 'sicpro.app.transporte.historial',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_driver_id': self.driver_id.id,
                        'default_vehicle_id': self.id}
        }
