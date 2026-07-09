odoo.define('sicpro_dashboard.dashboard_view', function (require) {
    'use strict';

    var BasicController = require('web.BasicController');
    var FormController = require('web.FormController');
    var AbstractAction = require('web.AbstractAction');
    var framework = require('web.framework');
    var session = require('web.session');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var web_client = require('web.web_client');
    var assets = require('@web/core/assets');
    var formController = require('web.FormController');
    var _t = core._t;
    var QWeb = core.qweb;
    var self = this;

    var colores_pie_donut = [
    "#003f5c",
    "#2f4b7c",
    "#f95d6a",
    "#665191",
    "#d45087",
    "#ff7c43",
    "#ffa600",
    "#a05195",
    "#6d5c16",
    "#5f1380",
    "#644fdb",
    "#1f77b4",
    "#ff7f0e",
    "#aec7e8",
    "#ffbb78",
    "#2ca02c",
    "#98df8a",
    "#d62728",
    "#ff9896",
    "#9467bd",
    "#c5b0d5",
    "#8c564b",
    "#c49c94",
    "#e377c2",
    "#f7b6d2",
    "#7f7f7f",
    "#c7c7c7",
    "#bcbd22",
    "#dbdb8d",
    "#17becf",
    "#9edae5",
    ];

    function datos_faltantes_tarjetas(callbacks_todos,callbacks_restringidos) {
        var Texto = "(Acceso a " + callbacks_restringidos.length + " registros de " + callbacks_todos.length + ")";
        return Texto;
    }

    function datos_faltantes_embudo(callbacks_todos,callbacks_restringidos) {
        //////aqui recorrer los grupos de cada grafico
        var Texto = "(Acceso a " + callbacks_restringidos.length + " registros de " + callbacks_todos.length + ")";
        return Texto;
    }

    function filtrar_datos(actual) {

        var dominio = [];
        
        if(actual.dominio != '[]')
        {
            var dominioTemporal = actual.dominio.replaceAll("True","true");
            dominioTemporal = dominioTemporal.replaceAll("False","false");
            dominio = JSON.parse(dominioTemporal);
        }

        var valores_extra = actual.valores_extras_nombres;
        var valores_extra_nombre_serie = actual.valores_extras_nombre_serie;

        if(valores_extra) {
            valores_extra = valores_extra.replace("[", "");
            valores_extra = valores_extra.replace("]", "");
            valores_extra = valores_extra.replaceAll("'", "");
            valores_extra = valores_extra.replaceAll(" ", "")
            valores_extra = valores_extra.split(",");

            valores_extra_nombre_serie = valores_extra_nombre_serie.replace("[", "");
            valores_extra_nombre_serie = valores_extra_nombre_serie.replace("]", "");
            valores_extra_nombre_serie = valores_extra_nombre_serie.replaceAll("'", "");
            valores_extra_nombre_serie = valores_extra_nombre_serie.split(",");
        }

        var agrupar_extra = actual.agrupar_extra_nombre;
        if (agrupar_extra) {
            agrupar_extra = agrupar_extra.replace("[", "");
            agrupar_extra = agrupar_extra.replace("]", "");
            agrupar_extra = agrupar_extra.replaceAll("'", "");
            agrupar_extra = agrupar_extra.replaceAll(" ", "")
            agrupar_extra = agrupar_extra.split(",");
        }

        var agrupar = actual.agrupar_nombre;
        if (agrupar) {
            agrupar = agrupar.replace("[", "");
            agrupar = agrupar.replace("]", "");
            agrupar = agrupar.replaceAll("'", "");
            agrupar = agrupar.replaceAll(" ", "")
            agrupar = agrupar.split(",");

            if(agrupar_extra) {
                agrupar = agrupar.concat(agrupar_extra);
            }
        }

        var valores = actual.valores_nombre;
        if(valores) {
            valores = valores.replace("[", "");
            valores = valores.replace("]", "");
            valores = valores.replaceAll("'", "");
            valores = valores.replaceAll(" ", "")
            valores = valores.split(",");

            if(valores_extra) {
                valores = valores.concat(valores_extra);
            }
        }

        return { dominio, agrupar, valores, valores_extra_nombre_serie};
    }

    function filtrar_indice(indiceOriginal) {
        return indiceOriginal.replace("grafico-","");
    }

    function filtrar_callback_con_acceso_filtrado(filtered_callbacks, con_acceso_filtrado,es_embudo) {
        let callback_filtrados = [];
        let con_access_filtrado = [];

        if(!es_embudo)
        {
            for (var i = 0; i < filtered_callbacks[0].length; i++) {
                callback_filtrados[i] = [filtered_callbacks[1][i],filtered_callbacks[0][i]];
            }
            for (var i = 0; i < con_acceso_filtrado[0].length; i++) {
                con_access_filtrado[i] = [con_acceso_filtrado[1][i],con_acceso_filtrado[0][i]];
            }
        }else{
            callback_filtrados = filtered_callbacks;
            con_access_filtrado = con_acceso_filtrado;
        }

        let arr = [];
        for (var i = con_access_filtrado.length - 1; i >= 0; i--) {
            let Texto = "";
            let condicion = false;
            let index = callback_filtrados.findIndex(function(element) {
                if(con_access_filtrado[i][0] == element[0])
                {
                    Texto = "(Acceso a " + con_access_filtrado[i][1] + " registros de " + element[1] + ")";
                    condicion = con_access_filtrado[i][1] != element[1];
                }
                return con_access_filtrado[i][0] == element[0];
            });
            if(index >= 0)
            {
                arr[index] = [con_access_filtrado[i][1],condicion, Texto];
            }
        }

        return arr;

    }

    function filtrar_callback_groupby_double(callbacks,datos_filtrados) {
        var filtered_callbacks = {};

        for (let i = callbacks.length - 1; i >= 0; i--) {
            let value = callbacks[i].__count, labels = [callbacks[i][datos_filtrados.agrupar[0]],callbacks[i][datos_filtrados.agrupar[1]]];
            if (value != 0){
                for (var k = 0; k < labels.length; k++) {
                    if (typeof(labels[k]) == 'boolean') {
                        if(!labels[k])
                        {
                            labels[k] = "Desconocido";
                        }else{
                            labels[k] = "Es " + datos_filtrados.agrupar[k];
                        }
                    }
                    else{
                        if (typeof(labels[k]) == 'object') {
                            labels[k] = labels[k][1];
                        }
                    }
                }
                if(!filtered_callbacks[labels[0]])
                {
                    filtered_callbacks[labels[0]] = {};
                }
                filtered_callbacks[labels[0]][labels[1]] = value;
            }
        }

        return filtered_callbacks;
    }

    function filtrar_callback(callbacks, isGroupBy, tipo, datos_filtrados) {
        var filtered_callbacks = [[],[]];
        if (tipo == "embudo")
        {
            filtered_callbacks = [];
        }
        if (isGroupBy) {
            for (let i = callbacks.length - 1; i >= 0; i--) {

                let arr_label_value = extraer_label_value(callbacks[i],tipo);
                let value = arr_label_value[1], label = arr_label_value[0];
                
                if (value != 0){
                    if (tipo == "embudo")
                    {
                        filtered_callbacks.push([label,value]);
                    }
                    else
                    {
                        filtered_callbacks[0].push(value);
                        filtered_callbacks[1].push(label);
                    }   
                }
            }
        }
        else{
            if (datos_filtrados.valores[1] && (tipo == "bar" || tipo == "line")) {
                let arr_relleno = new Array(datos_filtrados.valores.length - 1).fill([]);
                filtered_callbacks.push(...arr_relleno);
            }
            for (let i = callbacks.length - 1; i >= 0; i--) {
                if(callbacks[i][datos_filtrados.valores[0]] != 0)
                {
                    let label = callbacks[i][datos_filtrados.agrupar[0]];
                    if (typeof(label) == 'object') {
                        label = label[1];
                    }
                    if (tipo == "embudo") {
                        filtered_callbacks.push([label,callbacks[i][datos_filtrados.valores[0]]]);
                    }
                    else{
                        if (datos_filtrados.valores[1] && (tipo == "bar" || tipo == "line")) {
                            var j = 0;
                            for (j = 0; j < datos_filtrados.valores.length; j++) {
                                filtered_callbacks[j].push(callbacks[i][datos_filtrados.valores[j]]);
                            }
                            filtered_callbacks[j].push(label);
                        }
                        else
                        {
                            filtered_callbacks[0].push(callbacks[i][datos_filtrados.valores[0]]);
                            filtered_callbacks[1].push(label);
                        }
                    }
                }
            }
        }

        return filtered_callbacks;
    }

    function extraer_labels_originales(callbacks) {
        var labelsOriginales = [];
        for (let i = callbacks.length - 1; i >= 0; i--) {
            let callback = callbacks[i];
            let value = 0;
            Object.keys(callback).find(element => {
                if(element.includes('_count'))
                {
                    value = callback[element];
                }
            });
            if (value != 0) {
                labelsOriginales.push(callback.__domain);
            }
        }
        
        return labelsOriginales;
    }

    function extraer_labels_originales_double(callbacks) {
        var labelsOriginales = [];
        for (let i = callbacks.length - 1; i >= 0; i--) {
            let callback = callbacks[i];
            if (callbacks[i].__count != 0) {
                labelsOriginales.push(callback.__domain);
            }
        }
        
        return labelsOriginales;
    }

    function extraer_labels_originales_con_valor(callbacks) {
        var labelsOriginales = [];
        for (let i = callbacks.length - 1; i >= 0; i--) {
            let callback = callbacks[i];
            let labelOriginal = "";
            let value = 0;
            Object.keys(callback).find(element => {
                if(element.includes('_count'))
                {
                    value = callback[element];
                    labelOriginal = callback[element.replaceAll('_count','')];
                }
            });
            if (value != 0) {
                labelsOriginales.push([callback.__domain,labelOriginal]);
            }
        }

        return labelsOriginales;
    }

    function extraer_labels_originales_con_valor_acceso(callbacks, con_acceso) {
        var labelsOriginales = {};
        for (let i = callbacks.length - 1; i >= 0; i--) {
            let callback = callbacks[i];
            let labelOriginal = "";
            let value = 0;
            Object.keys(callback).find(element => {
                if(element.includes('_count'))
                {
                    value = callback[element];
                    labelOriginal = callback[element.replaceAll('_count','')];
                }
            });
            if (value != 0) {
                if (typeof(labelOriginal) == 'object') {
                    labelOriginal = labelOriginal[1];
                }
                labelsOriginales[labelOriginal] = [callback.__domain,value];
            }
        }

        for (let i = con_acceso.length - 1; i >= 0; i--) {
            let acces = con_acceso[i];
            let labelAcces = "";
            let value_acces = 0;
            Object.keys(acces).find(element => {
                if(element.includes('_count'))
                {
                    value_acces = acces[element];
                    labelAcces = acces[element.replaceAll('_count','')];
                }
            });
            if (value_acces != 0) {
                if (typeof(labelAcces) == 'object') {
                    labelAcces = labelAcces[1];
                }
                if(labelsOriginales[labelAcces])
                {
                    labelsOriginales[labelAcces].push(value_acces);
                }
            }
        }

        return labelsOriginales;
    }

    function extraer_labels_originales_con_valor_acceso_double(callbacks, con_acceso,datos_filtrados) {
        var labelsOriginales = {};

        for (let i = callbacks.length - 1; i >= 0; i--) {
            let callback = callbacks[i];
            let labelExterna = "";
            let labelInterna = "";
            let value = callback.__count;
            labelExterna = callback[datos_filtrados.agrupar[0]];
            labelInterna = callback[datos_filtrados.agrupar[1]];
            if (value != 0) {
                if (typeof(labelExterna) == 'object') {
                    labelExterna = labelExterna[1];
                }
                if (typeof(labelInterna) == 'object') {
                    labelInterna = labelInterna[1];
                }
                if(!labelsOriginales[labelExterna])
                {
                    labelsOriginales[labelExterna] = {};
                }
                labelsOriginales[labelExterna][labelInterna] = [callback.__domain,value];
            }
        }

        for (let i = con_acceso.length - 1; i >= 0; i--) {
            let acces = con_acceso[i];
            let labelAccesExt = "";
            let labelAccesInt = "";
            let value_acces = acces.__count;
            labelAccesExt = acces[datos_filtrados.agrupar[0]];
            labelAccesInt = acces[datos_filtrados.agrupar[1]];


            if (value_acces != 0) {
                if (typeof(labelAccesExt) == 'object') {
                    labelAccesExt = labelAccesExt[1];
                }
                if (typeof(labelAccesInt) == 'object') {
                    labelAccesInt = labelAccesInt[1];
                }
                if(!labelsOriginales[labelAccesExt])
                {
                    labelsOriginales[labelAccesExt] = {};
                }
                if(labelsOriginales[labelAccesExt][labelAccesInt])
                {
                    labelsOriginales[labelAccesExt][labelAccesInt].push(value_acces);
                }
            }
        }

        return labelsOriginales;
    }

    function extraer_label_value(callback,tipo) {
        var value = 0, label = "";
        let once = false;
        Object.keys(callback).find(element => {
            if(element.includes('_count') && !once)
            {
                let elemento_sin_count = element.replaceAll('_count','');
                value = callback[element];
                let elemento = callback[elemento_sin_count];
                label = elemento;

                if (typeof(elemento) == 'boolean') {
                    if(!elemento)
                    {
                        label = "Desconocido";
                    }else{
                        label = "Es " + elemento_sin_count;
                    }
                }
                else{
                    if (typeof(elemento) == 'object') {
                        Object.keys(elemento).find(key => {
                            if(key != 'id'){
                                label = elemento[key];
                            }
                        });
                    }
                }
                once = true;
            }
        });
        return [label,value];
    }

    function ordenar_callback(callbacks, datos_filtrados, orden) {
        let ordenado = callbacks;
        if('desc' == orden){
            ordenado.sort((a,b) => (a[datos_filtrados.valores[0]] < b[datos_filtrados.valores[0]] ? 1 : -1));
        }
        else {
            ordenado.sort((a,b) => (a[datos_filtrados.valores[0]] < b[datos_filtrados.valores[0]] ? -1 : 1));
        }

        return ordenado;
    }    

    var DashboardView = AbstractAction.extend({
        contentTemplate: 'DashboardView',

        
        _sudo_rpc_groupby: function(argumentos){
            return rpc.query({
                model: 'sicpro.modulo.dashboard.tableros',
                method: 'leer_group',
                args: [argumentos.model,argumentos.fields,argumentos.domain,argumentos.groupBy],
            });
        },

        _sudo_rpc_groupby_double: function(argumentos,lazy){
            return rpc.query({
                model: 'sicpro.modulo.dashboard.tableros',
                method: 'leer_group_double',
                args: [argumentos.model,argumentos.fields,argumentos.domain,argumentos.groupBy,lazy],
            });
        },

        _rpc_groupby: function(argumentos){
            return rpc.query({
                model: argumentos.model,
                method: 'read_group',
                fields: argumentos.fields,
                domain: argumentos.domain,
                groupBy: argumentos.groupBy,
            });
        },

        _rpc_groupby_double: function(argumentos, lazy=false){
            return rpc.query({
                model: argumentos.model,
                method: 'read_group',
                fields: argumentos.fields,
                domain: argumentos.domain,
                groupBy: argumentos.groupBy,
                lazy: lazy,
            });
        },

        _sudo_rpc_searchRead: function(argumentos){
            return rpc.query({
                model: 'sicpro.modulo.dashboard.tableros',
                method: 'leer_busqueda',
                args: [argumentos.model, argumentos.domain, argumentos.values],
            });
        },

        _sudo_rpc_read: function(argumentos){
            return rpc.query({
                model: 'sicpro.modulo.dashboard.tableros',
                method: 'leer',
                args: [argumentos.model,argumentos.domain],
            });
        },


        _rpc_search: function(argumentos){
            return rpc.query({
                model: argumentos.model,
                method: 'search',
                args: [argumentos.domain],
            });
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['EncabezadoDashboard', 'TableroDashboard'];
            this.identificador = context.context.nombre_modelo_dashboard;
            this.title = "Dashboard";
            this.subtitle = "";
        },

        willStart: function(){
            var self = this;
            return this._super()
            .then(async function () {
                await assets.useAssets({ jsLibs: ["/sicpro_modulo_dashboard_extendido/static/src/lib/Chart.bundle.js","/sicpro_modulo_dashboard_extendido/static/src/lib/chartjs-plugin-datalabels.min.js"]});
                if(!window.ChartLib){
                    window.ChartLib = Chart; 
                    ChartLib.pluginService.register({
                        beforeDraw: function(chart, easing) {
                            if(chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor)
                            {
                                var helpers = ChartLib.helpers;
                                var ctx = chart.chart.ctx;
                                var chartArea = chart.chartArea;
                                ctx.save();
                                ctx.fillStyle = chart.config.options.chartArea.backgroundColor;
                                ctx.fillRect(chartArea.left,chartArea.top,chartArea.right - chartArea.left,chartArea.bottom - chartArea.top);
                                ctx.restore();
                            }
                        }
                    });
                }
                
                self.ChartLib = ChartLib;

                let argumentos = [(['identificador_tablero', '=', self.identificador])];

                var secciones = rpc.query({
                    model: 'sicpro.modulo.dashboard.tableros',
                    method: 'search',
                    args: [argumentos],
                }).then(function(result) {
                    let id = result[0];
                    return rpc.query({
                        model: 'sicpro.modulo.dashboard.tableros',
                        method: 'contenido_tablero',
                        args: [id],
                    }).then(function(resultA) {
                        self.graficos_nuevos = resultA.graficos;
                        self.charts = [];
                        self.reglas_acceso = [];
                        if(resultA.nombre_tablero)
                        {
                            self.title = resultA.nombre_tablero;
                        }
                        if(resultA.subtitulo_tablero)
                        {
                            self.subtitle = resultA.subtitulo_tablero;
                        }

                        self.title_color = resultA.color_nombre_tablero;
                        self.subtitle_color = resultA.color_subtitulo;
                        self.warning_color = resultA.color_advertencia;
                        self.board_color = resultA.color_fondo;
                        self.board_header_color = resultA.color_fondo_encabezado;
                        self.color_imprimir = resultA.color_imprimir;
                        self.color_background_imprimir = resultA.color_background_imprimir;

                        // height_dashboard_print = 1886.5500000000002
                        // width dashboard = 1798
                        self.height_dashboard_print = 1886.55;
                        self.width_dashboard_print = self.height_dashboard_print / 1.04924917;

                        self.secciones_nuevos = resultA.secciones;
                        // self.ultima_seccion = [self.secciones_nuevos.pop()];
                        self.cantidad_graficos_seccion = [];
                        if(self.secciones_nuevos){
                            self.secciones_nuevos.forEach(function(seccion) {
                                let contador = 0;
                                seccion.forEach(function(grupo) {
                                    grupo.forEach(function(grafico) {
                                        contador++;
                                    });
                                });
                                self.cantidad_graficos_seccion.push(contador);
                            });
                        }
                    });
                });
                
                return $.when(secciones);
            });
},

start: function() {
    var self = this;
    this.set("title", self.title);
    return this._super().then(function() {
        self = self.update_cp();
        self.render_dashboards();
        self = self.update_cp();
        self.render_graphs();
        self.$el.parent().addClass('oe_background_grey');
        let dashboard_element = self.$el.find('.oh_dashboards')[0];
        dashboard_element.style.backgroundColor = self.board_color;
        let elements_last_row = self.$el.find('.row:last-child .chart-container.card-shadow');
        elements_last_row.css("height","96%");
        let color_image_background = "conic-gradient( " + self.board_header_color + " 0deg 90deg, " + self.board_color + " 90deg 270deg, " + self.board_header_color + " 270deg 360deg )";
        self.$el[0].style.backgroundImage = color_image_background;
        self.dashboard_element = dashboard_element;
    });
},

render_graphs: function(){
    var self = this;
    self.tarjetas();
    self.grafico_embudo();
    self.grafico_doughnut();
    self.grafico_pie();
    self.grafico_bar();
    self.grafico_linea();
    self.tabla_heatmap();
    self.tabla_normal();
    self.tabla_top_10();
    self.doc_ready();
},

grafico_embudo: function () {
    var self = this;
    var contenedoresEmbudo = self.$el.find('.container-funnel');
    contenedoresEmbudo.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
        }

        let colores_graficos = actual.colores_graficos;

        if(!colores_graficos[0])
        {
            colores_graficos = colores_pie_donut;
        }
        
        self._sudo_rpc_groupby(argumentos).then(function (callbacks) {

            var filtered_callbacks = null;
            var valores_de_etiquetas_originales = null;
            var rpc_temp = null;
            var chart = null;

            filtered_callbacks = filtrar_callback(callbacks, true, "embudo");
            valores_de_etiquetas_originales = extraer_labels_originales(callbacks);

            rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                self.reglas_acceso[indice] = filtrar_callback_con_acceso_filtrado(filtered_callbacks,filtrar_callback(con_acceso, true, "embudo"),true);
            });

            self.charts[indice] = ['', valores_de_etiquetas_originales];

            chart = Highcharts.chart({
                chart: {
                    type: "funnel",
                    renderTo: self.$el.find("." + indiceOriginal)[0],
                },
                title: false,
                credits: {
                    enabled: false
                },
                plotOptions: {
                    series: {
                        colors: colores_graficos,
                        dataLabels: {
                            enabled: true,
                            softConnector: true
                        },
                        center: ['35%', '50%'],
                        neckWidth: '20%',
                        neckHeight: '35%',
                        width: '70%',
                        height: '80%',
                        point: {
                            events: {
                                click: function(event) {
                                    event.stopPropagation();
                                    event.preventDefault();

                                    let elementAtClick = this;

                                    let arr_dominios = self.charts[indice][1];
                                    let dominio = [];
                                    let reglas_acceso = [];

                                    let index = filtered_callbacks.findIndex(function(ite) {
                                        let item = ite[0];
                                        if(typeof(item) == 'string')
                                        {
                                            return item.trim() == elementAtClick.name.trim();
                                        }
                                        else
                                        {
                                            return item == elementAtClick.name;
                                        }
                                    });

                                    if(index >= 0)
                                    {
                                        dominio = self.charts[indice][1][index];
                                        reglas_acceso = self.reglas_acceso[indice];
                                    }

                                    var options = {
                                        on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                                    };
                                    var modelo = self.graficos_nuevos[indice].modelo_nombre;
                                    if(reglas_acceso[index]){
                                        let nombre_accion = actual.name + " ";
                                        if(reglas_acceso[index][1])
                                        {
                                            nombre_accion = nombre_accion + reglas_acceso[index][2];
                                        }
                                        self.do_action({
                                            name: nombre_accion,
                                            type: 'ir.actions.act_window',
                                            res_model: modelo,
                                            view_mode: 'tree,form,calendar',
                                            views: [[false, 'list'],[false, 'form']],
                                            target: 'current',
                                            domain: dominio,
                                        }, options);
                                    }else{
                                        self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
                                    }

                                }
                            },
                        },
                    }
                },
                series: [ {
                    name: actual.nombre_serie,
                    data: filtered_callbacks,
                }],
            });
            self.charts[indice] = [chart, valores_de_etiquetas_originales];

            return rpc_temp;

        });
});
},


