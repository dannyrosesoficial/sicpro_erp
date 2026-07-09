# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class TransferenciasGastosCJ74Wizard(models.TransientModel):
    _name = "sicpro.app.transferencias.gastos.cj74.wizard"
    _description = "Enviar gastos a revisión económica"

    def _gastos_cj74_modificar_meses(self):
        mes_ids = []
        gastos = self.env['sicpro.app.transferencias.gastos.importar'].search(
            ['&', ('active', '=', True), ('name', '=', 'pendiente')])
        if gastos:
            for item in gastos:
                mes_ids.append(item.mes.id)
            return mes_ids
        # else:
        #     raise ValidationError(_("¡No existen gastos para enviar a revisión económica!. "
        #                             "Si cree que es un error contacte al administrador"))

    def _get_mes_domain(self):
        return [('id', 'in', self._gastos_cj74_modificar_meses())]

    anio = fields.Char(string="Año", required=True, default=fields.Datetime.now().strftime("%Y"))
    mes_ids = fields.Many2many('sicpro.nomenclador.meses', 'cj74_meses_rel', 'gastos_id', 'mes_id', string='Meses',
                               default=_gastos_cj74_modificar_meses, domain=_get_mes_domain, required=True)

    # modifico el nomenclador de la orden de trabajo
    def enviar_cj74_gastos(self):
        meses_ids = 0
        anio = self.anio

        # verífico cuantos meses hay el el campo, solo debe existir uno
        for value in self.mes_ids:
            meses_ids += 1
        if meses_ids == 1:
            # compruebo que no existan cuentas con errores
            error = self.env['sicpro.app.transferencias.gastos.importar'].search(
                ['&', ('mes', '=', self.mes_ids.id), ('name', '=', 'error')])
            if not error:
                # compruebo que en los gastos de economía tengan estados diferentes a la revisión económica
                gastos = self.env['sicpro.app.transferencias.gastos'].search(
                    ['&', '&', ('mes', '=', self.mes_ids.id), ('anio', '=', anio), ('active', '=', True),
                     ('estado', '!=', 'revision_economica')])
                if not gastos:
                    # elimino todas las cuentas del mes, archivadas o no
                    self.env['sicpro.app.transferencias.gastos'].search(
                        ['&', '&', ('mes', '=', self.mes_ids.id), ('anio', '=', anio),
                         ('active', '=', True)]).sudo().unlink()
                    self.env['sicpro.app.transferencias.gastos'].search(
                        ['&', '&', ('mes', '=', self.mes_ids.id), ('anio', '=', anio),
                         ('active', '=', False)]).sudo().unlink()
                    # transfiero los gastos a revisar por economías
                    cjt4 = self.env['sicpro.app.transferencias.gastos.importar'].search(
                        ['&', ('mes', '=', self.mes_ids.id), ('active', '=', True)])

                    for item in cjt4:
                        data = {'per': item.per, 'anio': item.anio, 'mes': item.mes.id, 'usuario': item.usuario,
                                'fecha_contable': item.fecha_contable, 'fecha_doc': item.fecha_doc, 'monO': item.monO,
                                # 'fecha_contable_compute': item.fecha_contable_compute,
                                # 'fecha_doc_compute': item.fecha_doc_compute, 'objeto': item.objeto,
                                'denominacion_objeto': item.denominacion_objeto, 'valor_var': item.valor_var,
                                # 'valor_var_compute': item.valor_var_compute,
                                'cl_coste': item.cl_coste, 'denom_cl_coste': item.denom_cl_coste, 'cta_cp': item.cta_cp,
                                'denomctacp': item.denomctacp, 'n_doc': item.n_doc,  'name': item.orden.id,
                                'n_doc_ref': item.n_doc_ref, 'denominacion': item.denominacion,
                                'texto_cabecera_documento': item.texto_cabecera_documento, 'material': item.material,
                                'texto_breve_material': item.texto_breve_material,
                                'ud_cantidad_contab': item.ud_cantidad_contab,
                                'cantidad_total_reg': item.cantidad_total_reg,
                                }
                        # creo el registro de gastos
                        self.env['sicpro.app.transferencias.gastos'].create(data)
                        # elimino el registro transferido de la cj74
                        item.unlink()

                    group_eco = self.env.ref('sicpro_app_transferencias_gastos.grupo_transferencias_economia').users
                    id_gastos = self.env['sicpro.app.transferencias.gastos'].search([('active', '=', True)], limit=1)
                    # Selecciono el registro de seguidores
                    for participante in group_eco:
                        # envío el correo electrónico
                        email_values = {'email_to': participante.email_formatted,
                                        'email_from': '"SICPRO ERP" <sicproerp@etecsa.cu>',
                                        }
                        template = self.env.ref('sicpro_app_transferencias_gastos.gastos_revision_economica')
                        template.send_mail(id_gastos.id, force_send=True, email_values=email_values, )

                    action = \
                        self.sudo().env.ref('sicpro_app_transferencias_gastos.transferencias_gastos_action').read()[0]
                    return action
                else:
                    raise ValidationError(
                        _("¡No se pueden transferir los gastos del mes solicitado debido a que fueron liberados a "
                          "los procesos claves de la DVPE!. Si cree que es un error contacte al administrador"))

            else:
                raise ValidationError(
                    _("¡El MES solicitado tiene cuentas de gastos con errores, soluciónalo antes de continuar!. "
                      "Si cree que es un error contacte al administrador"))
        else:
            raise ValidationError(_("¡Solo se puede seleccionar un mes a la vez para enviarlo a revisión económica!. "
                                    "Si cree que es un error contacte al administrador"))
