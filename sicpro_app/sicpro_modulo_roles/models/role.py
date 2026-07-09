# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import datetime
import logging
from random import randint

from odoo import SUPERUSER_ID, api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


def _default_color():
    return randint(1, 11)


class ResUsersRole(models.Model):
    _name = "res.users.role"
    _inherits = {"res.groups": "group_id"}
    _description = "Rol de usuario"
    _order = "sequence"

    group_id = fields.Many2one(comodel_name="res.groups", required=True,
                               ondelete="cascade", readonly=True,
                               string="Grupos asociados", )
    line_ids = fields.One2many(comodel_name="res.users.role.line",
                               inverse_name="role_id", string="Líneas de rol")
    user_ids = fields.One2many(comodel_name="res.users",
                               string="Lista de Usuarios",
                               compute="_compute_user_ids")
    rule_ids = fields.Many2many(comodel_name="ir.rule",
                                compute="_compute_rule_ids",
                                string="Reglas de registro", required=False, )
    rules_count = fields.Integer(compute="_compute_rule_ids")
    model_access_ids = fields.Many2many(comodel_name="ir.model.access",
                                        compute="_compute_model_access_ids",
                                        string="Derechos de acceso",
                                        required=False, )
    model_access_count = fields.Integer(compute="_compute_model_access_ids")
    group_privilege_id = fields.Many2one(related="group_id.privilege_id",
                                         string="Associated privilege",
                                         help="Privilege assigned to the associated group.",
                                         readonly=False, )
    is_default = fields.Boolean(string="Predeterminado en nuevos usuarios",
                                help=(
                                    "Cuando está habilitado, este rol se asigna a los usuarios recién creados de "
                                    "forma predeterminada."), )
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    descripcion = fields.Text(string="Descripción del ROL", required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    roles_especiales = fields.Boolean(string='Roles Especiales', default=False)

    @api.depends("line_ids.user_id")
    def _compute_user_ids(self):
        for role in self.sudo() if self._bypass_rules() else self:
            role.user_ids = role.line_ids.mapped("user_id")

    @api.depends("implied_ids", "implied_ids.model_access")
    def _compute_model_access_ids(self):
        for rec in self:
            rec.model_access_ids = rec.implied_ids.model_access.ids
            rec.model_access_count = len(rec.model_access_ids)

    @api.depends("implied_ids", "implied_ids.rule_groups")
    def _compute_rule_ids(self):
        for rec in self:
            rec.rule_ids = rec.implied_ids.rule_groups.ids
            rec.rules_count = len(rec.rule_ids)

    # Ejecute métodos como superusuario para evitar problemas con el
    # "Administrador/Derecho de acceso"
    @api.model
    def _bypass_rules(self):
        return self._name == "res.users.role" and self.env.user.has_group(
            "base.group_erp_manager")

    @api.model_create_multi
    def create(self, vals_list):
        model = (self.sudo() if self._bypass_rules() else self).browse()
        new_records = super(ResUsersRole, model).create(vals_list)
        new_records.update_users()
        return new_records

    def read(self, fields=None, load="_classic_read"):
        recs = self.sudo() if self._bypass_rules() else self
        return super(ResUsersRole, recs).read(fields, load)

    def write(self, vals):
        recs = self.sudo() if self._bypass_rules() else self
        groups_vals = {}
        for field in recs.group_id._fields:
            if field in vals:
                groups_vals[field] = vals.pop(field)
        if groups_vals:
            recs.group_id.write(groups_vals)
        res = super(ResUsersRole, recs).write(vals)
        recs.update_users()
        return res

    def unlink(self):
        users = self.mapped("user_ids")
        res = super().unlink()
        users.set_groups_from_roles(force=True)
        return res

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, name="%s (copia)" % (self.name or ''))
        return super().copy(default)

    def update_users(self):
        users = self.mapped("user_ids")
        users.set_groups_from_roles()
        return True

    @api.model
    def cron_update_users(self):
        logging.info("Update user roles")
        offset = 0
        batch = 2000
        while True:
            roles = self.search([], offset=offset, limit=batch)
            if not roles:
                break
            roles.update_users()
            offset += batch

    def show_rule_ids(self):
        action = self.env["ir.actions.actions"]._for_xml_id("base.action_rule")
        action["domain"] = [("id", "in", self.rule_ids.ids)]
        return action

    def show_model_access_ids(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "base.ir_access_act")
        action["domain"] = [("id", "in", self.model_access_ids.ids)]
        return action


class ResUsersRoleLine(models.Model):
    _name = "res.users.role.line"
    _description = "Usuarios asociados a un rol"

    active = fields.Boolean(string= 'Activo', related="user_id.active", index=True)
    role_id = fields.Many2one(comodel_name="res.users.role", required=True,
        string="Roles", ondelete="cascade")
    user_id = fields.Many2one(comodel_name="res.users", required=True,
                              string="Usuarios",
                              domain=[("id", "!=", SUPERUSER_ID)],
                              ondelete="cascade", )
    date_from = fields.Date(string="Desde")
    date_to = fields.Date(string="Hasta")
    is_enabled = fields.Boolean(string="Activado", compute="_compute_is_enabled")

    @api.constrains('user_id', 'role_id')
    def _check_user_role_uniqueness(self):
        for record in self:
            # Buscamos si ya existe la combinación usuario + rol
            domain = [('user_id', '=', record.user_id.id),
                ('role_id', '=', record.role_id.id), ('id', '!=', record.id)
                # Excluimos el registro actual
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "El usuario '%s' ya tiene asignado el rol '%s'. "
                    "Los roles solo se pueden asignar una vez.\n\n" % (
                    record.user_id.name,
                    record.role_id.name) + MSG_SOPORTE_SICPRO)

    @api.depends("date_from", "date_to")
    def _compute_is_enabled(self):
        today = datetime.date.today()
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
        res = super().unlink()
        users.set_groups_from_roles(force=True)
        return res