// AL Final /////////////////////////////////////////////////////////////////////////////////////////


// AL Final /////////////////////////////////////////////////////////////////////////////////////////

grafico_doughnut:function(){
    var self = this;
    var contenedoresDoughnut = self.$el.find('.container-doughnut');
    contenedoresDoughnut.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
        }

        let colores_graficos = actual.colores_graficos;
        
        self._sudo_rpc_groupby(argumentos).then(function (callbacks) {

            let filtered_callbacks = filtrar_callback(callbacks, true, "doughnut");
            let valores_de_etiquetas_originales = extraer_labels_originales(callbacks);
            
            var data = {
                labels : filtered_callbacks[1],
                datasets: [{
                        label: "", /////Inutil ////////////////////////////////////////////
                        data: filtered_callbacks[0],
                        backgroundColor: colores_pie_donut,
                        borderColor: colores_pie_donut,
                        borderWidth: 1
                    },]
                };

                if(colores_graficos[0])
                {
                    let dataset = data.datasets[0];
                    colores_graficos.push(...colores_pie_donut);
                    dataset.backgroundColor = colores_graficos;
                    dataset.borderColor = colores_graficos;
                }

                var options = {
                    plugins: {
                        datalabels: {
                            formatter: function(value, context) {
                                let sum = 0;
                                let dataArr = context.chart.data.datasets[0].data;
                                dataArr.map(data => {
                                    sum += data;
                                });
                                let percentage = (value*100 / sum).toFixed(2) + "%";
                                return percentage;
                            },
                            font: {
                                weight: 'bold',
                            },
                            color: 'white',
                        },
                    },
                    responsive: true,
                    title: false,
                    legend: {
                        display: true,
                        position: "right",
                        labels: {
                            fontColor: "#333",
                            fontSize: 16
                        }
                    },
                    scales: {
                        yAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                                display: false,
                            },
                            ticks: {
                                min: 0,
                                display: false,
                            }
                        }]
                    },
                    onResize: function(chart, size) {
                        let showLegend = (size.width < 450) ? false : true;
                        let sizeLegend = (size.width > 450) ? 16 : size.width/28.125;

                        chart.options.legend.display = showLegend;
                        chart.options.legend.labels.font_size = sizeLegend;
                    },
                };

                var chart = new self.ChartLib(self.$el.find("." + indiceOriginal)[0], {
                    type: "doughnut",
                    data: data,
                    plugins: [ChartDataLabels],
                    options: options,
                });

                if(chart.width < 450)
                {
                    chart.options.legend.display = false;
                }
                chart.update();

                var rpc_temp =  self._rpc_groupby(argumentos).then(function(con_acceso) {
                    self.reglas_acceso[indice] = filtrar_callback_con_acceso_filtrado(filtered_callbacks,filtrar_callback(con_acceso, true, "doughnut"),false);
                });

                self.charts[indice] = [chart, valores_de_etiquetas_originales];

                return rpc_temp;
            });

    });
},

