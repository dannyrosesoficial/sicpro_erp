odoo.define('sicpro_app_encuestas.survey_statistics_inherit', function (require) {
    "use strict";

    var core = require('web.core');
    var SurveyResult = require('survey.result');
    var publicWidget = require('web.public.widget');

    var SurveyResultChart = SurveyResult.chartWidget;
    var SurveyResultWidget = SurveyResult.resultWidget;

    // 1. Lógica para forzar la inicialización (la que ya funciona)
    SurveyResultWidget.include({
        start: function () {
            var self = this;
            var basePromise = this._super.apply(this, arguments);
            var allPromises = [basePromise];

            self.$('.survey_stats .survey_graph').each(function () {
                var $chartEl = $(this);
                if ($chartEl.data("graphData")) {
                    // Si el template está en 'pie', ya no necesitamos forzarlo aquí.
                    // Nos aseguramos de que el widget se adjunte.
                    allPromises.push(new publicWidget.registry.SurveyResultChart(self)
                        .attachTo($chartEl));
                }
            });
            return Promise.all(allPromises);
        },
    });

    // 2. Lógica CRÍTICA para arreglar el formato de datos para el gráfico PIE
    SurveyResultChart.include({
        start: function () {
            var self = this;
            var graphType = self.$el.data("graphType");

            // Dejamos que el método base se ejecute. Fallará en la configuración del gráfico PIE.
            return this._super.apply(this, arguments).then(function () {

                // Comprobamos si es un gráfico de pastel y si el base falló (porque los datos eran de grupo)
                if (graphType === 'pie' && self.graphData && self.graphData.length > 0) {

                    // Si el primer elemento tiene la clave 'values', significa que es el formato de grupo.
                    if (self.graphData[0].values) {

                        // 1. Desenvuelve los datos: Reemplazamos self.graphData por el array plano 'values'
                        self.graphData = self.graphData[0].values;

                        // 2. Forzamos la creación de la configuración del gráfico PIE (ahora con los datos planos)
                        self.chartConfig = self._getPieChartConfig();

                        // 3. Volvemos a dibujar el gráfico con la configuración corregida
                        if (self.chartConfig) {
                            self._loadChart();
                        }
                    }
                }
            });
        },
    });

    return SurveyResult;
});