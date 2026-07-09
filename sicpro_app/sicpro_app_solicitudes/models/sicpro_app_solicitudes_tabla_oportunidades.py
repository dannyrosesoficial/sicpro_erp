# -*- coding: utf-8 -*-

from odoo import fields, models


Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'),
                       ('2', 'Alta'), ('3', 'Muy Alta'),
]


class SolicitudesTablaOportunidades(models.Model):
    _name = 'sicpro.app.solicitudes.tabla.oportunidades'
    _description = "Tabla de Solicitudes y oportunidades"
    _order = 'priority desc, id asc'
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    oportunidades = fields.Many2one(
        comodel_name='sicpro.app.solicitudes.oportunidades',
        string='Oportunidades')
    name = fields.Char(string="Oportunidad", related='oportunidades.name',
                       store=True)
    id_solicitud = fields.Char(string='Solicitud ID', store=True,
                               related='oportunidades.id_solicitud')
    partner_id = fields.Many2one('sicpro.app.clientes', string='Cliente',
                                 store=True,
                                 related='oportunidades.partner_id')
    partner_name = fields.Char("Nombre de la entidad",
                               related='oportunidades.partner_name', store=True,)
    territorio_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.territorios", string="Territorio",
        related='oportunidades.territorio_id', store=True, )
    provincia_id = fields.Many2one(comodel_name="sicpro.nomenclador.provincia",
                                   store=True, string="Provincia",
                                   related='oportunidades.provincia_id')
    website = fields.Char('Sitio Web', related='oportunidades.website',
                          store=True,)
    cargo = fields.Char(string="Cargo",
                        related='oportunidades.cargo', store=True, )
    telefono_fijo = fields.Char(string="Teléfono",
                                related='oportunidades.telefono_fijo',
                                store=True,)
    telefono_movil = fields.Char(string="Móvil",
                                 related='oportunidades.telefono_movil',
                                 store=True,)
    correo = fields.Char(string="Correo electrónico",
                         related='oportunidades.correo', store=True,)
    pagina_web = fields.Char(string="Pagina Web",
                             related='oportunidades.pagina_web', store=True,)
    active = fields.Boolean('Activo', related='oportunidades.active')
    color = fields.Integer('Indice de colores', related='oportunidades.color',
                           store=True,)

    especialista_ejecutor = fields.Many2one(
        comodel_name="sicpro.app.trabajadores", string='Asignar a', store=True,
        related='oportunidades.especialista_ejecutor')
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Área',
                              related='especialista_ejecutor.area_id')
    cargo_especialista = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.ocupacion", string='Cargo.',
        store=True,
        related='oportunidades.cargo_especialista')
    description = fields.Text('Notes', related='oportunidades.description',
                              store=True,)
    observaciones_grupo_ejecutor = fields.Text(
        'observaciones', store=True,
        related='oportunidades.observaciones_grupo_ejecutor')
    tag_ids = fields.Many2many(
        'sicpro.app.solicitudes.etiquetas',
        'sicpro_app_solicitudes_iniciativas_tabla_etiquetas_rel',
        'lead_id', 'tag_id', string='Etiqueta',)
    priority = fields.Selection(string='Prioridad', store=True,
                                related='oportunidades.priority')
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 store=True,
                                 related='oportunidades.company_id')
    departamento = fields.Many2one(
        'sicpro.app.trabajadores.areas', string="Departamento", store=True,
        related='oportunidades.departamento')
    company_cliente = fields.Many2one('res.company', store=True,
                                      string='Proceso del Cliente',
                                      related='oportunidades.company_cliente')
    fecha_solicitud_trabajo = fields.Date(
        'Fecha de solicitud', store=True,
        related='oportunidades.fecha_solicitud_trabajo')
    anio = fields.Char(string="Año", related='oportunidades.anio', store=True,)
    fecha_aprobacion = fields.Date('Fecha de aprobación',
                                   related='oportunidades.fecha_aprobacion',
                                   store=True,)
    fecha_asignacion = fields.Date('Fecha de asignación',
                                   related='oportunidades.fecha_asignacion',
                                   store=True,)
    pep_corto = fields.Char(string='Número SAP',
                            related='oportunidades.pep_corto', store=True,)
    ejecucion_proyecto = fields.Boolean(
        string="Proyecto", related='oportunidades.ejecucion_proyecto',
        store=True,)
    consecutivo_proyecto = fields.Char(
        string="Consecutivo", related='oportunidades.consecutivo_proyecto',
        store=True, )
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos",
                                      related='oportunidades.attachment_ids')
    ejecucion_tt = fields.Boolean(string="Tarea Técnica",
                                  related='oportunidades.ejecucion_tt',
                                  store=True,)
    codigo_tt = fields.Char(string="Código TT",
                            related='oportunidades.codigo_tt', store=True,)
    datos_equipamiento_1 = fields.Boolean(
        string="En Espera llegada a Cuba",
        related='oportunidades.datos_equipamiento_1', store=True,)
    datos_equipamiento_2 = fields.Boolean(
        string="En Almacén de ETECSA",
        related='oportunidades.datos_equipamiento_2', store=True,)
    datos_equipamiento_3 = fields.Boolean(
        string="En Almacén de Terceros",
        related='oportunidades.datos_equipamiento_3', store=True,)
    datos_equipamiento_4 = fields.Boolean(
        string="En el lugar de Ejecución",
        related='oportunidades.datos_equipamiento_4', store=True,)
    datos_equipamiento_5 = fields.Boolean(
        string="No Procede", related='oportunidades.datos_equipamiento_5',
        store=True,)
    datos_materiales_1 = fields.Boolean(
        string="Con Reserva SAP", related='oportunidades.datos_materiales_1',
        store=True,)
    datos_materiales_2 = fields.Boolean(
        string="Pdte por Reservar", related='oportunidades.datos_materiales_2',
        store=True,)
    datos_materiales_3 = fields.Boolean(
        string="Por el Ejecutor", related='oportunidades.datos_materiales_3',
        store=True,)
    datos_materiales_4 = fields.Boolean(
        string="No Procede.", related='oportunidades.datos_materiales_4',
        store=True,)
    company_currency = fields.Many2one(string='Currency',
                                       related='company_id.currency_id',
                                       readonly=True,)
    valor_sap_cup = fields.Monetary('Presupuesto', store=True,
                                    currency_field='company_currency',
                                    related='oportunidades.valor_sap_cup')
    valor_sap_total = fields.Monetary('Presupuesto Total', store=True,
                                      currency_field='company_currency',
                                      related='oportunidades.valor_sap_total')
    stage_id = fields.Many2one('sicpro.app.solicitudes.estados',
                               string='Estados', store=True,
                               related='oportunidades.stage_id')
    type = fields.Selection(related='oportunidades.type', store=True,)
    estado_interno = fields.Selection(related='oportunidades.estado_interno',
                                      store=True,)
    tipo = fields.Selection(related='oportunidades.tipo', store=True,)
    pep = fields.Char(string='Sap', related='oportunidades.pep', store=True,)
    solicitud = fields.Many2one(
        comodel_name="sicpro.app.solicitudes.oportunidades", store=True,
        related='oportunidades.solicitud')
    hijos_ids = fields.One2many(
        comodel_name="sicpro.app.solicitudes.oportunidades",
        inverse_name="solicitud", string="Especialidad", related='oportunidades.hijos_ids')
    especialidad = fields.Many2one(
        comodel_name="sicpro.nomenclador.especialidad", string="Especialidad.",
        related='oportunidades.especialidad', store=True,)
    codigo_especialidad = fields.Integer(
        string="Código", store=True,
        related='oportunidades.codigo_especialidad')
    microlocalizacion = fields.Char(string='Micro Localización', store=True,
                                    related='oportunidades.microlocalizacion')
    enia = fields.Char(string='Estudio de la ENIA',
                       related='oportunidades.enia', store=True,)
    ipf = fields.Date(string='Aprobación del IPF',
                      related='oportunidades.ipf', store=True,)
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_1920 = fields.Image("Image", related='oportunidades.image_1920',
                              store=True,
                              max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024)
    image_512 = fields.Image("Image 512", related="image_1920",
                             max_width=512, max_height=512)
    image_256 = fields.Image("Image 256", related="image_1920",
                             max_width=256, max_height=256)
    image_128 = fields.Image("Image 128", related="image_1920",
                             max_width=128, max_height=128)
    motivo_rechazo = fields.Many2one('sicpro.app.solicitudes.rechazadas',
                                     store=True,
                                     string='Motivo de Rechazo',
                                     related='oportunidades.motivo_rechazo')
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación", store=True,
                                     related='oportunidades.motivo_cancelacion')
    user_id = fields.Many2one('res.users', string='Gestor de la Solicitud',
                              store=True,
                              related='oportunidades.user_id' )
    meeting_count = fields.Integer('# Meetings',
                                   related='oportunidades.meeting_count',)
    dias_aprobar = fields.Integer(string='Días en aprobar',
                                related='oportunidades.dias_aprobar',
                                store=True,)
    dias_asignar = fields.Integer(string='Dias en asignar',
                                related='oportunidades.dias_asignar',
                                store=True,)
    date_last_stage_update = fields.Datetime(
        string='Last Stage Update', store=True,
        related='oportunidades.date_last_stage_update')
    date_conversion = fields.Datetime(
        'Conversion Date', related='oportunidades.date_conversion', store=True,)
    partner_address_name = fields.Char(
        'Partner Contact Name',
        related='oportunidades.partner_address_name', store=True,)
    partner_address_email = fields.Char(
        'Partner Contact Email',
        related='oportunidades.partner_address_email', store=True,)
    partner_address_phone = fields.Char(
        'Partner Contact Phone',
        related='oportunidades.partner_address_phone', store=True,)
    user_email = fields.Char('User Email',
                             related='oportunidades.user_email', store=True,)
    user_login = fields.Char('User Login',
                             related='oportunidades.user_login', store=True,)
    temporal_1 = fields.Boolean(default=False,
                                related='oportunidades.temporal_1', store=True,)  # control del campo stage_id
    temporal_2 = fields.Boolean(default=False,
                                related='oportunidades.temporal_2', store=True,)  # control del campo especialista_ejecutor