grafico_pie:function(){
    var self = this;
    var contenedoresPie = self.$el.find('.container-pie');
    contenedoresPie.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
        }

        let colores_graficos = actual.colores_graficos;
        
        self._sudo_rpc_groupby(argumentos).then(function (callbacks) {

            var filtered_callbacks = filtrar_callback(callbacks, true, "pie");
            let valores_de_etiquetas_originales = extraer_labels_originales(callbacks);
            
            var data = {
                labels : filtered_callbacks[1],
                datasets: [{
                        label: "", /////Inutil ////////////////////////////////////////////
                        data: filtered_callbacks[0],
                        backgroundColor: colores_pie_donut,
                        borderColor: colores_pie_donut,
                        borderWidth: 1
                    },]
                };

            if(colores_graficos[0])
            {
                let dataset = data.datasets[0];
                colores_graficos.push(...colores_pie_donut);
                dataset.backgroundColor = colores_graficos;
                dataset.borderColor = colores_graficos;
            }

                var options = {
                    plugins: {
                        datalabels: {
                            formatter: function(value, context) {
                                let sum = 0;
                                let dataArr = context.chart.data.datasets[0].data;
                                dataArr.map(data => {
                                    sum += data;
                                });
                                let percentage = (value*100 / sum).toFixed(2) + "%";
                                return percentage;
                            },
                            font: {
                                weight: 'bold',
                            },
                            color: 'white',
                        },
                    },
                    responsive: true,
                    title: false,
                    legend: {
                        display: true,
                        position: "right",
                        labels: {
                            fontColor: "#333",
                            fontSize: 16
                        }
                    },
                    scales: {
                        yAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                                display: false,
                            },
                            ticks: {
                                min: 0,
                                display: false,
                            }
                        }]
                    },
                    onResize: function(chart, size) {
                        let showLegend = (size.width < 450) ? false : true;
                        let sizeLegend = (size.width > 450) ? 16 : size.width/28.125;

                        chart.options.legend.display = showLegend;
                        chart.options.legend.labels.font_size = sizeLegend;
                    },
                };

                var chart = new self.ChartLib(self.$el.find("." + indiceOriginal)[0], {
                    type: "pie",
                    data: data,
                    plugins: [ChartDataLabels],
                    options: options,
                });

                if(chart.width < 450)
                {
                    chart.options.legend.display = false;
                }
                chart.update();

                var rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                    self.reglas_acceso[indice] = filtrar_callback_con_acceso_filtrado(filtered_callbacks,filtrar_callback(con_acceso, true, "pie"),false);
                });

                self.charts[indice] = [chart, valores_de_etiquetas_originales];

                return rpc_temp;
            });

    });
},

_grafico_bar_groupBy_double:function(self, indice, indiceOriginal, actual, datos_filtrados, argumentos, colores_graficos) {
    self._sudo_rpc_groupby_double(argumentos).then(function (callbacks) {
                var etiqueta = actual.nombre_serie; 
                
                var filtered_callbacks = filtrar_callback_groupby_double(callbacks, datos_filtrados);
                let valores_de_etiquetas_originales = extraer_labels_originales(callbacks);

                let type = "bar";
                if(!actual.es_barra_vertical){
                    type = "horizontalBar";
                }

                let external_labels = [];
                let series_labels = [];
                let arr_values = {}

                Object.keys(filtered_callbacks).forEach(function(key,index) {
                    external_labels.push(key);
                    Object.keys(filtered_callbacks[key]).forEach(function(key2) {
                        if(!arr_values[key2])
                        {
                            arr_values[key2] = new Array(Object.keys(filtered_callbacks).length).fill(null);
                            series_labels.push(key2);
                        }
                        arr_values[key2][index] = filtered_callbacks[key][key2];
                    });
                });

                let datasets_arr = [];

                for (var i = 0; i < series_labels.length; i++) {
                    let dataset_item =  {
                                label: series_labels[i], // Parámetro ///////////////////////////////////////////////////////////////////////
                                data: arr_values[series_labels[i]],
                                backgroundColor: '#66aecf',
                                borderColor: '#66aecf',
                                barPercentage: 0.5,
                                barThickness: 6,
                                maxBarThickness: 8,
                                minBarLength: 0,
                                borderWidth: 1, // Specify bar border width
                                type: type, // Set this data to a line chart
                                fill: false
                            };
                    datasets_arr.push(dataset_item);
                }

                var data = {
                    labels : external_labels,
                    datasets: datasets_arr};

                        if(colores_graficos[0])
                        {
                            for (var i = 0; i < data.datasets.length; i++) {
                                let dataset = data.datasets[i];
                                if(colores_graficos[i])
                                {
                                    dataset.backgroundColor = colores_graficos[i];
                                    dataset.borderColor = colores_graficos[i];
                                }
                                else
                                {
                                    dataset.backgroundColor = colores_graficos[0]; 
                                    dataset.borderColor = colores_graficos[0];
                                }
                            }
                        }

                        let valores = [];

                        for (var i = 0; i < data.datasets.length; i++) {
                            valores.push(...data.datasets[i].data);
                        }

                        let valor_max = Math.max(...valores);
                        valor_max = valor_max + valor_max / 5;

                        var options = {
                            plugins: {
                                datalabels: {
                                    anchor: 'end',
                                    align: 'top',
                                    offset: 0,
                                    font: {
                                        weight: 'bold',
                                    },
                                    color: 'black',
                                },
                            },
                            scales: {
                                xAxes: [{
                                    scaleLabel: {
                                        fontSize: actual.font_size,
                                        display: true,
                                        labelString: actual.nombre_eje_x,
                                    },
                                }],
                                yAxes: [{
                                    scaleLabel: {
                                        fontSize: actual.font_size,
                                        display: true,
                                        labelString: actual.nombre_eje_y,
                                    },
                                    ticks: {
                                        max: valor_max,
                                        beginAtZero: true,
                                    },
                                }],
                            },
                            responsive: true, // Instruct chart js to respond nicely.
                            chartArea: {
                                backgroundColor: actual.color_background_grafico,
                            },
                            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        };

                        var chart = new self.ChartLib(self.$el.find("." + indiceOriginal)[0], {
                            type: type,
                            data: data,
                            plugins: [ChartDataLabels],
                            options: options,
                        });

                        var rpc_temp = self._rpc_groupby_double(argumentos).then(function(con_acceso) {
                            self.reglas_acceso[indice] = extraer_labels_originales_con_valor_acceso_double(callbacks,con_acceso,datos_filtrados);
                        });

                        self.charts[indice] = [chart, valores_de_etiquetas_originales];

                        return rpc_temp;
                        });
},

