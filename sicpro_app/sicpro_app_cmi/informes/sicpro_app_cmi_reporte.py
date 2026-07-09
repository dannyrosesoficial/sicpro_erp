from odoo import fields, models, api, _


class AppCMIReportes(models.TransientModel):
    _name = 'sicpro.app.cmi.reporte'
    _description = 'Reportes del CMI'

    def _compute_buscar_anios(self):
        anio_obj = self.env['sicpro.app.cmi.perspectivas.anios'].search(
            [('active', '=', True)])
        lst = []
        for anios in anio_obj:
            lst.append((anios.anio, anios.anio))
        return lst

    def _compute_buscar_mes(self):
        mes_obj = self.env['sicpro.app.cmi.perspectivas.periodos'].search(
            [('active', '=', True)])
        lst = []
        for mes in mes_obj:
            lst.append((mes.name, mes.name))
        return lst

    anio = fields.Selection(selection=_compute_buscar_anios, string="Año",
                            required=True, )
    periodo = fields.Selection(selection=_compute_buscar_mes, string="Periodo",
                           required=True, )
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              default=lambda self: self.env.uid)
    tipo = fields.Selection(
        [('completo', 'Perspectivas'), ('eje', 'Ejes Estratégicos'),
         ('acciones', 'Plan de Acciones')], default='completo', required=True,
        string="Tipo")

    # busca los ejes estratégicos
    def reporte_cmi_anios_ejes(self):
        anio_activo = self.anio
        ejes_est = []
        ejes_estrategicos = self.env['sicpro.app.cmi.perspectivas.eje.estrategico'].search(
            [('active', '=', True)])

        for ejes in ejes_estrategicos:
            ejes_est.append({
                'id': ejes.id,
                'name': ejes.name,
            })
        return ejes_est

    # busca las perspectivas
    def reporte_cmi_anios_perspectivas(self):
        anio_activo = self.anio
        perspectivas = []
        obj_perspectivas = self.env['sicpro.app.cmi.perspectivas'].search(
            [('active', '=', True)])

        for pers in obj_perspectivas:
            obj_anuales_ids = pers.env['sicpro.app.cmi.objetivos.anuales'].search(
                [('obj_estrategico_id.perspectivas_id', '=', pers.id),
                 ('anio', '=', anio_activo)])
            real = 0
            meta = 0
            porciento_avance_barra = 0
            for anu in obj_anuales_ids:
                for valores in anu.obj_indicadores_ids:
                    valores_indicadores_ids = self.env[
                        'sicpro.app.cmi.indicadores.valores'].search(
                        [('mes', '=', self.periodo),
                         ('indicador_id', '=', valores.id)])
                    for inds in valores_indicadores_ids:
                        real += inds.real
                        meta += inds.meta

                if real != 0 and meta != 0:
                    porciento_avance_barra = round((real / meta) * 100)
                else:
                    porciento_avance_barra = 0

            perspectivas.append({
                'id': pers.id,
                'name': pers.name,
                'porciento_avance_barra': porciento_avance_barra,
            })
        return perspectivas

    # busca los objetivos estrategicos
    def reporte_cmi_anios_estrategicos(self):
        anio_activo = self.anio
        estrategicos = []
        obj_estrategico_ids = self.env[
            'sicpro.app.cmi.objetivos.estrategicos'].search(
            [('active', '=', True)])

        for est in obj_estrategico_ids:
            obj_anuales_ids = est.env['sicpro.app.cmi.objetivos.anuales'].search(
                [('obj_estrategico_id', '=', est.id),
                 ('anio', '=', anio_activo)])
            real = 0
            meta = 0
            porciento_avance_barra = 0
            for anu in obj_anuales_ids:
                for valores in anu.obj_indicadores_ids:
                    valores_indicadores_ids = self.env[
                        'sicpro.app.cmi.indicadores.valores'].search(
                        [('mes', '=', self.periodo),
                         ('indicador_id', '=', valores.id)])
                    for inds in valores_indicadores_ids:
                        real += inds.real
                        meta += inds.meta

                if real != 0 and meta != 0:
                    porciento_avance_barra = round((real / meta) * 100)
                else:
                    porciento_avance_barra = 0

            estrategicos.append({
                'id': est.id,
                'perspectivas_id': est.perspectivas_id.id,
                'eje_estrategico_id': est.eje_estrategico_id.id,
                'name': est.name,
                'porciento_avance_barra': porciento_avance_barra,
            })
        return estrategicos

    # busca los objetivos anuales
    def reporte_cmi_anios_anuales(self):
        anio_activo = self.anio
        anuales = []
        obj_anuales_ids = self.env['sicpro.app.cmi.objetivos.anuales'].search(
            [('anio', '=', anio_activo)])
        real = 0
        meta = 0
        porciento_avance_barra = 0
        for anu in obj_anuales_ids:
            for valores in anu.obj_indicadores_ids:
                valores_indicadores_ids = self.env['sicpro.app.cmi.indicadores.valores'].search(
                    [('mes', '=', self.periodo), ('indicador_id', '=', valores.id)])
                for inds in valores_indicadores_ids:
                    real += inds.real
                    meta += inds.meta

            if real != 0 and meta != 0:
                porciento_avance_barra = round((real / meta) * 100)
            else:
                porciento_avance_barra = 0

            anuales.append({
                'id': anu.id,
                'obj_estrategico_id': anu.obj_estrategico_id.id,
                'name': anu.name,
                'eje_estrategico_id': anu.eje_estrategico_id.id,
                'porciento_avance_barra': porciento_avance_barra,
                'anio': anu.anio,
            })
            real = 0
            meta = 0
            porciento_avance_barra = 0
        return anuales

    # busca los indicadores
    def reporte_cmi_anios_indicadores(self):
        indicadores = []
        obj_indicadores_ids = self.env['sicpro.app.cmi.indicadores'].search(
            [('active', '=', True), ('anio', '=', self.anio)])

        for ind in obj_indicadores_ids:
            # busca los valores real y meta del mes especifico
            real = 0
            meta = 0
            porciento_avance_barra = 0
            valores_indicadores_ids = self.env[
                'sicpro.app.cmi.indicadores.valores'].search(
                    [('indicador_id', '=', ind.id), ('mes', '=', self.periodo)])
            for inds in valores_indicadores_ids:
                real += inds.real
                meta += inds.meta

                if real != 0 and meta != 0:
                    porciento_avance_barra = round((real / meta) * 100)
                else:
                    porciento_avance_barra = 0

            indicadores.append({
                'id': ind.id,
                'anio': ind.anio,
                'obj_anuales_id': ind.obj_anuales_id.id,
                'name': ind.name,
                'real_acumulado': real,
                'meta_acumulado': meta,
                'porciento_avance_barra': porciento_avance_barra,
                'responsable_id': ind.responsable_id.name,
                'obj_anuales_name': ind.obj_anuales_id.name,
                'obj_estrategico_name': ind.obj_anuales_id.obj_estrategico_id.name,
                'perspectiva_name': ind.obj_anuales_id.obj_estrategico_id.perspectivas_id.name,
                'obj_ejes_name': ind.obj_anuales_id.eje_estrategico_id.name,
                'comentario': ind.comentario,
            })
            real = 0
            meta = 0
        return indicadores

    # busca las acciones
    def reporte_cmi_anios_acciones(self):
        acciones = []
        acciones_ids = self.env['sicpro.app.cmi.acciones'].search(
            [('active', '=', True)])

        for acc in acciones_ids:
            acciones.append({
                'id': acc.id,
                'anio': acc.anio,
                'indicador_id': acc.indicador_id.id,
                'name': acc.name,
                'fecha_inicio': acc.fecha_inicio,
                'fecha_fin': acc.fecha_fin,
                'participantes_ids': acc.participantes_ids,
                'responsable_id': acc.responsable_id.name,
                'controla_id': acc.controla_id.name,
                'modo_control': acc.modo_control.name,
            })
        return acciones

    # genera el reporte seleccionado
    def generar_reporte(self):
        if self.tipo == 'completo':
            report = self.env["ir.actions.actions"]._for_xml_id(
                "sicpro_app_cmi.reporte_cmi_report_action_completo")
            return report
        elif self.tipo == 'eje':
            report = self.env["ir.actions.actions"]._for_xml_id(
                'sicpro_app_cmi.reporte_cmi_report_action_ejes')
            return report
        else:
            report = self.env["ir.actions.actions"]._for_xml_id(
                'sicpro_app_cmi.reporte_cmi_report_action_acciones')
            return report
