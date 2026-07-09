# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class WizardCreateRoleFromUser(models.TransientModel):
    _name = "wizard.create.role.from.user"
    _description = "Crear rol desde el asistente de usuario"

    name = fields.Char(required=True)
    assign_to_user = fields.Boolean(string="Asignar al usuario", default=True)

    def create_from_user(self):
        self.ensure_one()

        user_ids = self.env.context.get("active_ids", [])
        assert len(user_ids) == 1

        user_id = user_ids[0]

        role_obj = self.env["res.users.role"]
        role_line_obj = self.env["res.users.role.line"]
        user_obj = self.env["res.users"]

        user = user_obj.browse(user_id)

        role = role_obj.create(
            {
                "name": self.name,
            }
        )

        role.implied_ids = [fields.Command.set(user.group_ids.ids)]

        if self.assign_to_user:
            role_line_obj.create(
                {
                    "role_id": role.id,
                    "user_id": user_id,
                }
            )

        return {
            "context": self.env.context,
            "name": "User Role",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "res.users.role",
            "res_id": role.id,
            "target": "current",
            "type": "ir.actions.act_window",
        }