_grafico_bar_groupBy:function() {
    var self = this;
    var contenedoresBar = self.$el.find('.container-bar.d-groupBy');
    contenedoresBar.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);
        
        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
        }

        var colores_graficos = actual.colores_graficos;

        if(actual.agrupar_extra_nombre){
            self._grafico_bar_groupBy_double(self, indice, indiceOriginal, actual, datos_filtrados, argumentos, colores_graficos);
        }
        else{
            self._sudo_rpc_groupby(argumentos).then(function (callbacks) {
                var etiqueta = actual.nombre_serie; 
                var filtered_callbacks = filtrar_callback(callbacks, true, "bar");
                let valores_de_etiquetas_originales = extraer_labels_originales(callbacks);

                let type = "bar"; 
                if(!actual.es_barra_vertical){
                    type = "horizontalBar";
                }

                var data = {
                    labels : filtered_callbacks[1],
                    datasets: [{
                                label: etiqueta, // Parámetro ///////////////////////////////////////////////////////////////////////
                                data: filtered_callbacks[0],
                                backgroundColor: '#66aecf',
                                    borderColor: '#66aecf',
                                    barPercentage: 0.5,
                                    barThickness: 6,
                                    maxBarThickness: 8,
                                    minBarLength: 0,
                                    borderWidth: 1, // Specify bar border width
                                    type: type, // Set this data to a line chart
                                    fill: false
                                }]
                            };

                            if(colores_graficos[0])
                            {
                                for (var i = 0; i < data.datasets.length; i++) {
                                    let dataset = data.datasets[i];
                                    if(colores_graficos[i])
                                    {
                                        dataset.backgroundColor = colores_graficos[i];
                                        dataset.borderColor = colores_graficos[i];
                                    }
                                    else
                                    {
                                       dataset.backgroundColor = colores_graficos[0]; 
                                       dataset.borderColor = colores_graficos[0];
                                    }
                                }
                            }

                            let valores = [];

                            for (var i = 0; i < data.datasets.length; i++) {
                                valores.push(...data.datasets[i].data);
                            }

                            let valor_max = Math.max(...valores);
                            valor_max = valor_max + valor_max / 5;

                            var options = {
                                plugins: {
                                    datalabels: {
                                        anchor: 'end',
                                        align: 'top',
                                        offset: 0,
                                        font: {
                                            weight: 'bold',
                                        },
                                        color: 'black',
                                    },
                                },
                                scales: {
                                    xAxes: [{
                                        scaleLabel: {
                                            fontSize: actual.font_size,
                                            display: true,
                                            labelString: actual.nombre_eje_x,
                                        },
                                    }],
                                    yAxes: [{
                                        scaleLabel: {
                                            fontSize: actual.font_size,
                                            display: true,
                                            labelString: actual.nombre_eje_y,
                                        },
                                        ticks: {
                                            max: valor_max,
                                            beginAtZero: true,
                                        },
                                    }],
                                },
                                responsive: true, // Instruct chart js to respond nicely.
                                chartArea: {
                                    backgroundColor: actual.color_background_grafico,
                                },
                                maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                            };

                            var chart = new self.ChartLib(self.$el.find("." + indiceOriginal)[0], {
                                type: type,
                                data: data,
                                plugins: [ChartDataLabels],
                                options: options,
                            });

                            var rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                                self.reglas_acceso[indice] = extraer_labels_originales_con_valor_acceso(callbacks,con_acceso);
                            });

                            self.charts[indice] = [chart, valores_de_etiquetas_originales];

                            return rpc_temp;
                            });

        }

        }); 
},

_grafico_bar_value:function() {
    var self = this;
    var contenedoresBar = self.$el.find('.container-bar.d-value');
    contenedoresBar.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);
        
        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
            values: datos_filtrados.agrupar.concat(datos_filtrados.valores),
        }

        let colores_graficos = actual.colores_graficos;
        
        self._sudo_rpc_groupby(argumentos).then(function (callbacks) {
            return self._sudo_rpc_searchRead(argumentos).then(function (callbacks_dos) {

                    var etiqueta = actual.nombre_serie;
                    var filtered_callbacks = filtrar_callback(callbacks_dos, false, "bar", datos_filtrados);
                    let valores_de_etiquetas_originales = extraer_labels_originales_con_valor(callbacks);
                    
                    let type = "bar"; 
                    if(!actual.es_barra_vertical){
                        type = "horizontalBar";
                    }

                    let datasets = [];
                    let labels = filtered_callbacks[filtered_callbacks.length - 1];

                    for (var i = 0; i < filtered_callbacks.length - 1; i++) {
                        let temp_obj = {
                            data: filtered_callbacks[i],
                            backgroundColor: '#66aecf',
                            borderColor: '#66aecf',
                            barPercentage: 0.5,
                            barThickness: 6,
                            maxBarThickness: 8,
                            minBarLength: 0,
                            borderWidth: 1, // Specify bar border width
                            type: type, // Set this data to a line chart
                            fill: false
                        }
                        if(i == 0)
                        {
                            temp_obj.label = etiqueta;
                        }
                        else
                        {
                            temp_obj.label = datos_filtrados.valores_extra_nombre_serie[i - 1];
                        }
                        datasets.push(temp_obj);
                    }

                    var data = {
                        labels : labels,
                        datasets: datasets,
                    };

                    if(colores_graficos[0])
                    {
                        for (var i = 0; i < data.datasets.length; i++) {
                            let dataset = data.datasets[i];
                            if(colores_graficos[i])
                            {
                                dataset.backgroundColor = colores_graficos[i];
                                dataset.borderColor = colores_graficos[i];
                            }
                            else
                            {
                               dataset.backgroundColor = colores_graficos[0]; 
                               dataset.borderColor = colores_graficos[0];
                            }
                        }
                    }

                    let valores = [];

                    for (var i = 0; i < data.datasets.length; i++) {
                        valores.push(...data.datasets[i].data);
                    }

                    let valor_max = Math.max(...valores);
                    valor_max = valor_max + valor_max / 5;

                    var options = {
                        plugins: {
                            datalabels: {
                                anchor: 'end',
                                align: 'top',
                                offset: 0,
                                font: {
                                    weight: 'bold',
                                },
                                color: 'black',
                            },
                        },
                        scales: {
                            xAxes: [{
                                scaleLabel: {
                                    fontSize: actual.font_size,
                                    display: true,
                                    labelString: actual.nombre_eje_x,
                                },
                            }],
                            yAxes: [{
                                scaleLabel: {
                                    fontSize: actual.font_size,
                                    display: true,
                                    labelString: actual.nombre_eje_y,
                                },
                                ticks: {
                                    max: valor_max,
                                    beginAtZero: true,
                                },
                            }],
                        },
                        responsive: true, // Instruct chart js to respond nicely.
                        chartArea: {
                            backgroundColor: actual.color_background_grafico,
                        },
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    };

                    var chart = new self.ChartLib(self.$el.find("." + indiceOriginal)[0], {
                        type: type,
                        data: data,
                        plugins: [ChartDataLabels],
                        options: options,
                    });

                    self.charts[indice] = [chart, valores_de_etiquetas_originales, datos_filtrados];

                    var rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                        self.reglas_acceso[indice] = extraer_labels_originales_con_valor_acceso(callbacks,con_acceso);
                    });

                    return rpc_temp;

                });
            });

    });
},

grafico_bar:function(){
    var self = this;
    self._grafico_bar_value();
    self._grafico_bar_groupBy();
},

_grafico_linea_value:function() {
    var self = this;
    var contenedoresLine = self.$el.find('.container-line.d-value');
    contenedoresLine.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
            values: datos_filtrados.agrupar.concat(datos_filtrados.valores),
        }

        let colores_graficos = actual.colores_graficos;

        var primero = self._sudo_rpc_groupby(argumentos).then(function (callbacks_solo_etiquetas) {
            return self._sudo_rpc_searchRead(argumentos).then(function (callbacks) {

                var etiqueta = actual.nombre_serie;
                var filtered_callbacks = filtrar_callback(callbacks, false, "line", datos_filtrados);
                let valores_de_etiquetas_originales = extraer_labels_originales_con_valor(callbacks_solo_etiquetas);
                let orden = actual.orden_valores;

                var callbacks_orden = [];

                for(let i = 0; i < filtered_callbacks[0].length; i++)
                {
                    let arr_des = [];
                    for (var j = 0; j < filtered_callbacks.length; j++) {
                        arr_des.push(filtered_callbacks[j][i]);
                    }
                    callbacks_orden.push(arr_des);
                }

                if('desc' == orden){
                    callbacks_orden.sort((a,b) => (a[0] < b[0] ? 1 : -1));
                }
                else {
                    callbacks_orden.sort((a,b) => (a[0] < b[0] ? -1 : 1));
                }

                filtered_callbacks = new Array(filtered_callbacks.length).fill(0);
                for (var i = 0; i < filtered_callbacks.length; i++) {
                    filtered_callbacks[i] = [];
                }

                for(let i = 0; i < callbacks_orden.length; i++)
                {
                    
                    for (var k = 0; k < filtered_callbacks.length; k++) {
                        filtered_callbacks[k].push(callbacks_orden[i][k]);
                    }
                }

                let datasets = [];
                    let labels = filtered_callbacks[filtered_callbacks.length - 1];

                    for (var i = 0; i < filtered_callbacks.length - 1; i++) {
                        let temp_obj = {
                            data: filtered_callbacks[i],
                            borderColor: '#66aecf',
                            type: 'line', // Set this data to a line chart
                            fill: true,
                            tension: 0.1,
                        }
                        if(i == 0)
                        {
                            temp_obj.label = etiqueta;
                        }
                        else
                        {
                            temp_obj.label = datos_filtrados.valores_extra_nombre_serie[i - 1].trim();
                        }
                        datasets.push(temp_obj);
                    }

                        var data = {
                            labels : labels,
                            datasets: datasets,
                        };

                        if(colores_graficos[0])
                        {
                            for (var i = 0; i < data.datasets.length; i++) {
                                let dataset = data.datasets[i];
                                if(colores_graficos[i])
                                {
                                    dataset.borderColor = colores_graficos[i];
                                }
                                else
                                {
                                   dataset.borderColor = colores_graficos[0];
                                }
                            }
                        }

                        let valores = [];

                        for (var i = 0; i < data.datasets.length; i++) {
                            valores.push(...data.datasets[i].data);
                        }

                        let valor_max = Math.max(...valores);
                        valor_max = valor_max + valor_max / 5;
                        
                        var options = {
                            plugins: {
                                datalabels: {
                                    anchor: 'end',
                                    align: 'top',
                                    offset: 0,
                                    font: {
                                        weight: 'bold',
                                    },
                                    color: 'black',
                                },
                            },
                            scales: {
                                xAxes: [{
                                    scaleLabel: {
                                        fontSize: actual.font_size,
                                        display: true,
                                        labelString: actual.nombre_eje_x,
                                    },
                                }],
                                yAxes: [{
                                    scaleLabel: {
                                        fontSize: actual.font_size,
                                        display: true,
                                        labelString: actual.nombre_eje_y,
                                    },
                                    ticks: {
                                        max: valor_max,
                                        beginAtZero: true,
                                    },
                                }],
                            },
                            responsive: true, // Instruct chart js to respond nicely.
                            chartArea: {
                                backgroundColor: actual.color_background_grafico,
                            },
                            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        }; 

                        var chart = new self.ChartLib(self.$el.find("." + indiceOriginal)[0], {
                            type: "line",
                            data: data,
                            plugins: [ChartDataLabels],
                            options: options,
                        });

                        self.charts[indice] = [chart, valores_de_etiquetas_originales, datos_filtrados];

                        var rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                            self.reglas_acceso[indice] = extraer_labels_originales_con_valor_acceso(callbacks_solo_etiquetas,con_acceso);
                        });

                        return rpc_temp;

                    }); 
        });

    });
},

