# -*- coding: utf-8 -*-

from odoo import models, tools
from odoo.addons.sicpro_modulo_ldap_query.models.sicpro_modulo_ldap_registros import SicproLdapRegistros


class ServiciosInternosCorreos(models.Model):
    _inherit = 'sicpro.app.servicios.internos.correos'

    # verífico que no se repita el trabajador en el registro
    def cron_correo_ldap_servicios_internos(self):
        # busco los usuarios con permisos a recibir los correos alerta
        admin = self.env['res.users'].sudo().search(
            [('groups_id', 'in', self.env.ref('sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])

        # Busco el usuario para realizar la comparación.
        trabajadores = self.env['sicpro.app.trabajadores'].search([('active', '=', True)])

        # Selecciono el usuario y los administradores
        notifica = ''
        for value in admin:
            notifica += str(value.partner_id.email_formatted)
        email_values = {'email_to': notifica, }

        # verifico el usuario
        for item in trabajadores:
            # Busco si existe el usuario registrado en el servicio de correo.
            correo = self.env['sicpro.app.servicios.internos.correos'].search(
                ['&', ('active', '=', True), ('trabajador', '=', item.id)])

            # si no existe el usuario registrado lo busco en ldap
            if not correo:
                cuenta_plaza = 8 - int(len(item.plaza_id))
                valor_contado = 0
                plaza = str(item.plaza_id)
                # relleno con ceros él no. de plaza para compararlo con el ldap
                while valor_contado < cuenta_plaza:
                    valor_contado += 1
                    plaza = '0' + plaza

                filtro = '(employeeNumber=' + plaza + ')'
                # realizo la solicitud de datos directamente al ldap empresarial
                data = SicproLdapRegistros.check_ldap_usuario(self, filtro)

                if data:
                    correo_ldap = tools.ustr(data[0][1]['mail'][0])
                    # creo el registro en los servicios de correo
                    servicio_data = {'name': correo_ldap, 'trabajador': item.id, }
                    self.env['sicpro.app.servicios.internos.correos'].create(servicio_data)

        # envío el correo de aviso de la ejecución de la acción
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_modulo_ldap_servicios_internos.servicios_internos_correos_actual_ldap')
        template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
