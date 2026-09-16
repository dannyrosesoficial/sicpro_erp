# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class RegistroWebController(http.Controller):

    @http.route('/sicpro/registro/', auth="public", website=True,
                sitemap=False)
    def index_registro(self, **kwargs):
        """Carga la base del template SPA"""
        return request.render(
            "sicpro_modulo_web_registro.web_plantilla_registro")

    @http.route('/sicpro/get_user_info', type='jsonrpc', auth="public",
                methods=['POST'], website=True, csrf=False)
    def get_user_info(self, correo, **kwargs):
        _logger.info(">>> Consultando info para: %s", correo)

        dic = {'existe': False, 'archivado': False, 'datos': {},
               'roles_internos': [], 'roles_especiales': [],
               'roles_externos_auto': []}

        try:
            # 1. CARGAR CONFIGURACIÓN DE AUTOMATIZACIÓN E IS_DEFAULT
            config_roles_web = request.env[
                'sicpro.modulo.web.registro.roles'].sudo().search(
                [('active', '=', True)])

            for config in config_roles_web:
                roles_list_tech = []
                default_rol_for_app = ""  # Variable para capturar el rol por defecto de esta config

                for r in config.roles:
                    tech_name = r.nombre_registro or (r.name.split(':')[
                                                          -1].strip() if ':' in r.name else r.name)

                    # Verificamos si el rol tiene marcado is_default
                    is_def = getattr(r, 'is_default', False)
                    if is_def:
                        default_rol_for_app = tech_name

                    roles_list_tech.append(
                        {'app': config.name, 'rol': tech_name,
                         'is_default': is_def})

                dic['roles_externos_auto'].append({
                    'automatizar_usuario_externo': config.automatizar_usuario_externo,
                    'app_name': config.name, 'roles_list': roles_list_tech,
                    'default_rol': default_rol_for_app
                    # Se envía al JS para pre-seleccionar
                })

            # 2. BÚSQUEDA DEL USUARIO EN SICPRO
            usuario = request.env['res.users'].sudo().search(
                ['|', ('active', '=', True), ('active', '=', False),
                 ('email', '=', correo)], limit=1)

            if usuario:
                dic['existe'] = True
                dic['archivado'] = not usuario.active

                # Carga de datos básicos
                es_inv = getattr(usuario, 'user_inversionista', False)
                if es_inv:
                    dic['datos'] = {
                        'nombre_apellidos': usuario.nombre_inversionista.name if usuario.nombre_inversionista else '',
                        'cargo': usuario.inversionista_cargo,
                        'area': usuario.inversionista_territorio.name if usuario.inversionista_territorio else '',
                        'uo': usuario.company_id.identificador_corto,
                        'codigo_sap': usuario.pep}
                else:
                    dic['datos'] = {
                        'nombre_apellidos': usuario.trabajador.name if getattr(
                            usuario, 'trabajador', False) else usuario.name,
                        'cargo': usuario.ocupacion_id.name.name if getattr(
                            usuario, 'ocupacion_id', False) else '',
                        'area': usuario.departamento.name if getattr(usuario,
                                                                     'departamento',
                                                                     False) else '',
                        'uo': usuario.company_id.identificador_corto,
                        'codigo_sap': getattr(usuario, 'pep', '')}

                # 3. EXTRACCIÓN DE ROLES ACTUALES DEL USUARIO
                lineas_activas = usuario.role_line_ids.sudo().filtered(
                    lambda l: l.is_enabled)

                for linea in lineas_activas:
                    rol = linea.role_id
                    tech_name = rol.nombre_registro or (rol.name.split(':')[
                                                            -1].strip() if ':' in rol.name else rol.name)

                    if rol.roles_especiales:
                        dic['roles_especiales'].append(tech_name)
                    else:
                        for config in config_roles_web:
                            if rol.id in config.roles.sudo().ids:
                                dic['roles_internos'].append(
                                    {'app': config.name, 'rol': tech_name})
                                break
            else:
                # 4. BÚSQUEDA EN LDAP SI NO EXISTE EN SICPRO
                ldap = request.env[
                    'sicpro.app.modulo.ldap.registros'].sudo().search(
                    [('active', '=', True), ('mail', '=', correo)], limit=1)

                if ldap:
                    dic['datos'] = {'nombre_apellidos': ldap.cn,
                                    'codigo_sap': ldap.employeeNumber,
                                    'cargo': ldap.title,
                                    'area': ldap.departmentNumber,
                                    'uo': ldap.ou}

            return {'status': 'success', 'data': dic}

        except Exception as e:
            _logger.error("Error crítico en get_user_info: %s", str(e))
            return {'status': 'error', 'message': str(e)}

    @http.route('/sicpro/verificar_identidad', type='jsonrpc', auth="public",
                methods=['POST'], website=True)
    def verificar_identidad(self, email, **kwargs):
        """
        Lógica centralizada de verificación.
        Busca primero en Usuarios de Odoo, luego en LDAP.
        """
        # 1. Buscar en res.users (Incluye activos y archivados)
        user = request.env['res.users'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False),
                ('email', '=', email)], limit=1)

        if user:
            es_inv = getattr(user, 'user_inversionista', False)
            return {'status': 'success', 'origen': 'odoo',
                'active': user.active, 'datos': {
                    'nombre': user.nombre_inversionista.name if es_inv else user.trabajador.name,
                    'id_trabajador': user.pep or '',
                    'cargo': user.inversionista_cargo if es_inv else (
                        user.ocupacion_id.name.name if user.ocupacion_id else ''),
                    'area': user.inversionista_territorio.name if es_inv else (
                        user.departamento.name if user.departamento else ''),
                    'uo': user.company_id.identificador_corto or '',
                    'correo': user.email}}

        # 2. Si no existe, buscar en el LDAP de SICPRO
        ldap_record = request.env[
            'sicpro.app.modulo.ldap.registros'].sudo().search(
            [('active', '=', True), ('mail', '=', email)], limit=1)

        if ldap_record:
            return {'status': 'success', 'origen': 'ldap',
                'datos': {'nombre': ldap_record.cn,
                    'id_trabajador': ldap_record.employeeNumber or '',
                    'cargo': ldap_record.title or '',
                    'area': ldap_record.departmentNumber or '',
                    'uo': ldap_record.ou or '', 'correo': ldap_record.mail}}

        # 3. No encontrado
        return {'status': 'not_found',
            'message': 'El usuario no se encuentra registrado en el LDAP '
                       'Empresarial.'}

    @http.route('/sicpro/get_roles_data', type='jsonrpc', auth="public",
                website=True)
    def get_roles_data(self, email, tipo, solicitud, **kwargs):
        roles_data = {'internos': [], 'externos': [], 'especiales': [],
                      'disponibles_especiales': []}

        # 1. SIEMPRE cargar todos los roles que son "especiales" para que la web los dibuje
        especiales_disponibles = request.env['res.users.role'].sudo().search(
            [('active', '=', True), ('roles_especiales', '=', True)])
        for spec in especiales_disponibles:
            roles_data['disponibles_especiales'].append(
                {'id': spec.id, 'nombre': spec.nombre_registro or spec.name,
                 'tecnico': spec.nombre_registro  # El 'name' para el input
                 })

        # Lógica para Usuarios Externos
        if tipo == 'externo':
            roles_ids = request.env['res.users.role'].sudo().search(
                [('active', '=', True),
                 ('automatizar_usuario_externo', '=', True)])
            for role in roles_ids:
                reg_ids = request.env[
                    'sicpro.modulo.web.registro.roles'].sudo().search(
                    [('active', '=', True), ('roles', 'in', role.id)])
                if reg_ids:
                    roles_data['externos'].append(
                        [reg_ids[0].name, role.nombre_registro])

        # Lógica para Usuarios Internos (Modificación/Reinicio/Eliminación)
        if tipo == 'interno' and solicitud in ['modificar', 'reiniciar',
                                               'eliminar']:
            user = request.env['res.users'].sudo().search(
                [('email', '=', email)], limit=1)
            if user:
                for role in user.role_ids:
                    reg_ids = request.env[
                        'sicpro.modulo.web.registro.roles'].sudo().search(
                        [('active', '=', True), ('roles', 'in', role.id)])
                    if reg_ids:
                        roles_data['internos'].append(
                            [reg_ids[0].name, role.nombre_registro])

                    # Roles que el usuario YA TIENE marcados
                    if role.roles_especiales:
                        roles_data['especiales'].append(role.nombre_registro)

        return roles_data

    @http.route('/sicpro/registro_submit', type='jsonrpc', auth="public",
                methods=['POST'], website=True, csrf=False)
    def registro_submit(self, vals, **kwargs):
        _logger.info(">>> Procesando Registro SICPRO. Datos: %s", vals)
        try:
            # --- VALIDACIÓN DE MÍNIMO 2 ROLES DE APLICACIÓN (Excluye Especiales) ---
            solicitud_tipo = vals.get('solicitud')
            if solicitud_tipo in ['crear', 'modificar']:
                conteo_roles_app = 0

                # Campos técnicos y personales que NO deben contarse como roles
                campos_no_roles = ['nombre', 'carnet', 'nivel', 'cargo',
                                   'area', 'uo', 'plaza', 'tipo_usuario',
                                   'contacto', 'correo',
                                   'detalles_uso_sistema', 'solicitud',
                                   'nombre_jefe_inmediato',
                                   'cargo_jefe_inmediato', 'uo_jefe_inmediato',
                                   'telefono_jefe_inmediato',
                                   'nombre_director', 'cargo_director',
                                   'uo_director', 'telefono_director',
                                   'permisos_especiales_lista',
                                   'detalles_permisos_especiales']

                # Obtenemos los nombres técnicos de las aplicaciones configuradas en Odoo
                # para asegurar que solo contamos lo que es un selector de rol
                nombres_apps_validas = request.env[
                    'sicpro.modulo.web.registro.roles'].sudo().search(
                    []).mapped('name')

                for k, v in vals.items():
                    # Validamos que la clave pertenezca a una App y tenga un valor seleccionado
                    if k in nombres_apps_validas and v and k not in campos_no_roles:
                        conteo_roles_app += 1

                if conteo_roles_app < 2:
                    return {'status': 'error',
                            'message': 'Validación: Debe seleccionar al menos 2 Roles de Aplicación. '
                                       'Los permisos especiales no cuentan para este mínimo.'}
            # -----------------------------------------------------------------

            # 1. Generar Consecutivo
            secuencia_final = request.env['ir.sequence'].sudo().next_by_code(
                'plantilla_acceso_numero_consecutivo') or "S-PENDIENTE"

            # 2. Mapear movimiento
            mov_map = {'crear': 'alta', 'modificar': 'modificacion',
                       'reiniciar': 'reinicio', 'eliminar': 'baja'}
            tipo_movimiento = mov_map.get(solicitud_tipo, 'alta')

            # 3. Crear Registro Principal
            data = {'name': vals.get('nombre'),
                    'carne_identidad': vals.get('carnet'),
                    'nivel_escolar': vals.get('nivel'),
                    'cargo': vals.get('cargo'), 'area': vals.get('area'),
                    'uo': vals.get('uo'), 'codigo_sap': vals.get('plaza'),
                    'tipo_usuario': vals.get('tipo_usuario'),
                    'telefonos': vals.get('contacto'),
                    'email': vals.get('correo'),
                    'fundamentacion_especificaciones': vals.get(
                        'detalles_uso_sistema'),
                    'fundamentacion_especiales': vals.get(
                        'detalles_permisos_especiales'),
                    'solicitado_por_nombre_apellidos': vals.get(
                        'nombre_jefe_inmediato'),
                    'solicitado_por_cargo': vals.get('cargo_jefe_inmediato'),
                    'solicitado_por_unidad_organizativa': vals.get(
                        'uo_jefe_inmediato'),
                    'solicitado_por_telefono': vals.get(
                        'telefono_jefe_inmediato'),
                    'autorizado_por_nombre_apellidos': vals.get(
                        'nombre_director'),
                    'autorizado_por_cargo': vals.get('cargo_director'),
                    'autorizado_por_unidad_organizativa': vals.get(
                        'uo_director'),
                    'autorizado_por_telefono': vals.get('telefono_director'),
                    'tipo_movimiento': tipo_movimiento,
                    'numero_consecutivo': secuencia_final,
                    'estado': 'pendiente', }

            # 4. Archivar anteriores pendientes
            request.env['sicpro.modulo.solicitud.acceso'].sudo().search(
                [('email', '=', vals.get('correo')),
                 ('estado', '=', 'pendiente')]).write(
                {'estado': 'rechazado', 'rechazado': True,
                 'rechazado_motivo': 'Sustituida por nueva solicitud.'})

            solicitud_creada = request.env[
                'sicpro.modulo.solicitud.acceso'].sudo().create(data)
            planilla_id = solicitud_creada.id

            # 5. Procesar Roles (Aplicaciones)
            roles_para_crear = []
            registros_roles_web = request.env[
                'sicpro.modulo.web.registro.roles'].sudo().search(
                [('active', '=', True)])

            for k, v in vals.items():
                if not v: continue
                categoria = registros_roles_web.filtered(lambda r: r.name == k)
                if categoria:
                    rol_especifico = categoria.roles.filtered(
                        lambda x: x.nombre_registro == v)
                    if rol_especifico:
                        roles_para_crear.append(
                            {'role_id': rol_especifico[0].id,
                             'planilla_id': planilla_id})

            # 6. Roles Especiales (Checkboxes) - SE PROCESAN PERO NO SUMAN AL MÍNIMO
            nombres_especiales = vals.get('permisos_especiales_lista', [])
            if nombres_especiales:
                roles_sp_bd = request.env['res.users.role'].sudo().search(
                    [('active', '=', True), ('roles_especiales', '=', True),
                     ('nombre_registro', 'in', nombres_especiales)])
                for r_sp in roles_sp_bd:
                    roles_para_crear.append(
                        {'role_id': r_sp.id, 'planilla_id': planilla_id})

            if roles_para_crear:
                request.env[
                    'sicpro.modulo.solicitud.acceso.roles'].sudo().create(
                    roles_para_crear)

            # 7. Email
            try:
                template = request.env.ref(
                    'sicpro_modulo_web_registro.solicitud_acceso_roles_creada')
                if template:
                    template.sudo().send_mail(solicitud_creada.id,
                                              force_send=True)
            except Exception as mail_err:
                _logger.error("Error enviando correo: %s", str(mail_err))

            return {'status': 'success', 'consecutivo': secuencia_final}

        except Exception as e:
            request.env.cr.rollback()
            _logger.error("Error crítico en registro_submit: %s", str(e))
            return {'status': 'error', 'message': str(e)}