_grafico_linea_groupBy_double:function(self, indice, indiceOriginal, actual, datos_filtrados, argumentos, colores_graficos) {
    self._sudo_rpc_groupby_double(argumentos).then(function (callbacks) {
                var etiqueta = actual.nombre_serie; 
                
                var filtered_callbacks = filtrar_callback_groupby_double(callbacks, datos_filtrados);
                let valores_de_etiquetas_originales = extraer_labels_originales(callbacks);
                let orden = actual.orden_valores;
                
                // var callbacks_orden = [];

                let external_labels = [];
                let series_labels = [];
                let arr_values = {}

                Object.keys(filtered_callbacks).forEach(function(key,index) {
                    external_labels.push(key);
                    Object.keys(filtered_callbacks[key]).forEach(function(key2) {
                        if(!arr_values[key2])
                        {
                            arr_values[key2] = new Array(Object.keys(filtered_callbacks).length).fill(0);
                            series_labels.push(key2);
                        }
                        arr_values[key2][index] = filtered_callbacks[key][key2];
                    });
                });

                let datasets_arr = [];

                for (var i = 0; i < series_labels.length; i++) {
                    let dataset_item =  {
                                label: series_labels[i], // Parámetro ///////////////////////////////////////////////////////////////////////
                                data: arr_values[series_labels[i]],
                                borderColor: '#66aecf',
                                type: 'line', // Set this data to a line chart
                                fill: true,
                                tension: 0.1,
                            };
                    datasets_arr.push(dataset_item);
                }

                var data = {
                    labels : external_labels,
                    datasets: datasets_arr};

                        if(colores_graficos[0])
                        {
                            for (var i = 0; i < data.datasets.length; i++) {
                                let dataset = data.datasets[i];
                                if(colores_graficos[i])
                                {
                                    dataset.borderColor = colores_graficos[i];
                                }
                                else
                                {
                                    dataset.borderColor = colores_graficos[0];
                                }
                            }
                        }

                        let valores = [];

                        for (var i = 0; i < data.datasets.length; i++) {
                            valores.push(...data.datasets[i].data);
                        }

                        let valor_max = Math.max(...valores);
                        valor_max = valor_max + valor_max / 5;
                        var options = {
                            plugins: {
                                datalabels: {
                                    anchor: 'end',
                                    align: 'top',
                                    offset: 0,
                                    font: {
                                        weight: 'bold',
                                    },
                                    color: 'black',
                                },
                            },
                            scales: {
                                xAxes: [{
                                    scaleLabel: {
                                        fontSize: actual.font_size,
                                        display: true,
                                        labelString: actual.nombre_eje_x,
                                    },
                                }],
                                yAxes: [{
                                    scaleLabel: {
                                        fontSize: actual.font_size,
                                        display: true,
                                        labelString: actual.nombre_eje_y,
                                    },
                                    ticks: {
                                        max: valor_max,
                                        beginAtZero: true,
                                    },
                                }],
                            },
                            responsive: true, // Instruct chart js to respond nicely.
                            chartArea: {
                                backgroundColor: actual.color_background_grafico,
                            },
                            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        };

                        var chart = new self.ChartLib(self.$el.find("." + indiceOriginal)[0], {
                            type: "line",
                            data: data,
                            plugins: [ChartDataLabels],
                            options: options,
                        });

                        var rpc_temp = self._rpc_groupby_double(argumentos).then(function(con_acceso) {
                            self.reglas_acceso[indice] = extraer_labels_originales_con_valor_acceso_double(callbacks,con_acceso,datos_filtrados);
                        });

                        self.charts[indice] = [chart, valores_de_etiquetas_originales];

                        return rpc_temp;
                        });
},

_grafico_linea_groupBy:function() {
    var self = this;
    var contenedoresLine = self.$el.find('.container-line.d-groupBy');
    contenedoresLine.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
        }

        var colores_graficos = actual.colores_graficos;

        if(actual.agrupar_extra_nombre){
            self._grafico_linea_groupBy_double(self, indice, indiceOriginal, actual, datos_filtrados, argumentos, colores_graficos);
        }
        else{
            self._sudo_rpc_groupby(argumentos).then(function (callbacks) {

                var etiqueta = actual.nombre_serie; 
                var filtered_callbacks = filtrar_callback(callbacks, true, "line");
                let valores_de_etiquetas_originales = extraer_labels_originales(callbacks);
                let orden = actual.orden_valores;

                var callbacks_orden = [];

                for(let i = 0; i < filtered_callbacks[0].length; i++)
                {
                    callbacks_orden.push([filtered_callbacks[0][i],filtered_callbacks[1][i]]);
                }

                if('desc' == orden){
                    callbacks_orden.sort((a,b) => (a[0] < b[0] ? 1 : -1));
                }
                else {
                    callbacks_orden.sort((a,b) => (a[0] < b[0] ? -1 : 1));
                }

                filtered_callbacks = [[],[]];

                for(let i = 0; i < callbacks_orden.length; i++)
                {
                    filtered_callbacks[0].push(callbacks_orden[i][0]);
                    filtered_callbacks[1].push(callbacks_orden[i][1]);
                }

                 var data = {
                        labels : filtered_callbacks[1],
                        datasets: [{
                                    label: etiqueta, // Parámetro ///////////////////////////////////////////////////////////////////////
                                    data: filtered_callbacks[0],
                                    
                                    borderColor: '#66aecf',
                                    type: 'line', // Set this data to a line chart
                                    fill: true,
                                    tension: 0.1,
                                }]
                            };

                            if(colores_graficos[0])
                            {
                                for (var i = 0; i < data.datasets.length; i++) {
                                    let dataset = data.datasets[i];
                                    if(colores_graficos[i])
                                    {
                                        dataset.borderColor = colores_graficos[i];
                                    }
                                    else
                                    {
                                       dataset.borderColor = colores_graficos[0];
                                    }
                                }
                            }

                            let valores = [];

                            for (var i = 0; i < data.datasets.length; i++) {
                                valores.push(...data.datasets[i].data);
                            }

                            let valor_max = Math.max(...valores);

                            valor_max = valor_max + valor_max / 5;
                            var options = {
                                plugins: {
                                    datalabels: {
                                        anchor: 'end',
                                        align: 'top',
                                        offset: 0,
                                        font: {
                                            weight: 'bold',
                                        },
                                        color: 'black',
                                    },
                                },
                                scales: {
                                    xAxes: [{
                                        scaleLabel: {
                                            fontSize: actual.font_size,
                                            display: true,
                                            labelString: actual.nombre_eje_x,
                                        },
                                    }],
                                    yAxes: [{
                                        scaleLabel: {
                                            fontSize: actual.font_size,
                                            display: true,
                                            labelString: actual.nombre_eje_y,
                                        },
                                        ticks: {
                                            max: valor_max,
                                            beginAtZero: true,
                                        },
                                    }],
                                },
                                responsive: true, // Instruct chart js to respond nicely.
                                chartArea: {
                                    backgroundColor: actual.color_background_grafico,
                                },
                                maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                            };

                            var chart = new self.ChartLib(self.$el.find("." + indiceOriginal)[0], {
                                type: "line",
                                data: data,
                                plugins: [ChartDataLabels],
                                options: options,
                            });

                            var rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                                self.reglas_acceso[indice] = extraer_labels_originales_con_valor_acceso(callbacks,con_acceso);
                            });

                            self.charts[indice] = [chart, valores_de_etiquetas_originales];

                            return rpc_temp;
                            });
        }
        
        }); 
},

grafico_linea:function(){
    var self = this;
    self._grafico_linea_value();
    self._grafico_linea_groupBy();
},

tabla_heatmap: function() {
    var self = this;
    self.heatmapsNombres = [];
    var contenedoresHeatmap = self.$el.find('.heatmap-table');
    contenedoresHeatmap.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
            values: datos_filtrados.agrupar.concat(datos_filtrados.valores),
        }

        var primero = self._sudo_rpc_groupby(argumentos).then(function (callbacks_solo_etiquetas) {
            return self._sudo_rpc_searchRead(argumentos).then(function (callbacks) {

                        //ordenar los valores

                        let ordenado = ordenar_callback(callbacks, datos_filtrados, actual.orden_valores);

                        let valores_de_etiquetas_originales = extraer_labels_originales_con_valor(callbacks_solo_etiquetas);

                        if($('.' + indiceOriginal + ' .table-encabezados')[0]){
                            let colorFondo = actual.color_background;
                            let colorFinal = '#';
                            for (var i = 1; i < colorFondo.length; i++) {
                                let numero = colorFondo.charCodeAt(i);
                                if(numero != 48)
                                {
                                    if(numero == 65)
                                    {
                                        numero = 57;
                                    }
                                    else{
                                        numero -= 1;
                                    }
                                }
                                colorFinal += String.fromCharCode(numero);
                            }
                            $('.' + indiceOriginal + ' .table-encabezados').append('<tr style="background-color: ' + colorFinal +'; color: ' + actual.color_encabezados + ';" class="tr-header-'+ 0 + '"></tr>');
                            $('.' + indiceOriginal + ' .table-encabezados .tr-header-' + 0).append('<th>'+ actual.encabezado_etiquetas + '</th>');
                            $('.' + indiceOriginal + ' .table-encabezados .tr-header-' + 0).append('<th>'+ actual.nombre_serie + '</th>');
                            if (datos_filtrados.valores_extra_nombre_serie[0]) {
                                for (var i = 0; i < datos_filtrados.valores_extra_nombre_serie.length; i++) {
                                    $('.' + indiceOriginal + ' .table-encabezados .tr-header-' + 0).append('<th>'+ datos_filtrados.valores_extra_nombre_serie[i] + '</th>');
                                }
                            }
                        }

                        //solo 10 valores

                        if (actual.limite_tabla > 0) {
                            for (var i = 0; i < actual.limite_tabla && i < ordenado.length; i++) {

                                let labelHeat = ordenado[i][datos_filtrados.agrupar[0]];

                                let temp = labelHeat;
                                let once = false;

                                if (typeof(labelHeat) == 'object') {
                                    Object.keys(labelHeat).find(key => {
                                        if(typeof(labelHeat[key] != 'number' && !once))
                                        {
                                            if(typeof(labelHeat[key]) == 'string'){
                                                temp = labelHeat[key];
                                                once = true;
                                            }
                                            else{
                                                if(typeof(labelHeat) == 'boolean'){
                                                    if (!labelHeat) {
                                                        temp = "Desconocido";
                                                    }
                                                    else{
                                                        temp = "Es " + datos_filtrados.agrupar[0];
                                                    }
                                                    once = true;
                                                }
                                            }   
                                        }
                                    });
                                }else{
                                    if (typeof(labelHeat)  == 'boolean') {
                                        if(typeof(labelHeat) == 'boolean'){
                                            if (!labelHeat) {
                                                temp = "Desconocido";
                                            }
                                            else{
                                                temp = "Es " + datos_filtrados.agrupar[0];
                                            }
                                        }
                                    }
                                }

                                labelHeat = temp;

                                if($('.' + indiceOriginal + ' .heatmap-table-body')[0]){
                                    $('.' + indiceOriginal + ' .heatmap-table-body').append('<tr style="color: ' + actual.color_etiquetas + ';" class="tr-'+ i + '"></tr>');
                                    $('.' + indiceOriginal + ' .heatmap-table-body .tr-' + i).append('<td style="color: ' + actual.color_etiquetas + ';">' + labelHeat + '</td>');
                                    for (var j = 0; j < datos_filtrados.valores.length; j++) {
                                        let dato = ordenado[i][datos_filtrados.valores[j]];

                                        if(typeof(dato) == 'object')
                                        {
                                            dato = dato[1];
                                        }
                                        if(typeof(dato) == 'string')
                                        {
                                            dato = dato.trim();
                                        }
                                        $('.' + indiceOriginal + ' .heatmap-table-body .tr-' + i).append('<td style="color: ' + actual.color_valor + ';">' + dato + '</td>');
                                    }
                                }
                            }
                        }
                        else{
                            for (var i = 0; i < ordenado.length; i++) {

                                let labelHeat = ordenado[i][datos_filtrados.agrupar[0]];

                                let temp = labelHeat;
                                let once = false;

                                if (typeof(labelHeat) == 'object') {
                                    Object.keys(labelHeat).find(key => {
                                        if(typeof(labelHeat[key] != 'number' && !once))
                                        {
                                            if(typeof(labelHeat[key]) == 'string'){
                                                temp = labelHeat[key];
                                                once = true;
                                            }
                                            else{
                                                if(typeof(labelHeat) == 'boolean'){
                                                    if (!labelHeat) {
                                                        temp = "Desconocido";
                                                    }
                                                    else{
                                                        temp = "Es " + datos_filtrados.agrupar[0];
                                                    }
                                                    once = true;
                                                }
                                            }   
                                        }
                                    });
                                }else{
                                    if (typeof(labelHeat)  == 'boolean') {
                                        if(typeof(labelHeat) == 'boolean'){
                                            if (!labelHeat) {
                                                temp = "Desconocido";
                                            }
                                            else{
                                                temp = "Es " + datos_filtrados.agrupar[0];
                                            }
                                        }
                                    }
                                }

                                labelHeat = temp;

                                if($('.' + indiceOriginal + ' .heatmap-table-body')[0]){
                                    $('.' + indiceOriginal + ' .heatmap-table-body').append('<tr style="color: ' + actual.color_etiquetas + ';" class="tr-'+ i + '"></tr>');
                                    $('.' + indiceOriginal + ' .heatmap-table-body .tr-' + i).append('<td style="color: ' + actual.color_etiquetas + ';">' + labelHeat + '</td>');
                                    for (var j = 0; j < datos_filtrados.valores.length; j++) {
                                        let dato = ordenado[i][datos_filtrados.valores[j]];

                                        if(typeof(dato) == 'object')
                                        {
                                            dato = dato[1];
                                        }
                                        if(typeof(dato) == 'string')
                                        {
                                            dato = dato.trim();
                                        }
                                        $('.' + indiceOriginal + ' .heatmap-table-body .tr-' + i).append('<td style="color: ' + actual.color_valor + ';">' + dato + '</td>');
                                    }
                                }
                            }
                        }

                        self.heatmapsNombres.push(indiceOriginal);
                        self.charts[indice] = [datos_filtrados, valores_de_etiquetas_originales];

                        var rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                            self.reglas_acceso[indice] = filtrar_callback_con_acceso_filtrado(filtrar_callback(callbacks_solo_etiquetas, true, "heat", datos_filtrados),filtrar_callback(con_acceso, true, "heat", datos_filtrados),false);
                        });

                    });
});

});
},

