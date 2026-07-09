# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import base64
from dateutil.relativedelta import relativedelta
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TransferenciasGastosOrdenes(models.Model):
    _name = 'sicpro.app.transferencias.gastos.ordenes'
    _description = "Órdenes vinculadas a las transferencias de Gastos"
    _rec_name = 'orden_id'
    _order = 'id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    # Es necesario para la inicialización la incorporación del campo id
    id = fields.Id()

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env[
            'sicpro.app.transferencias.gastos.ordenes.estados'].search(
            [('inicial', '=', True)], limit=1)

    name = fields.Char(string='Orden', related='orden_id.name', required=False)
    orden_id = fields.Many2one(comodel_name='sicpro.app.ordenes.trabajo',
                               string="Orden de Trabajo", required=False,
                               tracking=True, copy=False, index=True)
    active = fields.Boolean(string='Activo', default=True, tracking=True,
                            index=True)
    user_id = fields.Many2one('res.users', string='Generado por',
                              tracking=True, readonly=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso', store=True,
                                 related='orden_id.company_id')
    company_currency = fields.Many2one("res.currency", string='Moneda',
                                       related='company_id.currency_id')
    company_abreviatura = fields.Char(string='Abreviatura', required=False,
                                      related='company_id.identificador_corto')
    anio = fields.Char(string='Año', required=True, readonly=True)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses',
                          string='Mes', required=True, readonly=True)
    estado_id = fields.Many2one(
        'sicpro.app.transferencias.gastos.ordenes.estados', string='Estados',
        ondelete='restrict', tracking=True, copy=False,
        group_expand='_read_group_stage_ids', default=_get_default_stage_id)
    inicial = fields.Boolean(string='Estado Inicial',
                             related='estado_id.inicial')
    terminado = fields.Boolean(string='Estado Terminado',
                               related='estado_id.terminado')
    morosidad = fields.Boolean(string='Revisión de Morosidad',
                               related='estado_id.cron_morosidad')
    devuelto_economia = fields.Boolean(string='Devuelto a Economía',
                                       related='estado_id.devuelto_economia')
    color_barra = fields.Selection(string='Barra de Color',
                                   related='estado_id.color_barra')
    rol_interno = fields.Selection(string='Rol Interno',
                                   related='estado_id.rol_interno')
    gastos_ids = fields.One2many(
        comodel_name='sicpro.app.transferencias.gastos',
        inverse_name='gasto_id', copy=False, string='Gastos', required=False,
        tracking=True)
    fecha_liberado_gastos = fields.Date(string='Fecha Liberado',
                                        required=False, tracking=True,
                                        default=lambda
                                            self: fields.Date.context_today(
                                            self))
    fecha_revision_tecnico = fields.Date(string='Fecha Revisión DTP',
                                         required=False, tracking=True)
    fecha_validacion_ejecutor = fields.Date(string='Fecha Validación Ejecutor',
                                            required=False, tracking=True)
    fecha_validacion_inversionista = fields.Date(
        string='Fecha Validación Inversionista', required=False, tracking=True)
    fecha_contabilizado_economia = fields.Date(
        string='Fecha Contabilizado Economía', required=False, tracking=True)
    ############### ORDENES DE TRABAJO ########################################
    provincia_id = fields.Many2one(comodel_name="res.country.state",
                                   string="Provincia",
                                   related='orden_id.provincia_id', store=True)
    uo_id = fields.Many2one(comodel_name='sicpro.nomenclador.territorios',
                            string='Área', related='orden_id.uo_id',
                            required=True)
    uo_abreviatura = fields.Char(string='Unidad Organizativa', required=False,
                                 related='uo_id.abreviatura', store=True)
    titulo = fields.Char(string="Titulo", related='orden_id.titulo',
                         required=False)
    texto_breve_sap = fields.Char(string="Texto breve",
                                  related='orden_id.texto_breve_sap')
    pep = fields.Char(string='Sap', required=True, related='orden_id.pep')
    especialidad_id = fields.Many2one(
        comodel_name='sicpro.nomenclador.especialidad', string='Especialidad',
        related='orden_id.especialidad_id', store=False)
    agrupacion_id = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.areas', string='Asignado a',
        required=False, related='orden_id.agrupacion_id', store=True)
    departamento = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.areas', string='Departamento',
        required=False, tracking=True, compute='_compute_departamento',
        store=True)
    departamento_trabajador_id = fields.Many2one('sicpro.app.trabajadores',
                                                 string='Trabajador',
                                                 tracking=True,
                                                 related='departamento.manager_id')
    departamento_ocupacion_id = fields.Many2one(
        'sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo',
        related='departamento_trabajador_id.ocupacion_id')
    especialista_id = fields.Many2one(comodel_name='sicpro.app.trabajadores',
                                      string='Especialista',
                                      related='orden_id.especialista_id',
                                      store=True)
    detalles_economia = fields.Text(string="Detalles de Economía",
                                    required=False, tracking=True)
    observaciones_proyecto_ejecucion = fields.Text(
        string="Observaciones de Proyecto y Ejecutores", required=False,
        tracking=True)
    observaciones_inversionista = fields.Text(
        string="Observaciones del Inversionista", required=False,
        tracking=True)
    image_1920 = fields.Image("Image", related='especialidad_id.image_1920',
                              max_width=1920, max_height=1920)
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True)
    ############### INVERSIONISTA #############################################
    cliente_id = fields.Many2one('sicpro.app.clientes', string='Cliente',
                                 related='orden_id.cliente_id', store=True)
    cliente_territorio_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.territorios", string="UO Cliente",
        related='cliente_id.territorio', store=True)
    cliente_provincia_id = fields.Many2one(comodel_name="res.country.state",
                                           string="Provincia Cliente",
                                           related='cliente_id.provincias_id',
                                           store=True)
    cliente_cargo = fields.Char(string="Cargo", related='cliente_id.cargo',
                                required=False)
    cliente_telefono_fijo = fields.Char(string="Teléfono",
                                        related='cliente_id.telefono_fijo',
                                        required=False)
    cliente_telefono_movil = fields.Char(string="Móvil",
                                         related='cliente_id.telefono_movil',
                                         required=False)
    cliente_correo = fields.Char(string="Correo electrónico",
                                 related='cliente_id.correo', required=False)
    ###########################################################################
    cantidad_cuentas = fields.Integer(string="Cuentas",
        compute='_compute_cantidad_cuentas_gastos', store=False)
    total_gastos = fields.Monetary(currency_field='company_currency',
        string="Valor Total", compute='_compute_cantidad_cuentas_gastos',
        store=False)
    motivo_rechazo = fields.Text(string="Motivo del Rechazo", required=False,
                                 tracking=True)
    certificacion_rechazada = fields.Boolean(string='Certificación Rechazada',
                                             required=False, default=False)
    fecha_rechazada = fields.Date(string='Fecha de Rechazo', required=False,
                                  tracking=True)
    grupo_economia = fields.Boolean(string='grupo_economia',
                                    compute='_compute_grupo_economia')
    grupo_dtp = fields.Boolean(string='grupo_dtp',
                               compute='_compute_grupo_dtp', store=False)
    grupo_ejecutores = fields.Boolean(string='grupo_ejecutores',
                                      compute='_compute_grupo_ejecutores',
                                      store=False)
    grupo_inversionistas = fields.Boolean(string='grupo_inversionistas',
                                          compute='_compute_grupo_inversionistas',
                                          store=False)
    grupo_dtp_ejecutor = fields.Boolean(string='grupo_dtp_ejecutor',
                                        compute='_compute_grupo_dtp_ejecutor',
                                        store=False)
    doc_generado_count = fields.Integer(string="cuenta_modelo_generado",
                                        compute='_compute_gastos_docs_count')
    doc_firmado_count = fields.Integer(string="cuenta_modelo_firmado",
                                       compute='_compute_gastos_docs_count')
    modelo_gasto_attachment_ids = fields.Many2many('ir.attachment',
                                                   'modelo_gastos_attachment_rel',
                                                   'transferencia_id',
                                                   'attachment_id',
                                                   string="Generado")
    modelo_gasto_firmado_attachment_ids = fields.Many2many('ir.attachment',
                                                           'modelo_gastos_firmado_attachment_rel',
                                                           'transferencia_id',
                                                           'attachment_id',
                                                           string="Firmado")

    # generar el modelo de certificación en pdf
    def generar_modelo_gastos(self):
        # if self.env['res.users'].has_group(
        #     'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos'):
        if self.env.user.has_group(
            'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos'):
            # los roles del DTP, ejecutor, económico, responsable y admin pueden
            # generar los modelos de todos los procesos
            for item in self:
                # creo el nombre del documento
                doc_nombre = 'Transferencia de Gasto - ' + str(
                    item.anio) + '/' + str(item.mes.name) + ' - ' + str(
                    item.orden_id.name)
                data = self.env['ir.actions.report']._render_qweb_pdf(
                    'sicpro_app_transferencias_gastos.informe_modelo_transferencia_gastos_action',
                    item.ids)[0]
                attachment = self.env['ir.attachment'].create(
                    {'name': doc_nombre + '.pdf',
                     'datas': base64.b64encode(data), 'res_id': item.id,
                     'type': 'binary',
                     'res_model': 'sicpro.app.transferencias.gastos.ordenes',
                     'mimetype': 'application/pdf', })
                # guardo el documento en el campo establecido
                item.modelo_gasto_attachment_ids = attachment
        else:
            raise ValidationError(
                "Usted no tiene acceso a ejecutar esta acción.\n\n" + MSG_SOPORTE_SICPRO)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        stage_ids = stages.sudo()._search([], order=stages._order)
        return stages.browse(stage_ids)

    # verífica qué el usuario activo pertenezca al grupo de DTP o Ejecutor
    def _compute_grupo_dtp_ejecutor(self):
        # 1. Obtenemos ambos permisos del usuario actual (self.env.user)
        es_dtp = self.env.user.has_group(
            'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos')
        es_ejecutor = self.env.user.has_group(
            'sicpro_app_transferencias_gastos.grupo_transferencias_ejecutores_procesos')
        # 2. Iteramos sobre self (indispensable para evitar el Error de Singleton)
        for record in self:
            # La lógica: si es DTP es True, si no, depende de si es ejecutor
            if es_dtp:
                record.grupo_dtp_ejecutor = True
            else:
                record.grupo_dtp_ejecutor = es_ejecutor

    # verífica qué el usuario activo pertenezca al grupo de Economía
    def _compute_grupo_economia(self):
        # 1. Obtenemos el permiso del usuario actual una sola vez
        es_economia = self.env.user.has_group(
            'sicpro_app_transferencias_gastos.grupo_transferencias_economia')
        # 2. Iteramos para asignar el valor a cada registro en 'self'
        for record in self:
            # Asignamos el valor booleano directamente
            record.grupo_economia = es_economia

    # verífica qué el usuario activo pertenezca al grupo de DTP
    def _compute_grupo_dtp(self):
        # 1. Verificamos el grupo sobre el usuario actual (self.env.user)
        es_dtp = self.env.user.has_group(
            'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos')

        # 2. Verificamos la configuración de la compañía del usuario
        proceso_ejecuta = self.env.company.ejecuta_proceso

        # 3. Iteramos sobre self (obligatorio en computes)
        for record in self:
            if es_dtp and proceso_ejecuta:
                record.grupo_dtp = True
            else:
                record.grupo_dtp = False

    # verífica qué el usuario activo pertenezca al grupo de Ejecutores
    def _compute_grupo_ejecutores(self):
        # Obtenemos los valores del usuario actual una sola vez para ahorrar recursos
        es_ejecutor = self.env.user.has_group(
            'sicpro_app_transferencias_gastos.grupo_transferencias_ejecutores_procesos')
        # Accedemos directamente a la compañía del usuario actual
        proceso_activo = self.env.company.ejecuta_proceso

        # IMPORTANTE: Siempre iterar sobre self in un compute
        for record in self:
            if es_ejecutor and proceso_activo:
                record.grupo_ejecutores = True
            else:
                record.grupo_ejecutores = False

    # verífica qué el usuario activo pertenezca al grupo de Inversionistas
    def _compute_grupo_inversionistas(self):
        # Obtenemos los datos del usuario actual (self.env.user)
        es_inversionista = self.env.user.has_group(
            'sicpro_app_transferencias_gastos.grupo_transferencias_inversionistas')
        # Accedemos directamente al campo 'user_inversionista' del usuario actual
        # (Asegúrate de que el campo 'user_inversionista' exista en res.users)
        cliente_inversionista = self.env.user.user_inversionista
        # Iteramos sobre todos los registros de 'self'
        for record in self:
            if es_inversionista and cliente_inversionista:
                record.grupo_inversionistas = True
            else:
                record.grupo_inversionistas = False

    # actualiza el campo de departamento
    @api.depends('agrupacion_id')
    def _compute_departamento(self):
        for item in self:
            area = item.agrupacion_id
            if area:
                if area.tipo_registro == 'departamento':
                    item.departamento = area
                else:
                    item.departamento = area.parent_id
            else:
                item.departamento = False

    # cuanta la cantidad de cuentas y el valor total del gasto de la certificación
    @api.depends('gastos_ids', 'gastos_ids.valor_var')
    def _compute_cantidad_cuentas_gastos(self):
        for item in self:
            # Iniciamos valores por defecto para evitar errores
            suma = 0.0
            count = 0

            # Validamos que gastos_ids tenga registros
            if item.gastos_ids:
                for data in item.gastos_ids:
                    suma += float(data.valor_var)
                    count += 1

            item.total_gastos = suma
            item.cantidad_cuentas = count

    # Cuenta los adjuntos de la documentación de gastos
    def _compute_gastos_docs_count(self):
        for gastos in self:
            gastos.sudo().doc_generado_count = len(
                gastos.modelo_gasto_attachment_ids)
            gastos.sudo().doc_firmado_count = len(
                gastos.modelo_gasto_firmado_attachment_ids)

    # btn para aprobar la revisión de los gastos de la orden en el técnico productivo
    def gastos_revision_tecnico(self):
        if self.env.user.has_group(
            'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos'):
            for item in self:
                if item.inicial:
                    if item.doc_generado_count != 0:
                        estado = self.env[
                            'sicpro.app.transferencias.gastos.ordenes.estados'].search(
                            [('color_barra', '=', 'info'),
                             ('rol_interno', '=', 'ejecutores')])
                        item.write({
                            'fecha_revision_tecnico': fields.Date.context_today(
                                item), 'estado_id': estado.id,
                            'certificacion_rechazada': False, })
                        # actualizo el estado de los gastos de la cj74
                        estado_gastos = estado.valor_tecnico_gastos
                        for gastos in item.gastos_ids:
                            gastos.sudo().estado = estado_gastos

                        # Selecciono el registro de seguidores
                        grup_ejecutor = self.env.ref(
                            'sicpro_app_transferencias_gastos.grupo_transferencias_ejecutores_procesos',
                            raise_if_not_found=False)
                        group_ejecutor = self.env['res.users']
                        if grup_ejecutor:
                            group_ejecutor = grup_ejecutor.user_ids

                        for participante in group_ejecutor:
                            if participante.company_id.identificador_corto == item.company_abreviatura and participante.has_group(
                                'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos') == False:
                                print(participante.email_formatted)
                                # envío el correo electrónico
                                email_values = {
                                    'email_to': participante.email_formatted, }
                                local_context = item.env.context.copy()
                                template = self.env.ref(
                                    'sicpro_app_transferencias_gastos.gastos_revision_dtp')
                                template.with_context(local_context).send_mail(
                                    item.id, force_send=True,
                                    email_values=email_values)
                        # redirecciono la salida
                        action = self.sudo().env.ref(
                            'sicpro_app_transferencias_gastos.transferencias_ordenes_gastos_action').read()[
                            0]
                        return action
                    else:
                        raise ValidationError(
                            "Debe generar el modelo de transferencia de Gastos.\n\n" + MSG_SOPORTE_SICPRO)
                else:
                    raise ValidationError(
                        "Solo puede seleccionar órdenes que esten en estado de revisión técnica.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            raise ValidationError(
                "Usted no tiene acceso a ejecutar esta acción.\n\n" + MSG_SOPORTE_SICPRO)

    # btn para aprobar la validación de los gastos de la orden por el ejecutor
    def gastos_validacion_ejecutor(self):
        for item in self:
            if item.doc_generado_count != 0:
                estado = self.env[
                    'sicpro.app.transferencias.gastos.ordenes.estados'].search(
                    [('color_barra', '=', 'info'),
                     ('rol_interno', '=', 'inversionistas')])
                self.write({
                               'fecha_validacion_ejecutor': fields.Date.context_today(
                                   item), 'estado_id': estado.id,
                               'certificacion_rechazada': False, })
                # actualizo el estado de los gastos de la cj74
                estado_gastos = estado.valor_tecnico_gastos
                for gastos in item.gastos_ids:
                    gastos.sudo().estado = estado_gastos

                # Selecciono el registro de seguidores
                for participante in item.cliente_id.user_id:
                    # envío el correo electrónico
                    email_values = {'email_to': participante.email_formatted, }
                    local_context = item.env.context.copy()
                    template = self.env.ref(
                        'sicpro_app_transferencias_gastos.gastos_validacion_ejecutor')
                    template.with_context(local_context).send_mail(item.id,
                                                                   force_send=True,
                                                                   email_values=email_values)

                # redirecciono la salida
                action = self.sudo().env.ref(
                    'sicpro_app_transferencias_gastos.transferencias_ordenes_gastos_action').read()[
                    0]
                return action
            else:
                raise ValidationError(
                    "Debe generar el modelo de transferencia de Gastos.\n\n" + MSG_SOPORTE_SICPRO)

    # btn para aprobar la validación de los gastos de la orden por el inversionista
    def gastos_validacion_inversionista(self):
        for item in self:
            if item.doc_firmado_count != 0:
                estado = self.env[
                    'sicpro.app.transferencias.gastos.ordenes.estados'].search(
                    [('color_barra', '=', 'warning'),
                     ('rol_interno', '=', 'economia')], limit=1)
                item.write({
                    'fecha_validacion_inversionista': fields.Date.context_today(
                        item), 'estado_id': estado.id,
                    'certificacion_rechazada': False, })
                # actualizo el estado de los gastos de la cj74
                estado_gastos = estado.valor_tecnico_gastos
                for gastos in item.gastos_ids:
                    gastos.sudo().estado = estado_gastos

                # Selecciono el registro de seguidores del DTP
                grup_dtp = self.env.ref(
                    'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos',
                    raise_if_not_found=False)
                group_dtp = self.env['res.users']
                if grup_dtp:
                    group_dtp = grup_dtp.user_ids

                for participante in group_dtp:
                    if participante.company_id.identificador_corto == item.company_abreviatura:
                        # envío el correo electrónico
                        email_values = {
                            'email_to': participante.email_formatted, }
                        local_context = item.env.context.copy()
                        template = self.env.ref(
                            'sicpro_app_transferencias_gastos.gastos_certificacion_inversionista')
                        template.with_context(local_context).send_mail(item.id,
                                                                       force_send=True,
                                                                       email_values=email_values)

                # Selecciono el registro de seguidores de economía
                grup_eco = self.env.ref(
                    'sicpro_app_transferencias_gastos.grupo_transferencias_economia',
                    raise_if_not_found=False)
                group_eco = self.env['res.users']
                if grup_eco:
                    group_eco = grup_eco.user_ids

                for participante in group_eco:
                    # envío el correo electrónico a todos los miembros de economía
                    email_values = {'email_to': participante.email_formatted, }
                    local_context = item.env.context.copy()
                    template = self.env.ref(
                        'sicpro_app_transferencias_gastos.gastos_certificacion_inversionista')
                    template.with_context(local_context).send_mail(item.id,
                                                                   force_send=True,
                                                                   email_values=email_values)
            else:
                # Esta parte detiene la ejecución y avisa al usuario
                raise ValidationError(
                    "No se puede validar los gastos: el documento no ha sido "
                    "firmado.\n\n" + MSG_SOPORTE_SICPRO)

        action = self.sudo().env.ref(
            'sicpro_app_transferencias_gastos.transferencias_ordenes_gastos_action').read()[
            0]
        return action

    # btn para aprobar la contabilización de los gastos de la orden por economía
    def gastos_contabilizado_economia(self):
        for item in self:
            if item.doc_firmado_count != 0:
                estado = self.env[
                    'sicpro.app.transferencias.gastos.ordenes.estados'].search(
                    [('color_barra', '=', 'success'),
                     ('rol_interno', '=', 'economia')])
                self.write({
                               'fecha_contabilizado_economia': fields.Date.context_today(
                                   item), 'estado_id': estado.id,
                               'certificacion_rechazada': False, })
                # actualizo el estado de los gastos de la cj74
                estado_gastos = estado.valor_tecnico_gastos
                for gastos in item.gastos_ids:
                    gastos.sudo().estado = estado_gastos
                    gastos.contabilizado = True

                # Selecciono el registro de seguidores del DTP
                grup_dtp = self.env.ref(
                    'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos',
                    raise_if_not_found=False)
                group_dtp = self.env['res.users']
                if grup_dtp:
                    group_dtp = grup_dtp.user_ids

                for participante in group_dtp:
                    if participante.company_id.identificador_corto == item.company_abreviatura:
                        # envío el correo electrónico
                        email_values = {
                            'email_to': participante.email_formatted, }
                        local_context = self.env.context.copy()
                        template = self.env.ref(
                            'sicpro_app_transferencias_gastos.gastos_certificacion_contabilizado')
                        template.with_context(local_context).send_mail(item.id,
                                                                       force_send=True,
                                                                       email_values=email_values)

                # redirecciono la salida
                action = self.sudo().env.ref(
                    'sicpro_app_transferencias_gastos.transferencias_ordenes_gastos_action').read()[
                    0]
                return action
            else:
                raise ValidationError(
                    "El modelo de gastos certificados debe estar adjunto en el registro.\n\n" + MSG_SOPORTE_SICPRO)

    # ejecuta el cron para la revisión de los gastos pendientes por los inversionistas
    def cron_gastos_pendientes_inversionistas(self):
        # Busco las órdenes que están en estado de certificación por el inversionista
        ordenes = self.env['sicpro.app.transferencias.gastos.ordenes'].search(
            [('morosidad', '=', True)])

        for item in ordenes:
            config_morosidad = self.env[
                'sicpro.app.transferencias.gastos.ordenes.morosidad'].search(
                [('company_id', '=', item.company_id.id)], limit=1)

            # Validamos que exista configuración para evitar errores
            if not config_morosidad:
                continue

            dias = int(config_morosidad.name)

            fecha_limite = item.fecha_validacion_ejecutor + relativedelta(
                days=dias)

            # comparo la fecha límite con la fecha de entrega de los gastos al inversionista
            if fields.Date.context_today(self) > fecha_limite:
                # Selecciono el registro de seguidores del DTP y ejecutores
                grup_ejecutor = self.env.ref(
                    'sicpro_app_transferencias_gastos.grupo_transferencias_ejecutores_procesos',
                    raise_if_not_found=False)

                group_ejecutor = grup_ejecutor.user_ids if grup_ejecutor else \
                self.env['res.users']

                for participante in group_ejecutor:
                    if participante.company_id.identificador_corto == item.company_abreviatura:
                        # envío el correo electrónico
                        email_values = {
                            'email_to': participante.email_formatted, }
                        local_context = self.env.context.copy()
                        template = self.env.ref(
                            'sicpro_app_transferencias_gastos.gastos_morosidad_inversionista')
                        template.with_context(local_context).send_mail(item.id,
                                                                       force_send=True,
                                                                       email_values=email_values)