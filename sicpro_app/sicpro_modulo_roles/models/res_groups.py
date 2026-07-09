# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    view_access = fields.Many2many(groups="base.group_system", )

    # El campo inverso del campo group_id en el modelo res.users.role
    # Este campo debe usarse como relación One2one ya que un rol solo puede ser
    # representado por un grupo. Se declara como un campo One2many como él
    # campo inverso en res.users.role se declara como Many2one
    role_id = fields.One2many(comodel_name="res.users.role",
        inverse_name="group_id",
        help="Relation for the groups that represents a role", )
    role_ids = fields.Many2many(comodel_name="res.users.role",
        relation="res_groups_implied_roles_rel", string="User Roles",
        compute="_compute_role_ids",
        help="Roles in which the group is involved", )
    parent_ids = fields.Many2many("res.groups", "res_groups_implied_rel",
        "hid", "gid", string="Parents",
        help="Inverse relation for the Inherits field. "
             "The groups from which this group is inheriting", )
    trans_parent_ids = fields.Many2many(comodel_name="res.groups",
        string="Parent Groups", compute="_compute_trans_parent_ids",
        recursive=True, )
    role_count = fields.Integer(string="# User Roles", compute="_compute_role_count")

    def _compute_role_count(self):
        for group in self:
            group.role_count = len(group.role_ids)

    @api.depends("parent_ids.trans_parent_ids")
    def _compute_trans_parent_ids(self):
        for group in self:
            group.trans_parent_ids = (
                group.parent_ids | group.parent_ids.trans_parent_ids)

    def _compute_role_ids(self):
        for group in self:
            if group.trans_parent_ids:
                group.role_ids = group.trans_parent_ids.role_id
            else:
                group.role_ids = group.role_id

    def action_view_roles(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "sicpro_modulo_roles.action_res_users_role_list")
        action["context"] = {}
        if len(self.role_ids) > 1:
            action["domain"] = [("id", "in", self.role_ids.ids)]
        elif self.role_ids:
            form_view = [(
            self.env.ref("sicpro_modulo_roles.view_res_users_role_form").id,
            "form")]
            if "views" in action:
                action["views"] = form_view + [(state, view) for state, view in
                    action["views"] if view != "form"]
            else:
                action["views"] = form_view
            action["res_id"] = self.role_ids.id
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action