tabla_normal: function() {
    var self = this;
    var contenedoresTablemap = self.$el.find('.normal-table');
    contenedoresTablemap.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
            values: datos_filtrados.agrupar.concat(datos_filtrados.valores),
        }

        var primero = self._sudo_rpc_groupby(argumentos).then(function (callbacks_solo_etiquetas) {
            return self._sudo_rpc_searchRead(argumentos).then(function (callbacks) {

                        //ordenar los valores

                        let ordenado = ordenar_callback(callbacks, datos_filtrados, actual.orden_valores);

                        let valores_de_etiquetas_originales = extraer_labels_originales_con_valor(callbacks_solo_etiquetas);

                        if($('.' + indiceOriginal + ' .table-encabezados')[0]){
                            let colorFondo = actual.color_background_encabezados;
                            $('.' + indiceOriginal + ' .table-encabezados').append('<tr style="background-color: ' + colorFondo +'; color: ' + actual.color_encabezados + ';" class="tr-header-'+ 0 + '"></tr>');
                            $('.' + indiceOriginal + ' .table-encabezados .tr-header-' + 0).append('<th style="background-color: ' + colorFondo +';">'+ actual.encabezado_etiquetas + '</th>');
                            $('.' + indiceOriginal + ' .table-encabezados .tr-header-' + 0).append('<th style="background-color: ' + colorFondo +';">'+ actual.nombre_serie + '</th>');
                            if (datos_filtrados.valores_extra_nombre_serie[0]) {
                                for (var i = 0; i < datos_filtrados.valores_extra_nombre_serie.length; i++) {
                                    $('.' + indiceOriginal + ' .table-encabezados .tr-header-' + 0).append('<th style="background-color: ' + colorFondo +';">'+ datos_filtrados.valores_extra_nombre_serie[i] + '</th>');
                                }
                            }
                        }

                        //solo 10 valores

                        if(actual.limite_tabla > 0)
                        {
                            for (var i = 0; i < actual.limite_tabla && i < ordenado.length; i++) {

                                let labelTable = ordenado[i][datos_filtrados.agrupar[0]];

                                let temp = labelTable;
                                let once = false;

                                if (typeof(labelTable) == 'object') {
                                    Object.keys(labelTable).find(key => {
                                        if(typeof(labelTable[key] != 'number' && !once))
                                        {
                                            if(typeof(labelTable[key]) == 'string'){
                                                temp = labelTable[key];
                                                once = true;
                                            }
                                            else{
                                                if(typeof(labelTable) == 'boolean'){
                                                    if (!labelTable) {
                                                        temp = "Desconocido";
                                                    }
                                                    else{
                                                        temp = "Es " + datos_filtrados.agrupar[0];
                                                    }
                                                    once = true;
                                                }
                                            }   
                                        }
                                    });
                                }else{
                                    if (typeof(labelTable)  == 'boolean') {
                                        if(typeof(labelTable) == 'boolean'){
                                            if (!labelTable) {
                                                temp = "Desconocido";
                                            }
                                            else{
                                                temp = "Es " + datos_filtrados.agrupar[0];
                                            }
                                        }
                                    }
                                }

                                labelTable = temp;

                                if($('.' + indiceOriginal + ' .normal-table-body')[0]){
                                    $('.' + indiceOriginal + ' .normal-table-body').append('<tr style="background-color: ' + actual.color_background_etiquetas +'; color: ' + actual.color_etiquetas + ';" class="tr-'+ i + '"></tr>');
                                    $('.' + indiceOriginal + ' .normal-table-body .tr-' + i).append('<td style="background-color: ' + actual.color_background_etiquetas +'; color: ' + actual.color_etiquetas + ';">' + labelTable + '</td>');
                                    for (var j = 0; j < datos_filtrados.valores.length; j++) {
                                        let dato = ordenado[i][datos_filtrados.valores[j]];

                                        if(typeof(dato) == 'object')
                                        {
                                            dato = dato[1];
                                        }
                                        if(typeof(dato) == 'string')
                                        {
                                            dato = dato.trim();
                                        }
                                        $('.' + indiceOriginal + ' .normal-table-body .tr-' + i).append('<td style="background-color: ' + actual.color_background_valor +'; color: ' + actual.color_valor + ';" class="o_pivot_cell_value text-right font-weight-bold">' + dato + '</td>');
                                    }
                                }
                            }    
                        }

                        else
                        {
                            for (var i = 0; i < ordenado.length; i++) {

                                let labelTable = ordenado[i][datos_filtrados.agrupar[0]];

                                let temp = labelTable;
                                let once = false;

                                if (typeof(labelTable) == 'object') {
                                    Object.keys(labelTable).find(key => {
                                        if(typeof(labelTable[key] != 'number' && !once))
                                        {
                                            if(typeof(labelTable[key]) == 'string'){
                                                temp = labelTable[key];
                                                once = true;
                                            }
                                            else{
                                                if(typeof(labelTable) == 'boolean'){
                                                    if (!labelTable) {
                                                        temp = "Desconocido";
                                                    }
                                                    else{
                                                        temp = "Es " + datos_filtrados.agrupar[0];
                                                    }
                                                    once = true;
                                                }
                                            }   
                                        }
                                    });
                                }else{
                                    if (typeof(labelTable)  == 'boolean') {
                                        if(typeof(labelTable) == 'boolean'){
                                            if (!labelTable) {
                                                temp = "Desconocido";
                                            }
                                            else{
                                                temp = "Es " + datos_filtrados.agrupar[0];
                                            }
                                        }
                                    }
                                }

                                labelTable = temp;

                                if($('.' + indiceOriginal + ' .normal-table-body')[0]){
                                    $('.' + indiceOriginal + ' .normal-table-body').append('<tr style="background-color: ' + actual.color_background_etiquetas +'; color: ' + actual.color_etiquetas + ';" class="tr-'+ i + '"></tr>');
                                    $('.' + indiceOriginal + ' .normal-table-body .tr-' + i).append('<td style="background-color: ' + actual.color_background_etiquetas +'; color: ' + actual.color_etiquetas + ';">' + labelTable + '</td>');
                                    for (var j = 0; j < datos_filtrados.valores.length; j++) {
                                        let dato = ordenado[i][datos_filtrados.valores[j]];

                                        if(typeof(dato) == 'object')
                                        {
                                            dato = dato[1];
                                        }
                                        if(typeof(dato) == 'string')
                                        {
                                            dato = dato.trim();
                                        }
                                        $('.' + indiceOriginal + ' .normal-table-body .tr-' + i).append('<td style="background-color: ' + actual.color_background_valor +'; color: ' + actual.color_valor + ';" class="o_pivot_cell_value text-right font-weight-bold">' + dato + '</td>');
                                    }
                                }
                            }
                        }
                        
                        

                        self.charts[indice] = [datos_filtrados, valores_de_etiquetas_originales];

                        var rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                            self.reglas_acceso[indice] = filtrar_callback_con_acceso_filtrado(filtrar_callback(callbacks_solo_etiquetas, true, "table", datos_filtrados),filtrar_callback(con_acceso, true, "table", datos_filtrados),false);
                        });

                    });
});

});
},

