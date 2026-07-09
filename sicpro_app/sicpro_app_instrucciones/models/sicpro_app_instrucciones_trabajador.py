# -*- encoding: utf-8 -*-


from random import randint

from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class InstruccionesTrabajador(models.Model):
    _name = "sicpro.app.instrucciones.trabajador"
    _description = 'Instrucciones Laborales de los Trabajadores'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name asc"

    def _trabajador_default(self):
        trabajador = self.env['sicpro.app.trabajadores'].search(
            [('user_id', '=', self.env.uid)])
        return trabajador.id

    name = fields.Many2one('sicpro.app.trabajadores', string='Trabajador',
                           required=True,
                           domain="[('area_id', 'in', area_id_instruccion)]",
                           default=_trabajador_default)
    plaza_id = fields.Char(string="# Plaza", related="name.plaza_id",
                           store=True)
    company_id_trabajador = fields.Many2one('res.company',
                                            string='Proceso del Trabajador',
                                            related="name.company_id",
                                            store=True)
    clase_contrato = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.categorias',
        string='Clase de Contrato', related="name.clase_contrato", store=True)
    categoria_ocupacional = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.categorias', store=True,
        string='Categoría Ocupacional', related="name.categoria_ocupacional")
    parent_id = fields.Many2one(comodel_name='sicpro.app.trabajadores',
                                string='Jefe Inmediato',
                                related="name.parent_id", store=True)
    ocupacion_titulo = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.ocupacion', string="Cargo",
        related="name.ocupacion_titulo", store=True, )
    area_id = fields.Many2one(comodel_name='sicpro.app.trabajadores.areas',
                              string='Departamento', related="name.area_id",
                              store=True)
    inicio_contrato = fields.Date(string="Inicio del Contrato",
                                  related="name.inicio_contrato", store=True)
    fecha_incorporacion = fields.Date(string="Fecha de Incorporación",
                                      related="name.fecha_incorporacion",
                                      store=True)
    fecha_creacion = fields.Date(string='Fecha Creado', copy=False,
                                 default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one('res.users', string='Sesión', index=True,
                              tracking=True, readonly=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso Trabajador',
                                 required=True, readonly=True,
                                 related='name.company_id')
    active = fields.Boolean(string="Activo", default=True, index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    estado_ids = fields.Selection(string='Estado', store=True,
                                  compute="_compute_estado_id",
                                  selection=[('aprobado', 'Aprobado'),
                                             ('suspenso', 'Suspenso')], )
    instrucciones_id = fields.Many2one('sicpro.app.instrucciones.instruccion',
                                       string='Instrucción', required=True, )
    descripcion = fields.Text(string="Descripción", store=True,
                              related="instrucciones_id.descripcion")
    desde = fields.Date(string='Desde', store=True,
                        related="instrucciones_id.fecha_inicio", )
    hasta = fields.Date(string='Hasta', store=True,
                        related="instrucciones_id.fecha_fin", )
    company_id_instruccion = fields.Many2one('res.company',
                                             string='Proceso de Instrucción',
                                             related="instrucciones_id.company_id", )
    area_id_instruccion = fields.Many2many('sicpro.app.trabajadores.areas',
                                           'sicpro_app_instrucciones_trab_areaid_rel',
                                           string='Departamentos',
                                           related="instrucciones_id.area_id", )
    tipo = fields.Selection(string='Tipo de Instrucción', store=True,
                            related="instrucciones_id.tipo")
    abreviatura_IG = fields.Char(string='IG',
                                 compute="compute_tipo_instruccion")
    abreviatura_IE = fields.Char(string='IE',
                                 compute="compute_tipo_instruccion")
    abreviatura_P = fields.Char(string='P', compute="compute_tipo_instruccion")
    abreviatura_ET = fields.Char(string='ET',
                                 compute="compute_tipo_instruccion")
    abreviatura_OP = fields.Char(string='OP',
                                 compute="compute_tipo_instruccion")
    abreviatura_EM = fields.Char(string='EM',
                                 compute="compute_tipo_instruccion")
    abreviatura_EP = fields.Char(string='EP',
                                 compute="compute_tipo_instruccion")
    abreviatura_TC = fields.Char(string='TC',
                                 compute="compute_tipo_instruccion")
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos",
                                      related="instrucciones_id.attachment_ids")
    encuesta_id = fields.Many2one('survey.survey', "Encuesta", readonly=True,
                                  related="instrucciones_id.encuesta_id")
    response_id = fields.Many2one('survey.user_input', "respuesta id",
                                  ondelete="set null")
    response_id_final = fields.Many2one('survey.user_input', "Respuestas",
                                        compute='_compute_response_final',
                                        store=True)
    encuesta_aprobado = fields.Boolean(string='Está Aprobado?', store=True,
                                       related="response_id_final.scoring_success")
    encuesta_calificacion = fields.Float(string='Calificación (%)', store=True,
                                         related="response_id_final.scoring_percentage")
    partner_id = fields.Many2one('res.partner', "Contacto", copy=False)
    acepto_acuerdo_instrucion = fields.Boolean(
        string='Acepto_acuerdo_instrucion', default=False, required=False)

    @api.depends('encuesta_id', 'name.user_id', 'response_id.state')
    def _compute_response_final(self):
        for item in self:
            # Validación inicial de seguridad
            if not item.encuesta_id or not item.name or not item.name.user_id:
                item.response_id_final = False
                continue

            # Buscamos las respuestas terminadas de este trabajador para esta encuesta
            # Usamos sudo() por si el trabajador no tiene permisos de lectura generales en survey
            respuestas = self.env['survey.user_input'].sudo().search(
                [('survey_id', '=', item.encuesta_id.id),
                 ('partner_id', '=', item.name.user_id.partner_id.id),
                 ('state', '=', 'done')], order='scoring_percentage desc',
                limit=1)

            # Al usar order y limit en el search, obtenemos directamente la mejor o ninguna
            if respuestas:
                item.response_id_final = respuestas.id
            else:
                item.response_id_final = False

    # verífico que no exista el mismo trabajador con la misma instrucción
    @api.constrains('name', 'instrucciones_id')
    def _check_name_instrucciones_unico(self):
        for record in self:
            domain = [("active", "=", True), ("name", "=", record.name.id),
                      ("instrucciones_id", "=", record.instrucciones_id.id),
                      ("id", "!=", record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "El trabajador ya tiene asignada esta Instrucción.\n\n" + MSG_SOPORTE_SICPRO)

    # actualiza el estado de los cuestionarios del trabajador
    @api.depends('encuesta_calificacion', 'encuesta_aprobado')
    def _compute_estado_id(self):
        for stat in self:
            if stat.encuesta_calificacion and stat.encuesta_aprobado:
                stat.estado_ids = 'aprobado'
            elif stat.encuesta_calificacion and stat.encuesta_aprobado == False:
                stat.estado_ids = 'suspenso'
            else:
                stat.estado_ids = ''

    # lleno los campos por el tipo de Instrucción
    @api.depends('tipo')
    def compute_tipo_instruccion(self):
        tipos = ['IG', 'IE', 'P', 'ET', 'OP', 'EM', 'EP', 'TC']
        for item in self:
            for t in tipos:
                # Asignamos 'X' si coincide, si no, cadena vacía
                setattr(item, f'abreviatura_{t}',
                        'X' if item.tipo == t else '')

    # ACCIÓN: Iniciar Encuesta con Sudo controlado
    def action_iniciar_encuesta(self):
        self.ensure_one()

        # 1. Validaciones de negocio
        if not self.encuesta_id:
            raise ValidationError(
                "Esta instrucción no tiene una encuesta vinculada.")

        if not self.acepto_acuerdo_instrucion:
            raise ValidationError(
                "Debe aceptar los términos antes de iniciar.")

        # 2. Gestión de la Respuesta (User Input)
        if not self.response_id:
            # Creamos la respuesta vinculada al usuario actual
            # Eliminamos check_is_finished para evitar el ValueError anterior
            response = self.encuesta_id.sudo()._create_answer(
                user=self.env.user)
            self.sudo().write({'response_id': response.id})
        else:
            response = self.response_id

        # 3. Marcar el contexto para el controlador
        # Esto es vital para que tu controlador Instrucciones(Survey) salte la validación de partner
        self.env.user.sudo().write({"intrucciones_context": True})

        # 4. Redirección forzada con manejo de parámetros de URL
        base_url = response.get_start_url()
        # Verificamos si la URL ya tiene parámetros para usar '?' o '&'
        join_char = '&' if '?' in base_url else '?'
        final_url = f"{base_url}{join_char}answer_token={response.access_token}"

        return {'type': 'ir.actions.act_url', 'name': "Cuestionario",
                'target': 'self', 'url': final_url}
