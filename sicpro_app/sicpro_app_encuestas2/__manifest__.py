{
    "name": "sicpro_app_encuestas",
    "version": "15.0.1.0.0",
    "summary": "Encuestas: tipos extendidos y estad\u00edsticas",
    "author": "Generated",
    "depends": [
        "survey",
        "web",
        "base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/survey_templates.xml",
        "views/survey_print.xml",
        "views/survey_user_views.xml",
        "views/stats_inherit.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "sicpro_app_encuestas/static/src/js/survey_form.js",
            "sicpro_app_encuestas/static/src/js/survey_submit.js"
        ]
    },
    "installable": true,
    "application": false
}