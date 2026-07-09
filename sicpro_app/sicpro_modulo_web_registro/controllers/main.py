# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request


class WebRegistros(http.Controller):

    # controller del inicio del registro
    @http.route('/web/registro/', auth="public", website=True)
    def plantilla_web_registro(self, **kwargs):
        dic = {}
        if 'ejecutar_aviso' in kwargs.keys():
            dic['ejecutar'] = kwargs['ejecutar_aviso']
        return request.render("sicpro_modulo_web_registro.web_plantilla_registro", dic)

    # controller de la verificación del usuario y la selección de la acción
    @http.route('/web/registro_selector/', auth="public", website=True)
    def plantilla_web_registro_selector(self, **kwargs):
        dic = {}

        # verífico que exista el correo
        if 'correo' in kwargs.keys():
            email = kwargs['correo']
            dic['tipo'] = kwargs['tipo']

            # busco si existe el usuario registrado
            usuario = request.env['res.users'].sudo().search(
                ['|', ('active', '=', True), ('active', '=', False), ('email', '=', email)])

            # verífico que el usuario ya exista
            if usuario:
                dic['codigo_sap'] = usuario['pep']
                dic['email'] = usuario['email']

                # verifico si el usuario es interno o externo
                if usuario.user_inversionista:
                    dic['nombre_apellidos'] = usuario['nombre_inversionista']['name']
                    dic['cargo'] = usuario['inversionista_cargo']
                    dic['area'] = usuario['inversionista_territorio']['name']
                    dic['uo'] = usuario['company_id']['identificador_corto']
                    dic['inversionista'] = True
                else:
                    dic['nombre_apellidos'] = usuario['trabajador']['name']
                    dic['cargo'] = usuario['ocupacion_id']['name']['name']
                    dic['area'] = usuario['departamento']['name']
                    dic['uo'] = usuario['company_id']['identificador_corto']
                    dic['inversionista'] = False

                # verífico el estado del usuario (activo o archivado)
                if usuario.active:
                    dic['ejecutar'] = 'usuario_sistema_true'
                else:
                    dic['ejecutar'] = 'usuario_sistema_false'
            else:
                # como el usuario no existe busco el trabajador en los registros ldap
                ldap = request.env['sicpro.app.modulo.ldap.registros'].sudo().search(
                    [('active', '=', True), ('mail', '=', email)])

                # verífico que el trabajador ya exista en los registros ldap
                if ldap:
                    dic['nombre_apellidos'] = ldap['cn']
                    dic['codigo_sap'] = ldap['employeeNumber']
                    dic['cargo'] = ldap['title']
                    dic['area'] = ldap['departmentNumber']
                    dic['email'] = ldap['mail']
                    dic['uo'] = ldap['ou']
                    dic['ejecutar'] = 'usuario_ldap_true'
                else:
                    # redirecciono a la pagina anterior
                    url = '/web/registro/' + '?ejecutar_aviso=usuario_ldap_false'
                    return request.redirect(url)

        return request.render("sicpro_modulo_web_registro.web_plantilla_registro_selector", dic)

    # controller para realizar la selección de los roles y permisos
    @http.route('/web/registro_planilla/', auth="public", website=True)
    def plantilla_web_registro_planilla(self, **kwargs):
        global data_rol
        dic = {}
        correo = kwargs['correo']
        solicitud = kwargs['solicitud']
        tipo = kwargs['tipo']
        estado = kwargs['estado']

        # por defecto los roles están habilitados
        dic['disabled_roles'] = ''

        # verífico el tipo de usuario y lo envío a la plantilla
        if tipo == 'interno':
            dic['tipo_nombre'] = 'Usuario DVPE'
            # verífico el tipo de solicitud solo para deshabilitar los roles
            if solicitud == 'reiniciar' or solicitud == 'eliminar':
                dic['disabled_roles'] = 'disabled'
        else:
            dic['tipo_nombre'] = 'Usuario Externo'
            # verífico el tipo de solicitud solo para deshabilitar los roles
            dic['disabled_roles'] = 'disabled'

        dic['solicitud'] = solicitud
        dic['tipo_value'] = tipo
        dic['correo'] = correo

        # acción para crear un usuario, busco los datos directamente en el registro del ldap
        if solicitud == 'crear':
            # busco los datos del trabajador en el ldap empresarial
            ldap = request.env['sicpro.app.modulo.ldap.registros'].sudo().search(
                [('active', '=', True), ('mail', '=', correo)])

            dic['nombre_apellidos'] = ldap['cn']
            dic['codigo_sap'] = ldap['employeeNumber']
            dic['cargo'] = ldap['title']
            dic['area'] = ldap['departmentNumber']
            dic['uo'] = ldap['ou']

        # acción para modificar/reiniciar/eliminar un usuario, busco los datos en el registro de usuarios
        if solicitud == 'modificar' or solicitud == 'reiniciar' or solicitud == 'eliminar':
            # busco los datos del usuario
            usuario = request.env['res.users'].sudo().search(
                ['|', ('active', '=', True), ('active', '=', False), ('email', '=', correo)])

            dic['codigo_sap'] = usuario['pep']
            # verifico si el usuario es interno o externo
            if usuario.user_inversionista:
                dic['nombre_apellidos'] = usuario['nombre_inversionista']['name']
                dic['cargo'] = usuario['inversionista_cargo']
                dic['area'] = usuario['inversionista_territorio']['name']
                dic['uo'] = usuario['company_id']['identificador_corto']
                dic['inversionista'] = True
            else:
                dic['nombre_apellidos'] = usuario['trabajador']['name']
                dic['cargo'] = usuario['ocupacion_id']['name']['name']
                dic['area'] = usuario['departamento']['name']
                dic['uo'] = usuario['company_id']['identificador_corto']
                dic['inversionista'] = False

        # género la selección de roles automatizados
        if tipo == 'externo':
            # género un diccionario con los valores de los roles externos
            roles_externos = []
            # busco los roles que usan los usuarios externos
            roles_ids = request.env['sicpro.modulo.roles'].sudo().search(
                ['&', ('active', '=', True), ('automatizar_usuario_externo', '=', True)])
            # creo el dic con los ajustes de los roles externos
            for value in roles_ids:
                # busco los registro donde se encuentra los roles_ids
                registros_ids = request.env['sicpro.modulo.web.registro.roles'].sudo().search(
                    ['&', ('active', '=', True), ('roles', 'in', value.id)])
                rol_data = ['app', 'rol']
                rol_data[0] = registros_ids.name
                rol_data[1] = value.nombre_registro
                roles_externos.append(rol_data)
            dic['roles_externos'] = roles_externos  # fin del diccionario con los valores de los roles externos
        else:
            # género un diccionario con los valores de los roles internos
            roles_internos = []
            # busco los roles que usan los usuarios externos
            roles_ids = request.env['res.users'].sudo().search(
                ['|', '&', ('active', '=', True), ('active', '=', False), ('email', '=', correo)]).role_ids
            # creo el dic con los ajustes de los roles externos
            for value in roles_ids:
                # busco los registro donde se encuentra los roles_ids
                registros_ids = request.env['sicpro.modulo.web.registro.roles'].sudo().search(
                    ['&', ('active', '=', True), ('roles', 'in', value.id)])
                rol_data = ['app', 'rol']
                rol_data[0] = registros_ids.name
                rol_data[1] = value.nombre_registro
                roles_internos.append(rol_data)
            dic['roles_internos'] = roles_internos
            # fin del diccionario con los valores de los roles interno

        # género un diccionario con los valores de los roles especiales
        roles_especiales = []
        # busco los roles que usan los usuarios externos
        roles_ids = request.env['res.users'].sudo().search(
            ['&', ('active', '=', True), ('email', '=', correo)]).role_ids
        # busco los roles especiales del usuario
        for value in roles_ids:
            # busco los registro que sean roles especiales
            if value.roles_especiales:
                roles_especiales.append(value.nombre_registro)
        dic['roles_especiales'] = roles_especiales
        # fin del diccionario con los valores de los roles especiales

        return request.render("sicpro_modulo_web_registro.web_plantilla_registro_planilla", dic)

    @http.route('/web/registro_crear/', auth="public", website=True)
    def plantilla_web_registro_crear(self, **kwargs):
        global tipo_movimiento
        vals = {}

        for key in kwargs.keys():
            field_temp = key
            vals[field_temp] = kwargs[key]

        # creo el consecutivo de la solicitud
        secuencia = request.env['ir.sequence'].sudo().search_read(
            [['code', '=', 'plantilla_acceso_numero_consecutivo']], ['number_next_actual', 'prefix', 'padding'])
        valor_secuencia = len(secuencia[0]['prefix']) + len(str(secuencia[0]['number_next_actual']))
        valor_esperado = len(secuencia[0]['prefix']) + secuencia[0]['padding']
        secuencia_final = secuencia[0]['prefix']
        if valor_secuencia < valor_esperado:
            diferencia = valor_esperado - valor_secuencia
            while diferencia > 0:
                secuencia_final += '0'
                diferencia -= 1
        secuencia_final += str(secuencia[0]['number_next_actual'])

        # genero el tipo de solicitud
        if vals['solicitud'] == 'crear':
            tipo_movimiento = 'alta'
        if vals['solicitud'] == 'modificar':
            tipo_movimiento = 'modificacion'
        if vals['solicitud'] == 'reiniciar':
            tipo_movimiento = 'reinicio'
        if vals['solicitud'] == 'eliminar':
            tipo_movimiento = 'baja'

        # creo el diccionario para enviar los datos
        data = {'name': vals['nombre'], 'carne_identidad': vals['carnet'], 'nivel_escolar': vals['nivel'],
                'cargo': vals['cargo'], 'area': vals['area'], 'uo': vals['uo'], 'codigo_sap': vals['plaza'],
                'tipo_usuario': vals['tipo_usuario'], 'telefonos': vals['contacto'], 'email': vals['correo'],
                'fundamentacion_especificaciones': vals['detalles_uso_sistema'],
                'fundamentacion_especiales': vals['detalles_permisos_especiales'],
                'solicitado_por_nombre_apellidos': vals['nombre_jefe_inmediato'],
                'solicitado_por_cargo': vals['cargo_jefe_inmediato'],
                'solicitado_por_unidad_organizativa': vals['uo_jefe_inmediato'],
                'solicitado_por_telefono': vals['telefono_jefe_inmediato'],
                'autorizado_por_nombre_apellidos': vals['nombre_director'],
                'autorizado_por_cargo': vals['cargo_director'],
                'autorizado_por_unidad_organizativa': vals['uo_director'],
                'autorizado_por_telefono': vals['telefono_director'], 'tipo_movimiento': tipo_movimiento,
                'numero_consecutivo': secuencia_final, }

        # Para debug siempre comentar las 2 siguientes líneas y descomentar las de abajo
        request.env['ir.sequence'].sudo().next_by_code('plantilla_acceso_numero_consecutivo')
        # busco las solicitudes anteriores de los usuarios que esten pendientes y las archivo
        solicitudes_repetidas = request.env['sicpro.modulo.plantilla.acceso'].sudo().search(
            ['&', ('email', '=', vals['correo']), ('estado', '=', 'pendiente')])
        for item in solicitudes_repetidas:
            item.rechazado_motivo = 'Se rechaza por encontrarse una solicitud más actual en el sistema.'
            item.rechazado = True
            item.estado = 'rechazado'

        # creo el registro de la planilla
        solicitud_creada = request.env['sicpro.modulo.plantilla.acceso'].sudo().create(data)

        # género un diccionario con los valores de los roles internos
        roles_internos = []
        # busco el id de la planilla
        planilla_id = request.env['sicpro.modulo.plantilla.acceso'].sudo().search(
            [('numero_consecutivo', '=', secuencia_final)]).id
        # busco los registro donde se encuentra los roles_ids
        registros_ids = request.env['sicpro.modulo.web.registro.roles'].sudo().search([('active', '=', True)])
        # busco los roles
        roles_ids = request.env['sicpro.modulo.roles'].sudo().search([('active', '=', True)])

        # busco los roles seleccionados por el usuario, separándolos por clave/valor
        for k, v in vals.items():
            for value in registros_ids:
                for item in value.roles:
                    if value['name'] == k and item['nombre_registro'] == v:
                        rol = {'role_id': item['id'], 'planilla_id': planilla_id, }
                        roles_internos.append(rol)

        # busco los roles de los permisos especiales
        # verífico el permisos_especiales_importar
        if 'importar' in vals:
            for value in roles_ids:
                if value.nombre_registro == 'Importar Datos':
                    rol = {'role_id': value['id'], 'planilla_id': planilla_id, }
                    roles_internos.append(rol)
        if 'exportar_avanzado' in vals:
            for value in roles_ids:
                if value.nombre_registro == 'Exportar Datos':
                    rol = {'role_id': value['id'], 'planilla_id': planilla_id, }
                    roles_internos.append(rol)
        # verífico el permisos_especiales_multiprocesos
        if 'multiprocesos' in vals:
            for value in roles_ids:
                if value.nombre_registro == 'MultiProcesos':
                    rol = {'role_id': value['id'], 'planilla_id': planilla_id, }
                    roles_internos.append(rol)

        # creo el registro de los roles de la planilla
        request.env['sicpro.modulo.plantilla.acceso.roles'].sudo().create(roles_internos)

        # envío el correo electrónico con la planilla adjunta
        email_values = {'email_to': solicitud_creada.email, }
        template = request.env.ref('sicpro_modulo_plantilla_acceso.solicitud_acceso_roles_creada')
        template.sudo().send_mail(solicitud_creada.id, force_send=True, email_values=email_values, )

        # redirijo a la pagina de inicio
        return request.redirect('/web/inicio/')

    # controller que ejecuta el url de la página con los términos y condiciones
    @http.route('/web/registro_terminos/', auth="public", website=True)
    def plantilla_web_registro_terminos(self, **kwargs):
        return request.render("sicpro_modulo_web_registro.web_plantilla_registro_terminos", {})
