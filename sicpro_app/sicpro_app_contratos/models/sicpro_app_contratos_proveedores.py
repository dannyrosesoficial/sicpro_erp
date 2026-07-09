# -*- coding: utf-8 -*-


from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.exceptions import UserError
import os
import logging
from odoo.addons.smile_log.tools import SmileDBLogger

_logger = logging.getLogger(__name__)


class ContratosProveedores(models.Model):
    _name = 'sicpro.app.contratos.proveedores'
    _description = 'Gestión de los proveedores'
    _order = "id asc"
    _inherit = ['mail.activity.mixin', 'mail.thread']

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.contratos.proveedores.estados'].search([],
                                                                           limit=1)

    name = fields.Char(required=True, string='Proveedor', tracking=True, )
    domicilio_social = fields.Char(required=True, string='Domicilio')
    nombre_directivo = fields.Char(required=True, string='Nombre',
                                   tracking=True, )
    cargo_directivo = fields.Char(required=True, string='Cargo',
                                  tracking=True, )
    telefono_fijo = fields.Char(string="Teléfono", required=True,
                                tracking=True, )
    telefono_movil = fields.Char(string="Móvil", required=True,
                                 tracking=True, )
    correo = fields.Char(string="Correo electrónico", required=True,
                         tracking=True, )
    codigo_reeup = fields.Char(string="Código REEUP / ONE", required=False,
                               tracking=True, )
    servicio_comercializable = fields.Text(string="Servicio Comercial",
                                           required=False)
    pep = fields.Char(string="Código SAP", required=False, tracking=True, )
    user_id = fields.Many2one('res.users', string='Gestor del proveedor',
                              index=True, tracking=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Currency',
                                       related='company_id.currency_id',
                                       readonly=True)
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    monto_contratos_ejecutado = fields.Monetary(
        currency_field='company_currency', string="Facturado",
        compute='_compute_monto_contratos_ejecutados')
    valor_contrato = fields.Char(string="Valor", required=False,
                                 default='No exceder 6 millones de CUP')
    etiquetas = fields.Many2many('sicpro.app.contratos.proveedores.etiquetas',
                                 'sicpro_app_contratos_proveedores_etiquetas_rel',
                                 string='Etiqueta')
    tipo = fields.Many2one(
        comodel_name='sicpro.app.contratos.proveedores.tipo',
        string='Tipo Proveedor', required=True, tracking=True)
    fecha_agregado = fields.Date(string="Agregado", required=False,
                                 default=lambda self: fields.Date.context_today(self))
    anio = fields.Char(string="Año", required=False,
                       default=fields.Datetime.now().strftime("%Y"), )
    pagina_web = fields.Char(string="Pagína Web", required=False,
                             tracking=True, )
    observaciones = fields.Text(string="Observaciones del proveedor",
                                required=False, )
    active = fields.Boolean(string="Activo", default=True, tracking=True, )
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True)
    doc_count = fields.Integer(string="Documentos",
                               compute='_compute_proveedor_docs_count')
    stage_id = fields.Many2one('sicpro.app.contratos.proveedores.estados',
                               string='Estados', ondelete='restrict',
                               tracking=True, index=True, copy=False,
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id)
    kanban_state = fields.Selection(
        [('normal', 'Borrador'), ('secondary', 'secondary'), ('info', 'info'),
         ('blocked', 'Rechazado'), ('done', 'Aprobado'), ],
        string='Estado interno', copy=False, default='normal', readonly=True)
    fecha_validacion_documentacion = fields.Date(string='Doc. Validada',
                                                 index=True, tracking=True,
                                                 copy=False, readonly=True)
    fecha_validacion_proveedor = fields.Date(string='Proveedor Validado',
                                             index=True, tracking=True,
                                             copy=False, readonly=True)
    fecha_rechazo = fields.Date(string='Fecha de Rechazo', index=True,
                                tracking=True, copy=False, readonly=True)
    fecha_liberar_proveedor = fields.Date(string='Proveedor Liberado',
                                          index=True, tracking=True,
                                          copy=False, readonly=True)
    fecha_descontinuado = fields.Date(string='Descontinuado', index=True,
                                      tracking=True, copy=False, readonly=True)
    rechazar = fields.Char(string='Rechazar', required=False, readonly=True,
                           tracking=True)
    estado_interno = fields.Selection([('borrador', 'Borrador'), (
        'validar_documentos', 'Validar Documentos'), ('validar_proveedor',
                                                      'Validar Proveedor'),
                                       ('rechazado', 'Rechazado'),
                                       ('aprobado', 'Aprobado'),
                                       ('desactivado', 'Desactivado')],
                                      index=True, required=True, tracking=15,
                                      default=lambda self: 'borrador')
    sequence_consecutivo = fields.Char(string='Secuencia', copy=False,
                                       readonly=True, )
    contratos_count = fields.Integer('Contratos',
                                     compute='_compute_contratos_count')
    tipo_proveedor = fields.Selection(
        string='Tipo de Proveedor',
        selection=[('productor', 'Productor'),
                   ('oficial', 'Distribuidor Oficial'),
                   ('intermediario', 'Intermediario Reconocido'),
                   ('otros', 'Otros Servicios'), ],
        required=False, )
    puntos_documentacion = fields.Integer(string='Documentacion',
                                          required=False)
    puntos_fechas_entrega = fields.Integer(string='Fechas de Entrega',
                                           required=False)
    puntos_faltantes_sobrantes = fields.Integer(string='Faltantes/Sobrantes',
                                          required=False)
    puntos_reclamaciones = fields.Integer(string='Reclamaciones',
                                          required=False)
    puntos_penalidades = fields.Integer(string='Penalidades', required=False)
    puntos_total = fields.Integer(string='Total',
                                  compute='_compute_suma_puntos', store=True)
    puntos_cualitativa = fields.Integer(string='Valor Cualitativo',
                                        required=False)
    criterios_cualitativa = fields.Text(string="Criterios Cualitativa",
                                        required=False)
    puntuacion_final = fields.Selection(
        string='Puntación final', required=False,
        selection=[('satisfactorio', 'Proveedor Satisfactorio '),
                   ('aceptable', 'Proveedor Aceptable'),
                   ('no_satisfactorio', 'Proveedor No Satisfactorio'), ], )
    evaluacion_final = fields.Integer(string='Evaluación Final', store=True,
                                      compute='_compute_evaluacion_final', )
    periodo_evaluado = fields.Text(string="Periodo Evaluado", required=False)

    # suma puntos de los indicadores
    @api.depends('puntos_documentacion', 'puntos_fechas_entrega',
                 'puntos_faltantes_sobrantes', 'puntos_reclamaciones',
                 'puntos_penalidades')
    def _compute_suma_puntos(self):
        self.puntos_total = self.puntos_documentacion + \
                            self.puntos_fechas_entrega + \
                            self.puntos_faltantes_sobrantes + \
                            self.puntos_reclamaciones + \
                            self.puntos_penalidades

    # suma todos los puntos
    @api.depends('puntos_total', 'puntos_cualitativa')
    def _compute_evaluacion_final(self):
        self.evaluacion_final = self.puntos_total + self.puntos_cualitativa

    # suma monto facturado
    def _compute_monto_contratos_ejecutados(self):
        estado_activo = self.env['sicpro.app.contratos.estados'].search(
            [('is_won', '=', True)]).id
        estado_terminado = self.env['sicpro.app.contratos.estados'].search(
            [('is_terminada', '=', True)]).id
        data = self.env['sicpro.app.contratos']
        for monto in self:
            gasto = data.search(['&', ('proveedor', '=', monto.id), (
                'estado_id', 'in', (estado_activo, estado_terminado))])
            monto.monto_contratos_ejecutado = sum(
                gasto.mapped('presupuesto_cup'))

    # Redirige a la vista de contratos vinculados al proveedor especifico
    def proveedor_contratos_ejecutados_action(self):
        estado_activo = self.env['sicpro.app.contratos.estados'].search(
            [('is_won', '=', True)]).id
        estado_terminado = self.env['sicpro.app.contratos.estados'].search(
            [('is_terminada', '=', True)]).id
        domain = ['&', ('proveedor', '=', self._origin.id),
                  ('estado_id', 'in', (estado_activo, estado_terminado))]
        return {'name': _('Contratos Ejecutados'), 'domain': domain,
                'res_model': 'sicpro.app.contratos',
                'type': 'ir.actions.act_window', 'view_id': False,
                'view_mode': 'tree,form', 'view_type': 'form', 'limit': 80, }

    # Cuenta los contratos pertenecientes al proveedor
    def _compute_contratos_count(self):
        estado_activo = self.env['sicpro.app.contratos.estados'].search(
            [('is_won', '=', True)]).id
        estado_terminado = self.env['sicpro.app.contratos.estados'].search(
            [('is_terminada', '=', True)]).id
        contratos = self.env['sicpro.app.contratos']
        for record in self:
            record.contratos_count = contratos.search_count(
                ['&', ('proveedor', '=', record.id),
                 ('estado_id', 'in', (estado_activo, estado_terminado))])

    # carga los estados a la vista Kanban
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order,
                                   access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # Cuenta los adjuntos de la documentacion del proveedor
    def _compute_proveedor_docs_count(self):
        attachment_obj = self.env['ir.attachment']
        for documentos in self:
            documentos.doc_count = attachment_obj.search_count(
                ['&', ('res_model', '=', 'sicpro.app.contratos.proveedores'),
                 ('res_id', '=', documentos.id)])

    # acción liberar proveedor
    def action_liberar_proveedor(self, ):
        if self.doc_count != 0:
            estado = self.env[
                'sicpro.app.contratos.proveedores.estados'].search(
                [('is_aprobada', '=', True)]).id
            self.write({'fecha_liberar_proveedor': fields.Date.context_today(self),
                        'stage_id': estado,
                        'estado_interno': 'validar_documentos',
                        'kanban_state': 'secondary', })
            # mantiene actualizado el correo de los seguidores del registro
            correos = ''
            for follower in self.message_partner_ids:
                correos = str(correos) + str(follower.email_formatted)
            self.correo_seguidores = correos
            # envío el correo a los seguidores del registro
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_contratos.contratos_proveedores_cambio_estados')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True)
            # envio la notificacion a los seguidores
            self.message_post(body='Proveedor Liberado',
                              message_type='notification',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # Registro del log
            logger = SmileDBLogger(self._cr.dbname, self._name, self.id,
                                   self._uid)
            pid = os.getpid()
            data_log = [pid, self._name, self.id, self.sequence_consecutivo,
                        self.env.user.name]
            logger.time_info(
                '[%s] Cambio de estado: Proveedor Liberado - Records:'
                ' %s (%s) - %s. Usuario: %s - ' % tuple(data_log))
            # redirecciono la salida
            action = self.sudo().env.ref(
                'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
                0]
            return action
        else:
            raise UserError(
                _('Debe proporcionar una documentación valida, verifíquelo '))

    # acción del botón de validar documentacion
    def action_validar_documentacion(self, ):
        self.write({'fecha_validacion_documentacion': fields.Date.context_today(self),
                    'estado_interno': 'validar_proveedor',
                    'kanban_state': 'info', })
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_cambio_estados')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)
        # envio la notificación a los seguidores
        self.message_post(body='Documentación validada',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, self.sequence_consecutivo,
                    self.env.user.name]
        logger.time_info('[%s] Cambio de estado: Documentación validada - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(
            data_log))

    # acción del botón de desvalida documentacion
    def action_desvalidar_documentacion(self, ):
        self.write({'fecha_validacion_documentacion': '',
                    'estado_interno': 'validar_documentos', })
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_cambio_estados')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)
        # envio la notificación a los seguidores
        self.message_post(body='Documentación desvalidada',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, self.sequence_consecutivo,
                    self.env.user.name]
        logger.time_info('[%s] Cambio de estado: Documentación desvalidada - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(
            data_log))

    # acción del botón para validar el proveedor
    def action_validar_proveedor(self, ):
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_won', '=', True)]).id
        self.write({'fecha_validacion_proveedor': fields.Date.context_today(self),
                    'stage_id': estado, 'estado_interno': 'aprobado',
                    'kanban_state': 'done', })
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_cambio_estados')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)
        # envio la notificacion a los seguidores
        self.message_post(body='Proveedor Validado',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, self.sequence_consecutivo,
                    self.env.user.name]
        logger.time_info('[%s] Cambio de estado: Proveedor Validado - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(
            data_log))
        # redirecciono la salida
        action = self.sudo().env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]

        rainbow = {'effect': {
            'fadeout': 'slow',
            'message': 'Felicidades. El Proveedor ha sido '
                       'validado correctamente',
            'type': 'rainbow_man', }}

        return rainbow

    # acción reiniciar o regresar a borrador
    def action_regresar_borrador_proveedor(self, ):
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_inicial', '=', True)]).id
        self.write({'fecha_liberar_proveedor': '', 'stage_id': estado,
                    'fecha_validacion_proveedor': '',
                    'fecha_validacion_documentacion': '', 'rechazar': '',
                    'fecha_rechazo': '', 'estado_interno': 'borrador',
                    'kanban_state': 'normal', })
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_cambio_estados')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)
        # envió la notificación a los seguidores
        self.message_post(body='Proveedor a borrador',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, self.sequence_consecutivo,
                    self.env.user.name]
        logger.time_info('[%s] Cambio de estado: Proveedor a borrador - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(
            data_log))
        # redirecciono la salida
        action = self.sudo().env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]
        return action

    # acción desactivar proveedor
    def action_descontinuar_proveedor(self, ):
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_final', '=', True)]).id
        self.write(
            {'fecha_descontinuado': fields.Date.context_today(self), 'stage_id': estado,
             'estado_interno': 'desactivado', 'kanban_state': 'blocked', })
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_cambio_estados')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)
        # envió la notificación a los seguidores
        self.message_post(body='Proveedor descontinuado',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, self.sequence_consecutivo,
                    self.env.user.name]
        logger.time_info('[%s] Cambio de estado: Proveedor descontinuado - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(
            data_log))
        # redirecciono la salida
        action = self.sudo().env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]
        return action

    @api.model
    def create(self, vals):
        res = super(ContratosProveedores, self).create(vals)
        # Crear la secuencia de incremento para el consecutivo del proveedor
        res['sequence_consecutivo'] = self.env['ir.sequence'].next_by_code(
                'proveedor_consecutivo_incrementar')

        # busco los usuarios con permisos de visualización
        usuarios = self.env.ref(
            'sicpro_app_contratos.grupo_app_contratos_visual').users
        # creo la lista de seguidores
        seguidores = usuarios
        # agrego los seguidores al modelo
        res.message_subscribe(partner_ids=seguidores.partner_id.ids)
        # envió la notificación a los seguidores
        res.message_post(
            body='Nueva Proveedor Creado',
            message_type='notification', subtype_xmlid='mail.mt_comment',
            author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in seguidores:
            correos = str(correos) + str(follower.email_formatted)
        res['correo_seguidores'] = correos
        # envío el correo a los seguidores del registro
        template = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_nuevos')
        template.send_mail(res.id, force_send=True)
        return res


class ProveedorRechazado(models.TransientModel):
    _name = 'sicpro.app.contratos.proveedores.rechazadas'
    _description = 'Proveedores Rechazados'
    _inherit = ['mail.thread']

    lost_reason_id = fields.Char(string='Motivo', required=True, tracking=True)

    def action_motivo_rechazo(self):
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.contratos.proveedores'].browse(
            self.env.context.get('active_ids'))
        post.message_post(body='Proveedor rechazado.',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # cambio el estado interno del proveedor
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_rechazada', '=', True)]).id
        rechazo = self.env['sicpro.app.contratos.proveedores'].browse(
            self.env.context.get('active_ids'))
        for item in rechazo.sudo():
            item.rechazar = self.lost_reason_id
            item.sudo().stage_id = estado
            item.sudo().kanban_state = 'blocked'
            item.fecha_rechazo = fields.Date.context_today(self)
            item.estado_interno = 'rechazado'
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, rechazo.sequence_consecutivo,
                    self.env.user.name]
        logger.time_info('[%s] Cambio de estado: Proveedor rechazado - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(
            data_log))
        # redirecciono la salida
        action = self.sudo().env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]
        return action
