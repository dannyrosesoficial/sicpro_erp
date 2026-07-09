# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


# Este asistente se utiliza para agrupar diferentes grupos en un rol.
class GroupGroupsIntoRole(models.TransientModel):
    _name = "wizard.groups.into.role"
    _description = "Agrupar grupos en un rol."
    name = fields.Char(required=True,
                       help="Agrupar grupos en un rol y especificar un nombre para este rol", )

    def create_role(self):
        selected_group_ids = self.env.context.get("active_ids", [])
        vals = {"name": self.name, "implied_ids": selected_group_ids, }
        role = self.env["res.users.role"].create(vals)

        return {"type": "ir.actions.act_window", "res_model": "res.users.role",
            "view_mode": "form", "res_id": role.id, "target": "current",
            "context": {
                "form_view_ref": "sicpro_modulo_roles.view_res_users_role_form", }, }
