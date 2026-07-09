# -*- coding: utf-8 -*-


from odoo import fields, models, api
from odoo.exceptions import ValidationError

def order_by_secuence(elemento):
    return int(elemento[1])


class GraficosConfig(models.Model):
    _name = 'sicpro.modulo.dashboard.graficos'
    _description = "Gráficos de los grupos del dashboard"

    name = fields.Char(string='Nombre del Gráfico', required=True,
                       help='Nombre que aparecerá en la cima del Gráfico', )
    otro_id = fields.Integer(string='ID secondary', store=True, related='id',)
    tablero_many_2_one = fields.Many2one(
        string='Tablero Referencia',
        comodel_name='sicpro.modulo.dashboard.tableros',
        ondelete='no action',
    )
    app = fields.Many2one(
        'ir.module.module', string='Aplicación',
        help='Nombre de la Aplicación, utilizado para vincular los gráficos, '
             'grupos y secciones (Ejemplo: En las secciones solo aparecerán '
             'los grupos que posean la misma aplicación. Lo mismo sucede con '
             'los grupos y gráficos)', required=True, ondelete='no action',)
    app_name = fields.Char(string='Nombre Aplicación', related='app.name',)
    orden = fields.Selection(
        [('up', 'Arriba'), ('down', 'Abajo'), ], store=True, default='up',
        string="Posición", required=True,
        help='Posición en que aparecerán los gráficos(solo es útil cuando se '
             'muestran 2 gráficos en un mismo grupo')
    sequencia = fields.Integer(string='Orden', default=0, )
    modelo = fields.Many2one('ir.model', string='Modelo',
        help='Modelo del cual se extraerán los datos',
        required=True, ondelete='no action',)
    modelo_nombre = fields.Char(string='Nombre del Modelo',
                                related='modelo.model', store=True, )

    # Id del modelo para filtrar los campos y dejar solo los de dicho modelo
    # durante la selección
    modelo_id = fields.Integer(string="ID del Modelo", related='modelo.id',
                               store=True)
    tipo = fields.Selection(
        [('tarjeta', 'Tarjeta'), ('funnel', 'Gráfico de Embudo'),
         ('bar', 'Gráfico de Barras'), ('line', 'Gráfico de Líneas'),
         ('doughnut', 'Gráfico de Donut'), ('pie', 'Gráfico de Pie'),
         ('columnHeatmap', 'Tabla con mapa de calor'),
         ('table', 'Tabla común'),
         ('top', 'Tabla 10 mejores'), ], store=True, default='funnel',
        string="Tipo", help='Tipo de Gráfico a mostrar', required=True,)
    dominio = fields.Char(string='Dominio', default="[]",
                          help="Dominio para filtrar los datos", )
    agrupar = fields.Many2one(
        'ir.model.fields', string='Agrupador',
        help='Campo utilizado por los gráficos de donut, pie, barras  y embudo'
             ' para crear los grupos. En los gráficos de líneas, de top 10 y'
             ' de mapa de calor se utiliza para definir los '
             'nombres/identificadores/etiquetas de los valores a comparar '
             '(ya que dichos gráficos muestran los valores definidos en el'
             ' campo valores, este campo proporciona los nombres para '
             'identificar a quién pertenecen dichos valores)', )
    agrupar_extra = fields.Many2one(
        'ir.model.fields', string='Agrupador Extra',
        help='Campo utilizado por los gráficos de barras y de líneas embudo'
             ' para crear una segunda agrupación. Se agruparan por este valor '
             ' cada uno de los grupos obtenidos en el primer agrupador ', )
    agrupar_nombre = fields.Char(string='Nombre de Agrupar por', store=True,
                                 related='agrupar.name', )
    agrupar_extra_nombre = fields.Char(string='Nombre de Agrupar Extra',
                                       store=True, related='agrupar_extra.name', )
    operacion = fields.Selection(
        string='Operación', required=True, default='agrupar',
        help='La operación a realizar: Agrupar es para contar los valores por '
             'grupo seleccionado; Valor es para seleccionar un nombre y '
             'valores a mostrar',
        selection=[('agrupar', 'Agrupar'), ('valor', 'Valor')])
    es_agrupar = fields.Boolean(string='Es agrupador?', default=True,)
    orientacion_barra = fields.Selection(
        string='', required=True, default='vertical',
        help='La orientación de las barras del gráfico de barras:'
             ' Vertical (barras hacia arriba); Horizontal (barras'
             ' hacia los lados)',
        selection=[('vertical', 'Vertical'), ('horizontal', 'Horizontal')])
    es_barra_vertical = fields.Boolean(string='Es Barra vertical?', default=True,)
    icono = fields.Many2one(
        'sicpro.modulo.dashboard.iconos', string='Ícono', store=True,
        help='Ícono para mostrar en la tarjeta '
             '(disponible solo en el gráfico de tarjeta)', )
    icono_tarjeta = fields.Char(string='Clase del Ícono', store=True,
                                related='icono.clase', )
    nombre_serie = fields.Char(
        string='Nombre Serie', store=True,
        help='Nombre que tendrá la serie en los gráficos. En el mapa de  calor'
             ' se refiere a el encabezado de la columna de los valores. En el'
             ' gráfico de top 10 se refiere al subtítulo que tendrán '
             'todos los elementos', )
    encabezado_etiquetas = fields.Char(
        string='Encabezado Etiquetas', store=True,
        help='Encabezado de las etiquetas de la tabla mapa de calor '
             '(solo en mapa de calor)', )
    nombre_eje_x = fields.Char(
        string='Nombre Eje X', store=True,
        help='Nombre que aparecerá bajo el eje X (abajo del gráfico) en los '
             'gráficos de línea y de barras', )
    nombre_eje_y = fields.Char(
        string='Nombre Eje Y', store=True,
        help='Nombre que aparecerá junto el eje Y '
             '(al lateral izquierdo del gráfico) en los '
             'gráficos de línea y de barras', )
    font_size = fields.Integer(
        string='Tamaño Nombre Ejes', default=20,
        help='Tamaño (en pixels) que tendrán las etiquetas de los ejes X y Y. '
             'Utilizado en los gráficos de barras y de líneas', )
    active = fields.Boolean('Activo', default=True)
    grupos_contenido = fields.Many2many('sicpro.modulo.dashboard.grupos',
                                        'sicpro_modulo_dashboard_grupos_rel',
                                        string='Grupos')
    valores = fields.Many2one(
        'ir.model.fields', string='Valores',
        help='Campo por el cuál se seleccionarán los valores que se mostrarán '
             'en los gráficos de línea, de mapa de calor y de top 10', )
    valores_id = fields.Integer(string="ID del Valor", related='valores.id',
                               store=True)
    valores_nombre = fields.Char(string='Nombre de Valores a comparar',
                                 store=True, related='valores.name', )
    valores_extras = fields.One2many(
        comodel_name='sicpro.modulo.dashboard.graficos.values',
        string='Campos Extras', inverse_name='grafico',)
    valores_extras_nombres = fields.Char(
        string='Nombres Campos extras', store=True,)
    valores_extras_nombre_serie = fields.Char(
        string='Encabezado/Nombre de serie de Campos extras', store=True,)
    limite_tabla = fields.Integer(
        string='Cantidad de Datos', required=True, readonly=False,
        index=False, default=0,
        help="Límite de cantidad de registros a mostrar. \nPara mostrar todos usar 0"
    )
    orden_valores = fields.Selection(
        [('asc', 'Menor Primero'), ('desc', 'Mayor Primero'), ], store=True,
        default='desc', string="Orden de valores", required=True,
        help='Orden de los valores de las tablas de top 10 y mapa de calor. '
             'En mapa de calor también define el orden de los colores '
             '(Ejemplo: mayor primero representa a los mayores en color verde '
             'y los menores en rojo).\n También se utiliza para ordenar los '
             'valores de el gráfico de líneas (Solo cuando se agrupa por un solo '
             'valor)''')
    tarjeta_orientacion = fields.Selection(
        string='Ubicación del  Contenido', default='center',
        help='Ubicación del contenido de la Tarjeta dentro de la misma',
        selection=[('center', 'Centro'), ('left', 'Izquierda'), ('right', 'Derecha')])
    tarjeta_extra = fields.Char(
        string='Texto adicional',
        help='Texto adicional a mostrar junto al valor de la tarjeta',)
    tarjeta_extra_posicion = fields.Selection(
        string='Posición texto extra', required=True, default='prefijo',
        help='''Posición del texto extra del valor de la tarjeta (prefijo o sufijo'''
             '''). Si no existe texto extra el valor de este campo es ignorado.''',
        selection=[('prefijo', 'Antes del valor'), ('sufijo', 'Después del valor')])
    tarjeta_icono_posicion = fields.Selection(
        string='Posición Ícono', required=True, default='izquierda',
        help='''Posición del ícono con respecto al texto de la tarjeta''',
        selection=[('izquierda', 'Izquierda'), ('derecha', 'Derecha')])
    tarjeta_valor_titulo_posicion = fields.Selection(
        string='Posición Título/Valor', required=True, default='t-primero',
        help='''Posición del Valor y del título de la tarjeta (uno arriba y el otro abajo)''',
        selection=[('v-primero', 'Valor arriba'), ('t-primero', 'Título Arriba')])
    color_background = fields.Char(string='Fondo', required=True,  size=7,
                                   default='#FFFFFF', help='Color de Fondo del Gráfico',)
    color_name = fields.Char( string='Nombre', required=True, default='#000000',
                              size=7, help='Color de texto de Nombre del Gráfico',)
    color_icono = fields.Char(string='Ícono/Contador', required=True,
                              default='#7d7eaf', size=7,
                              help='Color del Ícono/Contador en tarjetas/tabla top',)
    color_background_icono = fields.Char(
        string='Fondo Ícono/Contador', size=7, required=True,
        default='#e5e5ef', help='Color del Fondo del Ícono/Contador en tarjetas/tabla top',)
    color_valor = fields.Char(
        string='Valor',
        required=True,
        default='#a6aaad',
        help='''Color de texto de Valor. En caso de la tabla'''
             ''' de top, el texto junto al valor también tendrá el mismo color.''',
        size=7,
    )
    color_background_valor = fields.Char(
        string='Fondo Valor',
        required=True,
        default='#ffffff',
        help='''Color de Fondo de celda del texto de Valor.''',
        size=7,
    )
    color_etiquetas = fields.Char(
        string='Etiquetas',
        required=True,
        default='#a6aaad',
        help='''Color de texto de etiquetas (grupos creados según el agrupador). ''',
        size=7,
    )
    color_background_etiquetas = fields.Char(
        string='Fondo Etiquetas',
        required=True,
        default='#ffffff',
        help='''Color de Fondo de celda del texto de etiquetas.''',
        size=7,
    )
    color_encabezados = fields.Char(
        string='Encabezados',
        required=True,
        default='#000000',
        help='''Color de texto de encabezados (grupos creados según el agrupador). ''',
        size=7,
    )
    color_background_encabezados = fields.Char(
        string='Fondo Encabezados',
        required=True,
        default='#ffffff',
        help='''Color de Fondo de celda del texto de encabezados.''',
        size=7,
    )
    color_background_grafico = fields.Char(
        string='Área Fondo',
        help='Color de Área Fondo en gráfico de Barras y de Líneas',
        size=7,
    )
    colores_graficos = fields.Many2one(
        'sicpro.modulo.dashboard.colores.set',
        string='Series de Gráficos',
        help='''Colores de las Series de los gráficos''',
    )
    color_top_subtitulo = fields.Char(
        string='Subtítulo',
        required=True,
        default='#a6aaad',
        help='''Color de texto de Subtítulo(Nombre de Serie)''',
        size=7,
    )

    @api.onchange('valores_extras')
    def _agregar_valores_extras_nombres(self):
        self.valores_extras_nombres = None
        self.valores_extras_nombre_serie = None
        
        if self.valores_extras:
            valores_temp = []
            for valor_temp in self.valores_extras:
                valores_temp.append([valor_temp,valor_temp.sequencia])

            valores_temp.sort(key=order_by_secuence)

            valores_extras = []
            for val_extra in valores_temp:
                valores_extras.append(val_extra[0])

            for valor in valores_extras:
                if self.valores_extras_nombres:
                    if not valor.valores.name in self.valores_extras_nombres:
                        self.valores_extras_nombres = self.valores_extras_nombres + "," + valor.valores.name
                else:
                    self.valores_extras_nombres = valor.valores.name

                if self.valores_extras_nombre_serie:
                   if not valor.name in self.valores_extras_nombre_serie:
                        self.valores_extras_nombre_serie = self.valores_extras_nombre_serie + "," + valor.name
                else:
                    self.valores_extras_nombre_serie = valor.name


    @api.onchange('orden')
    def _onchange_orden(self):
        if 'up' in self.orden:
            self.sequencia = 0
        else:
            self.sequencia = 1

    @api.onchange('operacion')
    def _onchange_operacion(self):
        if 'agrupar' in self.operacion:
            self.es_agrupar = True
        else:
            self.es_agrupar = False

    @api.onchange('orientacion_barra')
    def _onchange_orientacion_barra(self):
        if 'vertical' in self.orientacion_barra:
            self.es_barra_vertical = True
        else:
            self.es_barra_vertical = False

    @api.constrains('valores_extras','es_agrupar','valores')
    def _check_campo(self):
        existe = False
        for record in self:
            if not record.es_agrupar:
                for valor in record.valores_extras:
                    if valor.valores.id == record.valores.id:
                        existe = True
                        break
                if existe:
                    raise ValidationError('Error: No puede seleccionar como campo extra el campo de Valor Primario (Campo principal de valores): ' + record.valores.name)

    def button_colores_default(self):
        self.color_background = "#FFFFFF"
        self.color_name = "#000000"
        self.color_icono = "#7d7eaf"
        self.color_background_icono = "#e5e5ef"
        self.color_valor = "#a6aaad"
        self.color_background_valor = "#ffffff"
        self.color_etiquetas = "#a6aaad"
        self.color_background_etiquetas = "#ffffff"
        self.color_encabezados = "#000000"
        self.color_background_encabezados = "#ffffff"
        self.color_top_subtitulo = "#a6aaad"
        self.color_background_grafico = False
        self.colores_graficos = False




class ValoresExtraOrdenados(models.Model):
        _name = 'sicpro.modulo.dashboard.graficos.values'
        _description = "Valores Extra de Gráficos de los grupos del dashboard"
        _order = 'sequencia asc'

        name = fields.Char(string='Nombre', required=True,
                           help='Nombre del valor que aparecerá en su encabezado', )
        sequencia = fields.Integer(string='Orden', default=1, help='''Orden en'''
                                   ''' que aparecerán los valores''', required=True)
        valores = fields.Many2one(
            'ir.model.fields',
            string='Valores Extras',
            required=True,
            ondelete='no action',
        )
        grafico = fields.Many2one(
            'sicpro.modulo.dashboard.graficos',
            string='Gráfico',
        )
        modelo_id = fields.Integer(string="ID del Modelo",
                                   store=True)

        @api.constrains('valores')
        def _check_campo(self):
            for record in self:
                if not record.grafico.es_agrupar and record.grafico.valores.id == record.valores.id:
                    raise ValidationError('Error: No puede seleccionar como campo extra el campo de Valor Primario (Campo principal de valores): ' + record.valores.name)