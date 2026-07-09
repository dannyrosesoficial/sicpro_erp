# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models


class ServiciosInternosCorreos(models.Model):
    _inherit = 'sicpro.app.servicios.internos.correos'

    # verífico que no se repita el trabajador en el registro
    def cron_correo_ldap_servicios_internos(self):
        # 1. Corrección de groups_id: Buscamos a través del modelo res.groups
        admin = self.env['res.users']
        group_notif = self.env.ref(
            'sicpro_app_administracion.grupo_app_administracion_notificaciones',
            raise_if_not_found=False)

        if group_notif:
            admin = group_notif.user_ids

        # Preparar destinatarios de correo
        emails = [u.partner_id.email_formatted for u in admin if
                  u.partner_id.email]
        notifica = ','.join(emails)
        email_values = {'email_to': notifica}

        # Busco los trabajadores activos
        trabajadores = self.env['sicpro.app.trabajadores'].search(
            [('active', '=', True)])

        # Verífico cada trabajador
        for item in trabajadores:
            # Busco si ya tiene correo registrado en servicios internos
            correo_existente = self.env[
                'sicpro.app.servicios.internos.correos'].search(
                [('active', '=', True), ('trabajador', '=', item.id)], limit=1)

            # Si no existe, lo buscamos en el LDAP empresarial
            if not correo_existente:
                # Optimización del relleno de ceros (zfill es más rápido que el while)
                plaza = str(item.plaza_id).zfill(8)

                filtro = f'(employeeNumber={plaza})'

                # Llamada al método de búsqueda LDAP (asegúrate de que sea accesible)
                # Nota: Si el método está en el mismo modelo o heredado, usa self.check_ldap_usuario
                modelo_ldap = self.env['sicpro.app.modulo.ldap.registros']
                data = modelo_ldap.check_ldap_usuario(filtro)

                if data and 'mail' in data[0][1]:
                    # Decodificación segura para Odoo 19 (evita DeprecationWarning)
                    mail_raw = data[0][1]['mail'][0]
                    correo_ldap = mail_raw.decode('utf-8') if isinstance(
                        mail_raw, bytes) else str(mail_raw)

                    # Crear el registro en servicios internos
                    self.env['sicpro.app.servicios.internos.correos'].create(
                        {'name': correo_ldap, 'trabajador': item.id, })

        # Envío de correo de aviso
        template = self.env.ref(
            'sicpro_modulo_ldap_servicios_internos.servicios_internos_correos_actual_ldap',
            raise_if_not_found=False)

        if template:
            template.send_mail(self.id, force_send=True,
                               email_values=email_values)
