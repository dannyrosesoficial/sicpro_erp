# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


class TransferenciasGastosCJ74Wizard(models.TransientModel):
    _name = "sicpro.app.transferencias.gastos.cj74.wizard"
    _description = "Enviar gastos a revisión económica"

    def _gastos_cj74_modificar_meses(self):
        gastos = self.env['sicpro.app.transferencias.gastos.importar'].search(
            [('active', '=', True), ('name', '=', 'pendiente')])
        if gastos:
            return gastos.mapped('mes').ids
        return []

    def _get_mes_domain(self):
        return [('id', 'in', self._gastos_cj74_modificar_meses())]

    anio = fields.Char(string="Año", required=True,
                       default=fields.Datetime.now().strftime("%Y"))
    mes_ids = fields.Many2many('sicpro.nomenclador.meses', 'cj74_meses_rel',
                               'gastos_id', 'mes_id', string='Meses',
                               default=_gastos_cj74_modificar_meses,
                               domain=_get_mes_domain, required=True)

    # modifico el nomenclador de la orden de trabajo
    def enviar_cj74_gastos(self):
        self.ensure_one()
        anio = self.anio

        # Verifico cuántos meses hay en el campo, solo debe existir uno
        if len(self.mes_ids) == 1:
            mes_seleccionado_id = self.mes_ids.id

            # Odoo 19: Limpieza previa de registros basura creados por el Excel (filas de totales vacías)
            # Si el registro no tiene un 'objeto' (es basura del Excel), lo eliminamos directamente para que no estorbe
            self.env['sicpro.app.transferencias.gastos.importar'].search([
                ('objeto', '=', False)]).sudo().unlink()

            # Ahora comprobamos si quedan errores REALES (registros con objeto pero mal mapeados)
            error = self.env['sicpro.app.transferencias.gastos.importar'].search([
                ('mes', '=', mes_seleccionado_id),
                ('name', '=', 'error')
            ])

            if not error:
                # Compruebo que en los gastos de economía tengan estados diferentes a la revisión económica
                gastos = self.env['sicpro.app.transferencias.gastos'].search([
                    ('mes', '=', mes_seleccionado_id),
                    ('anio', '=', anio),
                    ('active', '=', True),
                    ('estado', '!=', 'revision_economica')
                ])

                # Si no hay gastos o está vacío, avanza perfectamente
                if not gastos:
                    # Elimino todas las cuentas del mes, archivadas o no, en un solo paso
                    self.env['sicpro.app.transferencias.gastos'].search([
                        ('mes', '=', mes_seleccionado_id),
                        ('anio', '=', anio),
                        ('active', 'in', [True, False])
                    ]).sudo().unlink()

                    # Transfiero los gastos a revisar por economías
                    cjt4 = self.env['sicpro.app.transferencias.gastos.importar'].search([
                        ('mes', '=', mes_seleccionado_id),
                        ('active', '=', True)
                    ])

                    # Preparación de inserción por lotes para alta eficiencia en Odoo 19
                    vals_to_create = []
                    for item in cjt4:
                        vals_to_create.append({
                            'per': item.per,
                            'anio': item.anio,
                            'mes': item.mes.id,
                            'usuario': item.usuario,
                            'fecha_contable': item.fecha_contable,
                            'fecha_doc': item.fecha_doc,
                            'monO': item.monO,
                            'denominacion_objeto': item.denominacion_objeto,
                            'valor_var': item.valor_var,
                            'cl_coste': item.cl_coste,
                            'denom_cl_coste': item.denom_cl_coste,
                            'cta_cp': item.cta_cp,
                            'denomctacp': item.denomctacp,
                            'n_doc': item.n_doc,
                            'name': item.orden.id,
                            'n_doc_ref': item.n_doc_ref,
                            'denominacion': item.denominacion,
                            'texto_cabecera_documento': item.texto_cabecera_documento,
                            'material': item.material,
                            'texto_breve_material': item.texto_breve_material,
                            'ud_cantidad_contab': item.ud_cantidad_contab,
                            'cantidad_total_reg': item.cantidad_total_reg,
                            'company_id': self.env.company.id,
                        })

                    # Odoo 19 Batch Create: Crea todo de una sola vez en lugar de meter el create en el bucle
                    if vals_to_create:
                        self.env['sicpro.app.transferencias.gastos'].create(vals_to_create)

                    # Borrado masivo de la tabla temporal de importaciones
                    cjt4.unlink()

                    grup_eco = self.env.ref(
                        'sicpro_app_transferencias_gastos.grupo_transferencias_economia',
                        raise_if_not_found=False
                    )
                    group_eco = self.env['res.users']
                    if grup_eco:
                        group_eco = grup_eco.user_ids

                    id_gastos = self.env['sicpro.app.transferencias.gastos'].search(
                        [('active', '=', True)], limit=1
                    )

                    template = self.env.ref(
                        'sicpro_app_transferencias_gastos.gastos_revision_economica',
                        raise_if_not_found=False
                    )

                    if template and id_gastos:
                        for participante in group_eco:
                            if participante.email_formatted:
                                email_values = {
                                    'email_to': participante.email_formatted,
                                    'email_from': '"SICPRO ERP" <sicproerp@etecsa.cu>',
                                }
                                template.send_mail(
                                    id_gastos.id,
                                    force_send=False,
                                    email_values=email_values,
                                )

                    action = self.sudo().env.ref(
                        'sicpro_app_transferencias_gastos.transferencias_gastos_action'
                    ).read()[0]
                    return action
                else:
                    raise ValidationError(
                        "¡No se pueden transferir los gastos del mes solicitado debido a que fueron liberados a "
                        "los procesos claves de la DVPE!.\n\n" + MSG_SOPORTE_SICPRO)
            else:
                raise ValidationError(
                    "¡El MES solicitado tiene cuentas de gastos con errores, soluciónalo antes de continuar!.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            raise ValidationError(
                "¡Solo se puede seleccionar un mes a la vez para enviarlo a revisión económica!.\n\n" + MSG_SOPORTE_SICPRO)