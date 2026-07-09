# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models
from odoo.exceptions import UserError


class PlantillaAccesoRoles(models.Model):
    _inherit = "sicpro.modulo.solicitud.acceso"

    bitacora_actualizada = fields.Boolean(string='Bitácora Actualizada',
                                          default=False)

    def actualizar_bitacora(self):
        self.ensure_one()
        # Buscamos al usuario (usamos limit=1 para evitar errores si hay duplicados)
        usuario = self.env['res.users'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False),
             ('pep', '=', self.codigo_sap)], limit=1)

        if not usuario:
            raise UserError(
                "No se encontró un usuario con el código SAP (PEP): %s" % self.codigo_sap)

        # Mapeo de datos según tipo de movimiento (Eliminamos 'global')
        map_movimientos = {'alta': ('crear',
                                    'El usuario fue creado correctamente, se le asignaron los roles y permisos solicitados.'),
                           'modificacion': ('modificar',
                                            'El usuario fue modificado correctamente, los roles y permisos del sistema fueron actualizados'),
                           'reinicio': ('reactivado',
                                        'El usuario fue reactivado correctamente, los roles y permisos del sistema fueron actualizados'),
                           'baja': ('eliminar',
                                    'El usuario fue archivado y deshabilitado. Se removieron sus roles.')}

        movimiento, nota = map_movimientos.get(self.tipo_movimiento, (
            'desconocido', 'Movimiento no definido'))

        # Lógica de roles
        if self.tipo_movimiento == 'baja':
            rol_eliminar = self.env['res.users.role'].sudo().search(
                [('nombre_registro', '=', 'Eliminar accesos de usuarios')],
                limit=1)
            roles = [(6, 0, rol_eliminar.ids)]
        else:
            roles = [(6, 0, usuario.role_line_ids.mapped('role_id').ids)]

        # 1. Crear registro en Bitácora
        bitacora = self.env['sicpro.app.soporte.bitacora'].create(
            {'name': movimiento, 'usuario': usuario.id, 'roles': roles,
             'nota': nota, 'numero_consecutivo': self.numero_consecutivo, })
        self.bitacora_actualizada = True

        # 2. Gestionar adjuntos desde el Ticket de Soporte
        soporte = self.env['sicpro.app.soporte'].search(
            [('numero_consecutivo', '=', self.numero_consecutivo)], limit=1)
        if soporte:
            attachments = self.env['ir.attachment'].search(
                [('res_id', '=', soporte.id),
                 ('res_model', '=', 'sicpro.app.soporte')])
            for att in attachments:
                att.copy({'res_model': 'sicpro.app.soporte.bitacora',
                          'res_id': bitacora.id})

        # 3. Acciones de baja / alta
        if self.tipo_movimiento == 'baja':
            usuario.sudo().write({'active': False})
            usuario.sudo().partner_id.write({'active': False})

        if self.tipo_movimiento == 'alta' and soporte:
            soporte.partner_user_id = usuario.id

        return True

    def ver_bitacora(self):
        self.ensure_one()
        return {'name': 'Bitácora del Usuario',
                'type': 'ir.actions.act_window',
                'res_model': 'sicpro.app.soporte.bitacora',
                'view_mode': 'list,form', 'domain': [
                ('numero_consecutivo', '=', self.numero_consecutivo)],
                'target': 'current', }

    @api.model_create_multi
    def create(self, vals_list):
        # Odoo 19 usa create_multi por defecto para mejor rendimiento
        records = super(PlantillaAccesoRoles, self).create(vals_list)

        for res in records:
            res.buscar_usuario_roles()
            res.buscar_inversionista()

            # Suscribir seguidores de notificaciones
            grupo_id = self.env.ref(
                'sicpro_app_administracion.grupo_app_administracion_notificaciones').id
            usuarios_notif = self.env['res.users'].sudo().search(
                [('groups_id', 'in', [grupo_id])])
            res.message_subscribe(
                partner_ids=usuarios_notif.mapped('partner_id').ids)
            res.message_post(body='Nueva Solicitud Creada',
                             subtype_xmlid='mail.mt_comment')

            # --- Lógica de creación de Ticket de Soporte ---
            user_ticket = self.env['res.users'].search(
                [('email', '=', res.email)], limit=1) or self.env[
                              'res.users'].search(
                [('email', '=', 'sicproerp@etecsa.cu')], limit=1)

            # Búsqueda de configuraciones base (con limit=1 para seguridad)
            canal = self.env['sicpro.app.soporte.canales'].search(
                [('code', '=', 'ticket_acceso')], limit=1).id
            equipo = self.env['sicpro.app.soporte.equipos'].search(
                [('bitacora', '=', True)], limit=1).id
            nucleo = self.env['sicpro.app.soporte.aplicaciones'].search(
                [('modulo_base', '=', True)], limit=1).id
            etiquetas = self.env['sicpro.app.soporte.etiquetas'].search(
                [('solicitudes_acceso', '=', True)]).ids

            # Versión y Estado
            v_estado = self.env['sicpro.app.soporte.estados.versiones'].search(
                [('inicial', '=', True)], limit=1)
            version = self.env['sicpro.app.soporte.versiones'].search(
                [('stage_id', '=', v_estado.id)], order='id ASC', limit=1).id

            # Descripción con formato
            desc_html = f'<span style="font-weight: bold; font-size: 18px;">El trabajador <span style="color: blue; text-decoration: underline;">{res.email}</span> ha solicitado: {res.tipo_movimiento}</span>'

            # Crear Ticket
            ticket = self.env['sicpro.app.soporte'].create(
                {'name': f'Gestión de Solicitudes - {res.tipo_movimiento}',
                 'partner_user_id': user_ticket.id, 'channel_id': canal,
                 'team_id': equipo,
                 'numero_consecutivo': res.numero_consecutivo,
                 'descripcion': desc_html, 'id_solicitud_acceso': res.id,
                 'aplicaciones': nucleo, 'tag_ids': [(6, 0, etiquetas)],
                 'version_id': version, 'priority': '2', })
            ticket.message_subscribe(partner_ids=user_ticket.partner_id.ids)

        return records
