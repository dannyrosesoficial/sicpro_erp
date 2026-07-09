odoo.define('sicpro_app_encuestas.survey_form', function (require) {
'use strict';
    console.log('sicpro_app_encuestas.survey_form')
    var rpc = require('web.rpc');
    var publicWidget = require('web.public.widget');

    var SurveyForm = publicWidget.Widget.extend({
        selector: '.o_survey_form',
        events: {
            'focus .o_select_Country': '_onSelectCountry',
            'change .o_select_Country': '_onSelectState',
        },
        _onSelectCountry: function(ev){
            /*
                * method to load country
            */
            var self = this
            rpc.query({
            route: '/survey/load_country',
            params: {},
            }).then(function (result){
                var count = 0;
                self.$el.find(`#${ev.target.id}`).html('<option value="">Country</option>')
                result['id'].forEach(element => {
                    self.$el.find(`#${ev.target.id}`).append(
                    `<option value='${result['name'][count]}'>${result['name'][count]}</option>`
                    )
                    count += 1
                })
            });
        },
        _onSelectState: function(ev){
            /*
                * method to load states
            */
            var self = this
            var country_id = ev.target.value
            var question_id = ev.target.dataset.id
            rpc.query({
            route: '/survey/load_states',
            params: { country_id },
            }).then(function (result){
                var count = 0;
                self.$el.find(`#${question_id}-state`).html('<option value="">State</option>')
                result['id'].forEach(element => {
                    self.$el.find(`#${question_id}-state`).append(
                    `<option value="${result['name'][count]}">${result['name'][count]}</option>`
                    )
                    count += 1
                })
            });
        },

    });
    publicWidget.registry.SurveyForm = SurveyForm;
})
