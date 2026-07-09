# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PlantillaAccesoRoles(models.Model):
    _inherit = "sicpro.modulo.plantilla.acceso"

    bitacora_actualizada = fields.Boolean(string='Bitácora Actualizada', default=False, required=False)

    # actualizo la bitácora del usuario
    def actualizar_bitacora(self):
        global movimiento, nota, roles
        usuario = self.env['res.users'].sudo().search(['|', ('active', '=', True), ('active', '=', False),
                                                       ('pep', '=', self.codigo_sap)])
        bitacora = []
        if usuario:
            if self.tipo_movimiento == 'alta':
                movimiento = 'crear'
                nota = 'El usuario fue creado correctamente, se le asignaron los roles y permisos solicitados.'
                roles = usuario.role_line_ids.role_id
            elif self.tipo_movimiento == 'modificacion':
                movimiento = 'modificar'
                nota = 'El usuario fue modificado correctamente, los roles y permisos del sistema fueron actualizados'
                roles = usuario.role_line_ids.role_id
            elif self.tipo_movimiento == 'reinicio':
                movimiento = 'reactivado'
                nota = 'El usuario fue reactivado correctamente, los roles y permisos del sistema fueron actualizados'
                roles = usuario.role_line_ids.role_id
            elif self.tipo_movimiento == 'baja':
                movimiento = 'eliminar'
                nota = 'El usuario fue archivado, pasando al estado de deshabilitado, fueron removidos ' \
                       'todos los roles y permisos que tenía asignado.'
                # busco el rol de eliminación
                rol = self.env['sicpro.modulo.roles'].sudo().search(
                    [('nombre_registro', '=', 'Eliminar accesos de usuarios')])
                roles = rol.ids

            bitacora_data = {'name': movimiento, 'usuario': usuario.id, 'roles': roles, 'nota': nota,
                             'numero_consecutivo': self.numero_consecutivo,}
            bitacora.append(bitacora_data)

            # creo el registro del usuario en la bitácora
            bitacora = self.env['sicpro.app.soporte.bitacora'].create(bitacora)
            self.bitacora_actualizada = True

            # busco él, id del registro del ticket de solicitud para agregarlo al registro de adjuntos
            soporte = self.env['sicpro.app.soporte'].search([('numero_consecutivo', '=', self.numero_consecutivo)])
            # busco los adjuntos para pasarlos a la bitácora
            attachment_id = self.env['ir.attachment'].search(
                ['&', ('res_id', '=', soporte.id), ('res_model', '=', 'sicpro.app.soporte')])

            attachement_values_list = []
            for item in attachment_id:
                attachement_values = {'name': item.name, 'datas': item.datas, 'type': 'binary', 'res_id': bitacora.id,
                                      'res_model': 'sicpro.app.soporte.bitacora', }
                attachement_values_list.append(attachement_values)
            new_attachments = self.env['ir.attachment'].create(attachement_values_list)

            # desactivo al usuario
            if self.tipo_movimiento == 'baja':
                usuario.sudo().active = False
                usuario.sudo().partner_id.active = False

            # actualizo el usuario del ticket
            if self.tipo_movimiento == 'alta':
                soporte.partner_user_id = usuario.id

            return new_attachments

    # ver la bitácora del usuario
    def ver_bitacora(self):
        domain = [('numero_consecutivo', '=', self.numero_consecutivo)]
        return {'name': _('Bitácora del Usuario'), 'domain': domain, 'res_model': 'sicpro.app.soporte.bitacora',
                'type': 'ir.actions.act_window', 'view_id': False, 'view_mode': 'tree,form', 'limit': 80, }

    # heredo el método completo de 'create' para agregar las funcionalidades que necesito en soporte
    @api.model
    def create(self, vals):
        res = super(PlantillaAccesoRoles, self).create(vals)
        # al crear el registro busco si existe el usuario en el sistema
        res.buscar_usuario_roles()
        # al crear el registro busco si existe el inversionista en el sistema
        res.buscar_inversionista()

        # busco los usuarios con permisos a recibir los correos de alerta
        usuarios = self.env['res.users'].sudo().search(
            [('groups_id', 'in', self.env.ref('sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])

        for item in usuarios:
            # agrego los seguidores al modelo
            res.message_subscribe(partner_ids=item.partner_id.ids)
            # envió la notificación a los seguidores
            res.message_post(body='Nueva Solicitud', subtype_xmlid='mail.mt_comment',
                             author_id=self.env.user.partner_id.id)

        # creo el ticket de soporte
        numero_consecutivo = vals['numero_consecutivo']
        correo = vals['email']
        user_id = self.env['res.users'].search(['|', ('active', '=', True), ('active', '=', False),
                                                ('email', '=', correo)])
        tipo = vals['tipo_movimiento']
        titulo = 'Gestión de Solicitudes de Accesos - Tipo: ' + tipo
        descripcion1 = 'El trabajador ' + correo + ' ha solicitado la siguiente acción de usuario ' + tipo + '.'
        descripcion = '<span style="font-weight: bolder; font-size: 18px;">El trabajador</span> ' \
                      '<span style="font-weight: bolder; font-size: 18px;"><u><font style="color: rgb(0, 0, 255);">' \
                      + correo + '</font></u></span> <span style="font-weight: bolder; font-size: 18px;">' \
                                 'ha solicitado la siguiente acción de usuario: </span> ' \
                                 '<span style="font-weight: bolder; font-size: 18px;">' + tipo + \
                      '</span><span style="font-weight: bolder; font-size: 18px;">.</span>'
        # buscar el canal de comunicación
        canal = self.env['sicpro.app.soporte.canales'].search([('code', '=', 'ticket_acceso')]).id
        # buscar el equipo de soporte
        equipo = self.env['sicpro.app.soporte.equipos'].search([('bitacora', '=', True)]).id
        # buscar el módulo base
        nucleo = self.env['sicpro.app.soporte.aplicaciones'].search([('modulo_base', '=', True)]).id
        # buscar las etiquetas pertenecientes a las solicitudes de accesos
        etiquetas = []
        tag_ids = self.env['sicpro.app.soporte.etiquetas'].search([('solicitudes_acceso', '=', True)])
        for item in tag_ids:
            etiquetas.append(item.id)

        # buscar la versión de la actualización
        version_estado = self.env['sicpro.app.soporte.estados.versiones'].search([('inicial', '=', True)]).id
        print(version_estado)
        version = self.env['sicpro.app.soporte.versiones'].search([('stage_id', '=', version_estado)],
                                                                  limit=1, order='id ASC').id

        # compruebo que exista el usuario en el sistema
        if not user_id:
            user_id = self.env['res.users'].search([('email', '=', 'sicproerp@etecsa.cu')])

        # creo el registro de la solicitud de soporte técnico
        ticket = self.env['sicpro.app.soporte'].create(
            {'name': titulo, 'partner_user_id': user_id.id, 'channel_id': canal, 'priority': '2', 'team_id': equipo,
             'numero_consecutivo': numero_consecutivo, 'descripcion': descripcion, 'id_solicitud_acceso': res.id,
             'aplicaciones': nucleo, 'tag_ids': [(6, 0, etiquetas)], 'version_id': version})

        # agrego al creador del correo como seguidor del registro
        partner_ids = user_id.partner_id.ids
        ticket.message_subscribe(partner_ids=list(partner_ids))

        return res
