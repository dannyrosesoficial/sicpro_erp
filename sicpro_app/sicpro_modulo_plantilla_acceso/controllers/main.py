from odoo import http
from odoo.http import request


class PlantillaAcceso(http.Controller):

    @http.route('/planilla_acceso/', auth="public", website=True)
    def plantilla(self, **kwargs):
        dic = {}
        if kwargs:
            if 'crear_consecutivo' in kwargs.keys():
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
                dic['numero_consecutivo'] = secuencia_final

            if 'accion' in kwargs.keys():
                if 'sap' in kwargs.keys():
                    usuario = request.env['res.users'].sudo().search(
                        ['|', ('active', '=', True), ('active', '=', False), ('pep', '=', kwargs['sap'])])

                    niveles = [('primaria', 'Primaria'), ('secundaria', 'Secundaria Básica'),
                               ('sintitulo', 'Sin Título'), ('tecnico', 'Técnico Medio'), ('medio', 'Medio'),
                               ('mediosuperior', 'Medio Superior'), ('superior', 'Superior'), ]

                    if usuario:
                        if usuario['user_inversionista']:
                            dic['nombre_apellidos'] = usuario['name']
                            dic['carne_identidad'] = ''
                            dic['codigo_sap'] = kwargs['sap']
                            dic['nivel_escolar'] = dict(niveles).get(usuario['inversionista_nivel_escolar'])
                            dic['cargo'] = usuario['inversionista_cargo']
                            dic['area'] = usuario['inversionista_territorio']['name']
                            dic['email'] = usuario['email']
                            dic['uo'] = usuario['company_id']['identificador_corto']
                            if usuario['inversionista_telefono_movil'] and usuario['inversionista_telefono_fijo']:
                                dic['telefonos'] = usuario['inversionista_telefono_movil'] + '  -  ' + usuario['inversionista_telefono_fijo']
                            elif usuario['inversionista_telefono_movil']:
                                dic['telefonos'] = usuario['inversionista_telefono_movil']
                            elif usuario['inversionista_telefono_fijo']:
                                dic['telefonos'] = usuario['inversionista_telefono_fijo']
                            else:
                                dic['telefonos'] = "-"
                        else:
                            dic['nombre_apellidos'] = usuario['name']
                            dic['carne_identidad'] = usuario['identification_id']
                            dic['codigo_sap'] = kwargs['sap']
                            dic['nivel_escolar'] = dict(niveles).get(usuario['nivel_escolar'])
                            dic['cargo'] = usuario['ocupacion_id']['name']['name']
                            dic['area'] = usuario['departamento']['name']
                            dic['email'] = usuario['email']
                            dic['uo'] = usuario['company_id']['identificador_corto']
                            if usuario['movil_trabajo'] and usuario['telefono_trabajo']:
                                dic['telefonos'] = usuario['movil_trabajo'] + '  -  ' + usuario['telefono_trabajo']
                            elif usuario['movil_trabajo']:
                                dic['telefonos'] = usuario['movil_trabajo']
                            elif usuario['telefono_trabajo']:
                                dic['telefonos'] = usuario['telefono_trabajo']
                            else:
                                dic['telefonos'] = "-"

                        roles_final = []
                        for item in usuario['role_ids']:
                            rol_data = item['name'].split(':')

                            rol_data[0] = item['clave_solicitud']
                            if len(rol_data) > 1:
                                rol_data[1] = rol_data[1].strip()

                            roles_final.append(rol_data)
                        dic['roles'] = roles_final

                dic['accion'] = kwargs['accion']

        return request.render("sicpro_modulo_plantilla_acceso.plantilla_solicitud_rol", dic)

    @http.route('/planilla_acceso/seleccion/', auth="public", website=True)
    def plantilla_seleccion(self, **kwargs):
        return request.render("sicpro_modulo_plantilla_acceso.plantilla_solicitud_rol_seleccion", {})

    @http.route('/planilla_acceso/crear_registro/', auth="public", website=True)
    def plantilla_crear_registro(self, **kwargs):
        global nueva_incorporacion, tipo_movimiento
        vals = {}
        solicitud = {}
        for key in kwargs.keys():
            field_temp = key.replace('-', '_')
            vals[field_temp] = kwargs[key]

        # verífico que sea un usuario de nueva incorporación
        if 'usuario_incoporacion_si' in vals:
            nueva_incorporacion = True
        if 'usuario_incoporacion_no' in vals:
            nueva_incorporacion = False

        # verífico el tipo de movimiento del usuario
        if 'tipo_movimiento_alta' in vals:
            tipo_movimiento = 'alta'
        if 'tipo_movimiento_modificar' in vals:
            tipo_movimiento = 'modificacion'
        if 'tipo_movimiento_baja' in vals:
            tipo_movimiento = 'baja'

        # verífico el tipo de acción
        if 'tipo_accion_reinicio' in vals:
            tipo_movimiento = 'reinicio'

        # verífico si existe la fundamentación

        especificaciones = None
        if 'fundamentacion_especificaciones' in vals:
            especificaciones = vals['fundamentacion_especificaciones']
        else:
            especificaciones = 'Solicitud de reinicialización del usuario en el sistema.'

        # creo el diccionario para enviar los datos
        solicitud = {
            'name': vals['nombre_apellidos'],
            'carne_identidad': vals['carne_identidad'],
            'codigo_sap': vals['codigo_sap'],
            'usuario_incoporacion': nueva_incorporacion,
            'tipo_movimiento': tipo_movimiento,
            'nivel_escolar': vals['nivel_escolar'],
            'uo': vals['uo'],
            'area': vals['area'],
            'cargo': vals['cargo'],
            'telefonos': vals['telefonos'],
            'email': vals['email'],
            'fundamentacion_especificaciones': especificaciones,
            'solicitado_por_nombre_apellidos': vals['solicitado_por_nombre_apellidos'],
            'solicitado_por_cargo': vals['solicitado_por_cargo'],
            'solicitado_por_unidad_organizativa': vals['solicitado_por_unidad_organizativa'],
            'solicitado_por_fecha': vals['solicitado_por_fecha'],
            'solicitado_por_telefono': vals['solicitado_por_telefono'],
            'autorizado_por_nombre_apellidos': vals['autorizado_por_nombre_apellidos'],
            'autorizado_por_cargo': vals['autorizado_por_cargo'],
            'autorizado_por_unidad_organizativa': vals['autorizado_por_unidad_organizativa'],
            'autorizado_por_fecha': vals['autorizado_por_fecha'],
            'autorizado_por_telefono': vals['autorizado_por_telefono'],
            'numero_consecutivo': vals['numero_consecutivo'],
            }

        # Para debug siempre comentar las 2 siguientes líneas y descomentar las de abajo
        request.env['ir.sequence'].sudo().next_by_code('plantilla_acceso_numero_consecutivo')
        # creo el registro de la planilla
        request.env['sicpro.modulo.plantilla.acceso'].sudo().create(solicitud)

        # busco los roles relacionados
        buscar_rol = []
        roles_ids = []
        data_roles = request.env['sicpro.modulo.roles'].sudo().search([('active', '=', True)])

        # busco el id de la planilla
        data_planilla = request.env['sicpro.modulo.plantilla.acceso'].sudo().search(
            [('numero_consecutivo', '=', vals['numero_consecutivo'])]).id

        # busco todos los roles y proceso el nombre (MÉTODO PARA LOS ROLES NO ESPECIALES)
        for item in data_roles:
            nombre_rol = item['name'].split(':')
            roles = {
                'id': item['id'],
                'code': item['clave_solicitud'],
                'rol': nombre_rol[1].strip()
            }
            buscar_rol.append(roles)

        # busco los roles seleccionados por el usuario, separándolos por clave/valor
        for k, v in vals.items():
            for value in buscar_rol:
                if value['code'] == k and value['rol'] == v:
                    rol = {'role_id': value['id'],
                           'planilla_id': data_planilla,
                           }
                    roles_ids.append(rol)

        # busco todos los roles y proceso el nombre (MÉTODO PARA LOS ROLES ESPECIALES)
        # permisos_especiales_importar ---------------- code_especial_importar
        # permisos_especiales_exportar_avanzado ------- code_especial_exportar
        # permisos_especiales_multiprocesos ----------- code_especial_multiprocesos
        ##############################################################################
        # otros qué actualmente no se procesan aquí:
        # code_especial_eliminar_accesos
        # code_especial_vpn

        roles_especiales = []
        # verífico el permisos_especiales_importar
        if 'permisos_especiales_importar' in vals:
            rol_especial = {'clave_solicitud': 'code_especial_importar', }
            roles_especiales.append(rol_especial)
        # verífico el permisos_especiales_exportar_avanzado
        if 'permisos_especiales_exportar_avanzado' in vals:
            rol_especial = {'clave_solicitud': 'code_especial_exportar', }
            roles_especiales.append(rol_especial)
        # verífico el permisos_especiales_multiprocesos
        if 'permisos_especiales_multiprocesos' in vals:
            rol_especial = {'clave_solicitud': 'code_especial_multiprocesos', }
            roles_especiales.append(rol_especial)

        for item_especial in data_roles:
            for esp in roles_especiales:
                if item_especial.clave_solicitud == esp['clave_solicitud']:
                    roles_esp = {
                        'role_id': item_especial['id'],
                        'planilla_id': data_planilla,
                    }
                    roles_ids.append(roles_esp)

        # creo el registro de los roles de la planilla
        request.env['sicpro.modulo.plantilla.acceso.roles'].sudo().create(roles_ids)

        return request.redirect('/web')

        # Debug para ver que se agregan al registro (descomentar las 2 siguientes líneas)
        #ident = request.env['sicpro.modulo.plantilla.acceso'].sudo().create(vals)
        #print(request.env['sicpro.modulo.plantilla.acceso'].sudo().search_read([['id','=',ident.id]],list(vals.keys())))