tabla_top_10: function() {
    var self = this;
    var contenedoresTop10 = self.$el.find('.item-container');
    contenedoresTop10.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
            values: datos_filtrados.agrupar.concat(datos_filtrados.valores),
        }

        var primero = self._sudo_rpc_groupby(argumentos).then(function (callbacks_solo_etiquetas) {
            return self._sudo_rpc_searchRead(argumentos).then(function (callbacks) {

                var ordenado = ordenar_callback(callbacks, datos_filtrados, actual.orden_valores);

                let valores_de_etiquetas_originales = extraer_labels_originales_con_valor(callbacks_solo_etiquetas);

                if (actual.limite_tabla > 0) {
                    for (var i = 0; i < actual.limite_tabla && i < ordenado.length; i++) {

                        let labelTop = ordenado[i][datos_filtrados.agrupar[0]];

                        let temp = labelTop;
                        let once = false;

                        if (typeof(labelTop) == 'object') {
                            Object.keys(labelTop).find(key => {
                                if(typeof(labelTop[key] != 'number' && !once))
                                {
                                    if(typeof(labelTop[key]) == 'string'){
                                        temp = labelTop[key];
                                        once = true;
                                    }
                                    else{
                                        if(typeof(labelTop) == 'boolean'){
                                            if (!labelTop) {
                                                temp = "Desconocido";
                                            }
                                            else{
                                                temp = "Es " + datos_filtrados.agrupar[0];
                                            }
                                            once = true;
                                        }
                                    }   
                                }
                            });
                        }else{
                            if (typeof(labelTop)  == 'boolean') {
                                if(typeof(labelTop) == 'boolean'){
                                    if (!labelTop) {
                                        temp = "Desconocido";
                                    }
                                    else{
                                        temp = "Es " + datos_filtrados.agrupar[0];
                                    }
                                }
                            }
                        }

                        labelTop = temp;

                        if($('.' + indiceOriginal + '.item-container')[0]){
                            let texto_valor = ordenado[i][datos_filtrados.valores[0]];
                            if(actual.tarjeta_extra){
                                if(actual.tarjeta_extra_posicion == 'prefijo')
                                {
                                    texto_valor = actual.tarjeta_extra + " " + texto_valor; 
                                }
                                else
                                {
                                    texto_valor = texto_valor + " " + actual.tarjeta_extra; 
                                }
                            }
                            $('.' + indiceOriginal).append('<div class="grafico-body-'+ (i + 1) + ' item-header"></div>');
                            $('.' + indiceOriginal + ' .grafico-body-' + (i + 1)).append('<div style="background-color: ' + actual.color_background_icono + '; color: ' + actual.color_icono + ';" class="count-container-' + (i + 1) +' count-container"></div>');
                            $('.' + indiceOriginal + ' .count-container-' + (i + 1)).append('<span>' + (i + 1) +'</span>');
                            $('.' + indiceOriginal + ' .grafico-body-' + (i + 1)).append('<div class="item-title pl-3 data-container-' + (i + 1) +'"></div>');
                            $('.' + indiceOriginal + ' .data-container-' + (i + 1)).append('<h3 style="color: ' + actual.color_valor +';">' + labelTop + ': ' + texto_valor + '</h3>');
                            $('.' + indiceOriginal + ' .data-container-' + (i + 1)).append('<div class="item-content content-container-' + (i + 1) + '"></div>');
                            $('.' + indiceOriginal + ' .content-container-' + (i + 1)).append('<ul></ul>');
                            $('.' + indiceOriginal + ' .content-container-' + (i + 1) + ' ul').append('<li></li>');
                            $('.' + indiceOriginal + ' .content-container-' + (i + 1) + ' li').append('<span style="color: ' + actual.color_top_subtitulo + ';">' + actual.nombre_serie + '</span>');
                        }
                    }
                }
                else{
                    for (var i = 0; i < ordenado.length; i++) {

                        let labelTop = ordenado[i][datos_filtrados.agrupar[0]];

                        let temp = labelTop;
                        let once = false;

                        if (typeof(labelTop) == 'object') {
                            Object.keys(labelTop).find(key => {
                                if(typeof(labelTop[key] != 'number' && !once))
                                {
                                    if(typeof(labelTop[key]) == 'string'){
                                        temp = labelTop[key];
                                        once = true;
                                    }
                                    else{
                                        if(typeof(labelTop) == 'boolean'){
                                            if (!labelTop) {
                                                temp = "Desconocido";
                                            }
                                            else{
                                                temp = "Es " + datos_filtrados.agrupar[0];
                                            }
                                            once = true;
                                        }
                                    }   
                                }
                            });
                        }else{
                            if (typeof(labelTop)  == 'boolean') {
                                if(typeof(labelTop) == 'boolean'){
                                    if (!labelTop) {
                                        temp = "Desconocido";
                                    }
                                    else{
                                        temp = "Es " + datos_filtrados.agrupar[0];
                                    }
                                }
                            }
                        }

                        labelTop = temp;

                        if($('.' + indiceOriginal + '.item-container')[0]){
                            let texto_valor = ordenado[i][datos_filtrados.valores[0]];
                            if(actual.tarjeta_extra){
                                if(actual.tarjeta_extra_posicion == 'prefijo')
                                {
                                    texto_valor = actual.tarjeta_extra + " " + texto_valor; 
                                }
                                else
                                {
                                    texto_valor = texto_valor + " " + actual.tarjeta_extra; 
                                }
                            }
                            $('.' + indiceOriginal).append('<div class="grafico-body-'+ (i + 1) + ' item-header"></div>');
                            $('.' + indiceOriginal + ' .grafico-body-' + (i + 1)).append('<div style="background-color: ' + actual.color_background_icono + '; color: ' + actual.color_icono + ';" class="count-container-' + (i + 1) +' count-container"></div>');
                            $('.' + indiceOriginal + ' .count-container-' + (i + 1)).append('<span>' + (i + 1) +'</span>');
                            $('.' + indiceOriginal + ' .grafico-body-' + (i + 1)).append('<div class="item-title pl-3 data-container-' + (i + 1) +'"></div>');
                            $('.' + indiceOriginal + ' .data-container-' + (i + 1)).append('<h3 style="color: ' + actual.color_valor +';">' + labelTop + ': ' + texto_valor + '</h3>');
                            $('.' + indiceOriginal + ' .data-container-' + (i + 1)).append('<div class="item-content content-container-' + (i + 1) + '"></div>');
                            $('.' + indiceOriginal + ' .content-container-' + (i + 1)).append('<ul></ul>');
                            $('.' + indiceOriginal + ' .content-container-' + (i + 1) + ' ul').append('<li></li>');
                            $('.' + indiceOriginal + ' .content-container-' + (i + 1) + ' li').append('<span style="color: ' + actual.color_top_subtitulo + ';">' + actual.nombre_serie + '</span>');
                        }
                    }
                }

                self.charts[indice] = [datos_filtrados, valores_de_etiquetas_originales];

                var rpc_temp = self._rpc_groupby(argumentos).then(function(con_acceso) {
                    self.reglas_acceso[indice] = filtrar_callback_con_acceso_filtrado(filtrar_callback(callbacks_solo_etiquetas, true, "heat", datos_filtrados),filtrar_callback(con_acceso, true, "heat", datos_filtrados),false);
                });
            });
        });

    });
},

tarjetas: function() {
    var self = this;
    var contenedoresTarjetas = self.$el.find('.dashboard-card');
    contenedoresTarjetas.each(function (index){
        var indiceOriginal = this.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        this.classList.add("j-" + actual.tarjeta_orientacion);

        var datos_filtrados = filtrar_datos(actual);

        var argumentos = {
            model: actual.modelo_nombre,
            fields: datos_filtrados.agrupar,
            domain: datos_filtrados.dominio,
            groupBy: datos_filtrados.agrupar,
        }

        var primero = self._sudo_rpc_read(argumentos).then(function (results) {
            let texto_valor = results.length;

            if(actual.tarjeta_extra){
                if(actual.tarjeta_extra_posicion == 'prefijo')
                {
                    texto_valor = actual.tarjeta_extra + " " + texto_valor; 
                }
                else
                {
                    texto_valor = texto_valor + " " + actual.tarjeta_extra; 
                }
            }
            if($('.' + indiceOriginal + '.tablero-card')[0]){
                $('.' + indiceOriginal + '.tablero-card').append('<span>' + texto_valor + '</span>');
            }
            return self._rpc_search(argumentos).then(function(con_acceso) {
                self.reglas_acceso[indice] = [con_acceso.length, (con_acceso.length!=results.length), datos_faltantes_tarjetas(results,con_acceso)];
            });
        });
    });

},

