odoo.define('sicpro_modulo_web_login/static/js/copy_paste.js', function (require) {
'use strict';

$(document).ready(function(){
  $("#bloquear").on('paste', function(e){
    e.preventDefault();
      alert('Esta acción esta prohibida');
        })
  $("#bloquear").on('copy', function(e){
    e.preventDefault();
      alert('Esta acción esta prohibida');
        })
})

});


