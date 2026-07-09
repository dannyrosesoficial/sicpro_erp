# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


class SicproWebFAQ(models.Model):
    _name = 'sicpro.modulo.web.preguntas'
    _description = 'Preguntas Frecuentes SICPRO'
    _order = "sequence, id"

    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    name = fields.Char(string='Pregunta', required=True)
    respuesta = fields.Text(string='Respuesta', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)

    # Integración con tu nomenclador
    icono_id = fields.Many2one('sicpro.nomenclador.iconos', string="Icono")
    icono_clase = fields.Char(related='icono_id.clase_icono')
    icono_tipo = fields.Selection(related='icono_id.tipo')
    preview = fields.Html(string='Vista previa', related='icono_id.preview',
                          readonly=True)

    def buscar_datos_faq(self):
        preguntas = self.sudo().search([('active', '=', True)])
        faq_list = []
        for item in preguntas:
            faq_list.append({'id': item.id, 'pregunta': item.name,
                             'respuesta': item.respuesta,
                             'icono': f"{item.icono_tipo} {item.icono_clase}" if item.icono_id else "fas fa-question-circle"})
        return faq_list
