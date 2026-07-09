# -*- coding: utf-8 -*-


from random import randint
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api, _


def _default_color():
    return randint(1, 11)


class AppCMIIndicadores(models.Model):
    _name = 'sicpro.app.cmi.indicadores'
    _order = "id asc"
    _description = 'Indicadores del CMI'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _compute_buscar_anios(self):
        anio_obj = self.env['sicpro.app.cmi.perspectivas.anios'].search([('active', '=', True)])
        lst = []
        for anios in anio_obj:
            lst.append((anios.anio, anios.anio))
        return lst

    # Busca los datos de los objetivos anuales
    def _context_anio(self):
        if not self._context.get('obj_anuales_id'):
            raise UserError(_('Para agregar un registro debe iniciar desde él '
                              'tablero de Años.'))
        else:
            valor = str(self._context.get('obj_anuales_id'))
            anio = self.env['sicpro.app.cmi.objetivos.anuales'].search([('id', '=', valor)]).anio
            return anio

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char('Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, default=lambda self: self.env.uid)
    responsable_id = fields.Many2one('res.users', string='Responsable', index=True, required=True)
    responsable_follower = fields.Many2one('res.users', string='follower')
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, )
    condicion_presupuesto = fields.Boolean(string="Condición de Presupuesto", default=False, )
    obj_anuales_id = fields.Many2one('sicpro.app.cmi.objetivos.anuales', string='Objetivo Anual', required=True,
        default=lambda self: self._context.get('obj_anuales_id'))
    anio = fields.Selection(selection=_compute_buscar_anios, string="Año", default=_context_anio, copy=False, )
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    detalles = fields.Text(string="Detalles", required=False)
    indicadores_ids = fields.One2many(comodel_name='sicpro.app.cmi.indicadores.valores', copy=False,
        inverse_name='indicador_id', string='Indicadores', required=False)
    indicadores_ids_2 = fields.One2many(comodel_name='sicpro.app.cmi.indicadores.valores', copy=False,
        inverse_name='indicador_id', string='Lista de Indicadores', required=False, related='indicadores_ids')
    acciones_ids = fields.One2many(comodel_name='sicpro.app.cmi.acciones', inverse_name='indicador_id', copy=False,
                                   string='Acciones', required=False)
    indicadores_visible = fields.Boolean(string='Indicadores_visible', required=False, default=False, copy=False, )
    activador_visible = fields.Boolean(string='Activador_visible', copy=False, required=False, default=False)
    grupo_responsable = fields.Boolean(string='grupo_responsable', compute="_compute_grupo_responsable",
        default=lambda self: self._compute_grupo_responsable())
    grupo_read_only = fields.Boolean(string='grupo_read_only', compute="_compute_grupo_read_only")
    porciento_enero = fields.Float(string='Porciento Ene', compute='compute_calculo_porciento')
    porciento_febrero = fields.Float(string='Porciento Feb', compute='compute_calculo_porciento')
    porciento_marzo = fields.Float(string='Porciento Mar', compute='compute_calculo_porciento')
    porciento_abril = fields.Float(string='Porciento Abr', compute='compute_calculo_porciento')
    porciento_mayo = fields.Float(string='Porciento May', compute='compute_calculo_porciento')
    porciento_junio = fields.Float(string='Porciento jun', compute='compute_calculo_porciento')
    porciento_julio = fields.Float(string='Porciento jul', compute='compute_calculo_porciento')
    porciento_agosto = fields.Float(string='Porciento Ago', compute='compute_calculo_porciento')
    porciento_septiembre = fields.Float(string='Porciento Sep', compute='compute_calculo_porciento')
    porciento_octubre = fields.Float(string='Porciento Oct', compute='compute_calculo_porciento')
    porciento_noviembre = fields.Float(string='Porciento Nov', compute='compute_calculo_porciento')
    porciento_diciembre = fields.Float(string='Porciento Dic', compute='compute_calculo_porciento')
    real_acumulado = fields.Float(string='Real Acumulado', store=True, compute='compute_indicadores_ids')
    meta_acumulado = fields.Float(string='Objetivo Acumulado', store=True, compute='compute_indicadores_ids')
    real_acumulado_kanban = fields.Float(string='Real Acumulado Kanban', compute='compute_acumulado')
    meta_acumulado_kanban = fields.Float(string='Objetivo Acumulado Kanban', compute='compute_acumulado')
    diferencia_acumulado = fields.Float(string='diferencia', compute='compute_diferencia_porciento')
    porciento_avance = fields.Float(string='Porciento Avance', compute='compute_diferencia_porciento')
    porciento_avance_barra = fields.Float(string='Avance', compute='compute_diferencia_porciento')
    comentario = fields.Text(string="Comentario", required=False, copy=False)
    seguridad_responsable = fields.Boolean(string='Seguridad_responsable', required=False, default=False, copy=False, )

    # calcula real y acumulado anual de sus indicadores
    def compute_acumulado(self):
        for data in self:
            periodo = self._context.get('default_periodo')
            real = 0
            meta = 0

            # Verifica el mes correspondiente
            if periodo in (
                    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
                    'noviembre', 'diciembre'):
                obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', data.id), ('mes', '=', periodo)])
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el primer trimestre
            elif periodo == '1t':
                obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', data.id), ('mes', 'in', ('enero', 'febrero', 'marzo'))])
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

                # Verifica el segundo trimestre

            elif periodo == '2t':
                obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', data.id), ('mes', 'in', ('abril', 'mayo', 'junio'))])
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el tercer trimestre
            elif periodo == '3t':
                obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', data.id), ('mes', 'in', ('julio', 'agosto', 'septiembre'))])
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el cuarto trimestre
            elif periodo == '4t':
                obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', data.id), ('mes', 'in', ('octubre', 'noviembre', 'diciembre'))])
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el primer semestre
            elif periodo == '1s':
                obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', data.id),
                     ('mes', 'in', ('enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio'))])
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el segundo semestre
            elif periodo == '2s':
                obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', data.id),
                     ('mes', 'in', ('julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'))])
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # Verifica el anual
            elif periodo == 'anual':
                obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', data.id), ('mes', 'in', (
                        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
                        'octubre', 'noviembre', 'diciembre'))])
                # sumo los valores totales del real y meta
                for inds in obj_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            # paso los valores a los campos
            data.real_acumulado_kanban = real
            data.meta_acumulado_kanban = meta

    # ejecutar acción al cambiar los valores de los indicadores
    @api.depends("indicadores_ids", "indicadores_ids_2")
    @api.onchange("indicadores_ids", "indicadores_ids_2")
    def compute_indicadores_ids(self):
        anio_activo = self._context.get('default_anual')
        periodo = self._context.get('default_periodo')
        real = 0
        meta = 0
        if self.indicadores_visible:
            listado = []
            datos = self.env['sicpro.app.cmi.indicadores.valores'].search([('indicador_id', '=', self._origin.id)])

            for data in datos:
                listado.append({"mes": data.mes, "real": data.real, "meta": data.meta})

            ene_real = listado[0]['real']
            feb_real = listado[1]['real']
            mar_real = listado[2]['real']
            abr_real = listado[3]['real']
            may_real = listado[4]['real']
            jun_real = listado[5]['real']
            jul_real = listado[6]['real']
            ago_real = listado[7]['real']
            sep_real = listado[8]['real']
            oct_real = listado[9]['real']
            nov_real = listado[10]['real']
            dic_real = listado[11]['real']

            ene_meta = listado[0]['meta']
            feb_meta = listado[1]['meta']
            mar_meta = listado[2]['meta']
            abr_meta = listado[3]['meta']
            may_meta = listado[4]['meta']
            jun_meta = listado[5]['meta']
            jul_meta = listado[6]['meta']
            ago_meta = listado[7]['meta']
            sep_meta = listado[8]['meta']
            oct_meta = listado[9]['meta']
            nov_meta = listado[10]['meta']
            dic_meta = listado[11]['meta']

            # valor del acumulado trimestre 1
            real_acumulado_trimestre1 = ene_real + feb_real + mar_real
            meta_acumulado_trimestre1 = ene_meta + feb_meta + mar_meta

            # valor del acumulado trimestre 2
            real_acumulado_trimestre2 = abr_real + may_real + jun_real
            meta_acumulado_trimestre2 = abr_meta + may_meta + jun_meta

            # valor del acumulado trimestre 3
            real_acumulado_trimestre3 = jul_real + ago_real + sep_real
            meta_acumulado_trimestre3 = jul_meta + ago_meta + sep_meta

            # valor del acumulado trimestre 4
            real_acumulado_trimestre4 = oct_real + nov_real + dic_real
            meta_acumulado_trimestre4 = oct_meta + nov_meta + dic_meta

            # valor del acumulado semestre 1
            real_acumulado_semestre1 = ene_real + feb_real + mar_real + abr_real + may_real + jun_real
            meta_acumulado_semestre1 = ene_meta + feb_meta + mar_meta + abr_meta + may_meta + jun_meta

            # valor del acumulado semestre 2
            real_acumulado_semestre2 = jul_real + ago_real + sep_real + oct_real + nov_real + dic_real
            meta_acumulado_semestre2 = jul_meta + ago_meta + sep_meta + oct_meta + nov_meta + dic_meta

            # valor del acumulado anual
            real_acumulado_anual = ene_real + feb_real + mar_real + abr_real + may_real + jun_real + jul_real + ago_real + sep_real + oct_real + nov_real + dic_real
            meta_acumulado_anual = ene_meta + feb_meta + mar_meta + abr_meta + may_meta + jun_meta + jul_meta + ago_meta + sep_meta + oct_meta + nov_meta + dic_meta

            # actualización anual
            self.real_acumulado = real_acumulado_anual
            self.meta_acumulado = meta_acumulado_anual

    # calcula la diferencia y porciento del acumulado
    def compute_diferencia_porciento(self):
        for item in self:
            # calculo la diferencia del acumulado
            item.diferencia_acumulado = item.real_acumulado_kanban - item.meta_acumulado_kanban
            # calculo del porcentaje del acumulado
            if item.real_acumulado_kanban != 0 and item.meta_acumulado_kanban != 0:
                item.porciento_avance = round(item.real_acumulado_kanban / item.meta_acumulado_kanban, 2)
                item.porciento_avance_barra = round((item.real_acumulado_kanban / item.meta_acumulado_kanban) * 100, 2)
            else:
                item.porciento_avance = 0
                item.porciento_avance_barra = 0

    # calcula el porciento de los indicadores de la sección inferior
    def compute_calculo_porciento(self):
        if self.indicadores_visible:
            listado = []
            datos = self.env['sicpro.app.cmi.indicadores.valores'].search([('indicador_id', '=', self._origin.id)])

            # creo lista con los valores del real y meta por meses
            for data in datos:
                listado.append({"mes": data.mes, "real": data.real, "meta": data.meta})

            # calculo del porcentaje en meses
            if listado[0]['real'] != 0 and listado[0]['meta'] != 0:
                self.porciento_enero = listado[0]['real'] / listado[0]['meta']
            else:
                self.porciento_enero = 0

            if listado[1]['real'] != 0 and listado[1]['meta'] != 0:
                self.porciento_febrero = listado[1]['real'] / listado[1]['meta']
            else:
                self.porciento_febrero = 0

            if listado[2]['real'] != 0 and listado[2]['meta'] != 0:
                self.porciento_marzo = listado[2]['real'] / listado[2]['meta']
            else:
                self.porciento_marzo = 0

            if listado[3]['real'] != 0 and listado[3]['meta'] != 0:
                self.porciento_abril = listado[3]['real'] / listado[3]['meta']
            else:
                self.porciento_abril = 0

            if listado[4]['real'] != 0 and listado[4]['meta'] != 0:
                self.porciento_mayo = listado[4]['real'] / listado[4]['meta']
            else:
                self.porciento_mayo = 0

            if listado[5]['real'] != 0 and listado[5]['meta'] != 0:
                self.porciento_junio = listado[5]['real'] / listado[5]['meta']
            else:
                self.porciento_junio = 0

            if listado[6]['real'] != 0 and listado[6]['meta'] != 0:
                self.porciento_julio = listado[6]['real'] / listado[6]['meta']
            else:
                self.porciento_julio = 0

            if listado[7]['real'] != 0 and listado[7]['meta'] != 0:
                self.porciento_agosto = listado[7]['real'] / listado[7]['meta']
            else:
                self.porciento_agosto = 0

            if listado[8]['real'] != 0 and listado[8]['meta'] != 0:
                self.porciento_septiembre = listado[8]['real'] / listado[8]['meta']
            else:
                self.porciento_septiembre = 0

            if listado[9]['real'] != 0 and listado[9]['meta'] != 0:
                self.porciento_octubre = listado[9]['real'] / listado[9]['meta']
            else:
                self.porciento_octubre = 0

            if listado[10]['real'] != 0 and listado[10]['meta'] != 0:
                self.porciento_noviembre = listado[10]['real'] / listado[10]['meta']
            else:
                self.porciento_noviembre = 0

            if listado[11]['real'] != 0 and listado[11]['meta'] != 0:
                self.porciento_diciembre = listado[11]['real'] / listado[11]['meta']
            else:
                self.porciento_diciembre = 0
        else:
            self.porciento_enero = 0
            self.porciento_febrero = 0
            self.porciento_marzo = 0
            self.porciento_abril = 0
            self.porciento_mayo = 0
            self.porciento_junio = 0
            self.porciento_julio = 0
            self.porciento_agosto = 0
            self.porciento_septiembre = 0
            self.porciento_octubre = 0
            self.porciento_noviembre = 0
            self.porciento_diciembre = 0

    # verifica q el usuario activo pertenezca al grupo Responsable
    def _compute_grupo_responsable(self):
        resp = self.env['res.users'].has_group('sicpro_app_cmi.grupo_app_cmi_responsable')
        self.grupo_responsable = resp
        return resp

    # verifica q el usuario activo pertenezca al
    # grupo Responsable o sea responsable del indicador
    def _compute_grupo_read_only(self):
        responsable = self.env['res.users'].has_group('sicpro_app_cmi.grupo_app_cmi_responsable')
        ejecutor = self.env['res.users'].has_group('sicpro_app_cmi.grupo_app_cmi_ejecutor')

        if responsable:
            self.grupo_read_only = True
        else:
            if ejecutor and self.responsable_id.id == self.env.uid:
                self.grupo_read_only = True
            else:
                self.grupo_read_only = False

    # llama a la vista de grafica
    def grafica_indicadores_ids_graph(self):
        active_id = self._context.get('default_id')
        # elimino los registros del usuario actual
        self.env['sicpro.app.cmi.indicadores.graficos'].search([('create_uid', '=', self.env.uid)]).unlink()
        # busco los registros de los valores del indicador
        indicador = self.env['sicpro.app.cmi.indicadores.valores'].search([('indicador_id', '=', active_id)])
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
        active_id = self._context.get('default_id')
        # elimino los registros del usuario actual
        self.env['sicpro.app.cmi.indicadores.graficos'].search([('create_uid', '=', self.env.uid)]).unlink()
        # busco los registros de los valores del indicador
        indicador = self.env['sicpro.app.cmi.indicadores.valores'].search([('indicador_id', '=', active_id)])
        # Crear registros de los meses
        for item in indicador:
            self.env['sicpro.app.cmi.indicadores.graficos'].sudo().create(
                {'mes': item.mes, 'porciento_pivot': item.porciento_pivot, 'real_pivot': item.real,
                 'meta_pivot': item.meta, 'nombre': item.name.name})

        action = self.env['ir.actions.act_window']._for_xml_id(
            'sicpro_app_cmi.action_informes_indicadores_informes_pivot')
        action['views'] = [(False, 'pivot')]
        action['context'] = {'group_by': [], 'pivot_measures': ['real_pivot', 'meta_pivot', 'porciento_pivot'],
                             'pivot_column_groupby': [], 'pivot_row_groupby': ['nombre', 'name']}
        action['domain'] = [('create_uid', '=', self.env.uid)]
        return action

    # Botón para eliminar el responsable de los seguidores del registro
    def unsubscribe_responsable(self):
        follower = self.responsable_follower.partner_id.ids
        super(AppCMIIndicadores, self).message_unsubscribe(partner_ids=follower)
        self.seguridad_responsable = False

    # ejecutar acción al cambiar el responsable del indicador
    @api.onchange("responsable_id")
    def _cambiar_responsable(self):
        if self.responsable_id:
            self.responsable_follower = self.responsable_id
            if self.indicadores_visible:
                self.seguridad_responsable = True
                self.message_subscribe(partner_ids=self.responsable_follower.partner_id.ids)
                self.env['sicpro.app.cmi.indicadores'].search([('id', '=', self._origin.id)]).update(
                    {'responsable_id': self.responsable_follower})

    def crear_sub_indicadores(self):
        # Crear registros de los meses
        for mes in ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
                    'noviembre', 'diciembre']:
            self.env['sicpro.app.cmi.indicadores.valores'].sudo().create(
                {'name': self._origin.id, 'indicador_id': self._origin.id, 'mes': mes, })
        # hago visible los valores de los indicadores
        self.indicadores_visible = True
        # hago invisible el botón del activador
        self.activador_visible = False
        self.message_subscribe(partner_ids=self.responsable_id.partner_id.ids)
        self.seguridad_responsable = True

    @api.model
    def create(self, vals):
        # hago visible el activador de los indicadores
        res = super(AppCMIIndicadores, self).create(vals)
        res['activador_visible'] = True
        return res


class AppCMIIndicadoresModalCambios(models.TransientModel):
    _name = 'sicpro.app.cmi.indicadores.modal.cambios'
    _description = 'Solicitud de cambios en los indicadores'
    _inherit = ['mail.thread']

    def _indicador_activo(self):
        active_id = self._context.get('default_id')
        return active_id

    indicadores_ids = fields.Many2one('sicpro.app.cmi.indicadores', string='Indicador', required=False,
                                      default=_indicador_activo)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, default=lambda self: self.env.uid)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, )
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
        responsables = self.env.ref('sicpro_app_cmi.grupo_app_cmi_responsable').users
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
            raise ValidationError(_('El valor de la meta solicitada no puede ser 0.'))
