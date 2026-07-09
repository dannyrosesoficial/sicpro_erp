# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from random import randint
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO

def _default_color():
    return randint(1, 11)


class AppCMIIndicadores(models.Model):
    _name = 'sicpro.app.cmi.indicadores'
    _order = "id asc"
    _description = 'Indicadores del CMI'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _compute_buscar_anios(self):
        anio_obj = self.env['sicpro.app.cmi.perspectivas.anios'].search(
            [('active', '=', True)])
        lst = []
        for anios in anio_obj:
            lst.append((anios.anio, anios.anio))
        return lst

    # Busca los datos de los objetivos anuales
    def _context_anio(self):
        if not self.env.context.get('obj_anuales_id'):
            raise UserError(
                "Para agregar un registro debe iniciar desde el tablero de Años.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            valor = str(self.env.context.get('obj_anuales_id'))
            anio = self.env['sicpro.app.cmi.objetivos.anuales'].search(
                [('id', '=', valor)]).anio
            return anio

    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              default=lambda self: self.env.uid)
    responsable_id = fields.Many2one('res.users', string='Responsable',
                                     index=True, required=True)
    responsable_follower = fields.Many2one('res.users', string='follower')
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, index=True)
    condicion_presupuesto = fields.Boolean(string="Condición de Presupuesto",
                                           default=False, )
    obj_anuales_id = fields.Many2one('sicpro.app.cmi.objetivos.anuales',
                                     string='Objetivo Anual', required=True,
                                     default=lambda self: self.env.context.get(
                                         'obj_anuales_id'))
    anio = fields.Selection(selection=_compute_buscar_anios, string="Año",
                            default=_context_anio, copy=False, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    detalles = fields.Text(string="Detalles", required=False)
    indicadores_ids = fields.One2many(
        comodel_name='sicpro.app.cmi.indicadores.valores', copy=False,
        inverse_name='indicador_id', string='Indicadores', required=False)
    indicadores_ids_2 = fields.One2many(
        comodel_name='sicpro.app.cmi.indicadores.valores', copy=False,
        inverse_name='indicador_id', string='Lista de Indicadores',
        required=False, related='indicadores_ids')
    acciones_ids = fields.One2many(comodel_name='sicpro.app.cmi.acciones',
                                   inverse_name='indicador_id', copy=False,
                                   string='Acciones', required=False)
    indicadores_visible = fields.Boolean(string='Indicadores_visible',
                                         required=False, default=False,
                                         copy=False, )
    activador_visible = fields.Boolean(string='Activador_visible', copy=False,
                                       required=False, default=False)
    grupo_responsable = fields.Boolean(string='grupo_responsable',
                                       compute="_compute_grupo_responsable",
                                       store=False)
    grupo_read_only = fields.Boolean(string='grupo_read_only',
                                     compute="_compute_grupo_read_only",
                                     store=False)
    porciento_enero = fields.Float(string='Porciento Ene',
                                   compute='compute_calculo_porciento')
    porciento_febrero = fields.Float(string='Porciento Feb',
                                     compute='compute_calculo_porciento')
    porciento_marzo = fields.Float(string='Porciento Mar',
                                   compute='compute_calculo_porciento')
    porciento_abril = fields.Float(string='Porciento Abr',
                                   compute='compute_calculo_porciento')
    porciento_mayo = fields.Float(string='Porciento May',
                                  compute='compute_calculo_porciento')
    porciento_junio = fields.Float(string='Porciento jun',
                                   compute='compute_calculo_porciento')
    porciento_julio = fields.Float(string='Porciento jul',
                                   compute='compute_calculo_porciento')
    porciento_agosto = fields.Float(string='Porciento Ago',
                                    compute='compute_calculo_porciento')
    porciento_septiembre = fields.Float(string='Porciento Sep',
                                        compute='compute_calculo_porciento')
    porciento_octubre = fields.Float(string='Porciento Oct',
                                     compute='compute_calculo_porciento')
    porciento_noviembre = fields.Float(string='Porciento Nov',
                                       compute='compute_calculo_porciento')
    porciento_diciembre = fields.Float(string='Porciento Dic',
                                       compute='compute_calculo_porciento')
    real_acumulado = fields.Float(string='Real Acumulado', store=True,
                                  compute='compute_indicadores_ids')
    meta_acumulado = fields.Float(string='Objetivo Acumulado', store=True,
                                  compute='compute_indicadores_ids')
    real_acumulado_kanban = fields.Float(string='Real Acumulado Kanban',
                                         compute='compute_acumulado')
    meta_acumulado_kanban = fields.Float(string='Objetivo Acumulado Kanban',
                                         compute='compute_acumulado')
    diferencia_acumulado = fields.Float(string='diferencia',
                                        compute='compute_diferencia_porciento')
    porciento_avance = fields.Float(string='Porciento Avance',
                                    compute='compute_diferencia_porciento')
    porciento_avance_barra = fields.Float(string='Avance',
                                          compute='compute_diferencia_porciento')
    comentario = fields.Text(string="Comentario", required=False, copy=False)
    seguridad_responsable = fields.Boolean(string='Seguridad_responsable',
                                           required=False, default=False,
                                           copy=False, )

    # calcula real y acumulado anual de sus indicadores
    @api.depends('indicadores_ids.real', 'indicadores_ids.meta')
    def compute_acumulado(self):
        for data in self:
            periodo = self.env.context.get('default_periodo')
            real = 0
            meta = 0

            # Verífica el mes correspondiente
            if periodo in (
                'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
                'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'):
                obj_indicadores_ids = data.indicadores_ids.filtered(
                    lambda l: l.mes == periodo)
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el primer trimestre
            elif periodo == '1t':
                obj_indicadores_ids = data.indicadores_ids.filtered(
                    lambda l: l.mes in ('enero', 'febrero', 'marzo'))
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

                # Verifica el segundo trimestre
            elif periodo == '2t':
                obj_indicadores_ids = data.indicadores_ids.filtered(
                    lambda l: l.mes in ('abril', 'mayo', 'junio'))
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el tercer trimestre
            elif periodo == '3t':
                obj_indicadores_ids = data.indicadores_ids.filtered(
                    lambda l: l.mes in ('julio', 'agosto', 'septiembre'))
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el cuarto trimestre
            elif periodo == '4t':
                obj_indicadores_ids = data.indicadores_ids.filtered(
                    lambda l: l.mes in ('octubre', 'noviembre', 'diciembre'))
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el primer semestre
            elif periodo == '1s':
                obj_indicadores_ids = data.indicadores_ids.filtered(
                    lambda l: l.mes in (
                    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio'))
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el segundo semestre
            elif periodo == '2s':
                obj_indicadores_ids = data.indicadores_ids.filtered(
                    lambda l: l.mes in (
                    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
                    'diciembre'))
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el anual
            elif periodo == 'anual':
                obj_indicadores_ids = data.indicadores_ids.filtered(
                    lambda l: l.mes in (
                    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
                    'diciembre'))
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # paso los valores a los campos
            data.real_acumulado_kanban = real
            data.meta_acumulado_kanban = meta

    # ejecutar acción al cambiar los valores de los indicadores
    @api.depends("indicadores_ids", "indicadores_ids_2")
    def compute_indicadores_ids(self):
        for record in self:
            real_total = 0.0
            meta_total = 0.0
            if record.indicadores_visible and record.indicadores_ids:
                for line in record.indicadores_ids:
                    real_total += line.real
                    meta_total += line.meta

            record.real_acumulado = real_total
            record.meta_acumulado = meta_total

    # calcula la diferencia y por ciento del acumulado
    # --- CÓDIGO CORREGIDO (Añadido depends) ---
    @api.depends('real_acumulado_kanban', 'meta_acumulado_kanban')
    def compute_diferencia_porciento(self):
        for item in self:
            # cálculo la diferencia del acumulado
            item.diferencia_acumulado = item.real_acumulado_kanban - item.meta_acumulado_kanban
            # cálculo del porcentaje del acumulado
            if item.real_acumulado_kanban != 0 and item.meta_acumulado_kanban != 0:
                item.porciento_avance = round(
                    item.real_acumulado_kanban / item.meta_acumulado_kanban, 2)
                item.porciento_avance_barra = round((
                                                            item.real_acumulado_kanban / item.meta_acumulado_kanban) * 100,
                                                    2)
            else:
                item.porciento_avance = 0
                item.porciento_avance_barra = 0

    # calcula el por ciento de los indicadores de la sección inferior
    @api.depends("indicadores_ids.real", "indicadores_ids.meta")
    def compute_calculo_porciento(self):
        for record in self:
            if record.indicadores_visible:
                meses = {'enero': 'porciento_enero',
                    'febrero': 'porciento_febrero', 'marzo': 'porciento_marzo',
                    'abril': 'porciento_abril', 'mayo': 'porciento_mayo',
                    'junio': 'porciento_junio', 'julio': 'porciento_julio',
                    'agosto': 'porciento_agosto',
                    'septiembre': 'porciento_septiembre',
                    'octubre': 'porciento_octubre',
                    'noviembre': 'porciento_noviembre',
                    'diciembre': 'porciento_diciembre'}

                # Inicializar a cero
                for campo in meses.values():
                    setattr(record, campo, 0.0)

                for line in record.indicadores_ids:
                    if line.mes in meses:
                        val = (
                                line.real / line.meta) if line.meta != 0 and line.real != 0 else 0.0
                        setattr(record, meses[line.mes], val)
            else:
                record.porciento_enero = 0
                record.porciento_febrero = 0
                record.porciento_marzo = 0
                record.porciento_abril = 0
                record.porciento_mayo = 0
                record.porciento_junio = 0
                record.porciento_julio = 0
                record.porciento_agosto = 0
                record.porciento_septiembre = 0
                record.porciento_octubre = 0
                record.porciento_noviembre = 0
                record.porciento_diciembre = 0

    # verífica que el usuario activo pertenezca al grupo Responsable
    @api.depends_context(
        'uid')  # Importante: el resultado depende del usuario que mira
    def _compute_grupo_responsable(self):
        has_group = self.env.user.has_group(
            'sicpro_app_cmi.grupo_app_cmi_responsable')
        for record in self:
            record.grupo_responsable = has_group

    # verifica q el usuario activo pertenezca al
    # grupo Responsable o sea responsable del indicador
    @api.depends('responsable_id')
    @api.depends_context('uid')
    def _compute_grupo_read_only(self):
        res_group = self.env.user.has_group(
            'sicpro_app_cmi.grupo_app_cmi_responsable')
        eje_group = self.env.user.has_group(
            'sicpro_app_cmi.grupo_app_cmi_ejecutor')
        current_uid = self.env.uid

        for record in self:
            # Simplificación de la lógica
            is_responsable = (record.responsable_id.id == current_uid)
            record.grupo_read_only = res_group or (
                    eje_group and is_responsable)

    # llama a la vista de grafica
    def grafica_indicadores_ids_graph(self):
        active_id = self.env.context.get('default_id')
        # elimino los registros del usuario actual
        self.env['sicpro.app.cmi.indicadores.graficos'].search(
            [('create_uid', '=', self.env.uid)]).unlink()
        # busco los registros de los valores del indicador
        indicador = self.env['sicpro.app.cmi.indicadores.valores'].search(
            [('indicador_id', '=', active_id)])
        # Crear registros de los meses
        for item in indicador:
            self.env['sicpro.app.cmi.indicadores.graficos'].sudo().create(
                {'mes': item.mes, 'valor': item.meta, 'tipo': 'meta'})
            self.env['sicpro.app.cmi.indicadores.graficos'].sudo().create(
                {'mes': item.mes, 'valor': item.real, 'tipo': 'real'})

        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.action_informes_indicadores_informes_graph')
        action['views'] = [(False, 'graph')]
        action['domain'] = [('create_uid', '=', self.env.uid)]
        return action

    # llama a la vista de pivot
    def grafica_indicadores_ids_pivot(self):
        active_id = self.env.context.get('default_id')
        # elimino los registros del usuario actual
        self.env['sicpro.app.cmi.indicadores.graficos'].search(
            [('create_uid', '=', self.env.uid)]).unlink()
        # busco los registros de los valores del indicador
        indicador = self.env['sicpro.app.cmi.indicadores.valores'].search(
            [('indicador_id', '=', active_id)])
        # Crear registros de los meses
        for item in indicador:
            self.env['sicpro.app.cmi.indicadores.graficos'].sudo().create(
                {'mes': item.mes, 'porciento_pivot': item.porciento_pivot,
                 'real_pivot': item.real, 'meta_pivot': item.meta,
                 'nombre': item.name.name})

        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.action_informes_indicadores_informes_pivot')
        action['views'] = [(False, 'pivot')]
        action['context'] = {'group_by': [],
                             'pivot_measures': ['real_pivot', 'meta_pivot',
                                                'porciento_pivot'],
                             'pivot_column_groupby': [],
                             'pivot_row_groupby': ['nombre', 'name']}
        action['domain'] = [('create_uid', '=', self.env.uid)]
        return action

    # Botón para eliminar el responsable de los seguidores del registro
    def unsubscribe_responsable(self):
        follower = self.responsable_follower.partner_id.ids
        super(AppCMIIndicadores, self).message_unsubscribe(
            partner_ids=follower)
        self.seguridad_responsable = False

    # ejecutar acción al cambiar el responsable del indicador
    @api.onchange("responsable_id")
    def _cambiar_responsable(self):
        if self.responsable_id:
            self.responsable_follower = self.responsable_id
            # Si el registro ya existe, suscribimos al nuevo responsable
            if self.indicadores_visible and self.id:
                self.seguridad_responsable = True
                self.message_subscribe(
                    partner_ids=self.responsable_follower.partner_id.ids)

    def crear_sub_indicadores(self):
        # Crear registros de los meses
        for mes in ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
                    'diciembre']:
            self.env['sicpro.app.cmi.indicadores.valores'].sudo().create(
                {'name': self._origin.id, 'indicador_id': self._origin.id,
                 'mes': mes, })
        # hago visible los valores de los indicadores
        self.indicadores_visible = True
        # hago invisible el botón del activador
        self.activador_visible = False
        self.message_subscribe(partner_ids=self.responsable_id.partner_id.ids)
        self.seguridad_responsable = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['activador_visible'] = True
        return super(AppCMIIndicadores, self).create(vals_list)


class AppCMIIndicadoresModalCambios(models.TransientModel):
    _name = 'sicpro.app.cmi.indicadores.modal.cambios'
    _description = 'Solicitud de cambios en los indicadores'
    _inherit = ['mail.thread']

    def _indicador_activo(self):
        active_id = self.env.context.get('default_id')
        return active_id

    indicadores_ids = fields.Many2one('sicpro.app.cmi.indicadores', string='Indicador', required=False,
                                      default=_indicador_activo)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, default=lambda self: self.env.uid)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, index=True)
    detalles = fields.Text(string="Detalles", required=True, tracking=True)
    meta_actual = fields.Integer(string='Meta Actual', compute='_cambiar_mes', store=True)
    meta_propuesta = fields.Integer(string='Meta Propuesta', required=True)
    responsable_id = fields.Many2one('res.users', string='Responsable', store=True,
                                     related='indicadores_ids.responsable_id')
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    mes = fields.Selection(
        [('enero', 'Enero'), ('febrero', 'Febrero'), ('marzo', 'Marzo'), ('abril', 'Abril'), ('mayo', 'Mayo'),
         ('junio', 'Junio'), ('julio', 'Julio'), ('agosto', 'Agosto'), ('septiembre', 'Septiembre'),
         ('octubre', 'Octubre'), ('noviembre', 'Noviembre'), ('diciembre', 'Diciembre')], required=True)

    # actualizo el valor de la meta según el mes
    @api.onchange("mes")
    def _cambiar_mes(self):
        data = self.env['sicpro.app.cmi.indicadores.valores'].search(
            ['&', ('indicador_id', '=', self.indicadores_ids.id), ('mes', '=', self.mes)])
        self.meta_actual = data.meta

    # envío la solicitud de cambio de meta
    def action_cambio_meta(self):
        data = self.env['sicpro.app.cmi.indicadores.valores'].search(
            ['&', ('indicador_id', '=', self.indicadores_ids.id), ('mes', '=', self.mes)])

        # Crear un registro de solicitud
        self.env['sicpro.app.cmi.indicadores.cambios'].sudo().create(
            {'detalles': self.detalles, 'name': self.indicadores_ids.id, 'meta_actual': data.meta,
             'meta_propuesta': self.meta_propuesta, 'responsable_id': self.responsable_id.id, 'mes': self.mes,
             'estado': 'pendiente', 'attachment_ids': self.attachment_ids, })

        # llamo al método para crear la notificación
        group_responsables = self.env.ref(
            'sicpro_app_cmi.grupo_app_cmi_responsable',
            raise_if_not_found=False)
        responsables = self.env['res.users']
        if group_responsables:
            responsables = group_responsables.user_ids

        post = self.env['sicpro.app.cmi.indicadores'].browse(self.env.context.get('active_ids'))
        post.message_subscribe(partner_ids=responsables.partner_id.ids)
        post.message_post(body='Cambio de Meta solicitado.', message_type='notification',
                          subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = post.env.context.copy()
            template = self.env.ref('sicpro_app_cmi.cmi_nueva_solicitud_cambio_indicador')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)

    # chequea que el valor de la meta propuesta no sea cero
    @api.constrains('meta_propuesta')
    def _check_meta_propuesta(self):
        if self.meta_propuesta == 0:
            raise ValidationError('El valor de la meta solicitada no puede ser 0.' + MSG_SOPORTE_SICPRO)
