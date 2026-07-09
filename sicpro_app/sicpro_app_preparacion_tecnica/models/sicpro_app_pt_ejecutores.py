# -*- coding: utf-8 -*-

from odoo import fields, models


class PreparacionTecnicaEjecutor(models.Model):
    _name = "sicpro.app.preparacion.tecnica.ejecutor"
    _description = "Ejecutores de la Preparación Técnica"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "sequence, name, id"

    name = fields.Many2one(comodel_name="sicpro.app.trabajadores.general",
                           string="Especialista",
                           index=True, required=True, tracking=True,
                           domain="[('company_id', '=', company_id)]")
    cargo_especialista = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.trabajos", string='Cargo',
        related="name.job_id", store=True, required=False)
    departamento = fields.Many2one(
        'sicpro.app.trabajadores.departmentos', string="Departamento",
        store=True, required=False, related='name.department_id',
        readonly=True)
    responsable = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.general",
        string="Responsable", related="name.parent_id",
        index=True, required=False, tracking=True, )
    cargo_responsable = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.trabajos",
        string="Cargo", related="responsable.job_id",
        index=True, required=False, tracking=True, )
    active = fields.Boolean(default=True, )
    sequence = fields.Integer(default=10, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    doc_count = fields.Integer(compute='_compute_attached_docs_count',
                               string="Cantidad de documentos adjuntos")
    task_count = fields.Integer(compute='_compute_task_count',
                                string="Cantidad de preparaciones")
    currency_id = fields.Many2one('res.currency',
                                  related="company_id.currency_id",
                                  string="Currency", readonly=True)
    color = fields.Integer(string='Color Index')
    is_favorite = fields.Boolean(string='Especialista favorito', )
    resource_calendar_id = fields.Many2one(
        'resource.calendar', string='Working Time',
        default=lambda self: self.env.company.resource_calendar_id.id,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )
    Preparaciones = fields.One2many(
        'sicpro.app.preparacion.tecnica.preparaciones',
        'especialista_ejecutor_id', string="Task Activities")
    Preparaciones_ids = fields.One2many(
        'sicpro.app.preparacion.tecnica.preparaciones',
        'especialista_ejecutor_id', string='Tasks',
        domain=['|', ('stage_id.fold', '=', False),
                ('stage_id', '=', False)])
    type_ids = fields.Many2many('sicpro.app.preparacion.tecnica.estados',
                                'sicpro_app_preparacion_ejecutor_rel', 'especialista_ejecutor_id',
                                'type_id', string='Tasks Stages')

    subtask_especialista_ejecutor_id = fields.Many2one(
        'sicpro.app.preparacion.tecnica.ejecutor', string='Sub-task Project',
        ondelete="restrict", )


    # Sube los adjuntos del especialista al sistema
    def attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['domain'] = str([
            '|',
            '&',
            ('res_model', '=', 'sicpro.app.preparacion.tecnica.ejecutor'),
            ('res_id', 'in', self.ids),
            '&',
            ('res_model', '=', 'sicpro.app.preparacion.tecnica.preparaciones'),
            ('res_id', 'in', self.Preparaciones_ids.ids)
        ])
        action[
            'context'] = "{'default_res_model': '%s','default_res_id': %d}" % (
            self._name, self.id)
        return action

    # Cuenta los adjuntos del especialista subidos al sistema
    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for doc_especialistas in self:
            doc_especialistas.doc_count = Attachment.search_count([
                '|', '&',
                ('res_model', '=', 'sicpro.app.preparacion.tecnica.ejecutor'),
                ('res_id', '=', doc_especialistas.id),
                '&',
                ('res_model', '=',
                 'sicpro.app.preparacion.tecnica.preparaciones'),
                ('res_id', 'in', doc_especialistas.Preparaciones_ids.ids)
            ])

    # Cuenta las preparaciones del especialista
    def _compute_task_count(self):
        preparaciones = self.env[
            'sicpro.app.preparacion.tecnica.preparaciones'].read_group(
            [('especialista_ejecutor_id', 'in', self.ids), '|',
             ('stage_id.fold', '=', False), ('stage_id', '=', False)],
            ['especialista_ejecutor_id'], ['especialista_ejecutor_id'])
        result = dict(
            (data['especialista_ejecutor_id'][0], data['especialista_ejecutor_id_count']) for data in
            preparaciones)
        for project in self:
            project.task_count = result.get(project.id, 0)


'''    def message_subscribe(self, partner_ids=None, channel_ids=None,
                          subtype_ids=None):
        res = super(PreparacionTecnicaEjecutor, self).message_subscribe(
            partner_ids=partner_ids, channel_ids=channel_ids,
            subtype_ids=subtype_ids)
        project_subtypes = self.env['mail.message.subtype'].browse(
            subtype_ids) if subtype_ids else None
        task_subtypes = project_subtypes.mapped(
            'parent_id').ids if project_subtypes else None
        if not subtype_ids or task_subtypes:
            self.mapped('tasks').message_subscribe(
                partner_ids=partner_ids, channel_ids=channel_ids,
                subtype_ids=task_subtypes)
        return res'''

'''    def message_unsubscribe(self, partner_ids=None, channel_ids=None):
        """ Unsubscribe from all tasks when unsubscribing from a project """
        self.mapped('tasks').message_unsubscribe(partner_ids=partner_ids,
                                                 channel_ids=channel_ids)
        return super(PreparacionTecnicaEjecutor, self).message_unsubscribe(
            partner_ids=partner_ids, channel_ids=channel_ids)'''
