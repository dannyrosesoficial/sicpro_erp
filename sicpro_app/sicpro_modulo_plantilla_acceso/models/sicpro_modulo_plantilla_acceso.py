# -*- coding: utf-8 -*-

from datetime import timedelta, datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PlantillaAccesoRoles(models.Model):
    _name = 'sicpro.modulo.plantilla.acceso'
    _description = "Planilla de Acceso"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id desc'

    # id del registro
    id = fields.Id()

    name = fields.Char(string='Nombre y Apellidos', required=True)
    active = fields.Boolean(string="Activo", default=True)
    estado = fields.Selection(string='Estado', selection=[('pendiente', 'Pendiente'), ('ejecutado', 'Ejecutado'),
                                                          ('rechazado', 'Rechazado'), ], default="pendiente",
                              required=True, )
    existe_usuario = fields.Boolean(string='Existe_usuario', required=False)
    existe_inversionista = fields.Boolean(string='Existe_inversionista', required=False)
    numero_consecutivo = fields.Char(string='Número Consecutivo')
    codigo_sap = fields.Char(string='Código SAP', required=True, size=10)
    tipo_movimiento = fields.Selection(string='Tipo de Solicitud',
                                       selection=[('alta', 'Alta'), ('modificacion', 'Modificación'),
                                                  ('reinicio', 'Reinicialización'), ('baja', 'Baja'), ],
                                       required=False, )
    rechazado = fields.Boolean(string='Rechazado', default=False, required=False)
    correo_actualizacion_roles = fields.Boolean(string='correo_act_roles', default=False, required=False)
    rechazado_motivo = fields.Text(string='Fundamentación del Rechazo')
    company_id = fields.Many2one('res.company', string='Proceso', index=True, readonly=True,
                                 default=lambda self: self.env.company.id)
    fecha_recibido = fields.Datetime(string='Documentación Recibida', required=False)
    carne_identidad = fields.Char(string='Carne de Identidad')
    nivel_escolar = fields.Char(string='Nivel Escolar')
    area = fields.Char(string='Área')
    uo = fields.Char(string='Unidad Organizativa')
    cargo = fields.Char(string='Cargo')
    telefonos = fields.Char(string='Teléfono(s)')
    email = fields.Char(string='Correo Electrónico')
    tipo_usuario = fields.Selection(string='Tipo de Usuario',
                                    selection=[('interno', 'Interno'), ('externo', 'Externo'), ], required=True, )
    ####################################################################################################################
    ################# ROLES y PERMISOS #################################################################################
    ####################################################################################################################
    role_line_ids = fields.One2many(comodel_name="sicpro.modulo.plantilla.acceso.roles", inverse_name="planilla_id",
                                    string="Grupo de Roles", )
    role_ids = fields.One2many(comodel_name="sicpro.modulo.roles", string="Roles", compute="_compute_role_ids")
    fecha_inicio = fields.Date(string='Fecha Inicio', required=False)
    fecha_fin = fields.Date(string='Fecha Fin', required=False)
    ####################################################################################################################
    ####################################################################################################################
    fundamentacion_especificaciones = fields.Text(string='Fundamentación y especificaciones')
    fundamentacion_especiales = fields.Text(string='Fundamentación permisos especiales')
    solicitado_por_nombre_apellidos = fields.Char(string='Solicitado Por: Nombre y Apellidos')
    solicitado_por_cargo = fields.Char(string='Solicitado Por: Cargo')
    solicitado_por_unidad_organizativa = fields.Char(string='Solicitado Por: Unidad Organizativa')
    solicitado_por_fecha = fields.Date(string='Solicitado Por: Fecha', default=fields.datetime.now())
    solicitado_por_telefono = fields.Char(string='Solicitado Por: Teléfono')
    autorizado_por_nombre_apellidos = fields.Char(string='Autorizado Por: Nombre y Apellidos')
    autorizado_por_cargo = fields.Char(string='Autorizado Por: Cargo')
    autorizado_por_unidad_organizativa = fields.Char(string='Autorizado Por: Unidad Organizativa')
    autorizado_por_fecha = fields.Date(string='Autorizado Por: Fecha', default=fields.datetime.now())
    autorizado_por_telefono = fields.Char(string='Autorizado Por: Teléfono')

    # busco el usuario en el sistema
    def buscar_usuario_roles(self):
        usuario = self.env['res.users'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False), ('email', '=', self.email)])
        if usuario:
            self.existe_usuario = True
            for item in self.role_line_ids:
                item.user_id = usuario.id
        else:
            self.existe_usuario = False
            for item in self.role_line_ids:
                item.user_id = None

    # busco el inversionista en el sistema
    def buscar_inversionista(self):
        inversionista = self.env['sicpro.app.clientes'].sudo().search(
            ['&', ('active', '=', True), ('correo', '=', self.email)])
        if inversionista:
            self.existe_inversionista = True
        else:
            self.existe_inversionista = False

    # acción para unificar la búsqueda de usuarios e inversionistas
    def buscar_usuario_inversionista(self):
        self.buscar_inversionista()
        self.buscar_usuario_roles()

    # envío actualización de roles
    def correo_actualiza_roles(self):
        self.correo_actualizacion_roles = True
        usuario = self.env['res.users'].sudo().search([('email', '=', self.email)]).id
        template = self.env.ref('sicpro_app_administracion.plantilla_actualizacion_roles')
        template.send_mail(usuario, force_send=True)

    # actualizo los roles en el usuario en aprobados (botón aprobar)
    def actualizar_usuario_roles_aprobar(self):
        roles = []
        data_rol = self.env['sicpro.modulo.plantilla.acceso.roles'].sudo().search(
            ['&', ('planilla_id', '=', self.id), ('aprobado', '=', True)])
        usuario = self.env['res.users'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False), ('email', '=', self.email)])

        # compruebo que exista la fecha de entrega
        if not self.fecha_recibido:
            raise ValidationError(_("¡Para aprobar la solicitud debe agregar la fecha de entrega de la documentación,"
                                    " verifíquelo!."))
        else:
            if self.tipo_movimiento == 'baja':
                # elimino los roles actuales del usuario
                usuario.role_line_ids = None
                # busco el rol especial de eliminar
                rol_id = self.env['sicpro.modulo.roles'].sudo().search(
                    [('nombre_registro', '=', 'Eliminar accesos de usuarios')]).id

                rol_data = {'role_id': rol_id, 'user_id': usuario.id, 'date_from': datetime.today(),
                            'date_to': datetime.today(), }
                roles.append(rol_data)
                # creo los roles en el usuario
                self.env['sicpro.modulo.roles.line'].create(roles)
                self.estado = 'ejecutado'
            else:
                # activo el usuario primeramente por si está archivado
                usuario.sudo().active = True
                usuario.sudo().partner_id.active = True
                if data_rol:
                    # elimino los roles actuales del usuario
                    usuario.role_line_ids = None

                    for item in data_rol:
                        rol_data = {'role_id': item.role_id.id, 'user_id': item.user_id.id, 'date_from': item.desde,
                                    'date_to': item.hasta, }
                        roles.append(rol_data)

                    # creo los roles en el usuario
                    self.env['sicpro.modulo.roles.line'].create(roles)
                    # Actualizo con la fecha actual el registro de user.log para que de comienzo el conteo
                    # de desactivación nuevamente
                    user_id_sql = usuario.id
                    date_sql = fields.Datetime.now()
                    self._cr.execute('INSERT INTO res_users_log (create_uid, create_date, write_uid, write_date) '
                                     'VALUES (%s, %s, %s, %s)', (user_id_sql, date_sql, user_id_sql, date_sql))
                    # eliminar duplicados de la tabla de res.user.log
                    self._cr.execute("""DELETE FROM res_users_log log1 WHERE EXISTS (SELECT 1 FROM res_users_log log2
                                WHERE log1.create_uid = log2.create_uid AND log1.create_date < log2.create_date)""")

                    # envío el correo de actualización de roles
                    self.correo_actualiza_roles()
                    self.estado = 'ejecutado'
                    # mando a actualizar los grupos de permisos según los roles seleccionados
                    usuario.sudo().set_groups_from_roles()
                else:
                    raise ValidationError(
                        _("¡Debe seleccionar los roles que se le asignaran al usuario, verifíquelo!."))

    # actualizo la fecha de los roles que serán asignados (botón Actualizar fechas y Usuario)
    def actualizar_fecha_roles(self):
        usuario = self.env['res.users'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False), ('email', '=', self.email)])
        if usuario:
            self.existe_usuario = True

            for item in self.role_line_ids:
                item.desde = self.fecha_inicio
                item.hasta = self.fecha_fin
                item.user_id = usuario.id
        else:
            raise ValidationError(_("¡Imposible actualizar fechas y usuarios, no se encontró un usuario con el número "
                                    " de plaza actual, verifíquelo!."))

    # pongo por defecto 1 año de validez para los roles
    @api.onchange('fecha_inicio')
    def _onchange_fecha_inicio(self):
        if self.fecha_inicio:
            self.fecha_fin = self.fecha_inicio + timedelta(days=365)

    # comprueba que no se repita la selección del mismo rol
    @api.depends("role_line_ids.role_id")
    def _compute_role_ids(self):
        for user in self:
            user.role_ids = user.role_line_ids.mapped("role_id")

    # buscar los roles para enviarlos a la planilla
    # determinar si se elimina, no se encuentra nada que llame a este método
    def planilla_busca_roles(self):
        roles = self.env['sicpro.modulo.roles'].sudo().search([('active', '=', True)])
        roles_ids = []

        for item in roles:
            nombre_rol = item['name'].split(':')
            nombre_rol[0] = nombre_rol[0].strip()
            if len(nombre_rol) > 1:
                nombre_rol[1] = nombre_rol[1].strip()

                data = {'name': nombre_rol[1], 'aplicativo': nombre_rol[0], 'clave_solicitud': item['clave_solicitud'],
                        'descripcion': item['descripcion'], }

                roles_ids.append(data)
        return roles_ids

    # la herencia de 'sicpro_modulo_plantilla_acceso_soporte_bitacora' cambia este método por completo
    # por lo que no se debe agregar ninguna funcionalidad nueva en este método, sino en la herencia.
    # @api.model
    # def create(self, vals):
    #     res = super(PlantillaAccesoRoles, self).create(vals)
    #     # al crear el registro busco si existe el usuario en el sistema
    #     res.buscar_usuario_roles()
    #     # al crear el registro busco si existe el inversionista en el sistema
    #     res.buscar_inversionista()
    #
    #     # busco los usuarios con permisos a recibir los correos de alerta
    #     usuarios = self.env['res.users'].sudo().search(
    #         [('groups_id', 'in', self.env.ref('sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])
    #
    #     for item in usuarios:
    #         # agrego los seguidores al modelo
    #         res.message_subscribe(partner_ids=item.partner_id.ids)
    #         # envió la notificación a los seguidores
    #         res.message_post(body='Nueva Solicitud', subtype_xmlid='mail.mt_comment',
    #                          author_id=self.env.user.partner_id.id)
    #
    #     # envío el correo electrónico (se deshabilita pq ya se envía de la herencia)
    #     # email_values = {'email_to': res.email, }
    #     # template = self.env.ref('sicpro_modulo_plantilla_acceso.solicitud_acceso_roles_creada')
    #     # template.send_mail(res.id, force_send=True, email_values=email_values,)
    #     return res


# cancelar solicitud
class PlantillaDeAccesoRechazar(models.TransientModel):
    _name = 'sicpro.modulo.plantilla.acceso.rechazar'
    _description = 'Plantilla de acceso rechazada'

    motivo_rechazo = fields.Text(string="Motivo de Rechazo", required=True, )
    company_id = fields.Many2one('res.company', string='Proceso', index=True, readonly=True,
                                 default=lambda self: self.env.company.id)

    def action_motivo_rechazo(self):
        # cambio el estado interno de la solicitud
        solicitud = self.env['sicpro.modulo.plantilla.acceso'].browse(self.env.context.get('active_ids'))
        for item in solicitud:
            item.rechazado_motivo = self.motivo_rechazo
            item.rechazado = True
            item.estado = 'rechazado'

        # envío el correo electrónico
        post = self.env['sicpro.modulo.plantilla.acceso'].browse(self.env.context.get('active_ids'))
        email_values = {'email_to': post.email, }
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_modulo_plantilla_acceso.solicitud_acceso_roles_rechazada')
        template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)

        # redirecciono la salida
        action = self.env.ref('sicpro_modulo_plantilla_acceso.action_solicitud_roles').sudo().read()[0]
        return action
