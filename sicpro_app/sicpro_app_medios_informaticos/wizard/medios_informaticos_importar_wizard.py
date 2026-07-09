# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import datetime

from odoo import fields, models


class MediosInformaticosImportarWizard(models.TransientModel):
    _name = "sicpro.app.medios.informaticos.importar.wizard"
    _description = "Actualizar Inventario de medios informáticos"

    def _get_tipos_equipos_domain(self):
        list_tipos_equipos = self._tipos_equipos_ids()
        if list_tipos_equipos is not None:
            return [('id', 'in', self._tipos_equipos_ids())]
        else:
            return []

    def _tipos_equipos_ids(self):
        tipos_equipos = []
        medios_importar = self.env[
            'sicpro.app.medios.informaticos.importar'].search(
            [('active', '=', True)])
        if medios_importar:
            for item in medios_importar:
                tipos_equipos.append(item.tipo_equipo.id)
            return tipos_equipos

    tipos_equipos = fields.Many2many(
        'sicpro.app.medios.informaticos.tipo.equipo',
        'tipos_importar_wizard_rel', 'tipos_id', 'wizard_id',
        string="Tipos de equipo", default=_tipos_equipos_ids,
        domain=_get_tipos_equipos_domain)

    def lista_a_texto(self, list):
        text_list = "', '".join(list)
        text_list = "['" + text_list + "']"
        return text_list

    def actualizar_datos(self):
        registros_creados = 0
        list_registros_creados = []
        registros_actualizados = 0
        list_registros_actualizados = []
        registros_archivados = 0
        list_registros_archivados = []
        date = datetime.today()
        tipos_ids = self.tipos_equipos

        try:

            medios_ids = self.env['sicpro.app.medios.informaticos'].search(
                [('active', '=', True)])
            for medio in medios_ids:
                medio_importar_ids = self.env[
                    'sicpro.app.medios.informaticos.importar'].search(
                    [('medio_informatico', '=', medio['name'])])
                if not medio_importar_ids:
                    medio.write({'active': False, 'archivado': True,
                                 'fecha_archivado': date})
                    registros_archivados += 1
                    list_registros_archivados.append(medio.name)

            for tipo in tipos_ids:
                medios_ids = self.env['sicpro.app.medios.informaticos'].search(
                    ['&', ('active', '=', True),
                     ('tipo_equipo', '=', tipo.id)])
                for medio in medios_ids:
                    medio_importar_ids = self.env[
                        'sicpro.app.medios.informaticos.importar'].search(
                        [('medio_informatico', '=', medio['name'])])
                    if medio_importar_ids:
                        for medio_importar in medio_importar_ids:
                            if medio_importar:
                                medio.write(
                                    {'equipo': medio_importar['equipo'],
                                     'tipo_equipo': medio_importar[
                                         'tipo_equipo'].id,
                                     'denominacion': medio_importar[
                                         'denominacion'],
                                     'local': medio_importar['local'].id,
                                     'emplazamiento': medio_importar[
                                         'emplazamiento'].id,
                                     'activo_fijo': medio_importar[
                                         'activo_fijo'],
                                     'no_pieza_fab': medio_importar[
                                         'no_pieza_fab'],
                                     'responsable': medio_importar[
                                         'responsable'],
                                     'trabajador_id': medio_importar.trabajador_id.id})
                                registros_actualizados += 1
                                list_registros_actualizados.append(
                                    medio_importar.medio_informatico)

                medios_importar_ids = self.env[
                    'sicpro.app.medios.informaticos.importar'].search(
                    ['&', ('active', '=', True),
                     ('tipo_equipo', '=', tipo.id)])
                for medio_importar in medios_importar_ids:
                    medio = self.env['sicpro.app.medios.informaticos'].search(
                        [('name', '=', medio_importar['medio_informatico'])])
                    if not medio:
                        self.env['sicpro.app.medios.informaticos'].create(
                            {'name': medio_importar.medio_informatico,
                             'equipo': medio_importar['equipo'],
                             'tipo_equipo': medio_importar['tipo_equipo'].id,
                             'denominacion': medio_importar['denominacion'],
                             'local': medio_importar['local'].id,
                             'emplazamiento': medio_importar[
                                 'emplazamiento'].id,
                             'activo_fijo': medio_importar['activo_fijo'],
                             'no_pieza_fab': medio_importar['no_pieza_fab'],
                             'responsable': medio_importar['responsable'],
                             'trabajador_id': medio_importar.trabajador_id.id})
                        registros_creados += 1
                        list_registros_creados.append(
                            medio_importar.medio_informatico)
                        medio_importar.sudo().unlink()

                    else:
                        medio_importar.sudo().unlink()

                text_list_registros_creados = self.lista_a_texto(
                    list_registros_creados)
                text_list_registros_actualizados = self.lista_a_texto(
                    list_registros_actualizados)
                text_list_registros_archivados = self.lista_a_texto(
                    list_registros_archivados)

                self.env[
                    'sicpro.app.medios.informaticos.historial'].sudo().create(
                    {'name': "Actualización inventario", 'fecha': date,
                     'registros_creados': registros_creados,
                     'list_registros_creados': text_list_registros_creados,
                     'registros_actualizados': registros_actualizados,
                     'list_registros_actualizados': text_list_registros_actualizados,
                     'registros_archivados': registros_archivados,
                     'list_registros_archivados': text_list_registros_archivados,
                     'estado': 'exito', 'descripcion_estado': 'Exitoso'})

        except Exception as error:
            text_list_registros_creados = self.lista_a_texto(
                list_registros_creados)
            text_list_registros_actualizados = self.lista_a_texto(
                list_registros_actualizados)
            text_list_registros_archivados = self.lista_a_texto(
                list_registros_archivados)

            self.env['sicpro.app.medios.informaticos.historial'].sudo().create(
                {'name': "Actualización inventario", 'fecha': date,
                 'registros_creados': registros_creados,
                 'list_registros_creados': text_list_registros_creados,
                 'registros_actualizados': registros_actualizados,
                 'list_registros_actualizados': text_list_registros_actualizados,
                 'registros_archivados': registros_archivados,
                 'list_registros_archivados': text_list_registros_archivados,
                 'estado': 'fallido', 'descripcion_estado': error.__str__()})

        action = self.env.ref(
            'sicpro_app_medios_informaticos.medios_informaticos_importar_action').sudo().read()[
            0]
        return action