doc_ready: function() {
    var self = this;
    $(document).on("mousemove", ".dashboard_main_section", function(event){
        self.heatmapsNombres.forEach(function(heatmapNombre) {
            if($('.' + heatmapNombre)[0]){
                let indice = filtrar_indice(heatmapNombre);
                let orden = false;
                if(self.graficos_nuevos[indice].orden_valores == 'desc')
                {
                    orden = true;
                }
                $('.' + heatmapNombre).columnHeatmap({
                    columns: [1],
                    inverse:orden,
                });                       
            }
        });
    });

    $(document).on("click", "button.imprimir_button", function(event){

        if(self.dashboard_element)
        {
            let opt = {
                pagebreak: { mode: 'avoid-all'},
                jsPDF: { unit:"px", hotfixes: ["px_scaling"], orientation: "p", format: [self.height_dashboard_print,self.width_dashboard_print]},
            }

            html2pdf().set(opt).from(self.dashboard_element).save(self.title);
        }
        
    });

    $(document).off("click", ".dashboard-card");
    $(document).on("click", ".dashboard-card",function(event){
        event.stopPropagation();
        event.preventDefault();
        var indiceOriginal = event.currentTarget.classList[0];
        var indice = filtrar_indice(indiceOriginal);
        var actual = self.graficos_nuevos[indice];

        var datos_filtrados = filtrar_datos(actual);
        var reglas_acceso = self.reglas_acceso[indice];

        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        var modelo = actual.modelo_nombre;
        if(reglas_acceso[0] > 0)
        {
            let nombre_accion = actual.name + " ";
            if(reglas_acceso[1])
            {
                nombre_accion = nombre_accion + reglas_acceso[2];
            }
            self.do_action({
                name: nombre_accion,
                type: 'ir.actions.act_window',
                res_model: modelo,
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                target: 'current',
                domain: datos_filtrados.dominio,
            }, options);
        }else{
            self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
        }
    });

            //donut, pie, barra
            $(document).off("click", ".container-doughnut, .container-pie");
            $(document).on("click", ".container-doughnut, .container-pie", function(event) {
                event.stopPropagation();
                event.preventDefault();
                var indiceOriginal = event.currentTarget.classList[0];
                var indice = filtrar_indice(indiceOriginal);
                var actual = self.graficos_nuevos[indice];

                let elementAtClick = self.charts[indice][0].getElementsAtEvent(event)[0];

                if(elementAtClick)
                {
                    let index = elementAtClick._index;
                    let dominio = self.charts[indice][1][index];

                    var options = {
                        on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                    };
                    var modelo = self.graficos_nuevos[indice].modelo_nombre;
                    let reglas_acceso = self.reglas_acceso[indice];
                    
                    if(reglas_acceso[index]){
                        let nombre_accion = actual.name + " ";
                        if(reglas_acceso[index][1])
                        {
                            nombre_accion = nombre_accion + reglas_acceso[index][2];
                        }
                        self.do_action({
                            name: nombre_accion,
                            type: 'ir.actions.act_window',
                            res_model: modelo,
                            view_mode: 'tree,form,calendar',
                            views: [[false, 'list'],[false, 'form']],
                            target: 'current',
                            domain: dominio,
                        }, options);
                    }else{
                        self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
                    }

                }
            });

            $(document).off("click", ".container-bar.d-groupBy, .container-line.d-groupBy");
            $(document).on("click", ".container-bar.d-groupBy, .container-line.d-groupBy", function(event) {
                event.stopPropagation();
                event.preventDefault();

                var indiceOriginal = event.currentTarget.classList[0];
                var indice = filtrar_indice(indiceOriginal);
                var actual = self.graficos_nuevos[indice];

                let chart = self.charts[indice][0];
                let reglas_acceso = self.reglas_acceso[indice];

                if(actual.agrupar_extra_nombre)
                {
                    let elementAtClick = chart.getElementAtEvent(event)[0];
                    if(elementAtClick)
                    {
                        let e_index = elementAtClick._index;
                        let e_etiqueta = chart.data.labels[e_index];
                        let e_dataSet = chart.data.datasets[elementAtClick._datasetIndex];
                        let e_serie_dataSet = e_dataSet.label;
                        let e_valor = e_dataSet.data[e_index];

                        if(typeof(e_etiqueta)=='string'){
                            e_etiqueta = e_etiqueta.trim();
                        }
                        if (e_etiqueta == 'Desconocido') {
                            e_etiqueta = false;
                        }
                        if(typeof(e_serie_dataSet)=='string'){
                            e_serie_dataSet = e_serie_dataSet.trim();
                        }
                        if (e_serie_dataSet == 'Desconocido') {
                            e_serie_dataSet = false;
                        }

                        let regla_acceso = reglas_acceso[e_etiqueta][e_serie_dataSet];

                        if(regla_acceso && regla_acceso[2]){
                            let dominio = regla_acceso[0];
                            let nombre = self.graficos_nuevos[indice].name;

                            let cant_accesos = regla_acceso[1] != regla_acceso[2];

                            if(cant_accesos)
                            {
                                nombre = nombre + " (Acceso a " + regla_acceso[2] + " registros de " + regla_acceso[1] + ")";
                            }

                            var options = {
                                    on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                                };
                                var modelo = self.graficos_nuevos[indice].modelo_nombre;

                                self.do_action({
                                    name: nombre,
                                    type: 'ir.actions.act_window',
                                    res_model: modelo,
                                    view_mode: 'tree,form,calendar',
                                    views: [[false, 'list'],[false, 'form']],
                                    target: 'current',
                                    domain: dominio,
                                }, options);

                        }
                        else{
                            self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
                        }
                    }
                }
                else
                {
                    let elementAtClick = chart.getElementsAtEvent(event)[0];
                    if(elementAtClick)
                    {
                        let e_index = elementAtClick._index;
                        let e_etiqueta = chart.data.labels[e_index];
                        let e_dataSet = chart.data.datasets[0];
                        let e_valor = e_dataSet.data[e_index];

                        if(typeof(e_etiqueta)=='string'){
                            e_etiqueta = e_etiqueta.trim();
                        }
                        if (e_etiqueta == 'Desconocido') {
                            e_etiqueta = false;
                        }

                        let regla_acceso = reglas_acceso[e_etiqueta];

                        if(regla_acceso[2]){
                            let dominio = regla_acceso[0];
                            let nombre = self.graficos_nuevos[indice].name;

                            let cant_accesos = regla_acceso[1] != regla_acceso[2];

                            if(cant_accesos)
                            {
                                nombre = nombre + " (Acceso a " + regla_acceso[2] + " registros de " + regla_acceso[1] + ")";
                            }

                            var options = {
                                    on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                                };
                                var modelo = self.graficos_nuevos[indice].modelo_nombre;

                                self.do_action({
                                    name: nombre,
                                    type: 'ir.actions.act_window',
                                    res_model: modelo,
                                    view_mode: 'tree,form,calendar',
                                    views: [[false, 'list'],[false, 'form']],
                                    target: 'current',
                                    domain: dominio,
                                }, options);

                        }
                        else{
                            self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
                        }
                    }
                }
            });

            $(document).off("click", ".container-line.d-value, .container-bar.d-value", );
            $(document).on("click", ".container-line.d-value, .container-bar.d-value", function(event) {
                event.stopPropagation();
                event.preventDefault();

                var indiceOriginal = event.currentTarget.classList[0];
                var indice = filtrar_indice(indiceOriginal);
                var actual = self.graficos_nuevos[indice];

                let chart = self.charts[indice][0];
                let reglas_acceso = self.reglas_acceso[indice];
                let elementAtClick = chart.getElementsAtEvent(event)[0];

                if(elementAtClick){
                    let e_index = elementAtClick._index;
                    let e_etiqueta = chart.data.labels[e_index];
                    let e_dataSet = chart.data.datasets[0];
                    let e_valor = e_dataSet.data[e_index];

                    if(typeof(e_etiqueta)=='string'){
                        e_etiqueta = e_etiqueta.trim();
                    }
                    if (e_etiqueta == 'Desconocido') {
                        e_etiqueta = false;
                    }

                    let regla_acceso = reglas_acceso[e_etiqueta];

                    if(regla_acceso[2]){
                        let dominio = regla_acceso[0];
                        let nombre = self.graficos_nuevos[indice].name;

                        let cant_accesos = regla_acceso[1] != regla_acceso[2];

                        if(cant_accesos)
                        {
                            nombre = nombre + " (Acceso a " + regla_acceso[2] + " registros de " + regla_acceso[1] + ")";
                        }

                        var options = {
                                on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                            };
                            var modelo = self.graficos_nuevos[indice].modelo_nombre;

                            self.do_action({
                                name: nombre,
                                type: 'ir.actions.act_window',
                                res_model: modelo,
                                view_mode: 'tree,form,calendar',
                                views: [[false, 'list'],[false, 'form']],
                                target: 'current',
                                domain: dominio,
                            }, options);

                    }
                    else{
                        self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
                    }
                }

            });

            $(document).off("click", ".heatmap-table tr");
            $(document).on("click", ".heatmap-table tr",function(event){
                event.stopPropagation();
                event.preventDefault();

                var fila = event.currentTarget;
                if(fila){
                    var tabla = fila.closest('.heatmap-table');

                    var indiceOriginal = tabla.classList[0];
                    var indice = filtrar_indice(indiceOriginal);
                    var actual = self.graficos_nuevos[indice];

                    let celdas = fila.childNodes;
                    let reglas_acceso = self.reglas_acceso[indice];
                    let c_label = celdas[0].innerText;
                    let c_value = celdas[1].innerText;

                    if(typeof(c_label)=='string'){
                        c_label = c_label.trim();
                    }
                    if (c_label == 'Desconocido') {
                        c_label = false;
                    }

                    let datos_filtrados = self.charts[indice][0];
                    let dominios = self.charts[indice][1];
                    let dominio = [];

                    let dom_index = Object.keys(dominios).findIndex(e => {
                        let element = dominios[e];
                        let valor = element[1];
                        if(typeof(valor) == 'object')
                        {
                            valor = valor[1];
                        }
                        if(typeof(valor) == 'string')
                        {
                            valor = valor.trim();
                        }
                        return valor == c_label;
                    });

                    if(dom_index >= 0)
                    {
                        if(reglas_acceso[dom_index])
                        {
                            dominio = dominios[dom_index][0];
                            let arr_agregar = [datos_filtrados.valores[0].trim(), '=', c_value];
                            let arr_existe = Object.keys(dominio).findIndex(e => {
                                return dominio[e][0].trim() == datos_filtrados.valores[0].trim();
                            });
                            if(arr_existe >= 0)
                            {
                                dominio[arr_existe] = arr_agregar;
                            }else{
                                dominio.push(arr_agregar);
                            }


                            var options = {
                                on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                            };
                            var modelo = self.graficos_nuevos[indice].modelo_nombre;

                            self.do_action({
                                name: self.graficos_nuevos[indice].name,
                                type: 'ir.actions.act_window',
                                res_model: modelo,
                                view_mode: 'tree,form,calendar',
                                views: [[false, 'list'],[false, 'form']],
                                target: 'current',
                                domain: dominio,
                            }, options);
                        }else{
                            self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
                        }
                    }
                } 
                
            });

            $(document).off("click", ".normal-table tr");
            $(document).on("click", ".normal-table tr",function(event){
                event.stopPropagation();
                event.preventDefault();

                var fila = event.currentTarget;
                if(fila){
                    var tabla = fila.closest('.normal-table');

                    var indiceOriginal = tabla.classList[0];
                    var indice = filtrar_indice(indiceOriginal);
                    var actual = self.graficos_nuevos[indice];

                    let celdas = fila.childNodes;
                    let reglas_acceso = self.reglas_acceso[indice];
                    let c_label = celdas[0].innerText;
                    let c_value = celdas[1].innerText;

                    if(typeof(c_label)=='string'){
                        c_label = c_label.trim();
                    }
                    if (c_label == 'Desconocido') {
                        c_label = false;
                    }

                    let datos_filtrados = self.charts[indice][0];
                    let dominios = self.charts[indice][1];
                    let dominio = [];

                    let dom_index = Object.keys(dominios).findIndex(e => {
                        let element = dominios[e];
                        let valor = element[1];
                        if(typeof(valor) == 'object')
                        {
                            valor = valor[1];
                        }
                        if(typeof(valor) == 'string')
                        {
                            valor = valor.trim();
                        }
                        return valor == c_label;
                    });

                    if(dom_index >= 0)
                    {
                        if(reglas_acceso[dom_index])
                        {
                            dominio = dominios[dom_index][0];
                            let arr_agregar = [datos_filtrados.valores[0].trim(), '=', c_value];
                            let arr_existe = Object.keys(dominio).findIndex(e => {
                                return dominio[e][0].trim() == datos_filtrados.valores[0].trim();
                            });
                            if(arr_existe >= 0)
                            {
                                dominio[arr_existe] = arr_agregar;
                            }else{
                                dominio.push(arr_agregar);
                            }


                            var options = {
                                on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                            };
                            var modelo = self.graficos_nuevos[indice].modelo_nombre;

                            self.do_action({
                                name: self.graficos_nuevos[indice].name,
                                type: 'ir.actions.act_window',
                                res_model: modelo,
                                view_mode: 'tree,form,calendar',
                                views: [[false, 'list'],[false, 'form']],
                                target: 'current',
                                domain: dominio,
                            }, options);
                        }else{
                            self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
                        }
                    }
                } 
                
            });

            
            // $(document).off("click", ".item-container .pl-3 h3");
            // $(document).on("click", ".item-container .pl-3 h3",function(event){
                $(document).off("click", ".item-container .item-header");
                $(document).on("click", ".item-container .item-header",function(event){
                    event.stopPropagation();
                    event.preventDefault();

                    var currentTarget = event.currentTarget;

                    let fila = currentTarget.querySelector('.pl-3 h3');

                    if(fila){
                        var tabla = fila.closest('.item-container');

                        var indiceOriginal = tabla.classList[0];
                        var indice = filtrar_indice(indiceOriginal);
                        var actual = self.graficos_nuevos[indice];

                        let texto = fila.innerText;
                        let reglas_acceso = self.reglas_acceso[indice];
                        texto = texto.replace(actual.tarjeta_extra,'');
                        let texto_filtrado = texto.split(': ');
                        let t_etiqueta = texto_filtrado[0];
                        let t_valor = Number(texto_filtrado[1]);

                        if(typeof(t_etiqueta)=='string'){
                            t_etiqueta = t_etiqueta.trim();
                        }
                        if (t_etiqueta == 'Desconocido') {
                            t_etiqueta = false;
                        }

                        let datos_filtrados = self.charts[indice][0];
                        let dominios = self.charts[indice][1];
                        let dominio = [];

                        let dom_index = Object.keys(dominios).findIndex(e => {
                            let element = dominios[e];
                            let valor = element[1];
                            if(typeof(valor) == 'object')
                            {
                                valor = valor[1];
                            }
                            if(typeof(valor) == 'string')
                            {
                                valor = valor.trim();
                            }
                            return valor == t_etiqueta;
                        });

                        if(dom_index >= 0)
                        {
                            if(reglas_acceso[dom_index])
                            {
                                dominio = dominios[dom_index][0];
                                let arr_agregar = [datos_filtrados.valores[0].trim(), '=', t_valor];
                                let arr_existe = Object.keys(dominio).findIndex(e => {
                                    return dominio[e][0].trim() == datos_filtrados.valores[0].trim();
                                });
                                if(arr_existe >= 0)
                                {
                                    dominio[arr_existe] = arr_agregar;
                                }else{
                                    dominio.push(arr_agregar);
                                }
                                

                                var options = {
                                    on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                                };
                                var modelo = self.graficos_nuevos[indice].modelo_nombre;

                                self.do_action({
                                    name: self.graficos_nuevos[indice].name,
                                    type: 'ir.actions.act_window',
                                    res_model: modelo,
                                    view_mode: 'tree,form,calendar',
                                    views: [[false, 'list'],[false, 'form']],
                                    target: 'current',
                                    domain: dominio,
                                }, options);
                            }else{
                                self.do_action('sicpro_modulo_dashboard_extendido.ir_actions_server_error_acceso');
                            }
                        }
                    } 
                    
                });

                $(document).ready(function() {
                    let dashboard_element = self.$el.find('.oh_dashboards');
                });

            },

            fetch_data: function() {
                var self = this;
                return $.when();
            },

            render_dashboards: function() {
                var self = this;
                var templates = ['EncabezadoDashboard'];
                
                if(self.graficos_nuevos){
                    templates = this.dashboards_templates;
                }
                if(self.$('.o_hr_dashboard')[0].childElementCount == 0)
                {
                    _.each(templates, function(template) {
                        self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}));
                    });
                }
            },

            on_reverse_breadcrumb: function() {
                var self = this;
                web_client.do_push_state({});
                this.update_cp();
                this.fetch_data().then(function() {
                    self.render_dashboards();  
                    self.doc_ready();  
                });
            },

            update_cp: function() {
                var self = this;
                return self;
            },
        });

core.action_registry.add('sicpro_dashboard_view', DashboardView);
return DashboardView;
});
