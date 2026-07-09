# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import timedelta, datetime

from odoo import api, fields, models
# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class SolicitudAccesoRoles(models.Model):
    _name = 'sicpro.modulo.solicitud.acceso'
    _description = "Planilla de Acceso"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id desc'

    # --- CAMPOS DE IDENTIFICACIÓN Y ESTADO ---
    name = fields.Char(string='Nombre y Apellidos', required=True)
    active = fields.Boolean(string="Activo", default=True, index=True)
    estado = fields.Selection(string='Estado',
                              selection=[('pendiente', 'Pendiente'),
                                         ('ejecutado', 'Ejecutado'),
                                         ('rechazado', 'Rechazado')],
                              default="pendiente", required=True)
    existe_usuario = fields.Boolean(string='Existe_usuario', required=False)
    existe_inversionista = fields.Boolean(string='Existe_inversionista',
                                          required=False)
    numero_consecutivo = fields.Char(string='Número Consecutivo')
    codigo_sap = fields.Char(string='Código SAP', required=True, size=10)

    tipo_movimiento = fields.Selection(string='Tipo de Solicitud',
                                       selection=[('alta', 'Alta'), (
                                           'modificacion', 'Modificación'), (
                                                      'reinicio',
                                                      'Reinicialización'),
                                                  ('baja', 'Baja')],
                                       required=False)

    rechazado = fields.Boolean(string='Rechazado', default=False,
                               required=False)
    correo_actualizacion_roles = fields.Boolean(string='correo_act_roles',
                                                default=False, required=False)
    rechazado_motivo = fields.Text(string='Fundamentación del Rechazo')
    company_id = fields.Many2one('res.company', string='Proceso', index=True,
                                 readonly=True,
                                 default=lambda self: self.env.company.id)
    fecha_recibido = fields.Datetime(string='Documentación Recibida',
                                     required=False)
    # --- DATOS DEL SOLICITANTE ---
    carne_identidad = fields.Char(string='Carne de Identidad')
    nivel_escolar = fields.Char(string='Nivel Escolar')
    area = fields.Char(string='Área')
    uo = fields.Char(string='Unidad Organizativa')
    cargo = fields.Char(string='Cargo')
    telefonos = fields.Char(string='Teléfono(s)')
    email = fields.Char(string='Correo Electrónico')
    tipo_usuario = fields.Selection(string='Tipo de Usuario',
                                    selection=[('interno', 'Interno'),
                                               ('externo', 'Externo')],
                                    required=True)

    # --- ROLES Y PERMISOS ---
    role_line_ids = fields.One2many(
        comodel_name="sicpro.modulo.solicitud.acceso.roles",
        inverse_name="planilla_id", string="Grupo de Roles")

    role_ids = fields.One2many(comodel_name="res.users.role", string="Roles",
                               compute="_compute_role_ids")
    fecha_inicio = fields.Date(string='Fecha Inicio', required=False)
    fecha_fin = fields.Date(string='Fecha Fin', required=False)
    fundamentacion_especificaciones = fields.Text(
        string='Fundamentación y especificaciones')
    fundamentacion_especiales = fields.Text(
        string='Fundamentación permisos especiales')
    # --- AUDITORÍA DE SOLICITUD ---
    solicitado_por_nombre_apellidos = fields.Char(
        string='Solicitado Por: Nombre y Apellidos')
    solicitado_por_cargo = fields.Char(string='Solicitado Por: Cargo')
    solicitado_por_unidad_organizativa = fields.Char(
        string='Solicitado Por: Unidad Organizativa')
    solicitado_por_fecha = fields.Date(string='Solicitado Por: Fecha',
                                       default=fields.Date.context_today)
    solicitado_por_telefono = fields.Char(string='Solicitado Por: Teléfono')
    # --- AUDITORÍA DE AUTORIZACIÓN ---
    autorizado_por_nombre_apellidos = fields.Char(
        string='Autorizado Por: Nombre y Apellidos')
    autorizado_por_cargo = fields.Char(string='Autorizado Por: Cargo')
    autorizado_por_unidad_organizativa = fields.Char(
        string='Autorizado Por: Unidad Organizativa')
    autorizado_por_fecha = fields.Date(string='Autorizado Por: Fecha',
                                       default=fields.Date.context_today)
    autorizado_por_telefono = fields.Char(string='Autorizado Por: Teléfono')

    # --- MÉTODOS DE GENERACIÓN HTML ---
    def buscar_registro_roles(self, registro_id):
        roles = []
        registros = []
        td_html = []
        registros_ids = self.env[
            'sicpro.modulo.web.registro.roles'].sudo().search(
            [('active', '=', True)])
        solicitud_id = self.env[
            'sicpro.modulo.solicitud.acceso.roles'].sudo().search(
            [('planilla_id', '=', registro_id)])

        for item in registros_ids:
            valor = {'nombre': item.name, 'rol': '-'}
            registros.append(valor)

        for item in registros_ids:
            for var in item.roles:
                for value in solicitud_id.role_id:
                    if var.name == value.name:
                        valor = {'nombre': item.name,
                                 'rol': value.nombre_registro}
                        roles.append(valor)

        for item in registros:
            for value in roles:
                if item['nombre'] in value['nombre']:
                    item.update({'rol': value['rol']})

        for td in registros:
            data_td = {
                '<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px'
                ' solid #000000; border-right: 1px solid #000000" colspan="3" align="center" valign="middle"'
                ' height="28"><font size="3" face="Liberation Serif">' + td[
                    'nombre'] + '</font></td>'
                                '<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px'
                                ' solid #000000; border-right: 1px solid #000000" colspan="3" align="left" valign="middle">'
                                '<font size="3" style="margin-left:5px;" face="Liberation Serif">' +
                td['rol'] + '</font></td>'}
            td_html.append(data_td)

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

        return data_html.replace("'", "")

    # --- MÉTODOS DE BÚSQUEDA Y VALIDACIÓN ---
    def buscar_usuario_roles(self):
        usuario = self.env['res.users'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False),
             ('email', '=', self.email)])
        if usuario:
            self.existe_usuario = True
            for item in self.role_line_ids:
                item.user_id = usuario.id
        else:
            self.existe_usuario = False
            for item in self.role_line_ids:
                item.user_id = False

    def buscar_inversionista(self):
        inversionista = self.env['sicpro.app.clientes'].sudo().search(
            ['&', ('active', '=', True), ('correo', '=', self.email)])
        if inversionista:
            self.existe_inversionista = True
        else:
            self.existe_inversionista = False

    def buscar_usuario_inversionista(self):
        self.buscar_inversionista()
        self.buscar_usuario_roles()

    def correo_actualiza_roles(self):
        self.correo_actualizacion_roles = True
        usuario_id = self.env['res.users'].sudo().search(
            [('email', '=', self.email)], limit=1).id
        if usuario_id:
            template = self.env.ref(
                'sicpro_app_administracion.plantilla_actualizacion_roles')
            template.send_mail(usuario_id, force_send=True)

    # --- ACCIONES DE EJECUCIÓN (BOTONES) ---
    def actualizar_usuario_roles_aprobar(self):
        roles = []
        data_rol = self.env[
            'sicpro.modulo.solicitud.acceso.roles'].sudo().search(
            [('planilla_id', '=', self.id), ('aprobado', '=', True)])
        usuario = self.env['res.users'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False),
             ('email', '=', self.email)], limit=1)

        if not self.fecha_recibido:
            raise ValidationError(
                "¡Para aprobar la solicitud debe agregar la fecha de entrega de la documentación.\n\n" + MSG_SOPORTE_SICPRO)

        if not usuario:
            raise ValidationError(
                "¡No se encontró el usuario en el sistema!\n\n" + MSG_SOPORTE_SICPRO)

        if self.tipo_movimiento == 'baja':
            usuario.role_line_ids = [(5, 0, 0)]
            rol_id = self.env['res.users.role'].sudo().search(
                [('nombre_registro', '=', 'Eliminar accesos de usuarios')],
                limit=1).id
            rol_data = {'role_id': rol_id, 'user_id': usuario.id,
                        'date_from': fields.Date.today(),
                        'date_to': fields.Date.today()}
            roles.append(rol_data)
            self.env['res.users.role.line'].create(roles)
            self.estado = 'ejecutado'
        else:
            usuario.sudo().active = True
            if usuario.sudo().partner_id:
                usuario.sudo().partner_id.active = True

            if data_rol:
                usuario.role_line_ids = [(5, 0, 0)]
                for item in data_rol:
                    rol_data = {'role_id': item.role_id.id,
                                'user_id': item.user_id.id,
                                'date_from': item.desde,
                                'date_to': item.hasta, }
                    roles.append(rol_data)

                self.env['res.users.role.line'].create(roles)

                # Inserción en log para refrescar conteo de seguridad
                date_sql = datetime.now()
                self._cr.execute(
                    'INSERT INTO res_users_log (create_uid, create_date, write_uid, write_date) VALUES (%s, %s, %s, %s)',
                    (usuario.id, date_sql, usuario.id, date_sql))

                # Limpieza de duplicados en log
                self._cr.execute("""DELETE FROM res_users_log log1 WHERE EXISTS (SELECT 1 FROM res_users_log log2
                                WHERE log1.create_uid = log2.create_uid AND log1.create_date < log2.create_date)""")

                self.correo_actualiza_roles()
                self.estado = 'ejecutado'
                usuario.sudo().set_groups_from_roles()
            else:
                raise ValidationError(
                    "¡Debe seleccionar los roles que se le asignaran al usuario!.\n\n" + MSG_SOPORTE_SICPRO)

    def actualizar_fecha_roles(self):
        usuario = self.env['res.users'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False),
             ('email', '=', self.email)], limit=1)
        if usuario:
            self.existe_usuario = True
            for item in self.role_line_ids:
                item.desde = self.fecha_inicio
                item.hasta = self.fecha_fin
                item.user_id = usuario.id
        else:
            raise ValidationError(
                "¡Imposible actualizar fechas y usuarios, no se encontró un usuario con el número de plaza actual.")

    # --- ONCHANGES Y COMPUTES ---
    @api.onchange('fecha_inicio')
    def _onchange_fecha_inicio(self):
        if self.fecha_inicio:
            self.fecha_fin = self.fecha_inicio + timedelta(days=365)

    @api.depends("role_line_ids.role_id")
    def _compute_role_ids(self):
        for user in self:
            user.role_ids = user.role_line_ids.mapped("role_id")

    def planilla_busca_roles(self):
        roles = self.env['res.users.role'].sudo().search(
            [('active', '=', True)])
        roles_ids = []
        for item in roles:
            nombre_rol = item['name'].split(':')
            nombre_rol[0] = nombre_rol[0].strip()
            if len(nombre_rol) > 1:
                nombre_rol[1] = nombre_rol[1].strip()
                data = {'name': nombre_rol[1], 'aplicativo': nombre_rol[0],
                        'clave_solicitud': item['clave_solicitud'],
                        'descripcion': item['descripcion'], }
                roles_ids.append(data)
        return roles_ids

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numero_consecutivo') or vals.get(
                'numero_consecutivo') == '/':
                vals['numero_consecutivo'] = self.env[
                                                 'ir.sequence'].next_by_code(
                    'plantilla_acceso_numero_consecutivo') or '/'
        return super(SolicitudAccesoRoles, self).create(vals_list)


