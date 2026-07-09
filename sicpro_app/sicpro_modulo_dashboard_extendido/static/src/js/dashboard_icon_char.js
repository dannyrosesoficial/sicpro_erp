
odoo.define('sicpro_dashboard.dashboard_icono', function (require) {
	"use strict";

	var AbstractField = require('web.AbstractField');
	var basic_fields = require('web.basic_fields');
	var FieldChar = basic_fields.FieldChar;

	var FieldRegistry = require('web.field_registry');

	var core = require('web.core');
	var qweb = core.qweb;

	var WidgetIcono = FieldChar.extend({
		init: function(){
			this._super.apply(this,arguments);
		},
		_renderReadonly: function () {
			this.$el.html($(qweb.render('IconTemplate', {'widget': this})));			
		},
	});

	FieldRegistry.add('widget_icono', WidgetIcono);

	return WidgetIcono;
});