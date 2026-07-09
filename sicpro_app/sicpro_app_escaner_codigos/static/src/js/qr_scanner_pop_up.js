odoo.define('hr_attendance.kiosk_mode', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var rpc = require('web.rpc');

const { qweb } = require('web.core');

var QrScanner = AbstractAction.extend({
    contentTemplate: 'Qr_Popup',
    jsLibs: [
        '/sicpro_app_escaner_codigos/static/lib/html5_qrcode/html5_qrcode.js',
    ],
    events: {
        "click .qr_scanner_button": function() {
            $('body').append(qweb.render('qr_code_scanner_popup', {}));
            this.$succesMessageEl =  $('.qr_code_scanner_success_message');
            $('.qr_code_scanner_close_popup_btn').click(this._onClickClosePopupBtn.bind(this));
            $('#qr_code_scanner_save_resume_btn').click(this._onClickSaveContinueQRCode.bind(this));
            $('#qr_code_scanner_save_btn').click(this._onClickSaveQRCode.bind(this));
            $('#qr_code_scanner_resume_btn').click(this._onClickResumeScanning.bind(this));

            this.html5QrcodeScanner = new Html5QrcodeScanner(
                'qr_code_scanner',
                {
                    fps: 10,
                },
                false,
            );

            this.html5QrcodeScanner.render(this._onScanSuccess.bind(this));
        },
        "click .o_qr_scanner_button_manually": function() {
            this.do_action('sicpro_app_escaner_codigos.qr_scanner_action_tree_view', {
                additional_context: {'no_group_by': true},
            });
        },
    },

    _onScanSuccess: function (decodedText, decodedResult) {
            if(this.html5QrcodeScanner.getState() != 1)
            {
                this.html5QrcodeScanner.pause(true);
            }

            this.decodedText = decodedText;
            this.parseddecodedText = this._parse_model_id(decodedText);
            this.nombre_elemento = '';

            let self = this;

            console.log("flag1");

            if(this.parseddecodedText.nombre_modelo && this.parseddecodedText.identificador)
            {
                console.log("flag2");
                rpc.query({
                    model: this.parseddecodedText.nombre_modelo,
                    method: 'search_read',
                    args: [[["id","=",this.parseddecodedText.identificador]]],
                }).then(function(elemento) {
                    $('#qr_code_test').text("Nombre: " + elemento[0].name);
                    $('#qr_code_scanner_save_resume_btn,#qr_code_scanner_save_btn').show();
                    self.$succesMessageEl.removeClass('d-none');
                    self.nombre_elemento = elemento[0].name;
                });
            }
            else{
                $('#qr_code_test').text("El QR no contiene información sobre ningún Material");
                $('#qr_code_scanner_save_resume_btn,#qr_code_scanner_save_btn').hide();
                self.$succesMessageEl.removeClass('d-none');
            }
         },

         _parse_model_id: function(texto) {
            let temp = {};
            try{
                temp = JSON.parse(texto);
            }catch (error){

            }

            if(temp.modelo && temp.id)
            {
                temp = {
                    nombre_modelo: temp.modelo,
                    identificador: temp.id,
                };    
            }

            return temp;
            
         },

         _onClickSaveContinueQRCode: function () {
            let parseado = this._parse_model_id(this.decodedText);
            var self = this;

            if(parseado.nombre_modelo && parseado.identificador)
            {
                rpc.query({
                    model: 'sicpro.app.codigos.escaneados',
                    method: 'create',
                    args:[{'identificador': parseado.identificador, 'nombre_modelo': parseado.nombre_modelo, 'nombre_elemento': self.nombre_elemento}],
                });
            }

            this._onClickResumeScanning();  

            // .then(function(result) {
            //     return rpc.query({
            //         model: 'sicpro.app.codigos.escaneados',
            //         method: 'search_read',
            //         args: [[["id","=",result]]],
            //     });
            // }).then(function(result2) {
            //     console.log("result2",result2);
            // });
        },

        _onClickSaveQRCode: function () {
            this._closeScannerPopup();
            let parseado = this._parse_model_id(this.decodedText);

            var self = this;

            if(parseado.nombre_modelo && parseado.identificador)
            {
                rpc.query({
                    model: 'sicpro.app.codigos.escaneados',
                    method: 'create',
                    args:[{'identificador': parseado.identificador, 'nombre_modelo': parseado.nombre_modelo, 'nombre_elemento': self.nombre_elemento}],
                });
            }

            // .then(function(result) {
            //     return rpc.query({
            //         model: 'sicpro.app.codigos.escaneados',
            //         method: 'search_read',
            //         args: [[["id","=",result]]],
            //     });
            // }).then(function(result2) {
            //     console.log("result2",result2);
            // });
        },

        _onClickClosePopupBtn: function (event) {
            this._closeScannerPopup();
        },

        _onClickResumeScanning: function (event) {
            this.$succesMessageEl.addClass('d-none');
            if(this.html5QrcodeScanner.getState() != 1){
                this.html5QrcodeScanner.resume();
            }
        },

        _closeScannerPopup: function () {
            $('.qr_code_scanner_popup').remove();
            this.html5QrcodeScanner.clear();
            this.html5QrcodeScanner = null;
        },
});

core.action_registry.add('qr_scanner_action', QrScanner);

return QrScanner;

});
