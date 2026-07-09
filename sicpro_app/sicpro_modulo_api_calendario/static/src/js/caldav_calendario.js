odoo.define("sicpro_modulo_api_calendario.caldav", function (require) {
    "use strict";

    var CalendarRenderer = require("web.CalendarRenderer");
    var session = require("web.session");
    var rpc = require("web.rpc");
    var core = require("web.core");
    var _t = core._t;


    const CalendarioSync = CalendarRenderer.include({

        _initSidebar: function () {
            var self = this;
            this._super.apply(this, arguments);
            this.$caldav_txt_nube = this.$('#caldav_txt_nube');
            this.$caldav_sync_nube = this.$('#caldav_sync_nube');

            rpc.query({
                model: "calendar.event",
                method: "caldav_sync_manual_calendario_views",
                kwargs: {user_id: session.uid},
            }).then(function (result) {
                //console.log(result);
                if (!result) {
                    self.$caldav_sync_nube.hide();
                } else {
                    self.$caldav_txt_nube.hide();
                }
            });
        },

    });

    $(document).on("click", "#caldav_sync_nube", function (event) {
        rpc.query({
            model: "calendar.event",
            method: "caldav_sync_manual_calendario",
            kwargs: {user_id: session.uid},
        })
    });

    return {
        CalendarioSync
    };

});
