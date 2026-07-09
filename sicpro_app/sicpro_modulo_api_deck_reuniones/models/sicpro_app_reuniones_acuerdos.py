# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ReunionesAcuerdos(models.Model):
    _inherit = 'sicpro.app.reuniones.acuerdos'

    board_id = fields.Integer(string='Board', required=False)
    estados_id = fields.Integer(string='Estado', required=False)
    tarjeta_id = fields.Integer(string='Tarjeta', required=False)
    etiqueta_id = fields.Integer(string='Etiqueta', required=False)
    responsable_ids = fields.Integer(string='Responsable', required=False)
    participantes_ids = fields.Integer(string='Participantes', required=False)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ReunionesAcuerdos, self).create(vals_list)
        for item in res:
            # creo la lista de seguidores
            responsable = item['responsable_ids']
            # agrego los seguidores al modelo
            item.message_subscribe(partner_ids=responsable.partner_id.ids)
            # envió la notificación a los seguidores
            item.message_post(body='Acuerdo asignado', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

            # envío el correo electrónico
            for val in responsable:
                email_values = {'email_to': val.email_formatted}
                template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo')
                template.send_mail(item.id, force_send=True, email_values=email_values,)

        return res

    def write(self, values):
        # envío él, id y el estado de acción del evento
        # para ejecutar la sincronización
        estado = True
        for item in self:
            evento = item.id
            self.caldav_crear_actualizar_eliminar_calendario(evento, estado)

        return True

    def unlink(self):
        # envío él, id y el estado de acción del evento
        estado = False
        for item in self:
            evento = item.id
            self.caldav_crear_actualizar_eliminar_calendario(evento, estado)
        result = super().unlink()
        return result
