# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import json
from random import randint

from odoo import api, fields, models


def _default_color():
    return randint(1, 11)


class AdministracionMenus(models.Model):
    _name = 'sicpro.app.administracion.menus'
    _description = 'Menus de accesos a la administración'
    _order = "sequence"

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    company_id = fields.Many2one('res.company', string="Proceso", default=lambda self: self.env.company)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como adjunto) para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    accesos = fields.One2many('sicpro.app.administracion.menus.accesos', 'menu', string='Accesos', )
    json_menus = fields.Text(compute="_json_menus")

    # Busca los datos de los menus
    # Busca los datos de los menus
    @api.depends('accesos.name', 'accesos.action')
    def _json_menus(self):
        for data in self:
            dic = []
            for obj in data.accesos:
                if not obj.action:
                    continue

                # Limpiamos las comillas que pones en el compute de AdministracionAccesos
                pre_action = obj.action.replace("'", "")

                dic.append({"id": data.id, "menu_nombre": obj.name,
                    "menu_action": pre_action,
                    # Guardamos el XML_ID, no el ID numérico
                })

            # IMPORTANTE: Siempre asignar un valor, aunque sea un JSON vacío
            data.json_menus = json.dumps(dic) if dic else "[]"

    def action_open_menu(self):
        # Ahora menu_action es un XML_ID (string) y env.ref funcionará perfecto
        xml_id = self.env.context.get('menu_action')
        if xml_id:
            action = self.env.ref(xml_id).sudo().read()[0]
            return action
        return False

    # ejecuta la acción específica solicitada
    def action_menu_admin(self):
        obj_menu = self.env.context.get('default_obj_menu')
        action = self.env['ir.actions.act_window']._for_xml_id(obj_menu)
        return action



class AdministracionAccesos(models.Model):
    _name = 'sicpro.app.administracion.menus.accesos'
    _description = "Accesos de los menus de la administración"
    _order = "sequence"

    name = fields.Char(string='Nombre del Menu', required=True)
    accesos = fields.Many2one('ir.ui.menu', string='Menu', required=True, domain="[('action','!=', False)]")
    action = fields.Char(string='Acción', compute="_compute_action", store=False)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    menu = fields.Many2one('sicpro.app.administracion.menus', 'Menus', required=False, index=True)

    # buscar el nombre del menu
    @api.onchange('accesos')
    def onchange_accesos(self):
        for item in self:
            if item.accesos:
                item.name = item.accesos.name

    @api.depends('accesos')
    def _compute_action(self):
        for item in self:
            item.action = False

            if item.accesos and item.accesos.action:
                if item.accesos.action.xml_id:
                    item.action = f"'{item.accesos.action.xml_id}'"
