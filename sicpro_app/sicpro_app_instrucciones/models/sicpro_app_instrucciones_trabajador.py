# -*- encoding: utf-8 -*-


from random import randint

import werkzeug

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class InstruccionesTrabajador(models.Model):
    _name = "sicpro.app.instrucciones.trabajador"
    _description = 'Instrucciones Laborales de los Trabajadores'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name asc"

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    def _trabajador_default(self):
        trabajador = self.env['sicpro.app.trabajadores'].search([('user_id', '=', self.env.uid)])
        return trabajador.id

    name = fields.Many2one('sicpro.app.trabajadores', string='Trabajador', required=True,
                           domain="[('area_id', 'in', area_id_instruccion)]", default=_trabajador_default)
    plaza_id = fields.Char(string="# Plaza", related="name.plaza_id", store=True)
    company_id_trabajador = fields.Many2one('res.company', string='Proceso del Trabajador', related="name.company_id",
                                            store=True)
    clase_contrato = fields.Many2one(comodel_name='sicpro.app.trabajadores.categorias', string='Clase de Contrato',
                                     related="name.clase_contrato", store=True)
    categoria_ocupacional = fields.Many2one(comodel_name='sicpro.app.trabajadores.categorias', store=True,
                                            string='Categoría Ocupacional', related="name.categoria_ocupacional")
    parent_id = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Jefe Inmediato',
                                related="name.parent_id", store=True)
    ocupacion_titulo = fields.Many2one(comodel_name='sicpro.app.trabajadores.ocupacion', string="Cargo",
                                       related="name.ocupacion_titulo", store=True, )
    area_id = fields.Many2one(comodel_name='sicpro.app.trabajadores.areas', string='Departamento',
                              related="name.area_id", store=True)
    inicio_contrato = fields.Date(string="Inicio del Contrato", related="name.inicio_contrato", store=True)
    fecha_incorporacion = fields.Date(string="Fecha de Incorporación", related="name.fecha_incorporacion", store=True)
    fecha_creacion = fields.Date(string='Fecha Creado', copy=False, default=fields.datetime.now(), readonly=True)
    user_id = fields.Many2one('res.users', string='Sesión', index=True, tracking=True, readonly=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Proceso Trabajador', required=True, readonly=True,
                                 related='name.company_id')
    active = fields.Boolean(string="Activo", default=True, )
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    estado_ids = fields.Selection(string='Estado', store=True, compute="_compute_estado_id",
                                  selection=[('aprobado', 'Aprobado'), ('suspenso', 'Suspenso')], )
    instrucciones_id = fields.Many2one('sicpro.app.instrucciones.instruccion', string='Instrucción', required=True, )
    descripcion = fields.Text("Descripción", store=True, related="instrucciones_id.descripcion")
    desde = fields.Date(string='Desde', store=True, related="instrucciones_id.fecha_inicio", )
    hasta = fields.Date(string='Hasta', store=True, related="instrucciones_id.fecha_fin", )
    company_id_instruccion = fields.Many2one('res.company', string='Proceso de Instrucción',
                                             related="instrucciones_id.company_id", )
    area_id_instruccion = fields.Many2many('sicpro.app.trabajadores.areas', 'sicpro_app_instrucciones_trab_areaid_rel',
                                           string='Departamentos', related="instrucciones_id.area_id", )
    tipo = fields.Selection(string='Tipo de Instrucción', store=True, related="instrucciones_id.tipo")
    abreviatura_IG = fields.Char(string='IG', compute="compute_tipo_instruccion")
    abreviatura_IE = fields.Char(string='IE', compute="compute_tipo_instruccion")
    abreviatura_P = fields.Char(string='P', compute="compute_tipo_instruccion")
    abreviatura_ET = fields.Char(string='ET', compute="compute_tipo_instruccion")
    abreviatura_OP = fields.Char(string='OP', compute="compute_tipo_instruccion")
    abreviatura_EM = fields.Char(string='EM', compute="compute_tipo_instruccion")
    abreviatura_EP = fields.Char(string='EP', compute="compute_tipo_instruccion")
    abreviatura_TC = fields.Char(string='TC', compute="compute_tipo_instruccion")
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos", related="instrucciones_id.attachment_ids")
    encuesta_id = fields.Many2one('survey.survey', "Encuesta", readonly=True, related="instrucciones_id.encuesta_id")
    response_id = fields.Many2one('survey.user_input', "respuesta id", ondelete="set null")
    response_id_final = fields.Many2one('survey.user_input', "Respuestas", compute='_compute_response_final')
    encuesta_aprobado = fields.Boolean(string='Está Aprobado?', store=True, related="response_id_final.scoring_success")
    encuesta_calificacion = fields.Float(string='Calificación (%)', store=True,
                                         related="response_id_final.scoring_percentage")
    partner_id = fields.Many2one('res.partner', "Contacto", copy=False)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    acepto_acuerdo_instrucion = fields.Boolean(string='Acepto_acuerdo_instrucion', default=False, required=False)

    def _compute_response_final(self):
        for item in self:
            valor_superior = 0
            response_id_final = None
            respuestas = self.env['survey.user_input'].search([
                ('survey_id', '=', item.encuesta_id.id), ('partner_id', '=', item.name.user_id.partner_id.id)])
            for value in respuestas:
                # comparo las puntaciones y me quedo con la mayor
                if value.scoring_percentage > valor_superior:
                    valor_superior = value.scoring_percentage
                    response_id_final = value.id
            item.response_id_final = response_id_final

    # verífico que no exista el mismo trabajador con la misma instrucción
    @api.constrains('name')
    def _check_name_instrucciones_unico(self):
        uniq = self.env['sicpro.app.instrucciones.trabajador'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name.id),
             ("instrucciones_id", "=", self.instrucciones_id.id), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("El trabajador ya realizó la encuesta para esta Instrucción. "
                                    "Si cree que es un error contacte al administrador"))

    # iniciar cuestionario por el trabajador
    def action_iniciar_encuesta(self):
        self.ensure_one()
        # crea una nueva encuesta al trabajador
        if not self.response_id:
            response = self.encuesta_id.sudo()._create_answer(user=self.name.user_id)
            self.response_id = response
        else:
            response = self.response_id

        # ejecuto el context temporal del usuario para ejecutar la encuesta
        usuario = self.env["res.users"].browse(self.env.user.id)
        usuario.sudo().write({"intrucciones_context": True, })

        # Abre encuesta creada al trabajador
        return self.encuesta_id.action_start_survey(answer=response)

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
    def compute_tipo_instruccion(self):
        for item in self:
            tipo = item.tipo
            if tipo == 'IG':
                item.abreviatura_IG = 'X'
            else:
                item.abreviatura_IG = ''
            if tipo == 'IE':
                item.abreviatura_IE = 'X'
            else:
                item.abreviatura_IE = ''
            if tipo == 'P':
                item.abreviatura_P = 'X'
            else:
                item.abreviatura_P = ''
            if tipo == 'ET':
                item.abreviatura_ET = 'X'
            else:
                item.abreviatura_ET = ''
            if tipo == 'OP':
                item.abreviatura_OP = 'X'
            else:
                item.abreviatura_OP = ''
            if tipo == 'EM':
                item.abreviatura_EM = 'X'
            else:
                item.abreviatura_EM = ''
            if tipo == 'EP':
                item.abreviatura_EP = 'X'
            else:
                item.abreviatura_EP = ''
            if tipo == 'TC':
                item.abreviatura_TC = 'X'
            else:
                item.abreviatura_TC = ''
