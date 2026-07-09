# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models, api
from odoo.exceptions import AccessError


def order_by_secuence(elemento):
    return int(elemento[1])

def _default_color():
    return randint(1, 11)

class TablerosConfig(models.Model):
    _name = 'sicpro.modulo.dashboard.tableros'
    _description = "Tableros"

    # El nombre que posee el tablero en que se mostrará en la cima
    nombre_tablero = fields.Char(
        string='Nombre del Tablero',
        help='Nombre que aparecerá en la cima del Tablero',
        required=True, )
    app = fields.Many2one(
        'ir.module.module', string='Aplicación',
        help='Nombre de la Aplicación, utilizado para vincular los gráficos, '
             'grupos y secciones (Ejemplo: En las secciones solo aparecerán '
             'los grupos que posean la misma aplicación. '
             'Lo mismo sucede con los grupos y gráficos)',
             required=True,
             ondelete='no action',
        )
    app_name = fields.Char(
        string='Nombre Aplicación',
        related='app.name',
    )
    color = fields.Char(
        string='Título',
        required=True,
        default='#000000',
        help='''Color de Título de Dashboard''',
        size=7,
    )
    color_subtitulo = fields.Char(
        string='Descripción',
        required=True,
        default='#5d6369',
        help='''Color de Subtítulo de Dashboard''',
        size=7,
    )
    color_warning = fields.Char(
        string='Advertencia',
        required=True,
        default='#5d6369',
        help='''Color de Advertencia de Dashboard(a la derecha **)''',
        size=7,
    )
    color_background = fields.Char(
        string='Fondo',
        required=True,
        default='#f8f9fa',
        help='''Color de Fondo de Dashboard''',
        size=7,
    )
    color_background_header = fields.Char(
        string='Fondo Encabezado',
        required=True,
        default='#f8f9fa',
        help='''Color de Fondo de Dashboard''',
        size=7,
    )
    color_background_imprimir = fields.Char(
        string='Fondo Imprimir',
        required=True,
        default='#017E84',
        help='''Color de Fondo de Botón de Imprimir''',
        size=7,
    )
    color_imprimir = fields.Char(
        string='Imprimir',
        required=True,
        default='#d2c6cf',
        help='''Color de Letras de Botón de Imprimir''',
        size=7,
    )


    # 'ir.module.module'
    # El identificador del tablero se utiliza para vincular las secciones a
    # los tableros en que se deben mostrar
    identificador_tablero = fields.Selection(
        [('sicpro.app.administracion', 'Dashboard de Administración')],
        store=True, string="Identificador del Tablero", required=True,
        help='Utilizado para vincular el tablero con el menú/acción de la '
             'Aplicación en que se debe mostrar. En el código se hereda este '
             'modelo y a este campo y se le añade el identificador '
             '(con selection_add para no eliminar los existentes)')
    subtitulo_tablero = fields.Char(
        string='Descripción del Tablero',
        help='Subtítulo que aparecerá bajo el nombre del Tablero', )
    secciones = fields.Many2many(
        'sicpro.modulo.dashboard.secciones', 'sicpro_modulo_dashboard_sec_rel',
        help='Secciones que contendrá el tablero. No tiene límites en cuanto '
             'a cantidad de secciones', string='Secciones',)
    grupos = fields.Many2many(
        'sicpro.modulo.dashboard.grupos', 'sicpro_modulo_dashboard_gru_rel',
        help='Grupos que existen en las secciones del tablero ', string='Grupos',)
    graficos = fields.One2many(
        string='Gráficos',
        help='Gráficos que existen en las secciones del tablero ',
        comodel_name='sicpro.modulo.dashboard.graficos',
        inverse_name='tablero_many_2_one',
    )
    active = fields.Boolean('Activo', default=True)

    @api.onchange('secciones')
    def _onchange_secciones(self):
        if self.secciones:
            for seccion in self.secciones:
                seccion.app = self.app
                for grupo in seccion.grupos:
                    self.grupos = [(4,grupo.id)]
                    for grafico in grupo.graficos:
                        self.graficos = [(4,grafico.id)]

    @api.onchange('grupos')
    def _onchange_grupos(self):
        if self.grupos:
            for grupo in self.grupos:
                grupo.app = self.app
                for grafico in grupo.graficos:
                    self.graficos = [(4,grafico.id)]

    @api.model
    def leer_group(self, model, fields, domain, groupBy):
        temp = self.env[model].sudo().read_group(
            fields=fields, domain=domain, groupby=groupBy,)
        return temp

    @api.model
    def leer_group_double(self, model, fields, domain, groupBy, lazy):
        temp = self.env[model].sudo().read_group(
            fields=fields, domain=domain, groupby=groupBy, lazy=lazy)
        return temp

    @api.model
    def leer_busqueda(self, model, domain, values):
        temp = self.env[model].sudo().search_read(domain, values)
        return temp

    @api.model
    def leer(self, model, domain):
        temp = self.env[model].sudo().search(domain)
        temp2 = []
        for te in temp:
            temp2.append(te.id)
        return temp2

    @api.model
    def error_acceso(self):
        raise AccessError("Usted no tiene acceso a ninguno de los registros selecconados")

    def button_colores_default(self):
        self.color = "#000000"
        self.color_subtitulo = "#5d6369"
        self.color_warning = "#5d6369"
        self.color_background = "#f8f9fa"
        self.color_background_header = "#f8f9fa"
        self.color_background_imprimir = "#017E84"
        self.color_imprimir = "#d2c6cf"


    def contenido_tablero(self):
        secciones = []
        resultado = {'nombre_tablero': self.nombre_tablero, 'color_nombre_tablero': self.color, "subtitulo_tablero": self.subtitulo_tablero, "color_subtitulo": self.color_subtitulo, "color_advertencia": self.color_warning, "color_fondo": self.color_background, "color_fondo_encabezado": self.color_background_header, "color_imprimir": self.color_imprimir, "color_background_imprimir": self.color_background_imprimir, }
        if self.secciones:
            for seccion in self.secciones:
                grupos = []
                if seccion.grupos:
                    for grupo in seccion.grupos:
                        graficos = []
                        if grupo.graficos:
                            for grafico in grupo.graficos:
                                colores_seq = []
                                for color in grafico.colores_graficos.colores:
                                    colores_seq.append([color.color,color.orden])
                                colores_seq.sort(key=order_by_secuence)

                                colores = []

                                for color in colores_seq:
                                    colores.append(color[0])

                                graficos.append([{'name': grafico.name,
                                                  'modelo_nombre': grafico.modelo_nombre,
                                                  'es_agrupar': grafico.es_agrupar,
                                                  'es_barra_vertical': grafico.es_barra_vertical,
                                                  'tipo': grafico.tipo,
                                                  'dominio': grafico.dominio,
                                                  'limite_tabla': grafico.limite_tabla,
                                                  'agrupar_nombre': grafico.agrupar_nombre,
                                                  'agrupar_extra_nombre': grafico.agrupar_extra_nombre,
                                                  'icono_tarjeta': grafico.icono_tarjeta,
                                                  'nombre_serie': grafico.nombre_serie,
                                                  'encabezado_etiquetas': grafico.encabezado_etiquetas,
                                                  'nombre_eje_x': grafico.nombre_eje_x,
                                                  'nombre_eje_y': grafico.nombre_eje_y,
                                                  'font_size': grafico.font_size,
                                                  'valores_nombre': grafico.valores_nombre,
                                                  'valores_extras_nombres': grafico.valores_extras_nombres,
                                                  'valores_extras_nombre_serie': grafico.valores_extras_nombre_serie,
                                                  'orden_valores': grafico.orden_valores,
                                                  'tarjeta_orientacion': grafico.tarjeta_orientacion,
                                                  'tarjeta_extra': grafico.tarjeta_extra,
                                                  'tarjeta_extra_posicion': grafico.tarjeta_extra_posicion,
                                                  'tarjeta_icono_posicion': grafico.tarjeta_icono_posicion,
                                                  'tarjeta_valor_titulo_posicion': grafico.tarjeta_valor_titulo_posicion,
                                                  'color_background': grafico.color_background,
                                                  'color_name': grafico.color_name,
                                                  'color_icono': grafico.color_icono,
                                                  'color_background_icono': grafico.color_background_icono,
                                                  'color_valor': grafico.color_valor,
                                                  'color_background_grafico': grafico.color_background_grafico,
                                                  'colores_graficos': colores,
                                                  'color_background_valor': grafico.color_background_valor,
                                                  'color_etiquetas': grafico.color_etiquetas,
                                                  'color_background_etiquetas': grafico.color_background_etiquetas,
                                                  'color_encabezados': grafico.color_encabezados,
                                                  'color_background_encabezados': grafico.color_background_encabezados,
                                                  'color_top_subtitulo': grafico.color_top_subtitulo,},
                                                 grafico.sequencia])
                            graficos.sort(key=order_by_secuence)
                            grupos.append([graficos, grupo.sequencia])
                    grupos.sort(key=order_by_secuence)
                    secciones.append([grupos, seccion.sequencia])
            secciones.sort(key=order_by_secuence)

            secciones_final = []
            graficos_final = []

            if secciones:
                for seccion in secciones:
                    grupos_final = []
                    if seccion[0]:
                        for grupo in seccion[0]:
                            graficos_final_temp = []
                            if grupo[0]:
                                for grafico in grupo[0]:
                                    graficos_final_temp.append(grafico[0])
                                    graficos_final.append(grafico[0])
                            grupos_final.append(graficos_final_temp)
                    secciones_final.append(grupos_final)
                resultado = {'nombre_tablero': self.nombre_tablero,
                             'color_nombre_tablero': self.color,
                             'color_subtitulo': self.color_subtitulo, 
                             'color_advertencia': self.color_warning,
                             'color_fondo': self.color_background, 
                             'color_fondo_encabezado': self.color_background_header,
                             'color_imprimir': self.color_imprimir,
                             'color_background_imprimir': self.color_background_imprimir,
                             'subtitulo_tablero': self.subtitulo_tablero,
                             'secciones': secciones_final,
                             'graficos': graficos_final, }
        return resultado