# cancelar solicitud
class SolicitudAccesoRechazar(models.TransientModel):
    _name = 'sicpro.modulo.solicitud.acceso.rechazar'
    _description = 'Plantilla de acceso rechazada'

    motivo_rechazo = fields.Text(string="Motivo de Rechazo", required=True, )
    company_id = fields.Many2one('res.company', string='Proceso', index=True,
                                 readonly=True,
                                 default=lambda self: self.env.company.id)

    def action_motivo_rechazo(self):
        # cambio el estado interno de la solicitud
        solicitud = self.env['sicpro.modulo.solicitud.acceso'].browse(
            self.env.context.get('active_ids'))
        for item in solicitud:
            item.rechazado_motivo = self.motivo_rechazo
            item.rechazado = True
            item.estado = 'rechazado'

        # envío el correo electrónico
        post = self.env['sicpro.modulo.solicitud.acceso'].browse(
            self.env.context.get('active_ids'))
        email_values = {'email_to': post.email, }
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_modulo_web_registro.solicitud_acceso_roles_rechazada')
        template.with_context(local_context).send_mail(post.id,
                                                       force_send=True,
                                                       email_values=email_values)

        # redirecciono la salida
        action = self.env.ref(
            'sicpro_modulo_web_registro.action_solicitud_roles').sudo().read()[
            0]
        return action
