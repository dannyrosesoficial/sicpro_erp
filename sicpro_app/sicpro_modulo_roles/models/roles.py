# -*- coding: utf-8 -*-

import logging
from random import randint

from odoo import SUPERUSER_ID, api, fields, models

_logger = logging.getLogger(__name__)


def _default_color():
    return randint(1, 11)


class ResUsersRole(models.Model):
    _name = "sicpro.modulo.roles"
    _inherits = {"res.groups": "group_id"}
    _description = "Roles de usuarios"
    _order = "sequence"

    sequence = fields.Integer('Secuencia', default=1, )
    group_id = fields.Many2one(comodel_name="res.groups", required=True, ondelete="cascade", readonly=True,
                               string="Grupos asociados", )
    line_ids = fields.One2many(comodel_name="sicpro.modulo.roles.line", inverse_name="role_id", string="Roles lines")
    user_ids = fields.One2many(comodel_name="res.users", string="Lista de Usuarios", compute="_compute_user_ids")
    group_category_id = fields.Many2one(related="group_id.category_id", string="Asociar Categoría", readonly=False,
                                        default=lambda cls: cls.env.ref(
                                            "sicpro_modulo_roles.ir_module_category_role").id, )
    comment = fields.Html(string="Notas Internas", )
    descripcion = fields.Text(string="Descripción del ROL", required=True)
    active = fields.Boolean(string="Activo", default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    roles_especiales = fields.Boolean(string='Roles Especiales', required=False, default=False)

    @api.depends("line_ids.user_id")
    def _compute_user_ids(self):
        for role in self:
            role.user_ids = role.line_ids.mapped("user_id")

    @api.model
    def create(self, vals):
        new_record = super(ResUsersRole, self).create(vals)
        new_record.update_users()
        return new_record

    def write(self, vals):
        groups_vals = {}
        for field in self.group_id._fields:
            if field in vals:
                groups_vals[field] = vals.pop(field)
        if groups_vals:
            self.group_id.write(groups_vals)
        res = super(ResUsersRole, self).write(vals)
        self.update_users()
        return res

    def unlink(self):
        users = self.mapped("user_ids")
        res = super(ResUsersRole, self).unlink()
        users.set_groups_from_roles(force=True)
        return res

    def update_users(self):
        users = self.mapped("user_ids")
        users.set_groups_from_roles()
        return True

    @api.model
    def cron_update_users(self):
        logging.info("Update user roles")
        self.search([]).update_users()


class ResUsersRoleLine(models.Model):
    _name = "sicpro.modulo.roles.line"
    _description = "Usuarios asociados a los roles"

    role_id = fields.Many2one(comodel_name="sicpro.modulo.roles", required=True, string="Roles", ondelete="cascade")
    user_id = fields.Many2one(comodel_name="res.users", required=True, string="Usuarios",
                              domain=[("id", "!=", SUPERUSER_ID)], ondelete="cascade", )
    date_from = fields.Date("Desde")
    date_to = fields.Date("Hasta")
    is_enabled = fields.Boolean("Activado", compute="_compute_is_enabled")
    _sql_constraints = [
        ("user_role_uniq", "unique (user_id,role_id)", "Roles can be assigned to a user only once at a time",)]

    @api.depends("date_from", "date_to")
    def _compute_is_enabled(self):
        today = fields.Date.context_today(self)
        for role_line in self:
            role_line.is_enabled = True
            if role_line.date_from:
                date_from = role_line.date_from
                if date_from > today:
                    role_line.is_enabled = False
            if role_line.date_to:
                date_to = role_line.date_to
                if today > date_to:
                    role_line.is_enabled = False

    def unlink(self):
        users = self.mapped("user_id")
        res = super(ResUsersRoleLine, self).unlink()
        users.set_groups_from_roles(force=True)
        return res
