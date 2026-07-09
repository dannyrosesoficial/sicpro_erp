# -*- coding: utf-8 -*-

from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.exceptions import UserError


class ContratosProveedores(models.Model):
    _name = 'sicpro.app.contratos.proveedores'
    _description = 'Proveedores de los contratos'
    _order = "id asc"
    _inherit = ['mail.activity.mixin', 'mail.thread']

    # agrego el estado por defecto
    def _get_default_stage_id(self):
        return self.env['sicpro.app.contratos.proveedores.estados'].search(
            [], limit=1)

    name = fields.Char(required=True, string='Proveedor', tracking=True, )
    domicilio_social = fields.Char(required=True, string='Domicilio')
    nombre_directivo = fields.Char(required=True, string='Nombre',
                                   tracking=True, )
    cargo_directivo = fields.Char(required=True, string='Cargo',
                                  tracking=True, )
    telefono_fijo = fields.Char(string="Teléfono", required=False,
                                tracking=True, )
    telefono_movil = fields.Char(string="Móvil", required=False,
                                 tracking=True, )
    correo = fields.Char(string="Correo electrónico", required=False,
                         tracking=True, )
    codigo_reeup = fields.Char(string="Código REEUP", required=False,
                               tracking=True, )
    servicio_comercializable = fields.Text(string="Servicio Comercial",
                                           required=False)
    pep = fields.Char(string="Pep", required=True, tracking=True, )
    user_id = fields.Many2one('res.users', string='Gestor del proveedor',
                              index=True, tracking=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency',
                                       related='company_id.currency_id',
                                       readonly=True,
                                       relation="res.currency")
    presupuesto_cup = fields.Monetary('Presupuesto',
                                      currency_field='company_currency',
                                      tracking=True, required=True)
    valor_contrato = fields.Char(string="Valor", required=False,
                                 default='No exceder 200,000 mil CUC')
    etiquetas = fields.Many2many('sicpro.app.contratos.proveedores.etiquetas',
                                 'sicpro_app_contratos_proveedores_etiquetas_rel',
                                 string='Etiqueta')
    tipo = fields.Many2one(
        comodel_name='sicpro.app.contratos.proveedores.tipo',
        string='Tipo', required=True, tracking=True)
    fecha_agregado = fields.Date(string="Agregado", required=False,
                                 default=fields.datetime.today())
    anio = fields.Char(string="Año", required=False,
                       default=fields.datetime.today().strftime("%Y"), )
    pagina_web = fields.Char(string="Pagína Web", required=False,
                             tracking=True, )
    observaciones = fields.Text(string="Observaciones", required=False, )
    active = fields.Boolean(string="Activo", default=True, tracking=True, )
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920",
                             max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920",
                             max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920",
                             max_width=128, max_height=128, store=True)
    doc_count = fields.Integer(string="Documentos",
                               compute='_compute_proveedor_docs_count')
    stage_id = fields.Many2one('sicpro.app.contratos.proveedores.estados',
                               string='Estados', ondelete='restrict',
                               tracking=True, index=True, copy=False,
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id)
    kanban_state = fields.Selection([('normal', 'Borrador'),
                                     ('secondary', 'secondary'),
                                     ('info', 'info'),
                                     ('blocked', 'Rechazado'),
                                     ('done', 'Aprobado'), ],
                                    string='Estado interno',
                                    copy=False, default='normal',
                                    readonly=True)
    fecha_validacion_documentacion = fields.Date(
        string='Doc. Validada', index=True, tracking=True,
        copy=False, readonly=True)
    fecha_validacion_proveedor = fields.Date(
        string='Proveedor Validado', index=True, tracking=True,
        copy=False, readonly=True)
    fecha_rechazo = fields.Date(
        string='Fecha de Rechazo', index=True, tracking=True,
        copy=False, readonly=True)
    fecha_liberar_proveedor = fields.Date(
        string='Proveedor Liberado', index=True, tracking=True,
        copy=False, readonly=True)
    fecha_descontinuado = fields.Date(
        string='Descontinuado', index=True, tracking=True,
        copy=False, readonly=True)
    rechazar = fields.Char(string='Rechazar', required=False, readonly=True,
                           tracking=True)
    estado_interno = fields.Selection([
        ('borrador', 'Borrador'), ('validar_documentos', 'Validar Documentos'),
        ('validar_proveedor', 'Validar Proveedor'), ('rechazado', 'Rechazado'),
        ('aprobado', 'Aprobado'), ('desactivado', 'Desactivado')], index=True,
        required=True, tracking=15, default=lambda self: 'borrador')
    sequence_id = fields.Many2one('ir.sequence', string='Id Secuencia',
                                  required=False, copy=False)
    sequence_consecutivo = fields.Char(string='Secuencia', copy=False,
                                       readonly=True, )
    contratos_count = fields.Integer('Contratos',
                                     compute='_compute_contratos_count')

    # Cuenta los contratos pertenecientes al proveedor
    def _compute_contratos_count(self):
        contratos = self.env['sicpro.app.contratos']
        for record in self:
            record.contratos_count = contratos.search_count(
                [('proveedor', '=', record.id),
                 ('estado_interno', '=', 'activo')])

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
            documentos.doc_count = attachment_obj.search_count([
                '&', ('res_model', '=',
                      'sicpro.app.contratos.proveedores'),
                ('res_id', '=', documentos.id)
            ])

    # Sube los adjuntos de la documentacion del proveedor
    def proveedor_docs_view_action(self):
        self.ensure_one()
        domain = [
            '&',
            ('res_model', '=', 'sicpro.app.contratos.proveedores'),
            ('res_id', 'in', self.ids),
        ]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Adjunte la documentación del proveedor.</p>
                    '''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (
                self._name, self.id)
        }

    # accion liberar proveedor
    def action_liberar_proveedor(self, ):
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_aprobada', '=', True)]).id
        self.fecha_liberar_proveedor = fields.date.today()
        self.stage_id = estado
        self.estado_interno = 'validar_documentos'
        self.sudo().kanban_state = 'secondary'
        # envio la notificacion a los seguidores
        self.message_post(
            body='Proveedor Liberado',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]
        return action

    # accion del boton de validar documentacion
    def action_validar_documentacion(self, ):
        self.fecha_validacion_documentacion = fields.date.today()
        self.estado_interno = 'validar_proveedor'
        self.sudo().kanban_state = 'info'
        # envio la notificación a los seguidores
        self.message_post(
            body='Documentación validada',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )

    # accion del boton de desvalidar documentacion
    def action_desvalidar_documentacion(self, ):
        self.fecha_validacion_documentacion = ''
        self.estado_interno = 'validar_documentos'
        # envio la notificación a los seguidores
        self.message_post(
            body='Documentación desvalidada',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )

    # accion del boton para validar el proveedor
    def action_validar_proveedor(self, ):
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_won', '=', True)]).id
        self.fecha_validacion_proveedor = fields.date.today()
        self.stage_id = estado
        self.sudo().kanban_state = 'done'
        self.estado_interno = 'aprobado'
        # envio la notificacion a los seguidores
        self.message_post(
            body='Proveedor Validado',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]
        return action

    # accion reiniciar o regresar a borrador
    def action_regresar_borrador_proveedor(self, ):
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_inicial', '=', True)]).id
        self.fecha_liberar_proveedor = ''
        self.fecha_validacion_proveedor = ''
        self.fecha_validacion_documentacion = ''
        self.sudo().kanban_state = 'normal'
        self.rechazar = ''
        self.fecha_rechazo = ''
        self.stage_id = estado
        self.estado_interno = 'borrador'
        # envio la notificacion a los seguidores
        self.message_post(
            body='Proveedor a borrador',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]
        return action

    # accion desactivar proveedor
    def action_descontinuar_proveedor(self, ):
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_final', '=', True)]).id
        self.sudo().kanban_state = 'blocked'
        self.fecha_descontinuado = fields.date.today()
        self.stage_id = estado
        self.descontinuar = True
        self.estado_interno = 'desactivado'
        # envio la notificacion a los seguidores
        self.message_post(
            body='Proveedor descontinuado',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]
        return action

    @api.model
    def create(self, vals):
        if vals.get('presupuesto_cup') != 0:
            # Crear la secuencia de incremento para el consecutivo de los
            # proveedores
            seq_name = 'Consecutivo del Proveedor de Contratos '
            seq = {
                'code': 'proveedor_consecutivo_incrementar',
                'name': _('%s Sequence') % seq_name,
                'implementation': 'no_gap',
                'prefix': 'Proveedor/',
                'padding': 4,
                'number_increment': 1,
                'use_date_range': True,
            }
            vals['sequence_id'] = self.env['ir.sequence'].sudo().create(seq).id
            res = super(ContratosProveedores, self).create(vals)
            res['sequence_consecutivo'] = self.env['ir.sequence'].next_by_code(
                'proveedor_consecutivo_incrementar') or _('New')
            return res
        else:
            raise UserError(
                _('Debe proporcionar un valor de presupuesto, verifíquelo '))


class ProveedorRechazado(models.TransientModel):
    _name = 'sicpro.app.contratos.proveedores.rechazadas'
    _description = 'Proveedores Rechazados'

    lost_reason_id = fields.Char(string='Motivo', required=True, tracking=True)

    def action_motivo_rechazo(self):
        # llamo al metodo para crear la notificacion
        post = self.env['sicpro.app.contratos.proveedores'].browse(
            self.env.context.get('active_ids'))
        post.message_post(
            body='Proveedor rechazado.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # cambio el estado interno del proveedor
        estado = self.env['sicpro.app.contratos.proveedores.estados'].search(
            [('is_rechazada', '=', True)]).id
        rechazo = self.env[
            'sicpro.app.contratos.proveedores'].browse(
            self.env.context.get('active_ids'))
        for item in rechazo.sudo():
            item.rechazar = self.lost_reason_id
            item.esta_rechazada = True
            item.sudo().stage_id = estado
            item.sudo().kanban_state = 'blocked'
            item.fecha_rechazo = fields.date.today()
            item.estado_interno = 'rechazado'
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_contratos.contratos_proveedores_gestion_action').read()[
            0]
        return action
