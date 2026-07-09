# -*- coding: utf-8 -*-

from odoo import models


class PlantillaAccesoRoles(models.Model):
    _inherit = "sicpro.modulo.plantilla.acceso"

    # retorna el code html de los roles para generar la planilla de acceso
    def buscar_registro_roles(self, registro_id):
        roles = []
        registros = []
        td_html = []
        registros_ids = self.env['sicpro.modulo.web.registro.roles'].sudo().search([('active', '=', True), ])
        # solicitud_id = self.env['sicpro.modulo.plantilla.acceso'].sudo().search(
        #     ['&', ('active', '=', True), ('id', '=', registro_id)])
        solicitud_id = self.env['sicpro.modulo.plantilla.acceso.roles'].sudo().search([('planilla_id', '=', registro_id)])

        # creo la matrix de todos los roles del registro
        for item in registros_ids:
            valor = {'nombre': item.name, 'rol': '-', }
            registros.append(valor)

        # género los roles asignados al usuario
        for item in registros_ids:
            for var in item.roles:
                for value in solicitud_id.role_id:
                    if var.name == value.name:
                        valor = {'nombre': item.name, 'rol': value.nombre_registro, }
                        roles.append(valor)

        # actualizo el valor de los roles del registro
        for item in registros:
            for value in roles:
                if item['nombre'] in value['nombre']:
                    item.update({'rol': value['rol']})

        # creo el cuerpo del código html
        for td in registros:
            data_td = {'<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px'
                       ' solid #000000; border-right: 1px solid #000000" colspan="3" align="center" valign="middle"'
                       ' height="28"><font size="3" face="Liberation Serif">' + td['nombre'] + '</font></td>'
                       '<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px'
                       ' solid #000000; border-right: 1px solid #000000" colspan="3" align="left" valign="middle">'
                       '<font size="3" style="margin-left:5px;" face="Liberation Serif">' +
                       td['rol'] + '</font></td>'}
            td_html.append(data_td)

        # separo en dos las etiquetas td y las introduzco en un tr
        count_td = 0
        data_tr = ''
        data_html = ''
        for tr in td_html:
            count_td += 1
            data_tr += str(tr).replace("{", "").replace("}", "")
            if count_td == 2:
                data_html += '<tr>' + data_tr + '</tr>'
                count_td = 0
                data_tr = ''

        html_roles = data_html.replace("'", "")

        return html_roles
