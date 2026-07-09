odoo.define("sicpro_app_calendario.CalendarModel", function (require) {
    "use strict";

    const CalendarModel = require("web.CalendarModel");

    CalendarModel.include({

        _loadColors: function (element, events) {
            var self = this;
            if (this.fieldColor) {
                var fieldName = this.fieldColor;
                var filter = this.data.filters[fieldName];
                if (filter && filter.color_model && filter.field_color) {

                    var defs = [];
                    if (!this._field_color_map) {
                        var ids = _.map(events, function (event) {
                            return event.record[fieldName][0];
                        });
                        defs.push(
                            this._rpc({
                                model: filter.color_model,
                                method: "read",
                                args: [_.uniq(ids), [filter.field_color]],
                            }).then(function (res) {
                                self._field_color_map = self._field_color_map || {};
                                _.each(res, function (item) {
                                    self._field_color_map[item.id] =
                                        item[filter.field_color];
                                });
                            })
                        );
                    }
                    Promise.all(defs).then(function () {
                        _.each(events, function (event) {
                            var value = event.record[fieldName][0];
                            event.color_index = self._field_color_map[value];
                        });
                    });

                } else {
                    return this._super.apply(this, arguments);
                }
            }
            return Promise.resolve();
        },
    });

    return CalendarModel;
});
