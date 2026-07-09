# -*- coding: utf-8 -*-

import json
from datetime import date

from babel.dates import format_date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.release import version


class SolicitudesGrupoEjecutor(models.Model):
    _name = 'sicpro.app.solicitudes.grupo.ejecutor'
    _inherit = ['mail.thread']
    _description = 'Grupo Ejecutor'
    _order = "sequence"

    @api.model
    @api.returns('self', lambda value: value.id if value else False)
    def _get_default_team_id(self, user_id=None, domain=None):
        if not user_id:
            user_id = self.env.uid
        team_id = self.env['sicpro.app.solicitudes.grupo.ejecutor'].search([
            '|', ('user_id', '=', user_id), ('miembros_ids', '=', user_id),
            '|', ('company_id', '=', False),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        if not team_id and 'default_team_id' in self.env.context:
            team_id = self.env['sicpro.app.solicitudes.grupo.ejecutor'].browse(
                self.env.context.get('default_team_id'))
        if not team_id:
            team_domain = domain or []
            default_team_id = \
                self.env['sicpro.app.solicitudes.grupo.ejecutor'].search(
                    team_domain, limit=1)
            return default_team_id or self.env['sicpro.app.solicitudes.grupo.ejecutor']
        return team_id

    def _get_default_favorite_user_ids(self):
        return [(6, 0, [self.env.uid])]

    name = fields.Many2one(comodel_name="sicpro.app.trabajadores.departmentos",
                           string="Grupo ejecutor",
                           required=True,
                           domain="[('tipo_registro', '=', 'agrupacion')]")
    sequence = fields.Integer('Secuencia', default=10)
    active = fields.Boolean(default=True,
                            help="If the active field is set to false, "
                                 "it will allow you to hide the Sales "
                                 "Team without removing it.")
    currency_id = fields.Many2one("res.currency",
                                  related='company_id.currency_id',
                                  string="Currency", readonly=True)
    company_id = fields.Many2one('res.company', string='Proceso', store=True,
                                 related='name.company_id', readonly=True)
    departamento = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                   string="Departamento", store=True,
                                   related='name.parent_id', readonly=True)
    miembros_ids = fields.One2many(
        comodel_name="sicpro.app.trabajadores.general",
        string='Miembros del grupo',
        inverse_name="equipo_ejecutor_id",
        help="Add members to automatically assign their "
             "documents to this sales team. "
             "You can only be member of one team.")
    jefe_grupo = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.general",
        string='Líder del grupo',
        domain="[('department_id', '=', name)]", required=True, )
    use_leads = fields.Boolean('Iniciativas',
                               help="Check this box to filter and qualify "
                                    "incoming requests as leads before converting"
                                    " them into opportunities and assigning them to a salesperson.")
    use_opportunities = fields.Boolean('Oportunidades', default=True,
                                       help="Check this box to manage a "
                                            "presales process with opportunities.")
    color = fields.Integer(string='Indice de colores',
                           help="The color of the channel")
    dashboard_button_name = fields.Char(string="Dashboard Button")
    dashboard_graph_data = fields.Text(compute='_compute_dashboard_graph')
    unassigned_leads_count = fields.Integer(
        compute='_compute_unassigned_leads_count', string='Unassigned Leads')
    opportunities_count = fields.Integer(compute='_compute_opportunities',
                                         string='Number of open opportunities')
    overdue_opportunities_count = fields.Integer(
        compute='_compute_overdue_opportunities',
        string='Number of overdue opportunities')
    opportunities_amount = fields.Integer(compute='_compute_opportunities',
                                          string='Opportunities Revenues')
    overdue_opportunities_amount = fields.Integer(
        compute='_compute_overdue_opportunities',
        string='Overdue Opportunities Revenues')

    user_id = fields.Many2one('res.users', string='Team Leader')

    # accion para trae los datos del grupo
    @api.onchange('name')
    def _onchange_name(self, ):
        self.jefe_grupo = self.name.manager_id

    def _compute_dashboard_graph(self):
        for team in self:
            team.dashboard_graph_data = json.dumps(team._get_graph())

    def _compute_is_favorite(self):
        for team in self:
            team.is_favorite = self.env.user in team.favorite_user_ids

    def _inverse_is_favorite(self):
        sudoed_self = self.sudo()
        to_fav = sudoed_self.filtered(
            lambda team: self.env.user not in team.favorite_user_ids)
        to_fav.write({'favorite_user_ids': [(4, self.env.uid)]})
        (sudoed_self - to_fav).write(
            {'favorite_user_ids': [(3, self.env.uid)]})
        return True

    def _graph_get_model(self):
        """ skeleton function defined here because it'll be
        called by crm and/or sale
        """
        raise UserError(
            _('Undefined graph model for Sales Team: %s') % self.name)

    def _graph_get_dates(self, today):
        """ return a coherent start and end date for the dashboard graph
        covering a month period grouped by week.
        """
        start_date = today - relativedelta(months=1)
        # we take the start of the following week if we group by week
        # (to avoid having twice the same week from different month)
        start_date += relativedelta(days=8 - start_date.isocalendar()[2])
        return [start_date, today]

    def _graph_date_column(self):
        return 'create_date'

    def _graph_x_query(self):
        return 'EXTRACT(WEEK FROM %s)' % self._graph_date_column()

    def _graph_y_query(self):
        raise UserError(
            _('Undefined graph model for Sales Team: %s') % self.name)

    def _extra_sql_conditions(self):
        return ''

    def _graph_title_and_key(self):
        """ Returns an array containing the appropriate graph title
        and key respectively.

            The key is for lineCharts, to have the on-hover label.
        """
        return ['', '']

    def _graph_data(self, start_date, end_date):
        """ return format should be an iterable of dicts that contain
        {'x_value': ..., 'y_value': ...}
            x_values should be weeks.
            y_values are floats.
        """
        query = """SELECT %(x_query)s as x_value, %(y_query)s as y_value
                     FROM %(table)s
                    WHERE team_id = %(team_id)s
                      AND DATE(%(date_column)s) >= %(start_date)s
                      AND DATE(%(date_column)s) <= %(end_date)s
                      %(extra_conditions)s
                    GROUP BY x_value;"""

        # apply rules
        dashboard_graph_model = self._graph_get_model()
        GraphModel = self.env[dashboard_graph_model]
        graph_table = GraphModel._table
        extra_conditions = self._extra_sql_conditions()
        where_query = GraphModel._where_calc([])
        GraphModel._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()
        if where_clause:
            extra_conditions += " AND " + where_clause

        query = query % {
            'x_query': self._graph_x_query(),
            'y_query': self._graph_y_query(),
            'table': graph_table,
            'team_id': "%s",
            'date_column': self._graph_date_column(),
            'start_date': "%s",
            'end_date': "%s",
            'extra_conditions': extra_conditions
        }

        self._cr.execute(query,
                         [self.id, start_date, end_date] + where_clause_params)
        return self.env.cr.dictfetchall()

    def _get_graph(self):
        def get_week_name(start_date, locale):
            """ Generates a week name (string) from a datetime
            according to the locale:
                E.g.: locale    start_date (datetime)      return string
                      "en_US"      November 16th           "16-22 Nov"
                      "en_US"      December 28th           "28 Dec-3 Jan"
            """
            if (start_date + relativedelta(days=6)).month == start_date.month:
                short_name_from = format_date(start_date, 'd', locale=locale)
            else:
                short_name_from = format_date(start_date, 'd MMM',
                                              locale=locale)
            short_name_to = format_date(start_date + relativedelta(days=6),
                                        'd MMM', locale=locale)
            return short_name_from + '-' + short_name_to

        self.ensure_one()
        values = []
        today = fields.Date.from_string(fields.Date.context_today(self))
        start_date, end_date = self._graph_get_dates(today)
        graph_data = self._graph_data(start_date, end_date)
        x_field = 'label'
        y_field = 'value'

        # generate all required x_fields and update the y_values
        # where we have data for them
        locale = self._context.get('lang') or 'en_US'

        weeks_in_start_year = int(
            date(start_date.year, 12, 28).isocalendar()[
                1])  # This date is always in the last week of ISO years
        for week in range(0, (end_date.isocalendar()[1] -
                              start_date.isocalendar()[
                                  1]) % weeks_in_start_year + 1):
            short_name = get_week_name(
                start_date + relativedelta(days=7 * week), locale)
            values.append({x_field: short_name, y_field: 0})

        for data_item in graph_data:
            index = int((data_item.get('x_value') - start_date.isocalendar()[
                1]) % weeks_in_start_year)
            values[index][y_field] = data_item.get('y_value')

        [graph_title, graph_key] = self._graph_title_and_key()
        color = '#875A7B' if '+e' in version else '#7c7bad'
        return [{'values': values, 'area': True, 'title': graph_title,
                 'key': graph_key, 'color': color}]

    def _compute_dashboard_button_name(self):
        """ Sets the adequate dashboard button name depending on
        the Sales Team's options
        """
        for team in self:
            team.dashboard_button_name = _(
                "Big Pretty Button :)")  # placeholder

    def action_primary_channel_button(self):
        """ skeleton function to be overloaded
            It will return the adequate action depending on the Sales Team's options
        """
        return False

    def _add_members_to_favorites(self):
        for team in self:
            team.favorite_user_ids = [(4, member.id) for member in
                                      team.miembros_ids]

    def _compute_unassigned_leads_count(self):
        leads_data = self.env[
            'sicpro.app.solicitudes.oportunidades'].read_group([
            ('team_id', 'in', self.ids),
            ('type', '=', 'lead'),
            ('user_id', '=', False),
        ], ['team_id'], ['team_id'])
        counts = {datum['team_id'][0]: datum['team_id_count'] for datum in
                  leads_data}
        for team in self:
            team.unassigned_leads_count = counts.get(team.id, 0)

    def _compute_opportunities(self):
        opportunity_data = self.env[
            'sicpro.app.solicitudes.oportunidades'].search([
            ('team_id', 'in', self.ids),
            ('probability', '<', 100),
            ('type', '=', 'opportunity'),
        ]).read(['planned_revenue', 'team_id'])
        counts = {}
        amounts = {}
        for datum in opportunity_data:
            counts.setdefault(datum['team_id'][0], 0)
            amounts.setdefault(datum['team_id'][0], 0)
            counts[datum['team_id'][0]] += 1
            amounts[datum['team_id'][0]] += (datum.get('planned_revenue', 0))
        for team in self:
            team.opportunities_count = counts.get(team.id, 0)
            team.opportunities_amount = amounts.get(team.id, 0)

    def _compute_overdue_opportunities(self):
        opportunity_data = self.env[
            'sicpro.app.solicitudes.oportunidades'].read_group([
            ('team_id', 'in', self.ids),
            ('probability', '<', 100),
            ('type', '=', 'opportunity'),
            (
            'date_deadline', '<', fields.Date.to_string(fields.Datetime.now()))
        ], ['planned_revenue', 'team_id'], ['team_id'])
        counts = {datum['team_id'][0]: datum['team_id_count'] for datum in
                  opportunity_data}
        amounts = {datum['team_id'][0]: (datum['planned_revenue']) for datum in
                   opportunity_data}
        for team in self:
            team.overdue_opportunities_count = counts.get(team.id, 0)
            team.overdue_opportunities_amount = amounts.get(team.id, 0)

    def _compute_dashboard_button_name(self):
        super(SolicitudesGrupoEjecutor, self)._compute_dashboard_button_name()
        team_with_pipelines = self.filtered(lambda el: el.use_opportunities)
        team_with_pipelines.update({'dashboard_button_name': _("Pipeline")})

    def action_primary_channel_button(self):
        if self.use_opportunities:
            return self.env.ref(
                'sicpro_app_solicitudes.crm_case_form_view_salesteams_opportunity').read()[
                0]
        return super(SolicitudesGrupoEjecutor,
                     self).action_primary_channel_button()

    def _graph_get_model(self):
        if self.use_opportunities:
            return 'sicpro.app.solicitudes.oportunidades'
        return super(SolicitudesGrupoEjecutor, self)._graph_get_model()

    def _graph_date_column(self):
        if self.use_opportunities:
            return 'create_date'
        return super(SolicitudesGrupoEjecutor, self)._graph_date_column()

    def _graph_y_query(self):
        if self.use_opportunities:
            return 'count(*)'
        return super(SolicitudesGrupoEjecutor, self)._graph_y_query()

    def _extra_sql_conditions(self):
        if self.use_opportunities:
            return "AND type LIKE 'opportunity'"
        return super(SolicitudesGrupoEjecutor, self)._extra_sql_conditions()

    def _graph_title_and_key(self):
        if self.use_opportunities:
            return ['', _('New Opportunities')]  # no more title
        return super(SolicitudesGrupoEjecutor, self)._graph_title_and_key()
