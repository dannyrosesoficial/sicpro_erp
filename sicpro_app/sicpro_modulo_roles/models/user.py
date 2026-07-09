# -*- coding: utf-8 -*-


from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    role_line_ids = fields.One2many(comodel_name="sicpro.modulo.roles.line", inverse_name="user_id",
                                    string="Roles lines", default=lambda self: self._default_role_lines(), )
    role_ids = fields.One2many(comodel_name="sicpro.modulo.roles", string="Roles", compute="_compute_role_ids")

    @api.model
    def _default_role_lines(self):
        default_user = self.env.ref("base.default_user", raise_if_not_found=False)
        default_values = []
        if default_user:
            for role_line in default_user.role_line_ids:
                default_values.append(
                    {"role_id": role_line.role_id.id, "date_from": role_line.date_from, "date_to": role_line.date_to,
                     "is_enabled": role_line.is_enabled, })
        return default_values

    @api.depends("role_line_ids.role_id")
    def _compute_role_ids(self):
        for user in self:
            user.role_ids = user.role_line_ids.mapped("role_id")

    @api.model
    def create(self, vals):
        new_record = super(ResUsers, self).create(vals)
        new_record.set_groups_from_roles()
        return new_record

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        self.sudo().set_groups_from_roles()
        return res

    def _get_enabled_roles(self):
        return self.role_line_ids.filtered(lambda rec: rec.is_enabled)

    def set_groups_from_roles(self, force=False):
        role_groups = {}
        for role in self.mapped("role_line_ids.role_id"):
            role_groups[role] = list(set(role.group_id.ids + role.implied_ids.ids + role.trans_implied_ids.ids))
        for user in self:
            if not user.role_line_ids and not force:
                continue
            group_ids = []
            for role_line in user._get_enabled_roles():
                role = role_line.role_id
                group_ids += role_groups[role]
            group_ids = list(set(group_ids))
            # Eliminar duplicados IDs
            groups_to_add = list(set(group_ids) - set(user.groups_id.ids))
            groups_to_remove = list(set(user.groups_id.ids) - set(group_ids))
            to_add = [(4, gr) for gr in groups_to_add]
            to_remove = [(3, gr) for gr in groups_to_remove]
            groups = to_remove + to_add
            if groups:
                vals = {"groups_id": groups}
                super(ResUsers, user).write(vals)
        return True
