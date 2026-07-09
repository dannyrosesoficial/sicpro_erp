# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import api, fields, models, SUPERUSER_ID, _


class MetrologiaEquipos(models.Model):
    _name = 'sicpro.app.metrologia.equipos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipos de metrología'
    _check_company_auto = True

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'owner_user_id' in init_values and self.owner_user_id:
            return self.env.ref('sicpro_app_metrologia.mt_mat_assign')
        return super(MetrologiaEquipos, self)._track_subtype(init_values)

    def name_get(self):
        result = []
        for record in self:
            if record.name and record.serial_no:
                result.append(
                    (record.id, record.name + '/' + record.serial_no))
            if record.name and not record.serial_no:
                result.append((record.id, record.name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100,
                     name_get_uid=None):
        args = args or []
        equipment_ids = []
        if name:
            equipment_ids = self._search([('name', '=', name)] + args,
                                         limit=limit,
                                         access_rights_uid=name_get_uid)
        if not equipment_ids:
            equipment_ids = self._search([('name', operator, name)] + args,
                                         limit=limit,
                                         access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(
            equipment_ids).with_user(name_get_uid))

    maintenance_ids = fields.One2many(
        'sicpro.app.metrologia.solicitud.calibracion', 'equipment_id')
    maintenance_count = fields.Integer(compute='_compute_maintenance_count',
                                       string="Maintenance Count", store=True)
    maintenance_open_count = fields.Integer(
        compute='_compute_maintenance_count', string="Current Maintenance",
        store=True)
    maintenance_team_id = fields.Many2one('sicpro.app.metrologia.direcciones',
                                          string='Equipo del Proceso',
                                          check_company=True)
    name = fields.Char('Nombre del Equipo', required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('sicpro.app.metrologia.categoria',
                                  string='Categoría del equipo', tracking=True,
                                  group_expand='_read_group_category_ids',
                                  domain="[('company_id', '=', company_id)]")
    medicion = fields.Char(string="Limite de Medición", required=False,
                           tracking=True)
    presicion = fields.Char(string="Presición", required=False, tracking=True)
    marca = fields.Char(string="Marca", required=True, tracking=True)
    model = fields.Char(string="Modelo")
    pais_equipo = fields.Many2one('res.country', string="País del Equipo")
    unidad_medida = fields.Char(string="Unidad de Medida")
    serial_no = fields.Char('Nº de serie', copy=False)
    tipo = fields.Char(string="Tipo")
    magnitud = fields.Many2one(comodel_name="sicpro.app.metrologia.magnitud",
                               string="Magnitud", required=False, )
    area = fields.Char(string="Área", required=True, tracking=True)
    assign_date = fields.Date('Fecha de Alta', tracking=True)
    scrap_date = fields.Date('Fecha de Baja', tracking=True)
    inventario = fields.Char(string="Inventario", required=True, tracking=True)
    centro_costo = fields.Char(string="Centro de Costo", required=True,
                               tracking=True)
    inmovilizado = fields.Char(string="Inmovilizado", required=True,
                               tracking=True)
    local = fields.Char(string="Local", required=True, tracking=True)
    tarjeta = fields.Char(string="Tarjeta de control", tracking=True)
    tipo_control = fields.Char(string="Tipo Control")
    owner_user_id = fields.Many2one('sicpro.app.trabajadores.general',
                                    string='Trabajador', tracking=True)
    technician_user_id = fields.Many2one('res.users',
                                         string='Gestor de Equipos',
                                         tracking=True)
    centro_calibracion = fields.Many2one(
        comodel_name="sicpro.app.metrologia.centro.calibracion",
        string="Centro de Calibración",
        check_company=True, required=True, tracking=True, )
    estado_tecnico = fields.Many2one(
        comodel_name="sicpro.app.metrologia.estado.tecnico",
        string="Estado Técnico",
        required=True, tracking=True, )
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_1_1920 = fields.Image("Imagen anterior del equipo", max_width=1920,
                                max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1_1024 = fields.Image("Image 1024", related="image_1_1920",
                                max_width=1024, max_height=1024, store=True)
    image_1_512 = fields.Image("Image 512", related="image_1_1920",
                               max_width=512, max_height=512, store=True)
    image_1_256 = fields.Image("Image 256", related="image_1_1920",
                               max_width=256, max_height=256, store=True)
    image_1_128 = fields.Image("Image 128", related="image_1_1920",
                               max_width=128, max_height=128, store=True)
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_2_1920 = fields.Image("Imagen posterior del equipo",
                                max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_2_1024 = fields.Image("Image 1024", related="image_2_1920",
                                max_width=1024, max_height=1024, store=True)
    image_2_512 = fields.Image("Image 512", related="image_2_1920",
                               max_width=512, max_height=512, store=True)
    image_2_256 = fields.Image("Image 256", related="image_2_1920",
                               max_width=256, max_height=256, store=True)
    image_2_128 = fields.Image("Image 128", related="image_2_1920",
                               max_width=128, max_height=128, store=True)
    effective_date = fields.Date(
        'Fecha ultimo mantenimiento', default=fields.Date.context_today,
        required=True,
        help="Fecha de ultimo mantenimiento realizado al equipo.")
    next_action_date = fields.Date(compute='_compute_next_maintenance',
                                   string='Siguiente mantenimiento',
                                   store=True)
    period = fields.Integer('Frecuencia del mantenimiento en días')
    maintenance_duration = fields.Float(
        help="Duración del mantenimiento en horas.")
    color = fields.Integer('Índice de Colores')
    cost = fields.Float('Costo del equipo')
    note = fields.Text('Notas')
    warranty_date = fields.Date('Fecha Expiración Garantía')

    @api.depends('effective_date', 'period', 'maintenance_ids.request_date',
                 'maintenance_ids.close_date')
    def _compute_next_maintenance(self):
        date_now = fields.Date.context_today(self)
        equipments = self.filtered(lambda x: x.period > 0)
        for equipment in equipments:
            next_maintenance_todo = \
                self.env['sicpro.app.metrologia.solicitud.calibracion'].search(
                    [
                        ('equipment_id', '=', equipment.id),
                        ('maintenance_type', '=', 'preventive'),
                        ('stage_id.done', '!=', True),
                        ('close_date', '=', False)], order="request_date asc",
                    limit=1)
            last_maintenance_done = \
                self.env['sicpro.app.metrologia.solicitud.calibracion'].search(
                    [
                        ('equipment_id', '=', equipment.id),
                        ('maintenance_type', '=', 'preventive'),
                        ('stage_id.done', '=', True),
                        ('close_date', '!=', False)], order="close_date desc",
                    limit=1)
            if next_maintenance_todo and last_maintenance_done:
                next_date = next_maintenance_todo.request_date
                date_gap = next_maintenance_todo.request_date - \
                           last_maintenance_done.close_date

                if date_gap > timedelta(0) and date_gap > timedelta(
                        days=equipment.period) * 2 and \
                        next_maintenance_todo.request_date > date_now:
                    # If the new date still in the past, we set it for today
                    if last_maintenance_done.close_date + timedelta(
                            days=equipment.period) < date_now:
                        next_date = date_now
                    else:
                        next_date = last_maintenance_done.close_date + \
                                    timedelta(days=equipment.period)
            elif next_maintenance_todo:
                next_date = next_maintenance_todo.request_date
                date_gap = next_maintenance_todo.request_date - date_now

                if date_gap > timedelta(0) and date_gap > timedelta(
                        days=equipment.period) * 2:
                    next_date = date_now + timedelta(days=equipment.period)
            elif last_maintenance_done:
                next_date = last_maintenance_done.close_date + timedelta(
                    days=equipment.period)

                if next_date < date_now:
                    next_date = date_now
            else:
                next_date = self.effective_date + timedelta(
                    days=equipment.period)
            equipment.next_action_date = next_date
        (self - equipments).next_action_date = False

    @api.depends('maintenance_ids.stage_id.done')
    def _compute_maintenance_count(self):
        for equipment in self:
            equipment.maintenance_count = len(equipment.maintenance_ids)
            equipment.maintenance_open_count = len(
                equipment.maintenance_ids.filtered(
                    lambda x: not x.stage_id.done))

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.maintenance_team_id:
            if self.maintenance_team_id.company_id and not \
                    self.maintenance_team_id.company_id.id == \
                    self.company_id.id:
                self.maintenance_team_id = False
        if self.company_id and self.centro_calibracion:
            if self.centro_calibracion.company_id and not \
                    self.centro_calibracion.company_id.id == \
                    self.company_id.id:
                self.centro_calibracion = False

    @api.onchange('category_id')
    def _onchange_category_id(self):
        self.technician_user_id = self.category_id.technician_user_id

    @api.onchange('owner_user_id')
    def _onchange_owner_user_id(self):
        self.centro_costo = self.owner_user_id.centro_costo_usd
        self.local = self.owner_user_id.local.name
        self.area = self.owner_user_id.department_id.name

    _sql_constraints = [
        ('serial_no', 'unique(serial_no)',
         "Another asset already exists with this serial number!"),
    ]

    def write(self, vals):
        if vals.get('owner_user_id'):
            self.message_subscribe(partner_ids=self.env['res.users'].browse(
                vals['owner_user_id']).partner_id.ids)
        return super(MetrologiaEquipos, self).write(vals)

    @api.model
    def _read_group_category_ids(self, categories, domain, order):
        """ Read group customization in order to display all the categories in
            the kanban view, even if they are empty.
        """
        category_ids = categories._search([], order=order,
                                          access_rights_uid=SUPERUSER_ID)
        return categories.browse(category_ids)

    def _create_new_request(self, date):
        self.ensure_one()
        self.env['sicpro.app.metrologia.solicitud.calibracion'].create({
            'name': _('Mantenimiento Preventivo - %s') % self.name,
            'request_date': date,
            'schedule_date': date,
            'category_id': self.category_id.id,
            'equipment_id': self.id,
            'maintenance_type': 'preventive',
            'owner_user_id': self.owner_user_id.id,
            'user_id': self.technician_user_id.id,
            'maintenance_team_id': self.maintenance_team_id.id,
            'duration': self.maintenance_duration,
            'company_id': self.company_id.id or self.env.company.id
        })

    @api.model
    def _cron_generate_requests(self):
        """
            Generates maintenance request on the next_action_date or today
            if none exists
        """
        for equipment in self.search([('period', '>', 0)]):
            next_requests = \
                self.env['sicpro.app.metrologia.solicitud.calibracion'].search(
                    [('stage_id.done', '=', False),
                     ('equipment_id', '=', equipment.id),
                     ('maintenance_type', '=', 'preventive'),
                     ('request_date', '=', equipment.next_action_date)])
            if not next_requests:
                equipment._create_new_request(equipment.next_action_date)
