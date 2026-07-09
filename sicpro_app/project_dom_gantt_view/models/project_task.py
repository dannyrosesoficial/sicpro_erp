# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    planned_date_begin = fields.Datetime("Start date")
    planned_date_end = fields.Datetime("End date")
    html_color = fields.Char('Project HTML Color', related='project_id.html_color')

    _sql_constraints = [
        ('planned_date_check', "CHECK ((planned_date_begin <= planned_date_end))", "The start date must be prior to the end date."),
    ]
