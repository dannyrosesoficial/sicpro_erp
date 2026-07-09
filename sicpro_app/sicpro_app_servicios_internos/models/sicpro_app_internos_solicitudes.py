# -*- coding: utf-8 -*-

from random import randint

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


def _default_color():
    return randint(1, 11)


class ServiciosInternosSolicitudes(models.Model):
    _name = 'sicpro.app.servicios.internos.solicitudes'
    _description = "Gestión de las Solicitudes de los Servicios internos"
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = "fecha_solicitud desc"

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    active = fields.Boolean(default=True, )
    id_solicitud = fields.Char(string='Solicitud ID', tracking=True, copy=False, readonly=True, )
    name = fields.Selection(string='Tipo', required=True, selection=[('anexo1', 'Anexo 1'), ('anexo2', 'Anexo 2'),
                                                                     ('Compromiso_nauta', 'Compromiso Nauta'),
                                                                     ('Planilla_unica', 'Planilla Única'), ], )
    solicitante_trabajador = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Solicitante',
                                             required=False, tracking=True)
    solicitante_company_id = fields.Many2one('res.company', string='Proceso Solicitante', tracking=True,
                                             related='solicitante_trabajador.company_id', store=True)
    solicitante_ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo Solicitante',
                                   related='solicitante_trabajador.ocupacion_id', store=True, tracking=True)
    solicitante_correo = fields.Char('Correo solicitante', store=True, tracking=True,
                                     related='solicitante_trabajador.correo_trabajo')
    solicitante_area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento Solicitante', tracking=True,
                                          related='solicitante_trabajador.area_id', store=True)
    beneficiario_trabajador = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Beneficiario',
                                             required=False, tracking=True)
    beneficiario_company_id = fields.Many2one('res.company', string='Proceso Beneficiario', tracking=True,
                                              related='beneficiario_trabajador.company_id', store=True,)
    beneficiario_ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo Beneficiario'
                                                ,tracking=True, related='beneficiario_trabajador.ocupacion_id', store=True)
    beneficiario_correo = fields.Char('Correo Beneficiario',
                                         related='beneficiario_trabajador.correo_trabajo', store=True, tracking=True)
    beneficiario_area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento Beneficiario', tracking=True,
                                           related='beneficiario_trabajador.area_id', store=True)
    beneficiario_sap = fields.Char('# SAP', tracking=True,
                                           related='beneficiario_trabajador.plaza_id', store=True)
    beneficiario_CI = fields.Char('CI', tracking=True,
                                  related='beneficiario_trabajador.identification_id', store=True)
    ip = fields.Char(string='IP', required=False, tracking=True)
    almacen = fields.Char(string='Almacén SAP', required=False, tracking=True)
    fecha_solicitud = fields.Date(string='Fecha de Solicitud', required=True, tracking=True)
    telefono = fields.Char(string='Teléfono', required=False)
    observaciones = fields.Many2one('sicpro.app.servicios.internos.solicitudes.observaciones', 'Solicitud de:',
                                    tracking=True, required=False)
    aprueba_trabajador = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Aprobado por:',
                                             required=False, tracking=True)
    aprueba_company_id = fields.Many2one('res.company', string='Proceso Aprobado', tracking=True,
                                         related='aprueba_trabajador.company_id', store=True)
    aprueba_ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo Aprobado',
                                           tracking=True, related='aprueba_trabajador.ocupacion_id', store=True)
    aprueba_area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento Aprobado', tracking=True,
                                      related='aprueba_trabajador.area_id', store=True)
    aprueba_fecha = fields.Date(string='Fecha de Aprobación', required=False, tracking=True)
    servicio_mensaje = fields.Boolean(string='Plan mensaje', required=False, tracking=True)
    servicio_mensaje_voz = fields.Boolean(string='Plan mensaje/voz', required=False, tracking=True)
    servicio_voz = fields.Boolean(string='Servicio de voz', required=False, tracking=True)
    servicio_plan_tope = fields.Char(string='Plan Tope', required=False, tracking=True)
    servicio_ldi = fields.Boolean(string='LDI', required=False, tracking=True)
    servicio_roaming = fields.Boolean(string='Roaming', required=False, tracking=True)
    servicio_gprs = fields.Boolean(string='Servicios GPRS', required=False, tracking=True)
    servicio_intranet = fields.Boolean(string='Intranet UO', required=False, tracking=True)
    servicio_wap = fields.Boolean(string='WAP', required=False, tracking=True)
    servicio_mms = fields.Boolean(string='MMS', required=False, tracking=True)
    cambio_servicio = fields.Boolean(string='Cambio del servicio otorgado', required=False, tracking=True)
    gama = fields.Selection(string='Gama de Equipo a entregar', required=False, tracking=True,
                            selection=[('alta', 'Alta'), ('media', 'Media'),('baja', 'Baja'), ],)
    cambio_equipo = fields.Boolean(string='Cambio de Equipo', required=False, tracking=True)
    fecha_roaming = fields.Boolean(string='Fecha Roaming', required=False, tracking=True)
    fecha_roaming_inicio = fields.Date(string='Fecha de Roaming Inicio', required=False, tracking=True)
    fecha_roaming_fin = fields.Date(string='Fecha de Roaming Fin', required=False, tracking=True)
    directivo_trabajador = fields.Char(string='Directivo aprueba', required=False, tracking=True)
    directivo_cargo = fields.Char(string='Directivo cargo', required=False, tracking=True)
    directivo_uo = fields.Char(string='Directivo UO', required=False, tracking=True)
    directivo_cantidad_minutos = fields.Integer(string='Cantidad de Minutos', required=False, tracking=True)
    directivo_fecha = fields.Date(string='Fecha Directivo', required=False, tracking=True)
    estado = fields.Selection(string='Estado', tracking=True, required=True, default='borrador',
                              selection=[('borrador', 'Borrador'), ('revision', 'Revisión'),
                                         ('validacion', 'Validación'), ('aprobado', 'Aprobado'),
                                         ('rechazado_revision', 'Revisión Rechazada'),
                                         ('rechazado_validacion', 'Validación Rechazada'),('cancelado', 'Cancelado'), ],)
    observaciones_rechazo_revision = fields.Text(string="Observaciones Rechazo Revisión", required=False, tracking=True)
    observaciones_rechazo_revision_bool = fields.Boolean(string='rechazo_revision_bool', required=False, default=False,
                                                         tracking=True)
    observaciones_rechazo_validacion = fields.Text(string="Observaciones Rechazo Validación", required=False,
                                                   tracking=True)
    observaciones_rechazo_validacion_bool = fields.Boolean(string='rechazo_validar_bool', required=False, default=False,
                                                           tracking=True)
    observaciones_cancelacion = fields.Text(string="Observaciones Cancelación", required=False,
                                                   tracking=True)
    observaciones_cancelacion_bool = fields.Boolean(string='cancelacion_bool', required=False, default=False,
                                                           tracking=True)
    compromiso_trabajador = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Solicitante compromiso',
                                             required=False, tracking=False)
    compromiso_company_id = fields.Many2one('res.company', string='Proceso Compromiso', tracking=True,
                                             related='compromiso_trabajador.company_id', store=True)
    compromiso_ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo Compromiso',
                                               related='compromiso_trabajador.ocupacion_id', store=True, tracking=True)
    compromiso_area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento Compromiso', tracking=True,
                                          related='compromiso_trabajador.area_id', store=True)
    compromiso_html = fields.Html(
        string='Compromiso_html', required=False, 
        default="<body> <p class='western' style='line-height: 100%; margin-bottom: 0cm' align='center'>"
                "      <font color='#c9211e'><font face='Arial, sans-serif'><font style='font-size: 12pt'"
                "            size='3'><b>COMPROMISOS"
                "              PARA EL USO DEL SERVICIO NAUTA </b></font></font></font>"
                "    </p>"
                "    <p class='western' style='line-height: 100%; margin-bottom: 0cm' align='center'>"
                "      <font color='#c9211e'><font face='Arial, sans-serif'><font style='font-size: 12pt'"
                "            size='3'><b>DE"
                "              USUARIOS INTERNOS DE ETECSA.</b></font></font></font></p>"
                "    <p class='western' style='line-height: 100%; margin-bottom: 0cm' align='justify'>"
                "    </p>"
                "    <p class='western' style='line-height: 100%; margin-bottom: 0cm' align='justify'><font"
                "        face='Arial, sans-serif'><font style='font-size: 12pt' size='3'>E</font></font><font"
                "        face='Arial, sans-serif'><font style='font-size: 12pt' size='3'>n"
                "          correspondencia con lo regulado sobre el acceso a Redes de Alcance"
                "          Global, me comprometo a cumplir con todas las medidas que se"
                "          establecen en el Manual de Seguridad Informática de la Empresa de"
                "          Telecomunicaciones de Cuba S. A., con las Indicaciones y Resoluciones"
                "          que se emitan relacionadas con la Seguridad Informática del servicio"
                "          de navegación en salas, así como en particular con las siguientes:</font></font></p>"
                "    <ul>"
                "      <li>"
                "        <p style='line-height: 100%; margin-top: 0.49cm; margin-bottom: 0cm' align='justify'>"
                "          <font face='Times New Roman, serif'><font style='font-size: 12pt' size='3'><font"
                "                face='Arial, sans-serif'>El servicio ha sido otorgado debido a"
                "                mis funciones actuales y es personal e intransferible. Los"
                "                usuarios asumen en primera instancia la responsabilidad de las"
                "                consecuencias que se deriven de la utilización impropia de las"
                "                mismas.</font></font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Hacer uso de la facilidad"
                "              otorgada vía INTERNET únicamente en interés de funciones de"
                "              trabajo relacionadas con esta plataforma y el servicio que se"
                "              ofrece, en ningún caso con fines lucrativos o ilícitos.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Responder por el uso indebido del"
                "              servicio y darle un uso adecuado, acorde a los principios morales"
                "              de nuestra sociedad, controlando adecuadamente la clave de acceso"
                "              y su confidencialidad.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>No enviar a través de INTERNET"
                "              documentos clasificados o sensibles.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Al recibir información por vía"
                "              del correo electrónico, abrirlos sin macros y revisarlos con los"
                "              programas detectores de virus establecidos.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Informar de inmediato la"
                "              recepción de mensajes no deseados o que se contravengan con los"
                "              principios ético-morales de nuestra sociedad, así como"
                "              manifestaciones subversivas o contrarrevolucionarias.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Acatar las orientaciones que se"
                "              emitan en la Empresa en aras del buen funcionamiento del servicio.</font></font></p>"
                "      </li>"
                "    </ul>"
                "    <p style='line-height: 100%; margin-left: 1.27cm; margin-bottom: 0cm'>"
                "      <br>"
                "    </p>"
                "    <p class='western' style='line-height: 100%; margin-bottom: 0cm'>&nbsp;<font"
                "        face='Arial, sans-serif'><font style='font-size: 12pt' size='3'>Está"
                "          prohibido para todos los usuarios, independientemente del tipo de"
                "          usuario que sea:</font></font></p>"
                "    <ul>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Utilizar cuentas ajenas.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Dejar sesiones abiertas.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Violar las normas de seguridad"
                "              que se establezcan.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Enviar la clave de acceso por"
                "              correo electrónico.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Usar como clave de acceso los"
                "              nombres personales, de familiares o amigos.</font></font></p>"
                "      </li>"
                "      <li>"
                "        <p style='line-height: 100%; margin-bottom: 0cm'><font face='Arial, sans-serif'><font"
                "              style='font-size: 12pt' size='3'>Realizar sondeos de seguridad"
                "              tanto en la red, así como a otras redes externas.</font></font></p>"
                "      </li>"
                "    </ul>"
                "    <p class='western' style='line-height: 100%; margin-bottom: 0cm'><br>"
                "    </p>"
                "    <p></p>"
                "  </body>")

    color = fields.Integer(string='Color', default=lambda self: _default_color())
    doc_count = fields.Integer(compute='_compute_solicitudes_docs_count', string="Documentos")
    tipo_movimiento = fields.Selection(string='Tipo de movimiento', required=False, tracking=True,
                            selection=[('alta', 'Alta'), ('modificacion', 'Modificación'), ('baja', 'Baja'), ], )
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    app_OperCAT = fields.Boolean(string='Oper CAT', required=False)
    app_WebTransfer = fields.Boolean(string='WebTransfer', required=False)
    app_Boulevard_MiTransfer = fields.Boolean(string='Boulevard MiTransfer', required=False)
    app_RUNA = fields.Boolean(string='RUNA', required=False)
    app_KBS = fields.Boolean(string='KBS', required=False)
    app_SIGEN = fields.Boolean(string='SIGEN', required=False)
    app_reclamaciones_SIGEN = fields.Boolean(string='Módulo de reclamaciones de SIGEN', required=False)
    app_Avila_DocPro = fields.Boolean(string='Avila DocPro', required=False)
    app_Nauta_interna = fields.Boolean(string='Nauta interna', required=False)
    app_ReportesSINBADPLUS = fields.Boolean(string='Reportes SINBADPLUS', required=False)
    app_SINBADPLUS_GOS = fields.Boolean(string='SINBADPLUS/GOS', required=False)
    app_COBROS = fields.Boolean(string='COBROS', required=False)
    app_eCRM = fields.Boolean(string='eCRM', required=False)
    app_Capa_servicios = fields.Boolean(string='Capa de servicios', required=False)
    app_SIGC = fields.Boolean(string='SIGC', required=False)
    app_SADTEL = fields.Boolean(string='SADTEL', required=False)
    app_GESNAUTA = fields.Boolean(string='GESNAUTA', required=False)
    app_GESCOM = fields.Boolean(string='GESCOM', required=False)
    horas_nauta = fields.Selection(string='Horas Nauta', tracking=True, required=False,
                              selection=[('50', '50H'), ('80', '80H'), ], )

    # verífico que no se repita el trabajador si hay una solicitud activa
    @api.constrains('name', 'beneficiario_trabajador', 'estado')
    def _check_trabajador_solicitud_unico(self):
        uniq = self.env['sicpro.app.servicios.internos.solicitudes'].search(
            ['&', '&', '&', ("active", "=", True), ("name", "=", self.name),
             ('estado','not in', ['aprobado', 'cancelado']),
             ("beneficiario_trabajador", "=", self.beneficiario_trabajador.id), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El trabajador seleccionado, ya tiene una solicitud en trámite!. "
                                    "Si cree que es un error contacte al administrador"))

    # acción para generar la solicitud
    def action_generar_solicitud(self, ):
        # género el documento de certificación
        if self.name == 'anexo1':
            return {'type': 'ir.actions.report', 'model': 'sicpro.app.servicios.internos.solicitudes',
                    'report_type': 'qweb-pdf',
                    'report_name': 'sicpro_app_servicios_internos.informe_servicios_internos_anexo1', }
        elif self.name == 'anexo2':
            return {'type': 'ir.actions.report', 'model': 'sicpro.app.servicios.internos.solicitudes',
                    'report_type': 'qweb-pdf',
                    'report_name': 'sicpro_app_servicios_internos.informe_servicios_internos_anexo2', }
        elif self.name == 'Compromiso_nauta':
            return {'type': 'ir.actions.report', 'model': 'sicpro.app.servicios.internos.solicitudes',
                    'report_type': 'qweb-pdf',
                    'report_name': 'sicpro_app_servicios_internos.informe_servicios_internos_compromiso_nauta', }
        else:
            return {'type': 'ir.actions.report', 'model': 'sicpro.app.servicios.internos.solicitudes',
                         'report_type': 'qweb-pdf',
                         'report_name': 'sicpro_app_servicios_internos.informe_servicios_internos_planilla_unica', }


    # acción para liberar la solicitud y generar el consecutivo de la solicitud
    def action_liberar(self, ):
        if self.doc_count != 0:
            # Crear la secuencia de incremento para el consecutivo de la solicitud
            self.id_solicitud = self.env['ir.sequence'].next_by_code('solicitudes_id_consecutivo_incrementar')
            self.estado = 'revision'

            # busco usuarios del rol revisión de la solicitud
            rol_revision = self.env.ref('sicpro_app_servicios_internos.grupo_app_internos_solicitudes_revision').users
            # agrego los seguidores al modelo
            for item in rol_revision:
                self.message_subscribe(partner_ids=item.partner_id.ids)
                # envío la notificación a los seguidores
                self.message_post(body='Solicitud Liberada', subtype_xmlid='mail.mt_comment',
                                  author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref('sicpro_app_servicios_internos.solicitud_servicios_internos')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # redirecciono la salida
            action = self.sudo().env.ref('sicpro_app_servicios_internos.menu_servicios_internos_dashboard_action').read()[0]
            return action
        else:
            raise UserError(_('Debe proporcionar una documentación válida, verifíquelo '))

    # acción para aprobar la revision de la solicitud
    def action_revisado(self, ):
        self.estado = 'validacion'

        # busco usuarios del rol revisión de la solicitud
        rol_revision = self.env.ref('sicpro_app_servicios_internos.grupo_app_internos_solicitudes_validar').users
        # agrego los seguidores al modelo
        for item in rol_revision:
            self.message_subscribe(partner_ids=item.partner_id.ids)
            # envío la notificación a los seguidores
            self.message_post(body='Solicitud Revisada', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_servicios_internos.solicitud_servicios_internos')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_servicios_internos.menu_servicios_internos_dashboard_action').read()[0]
        return action

    # acción para validar la revision de la solicitud
    def action_validar(self, ):
        self.estado = 'aprobado'

        # envío la notificación a los seguidores
        self.message_post(body='Solicitud Aprobada', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_servicios_internos.solicitud_servicios_internos')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_servicios_internos.menu_servicios_internos_dashboard_action').read()[0]
        return action

    # acción para reiniciar la solicitud
    def action_reiniciar_solicitud(self, ):
        self.estado = 'borrador'
        self.observaciones_rechazo_validacion_bool = False
        self.observaciones_rechazo_revision_bool = False

    # Cuenta los adjuntos de la documentacion de la solicitud
    def _compute_solicitudes_docs_count(self):
        attachment_obj = self.env['ir.attachment']
        for documentos in self:
            documentos.doc_count = attachment_obj.search_count(
                ['&', ('res_model', '=', 'sicpro.app.servicios.internos.solicitudes'), ('res_id', '=', documentos.id)])

    # acción del botón documentos: no hace ninguna función
    def action_empaty_doc_solicitudes(self, ):
        action = None


# clase para rechazar la revisión
class SolicitudesRechazadoRevision(models.TransientModel):
    _name = 'internos.solicitudes.rechazado.revision'
    _description = 'Solicitudes de los Servicios internos Rechazados en la revisión'

    lost_reason_id = fields.Text(string='Motivo', required=True)

    def action_motivo_rechazo_revision(self):
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.servicios.internos.solicitudes'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Solicitud rechazada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # cambio el estado interno de la solicitud
        for item in post.sudo():
            item.estado = 'rechazado_revision'
            item.observaciones_rechazo_revision = self.lost_reason_id
            item.observaciones_rechazo_revision_bool = True

        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = post.env.context.copy()
            template = post.env.ref('sicpro_app_servicios_internos.solicitud_servicios_internos')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_servicios_internos.menu_servicios_internos_dashboard_action').read()[0]
        return action

# clase para rechazar la validación
class SolicitudesRechazadoValidacion(models.TransientModel):
    _name = 'internos.solicitudes.rechazado.validacion'
    _description = 'Solicitudes de los Servicios internos Rechazados en la validación'

    lost_reason_id = fields.Text(string='Motivo', required=True)

    def action_motivo_rechazo(self):
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.servicios.internos.solicitudes'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Solicitud rechazada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # cambio el estado interno de la solicitud
        for item in post.sudo():
            item.estado = 'rechazado_validacion'
            item.observaciones_rechazo_validacion = self.lost_reason_id
            item.observaciones_rechazo_validacion_bool = True

        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = post.env.context.copy()
            template = post.env.ref('sicpro_app_servicios_internos.solicitud_servicios_internos')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_servicios_internos.menu_servicios_internos_dashboard_action').read()[0]
        return action

# clase para cancelar la solicitud
class SolicitudesCancelado(models.TransientModel):
    _name = 'internos.solicitudes.cancelado'
    _description = 'Solicitudes de los Servicios internos Cancelados'

    lost_reason_id = fields.Text(string='Motivo', required=True)

    def action_motivo_cancelado(self):
        # llamo al método para crear la notificación
        post = self.env['sicpro.app.servicios.internos.solicitudes'].browse(self.env.context.get('active_ids'))
        post.message_post(body='Solicitud rechazada.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # cambio el estado interno de la solicitud
        for item in post.sudo():
            item.estado = 'cancelado'
            item.observaciones_cancelacion = self.lost_reason_id
            item.observaciones_cancelacion_bool = True

        # Selecciono el registro de seguidores
        for participante in post.message_partner_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.email_formatted, }
            local_context = post.env.context.copy()
            template = post.env.ref('sicpro_app_servicios_internos.solicitud_servicios_internos')
            template.with_context(local_context).send_mail(post.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.sudo().env.ref('sicpro_app_servicios_internos.menu_servicios_internos_dashboard_action').read()[0]
        return action