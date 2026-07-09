# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class MetrologiaSolicitudCalibracion(models.Model):
    _name = 'sicpro.app.metrologia.solicitud.calibracion'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'Solicitud de mantenimiento'
    _order = "id desc"
    _check_company_auto = True

    @api.returns('self')
    def _default_stage(self):
        return self.env['sicpro.app.metrologia.estado'].search([], limit=1)

    def _creation_subtype(self):
        return self.env.ref('sicpro_app_metrologia.mt_req_created')

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'stage_id' in init_values:
            return self.env.ref('sicpro_app_metrologia.mt_req_status')
        return super(MetrologiaSolicitudCalibracion, self)._track_subtype(
            init_values)

    def _get_default_team_id(self):
        MT = self.env['sicpro.app.metrologia.direcciones']
        team = MT.search([('company_id', '=', self.env.company.id)], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id

    name = fields.Char('Subjects', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    description = fields.Text('Description')
    request_date = fields.Date(
        'Fecha de solicitud', tracking=True, default=fields.Date.context_today,
        help="Date requested for the maintenance to happen")
    owner_user_id = fields.Many2one('res.users', string='Created by User',
                                    default=lambda s: s.env.uid)
    category_id = fields.Many2one('sicpro.app.metrologia.categoria',
                                  related='equipment_id.category_id',
                                  string='Categoría del equipo',
                                  store=True, readonly=True)
    equipment_id = fields.Many2one('sicpro.app.metrologia.equipos',
                                   string='Equipamiento',
                                   ondelete='restrict', index=True,
                                   check_company=True)
    user_id = fields.Many2one('res.users', string='Gestor de Equipos',
                              tracking=True)
    stage_id = fields.Many2one('sicpro.app.metrologia.estado', string='Stage',
                               ondelete='restrict', tracking=True,
                               group_expand='_read_group_stage_ids',
                               default=_default_stage, copy=False)

    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'),
                                 ('2', 'Normal'), ('3', 'High')],
                                string='Prioridad')
    color = fields.Integer('Color Index')
    close_date = fields.Date('Close Date',
                             help="Date the maintenance was finished. ")
    kanban_state = fields.Selection(
        [('normal', 'En progreso'), ('blocked', 'detenido'),
         ('done', 'En espera del siguiente estado')],
        string='Kanban State', required=True, default='normal', tracking=True)

    archive = fields.Boolean(default=False, help="Set archive to true to hide "
                                                 "the maintenance request "
                                                 "without deleting it.")
    maintenance_type = fields.Selection([('correctivo', 'Correctivo'),
                                         ('preventivo', 'Preventivo')],
                                        string='Tipos de mantenimiento',
                                        default="correctivo")
    schedule_date = fields.Datetime(
        'Fecha prevista', help="Date the maintenance team plans maintenance."
                               "It should not differ much from Request Date.")
    maintenance_team_id = fields.Many2one('sicpro.app.metrologia.direcciones',
                                          string='Equipos', required=True,
                                          default=_get_default_team_id,
                                          check_company=True)
    duration = fields.Float(string="Duración", help="Duración en horas.")
    done = fields.Boolean(related='stage_id.done')

    def archive_equipment_request(self):
        self.write({'archive': True})

    def reset_equipment_request(self):
        """ Reinsert the maintenance request into the maintenance
        pipe in the first stage"""
        first_stage_obj = self.env['sicpro.app.metrologia.estado'].search(
            [], order="sequence asc", limit=1)
        # self.write({'active': True, 'stage_id': first_stage_obj.id})
        self.write({'archive': False, 'stage_id': first_stage_obj.id})

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.maintenance_team_id:
            if self.maintenance_team_id.company_id and not \
                    self.maintenance_team_id.company_id.id == \
                    self.company_id.id:
                self.maintenance_team_id = False

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        if self.equipment_id:
            self.user_id = self.equipment_id.technician_user_id \
                if self.equipment_id.technician_user_id else \
                self.equipment_id.category_id.technician_user_id
            self.category_id = self.equipment_id.category_id
            if self.equipment_id.maintenance_team_id:
                self.maintenance_team_id = \
                    self.equipment_id.maintenance_team_id.id

    @api.onchange('category_id')
    def onchange_category_id(self):
        if not self.user_id or not self.equipment_id or (self.user_id and not
        self.equipment_id.technician_user_id):
            self.user_id = self.category_id.technician_user_id

    @api.model
    def create(self, vals):
        # context: no_log, because subtype already handle this
        request = super(MetrologiaSolicitudCalibracion, self).create(vals)
        if request.owner_user_id or request.user_id:
            request._add_followers()
        if request.equipment_id and not request.maintenance_team_id:
            request.maintenance_team_id = request.equipment_id.maintenance_team_id
        request.activity_update()
        return request

    def write(self, vals):
        # Overridden to reset the kanban_state to normal whenever
        # the stage (stage_id) of the Maintenance Request changes.
        if vals and 'kanban_state' not in vals and 'stage_id' in vals:
            vals['kanban_state'] = 'normal'
        res = super(MetrologiaSolicitudCalibracion, self).write(vals)
        if vals.get('owner_user_id') or vals.get('user_id'):
            self._add_followers()
        if 'stage_id' in vals:
            self.filtered(lambda m: m.stage_id.done).write(
                {'close_date': fields.Date.today()})
            self.activity_feedback(
                ['sicpro_app_metrologia.mail_act_maintenance_request'])
        if vals.get('user_id') or vals.get('schedule_date'):
            self.activity_update()
        if vals.get('equipment_id'):
            # need to change description of activity also so unlink old and
            # create new activity
            self.activity_unlink(
                ['sicpro_app_metrologia.mail_act_maintenance_request'])
            self.activity_update()
        return res

    def activity_update(self):
        """ Update maintenance activities based on current record set state.
        It reschedule, unlink or create maintenance request activities. """
        self.filtered(
            lambda request: not request.schedule_date).activity_unlink(
            ['maintenance.mail_act_maintenance_request'])
        for request in self.filtered(lambda request: request.schedule_date):
            date_dl = fields.Datetime.from_string(request.schedule_date).date()
            updated = request.activity_reschedule(
                ['maintenance.mail_act_maintenance_request'],
                date_deadline=date_dl,
                new_user_id=request.user_id.id or request.owner_user_id.id or
                            self.env.uid)
            if not updated:
                if request.equipment_id:
                    note = _(
                        'Actividad planificada paras <a href="#" data-oe-model="%s" data-oe-id="%s">%s</a>') % (
                               request.equipment_id._name,
                               request.equipment_id.id,
                               request.equipment_id.display_name)
                else:
                    note = False
                request.activity_schedule(
                    'sicpro_app_metrologia.mail_act_maintenance_request',
                    fields.Datetime.from_string(request.schedule_date).date(),
                    note=note,
                    user_id=request.user_id.id or request.owner_user_id.id or
                            self.env.uid)

    def _add_followers(self):
        for request in self:
            partner_ids = (
                    request.owner_user_id.partner_id +
                    request.user_id.partner_id).ids
            request.message_subscribe(partner_ids=partner_ids)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order,
                                   access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)
