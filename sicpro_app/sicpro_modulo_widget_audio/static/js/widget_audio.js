odoo.define('sicpro_modulo_widget_audio', function (require) {

    var core = require('web.core');
    var FieldBinaryFile = require("web.basic_fields").FieldBinaryFile
    var session = require('web.session');
    var _t = core._t;


    var fieldRegistry = require('web.field_registry');

    
    var AudioWidget = FieldBinaryFile.extend({

        supportedFieldTypes: ['binary'],
        accepted_file_extensions:'audio/*,application/ogg',


        _getAudioUrl: function (model, res_id, field, unique) {
            // every 
            return session.url('/web/content', {
                model: model,
                id: JSON.stringify(res_id),
                field: field,
            });
        },
    
    
        _renderReadonly: function () {
            // This function will run if we are not in "edit" mode
            self = this

           if (this.value) {
                url = this._getAudioUrl(this.model, this.res_id, this.name);
                // console.log(url)
                $audio = $('<audio>', {
                    'src': url,
                    'controls': true,
                    'preload':"metadata"
                })
                s = this.$el.append($audio);

                $audio.on("error",function(){
                    self.displayNotification({ title: _t('No se encontró la extensión'), message: _t("el campo "+self.name+" debe contener un audio"), type: 'danger' });

                })

                s[0].childNodes[0].onloadedmetadata =function() {
                        // console.log('metadata loaded!');
                        console.log(this.duration);//this refers to my audio
                }

            }



       },
       on_file_change: function (ev) {

        this._super.apply(this, arguments);
        var f_input = $(ev.target)

        var files = ev.target.files
        console.log(f_input.val())
        if (!files || files.length === 0) {
            return;
        }
        console.log(files)
        var valid_ext = ['wav', 'ogg', 'mp3','oga','ogx']

        // var file = ev.target.files;

        var msg = _t("El tipo de archivo debe ser un audio");
        var file = files[0];
        var name_arr = file.name.split(".")
        var ext = name_arr[name_arr.length - 1]

        // console.log(file.name)
        // console.log(ext)
        if(!valid_ext.includes(ext)){
            this.displayNotification({ title: _t('Extensión del archivo desconocida'), message: _t("el campo "+this.name+" solo puede contener archivos de Audio"), type: 'danger' });
        }
    }

    })

    fieldRegistry.add('audio_widget', AudioWidget);
    
    return {
        AudioWidget: AudioWidget,
    };

    
})

