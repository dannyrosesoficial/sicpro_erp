# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime

from odoo.addons.survey.controllers.main import Survey
from odoo.http import request

_logger = logging.getLogger(__name__)


class Instrucciones(Survey):

    # ------------------------------------------------------------
    # se heredó el método _check_validity para que no compruebe el token en el caso de las instrucciones periódicas
    # ------------------------------------------------------------

    def _check_validity(self, survey_token, answer_token, ensure_token=True, check_partner=True):
        """ La encuesta de verificación está abierta y se puede realizar. Esto no comprueba
        reglas de seguridad, solo reglas funcionales/comerciales. Devuelve una clave de cadena
        permitiendo una mayor manipulación de cuestiones de validez

         * encuesta_incorrecta: la encuesta no existe;
         * encuesta_auth: se requiere autenticación;
         * encuesta_cerrada: la encuesta está cerrada y ya no acepta entradas;
         * encuesta_void: la encuesta es nula y no debe realizarse;
         * token_wrong: token dado no reconocido;
         * token_required: no se proporciona token aunque es necesario para acceder al
           encuesta;
         * respuesta_deadline: token vinculado a una respuesta caducada;

        :param sure_token: si la existencia de entrada del usuario se basa en el token de acceso dado
          debe aplicarse o no, dependiendo de la ruta que solicita un token o
          permitir llamadas del mundo externo;

        :param check_partner: Si debemos verificar que el socio asociado al objetivo
          la respuesta corresponde al usuario activo.
        """
        survey_sudo, answer_sudo = self._fetch_from_access_token(survey_token, answer_token)

        if not survey_sudo.exists():
            return 'survey_wrong'

        if answer_token and not answer_sudo:
            return 'token_wrong'

        if not answer_sudo and ensure_token:
            return 'token_required'
        if not answer_sudo and survey_sudo.access_mode == 'token':
            return 'token_required'

        if survey_sudo.users_login_required and request.env.user._is_public():
            return 'survey_auth'

        if not survey_sudo.active and (not answer_sudo or not answer_sudo.test_entry):
            return 'survey_closed'

        if (not survey_sudo.page_ids and survey_sudo.questions_layout == 'page_per_section') or not survey_sudo.question_ids:
            return 'survey_void'

        # ------------------------------------------------------------
        # inicio del cambio en el controller
        # ------------------------------------------------------------
        # verífico que exista el valor del context de instrucciones
        # si existe no ejecuta la comprobación del token del trabajador contra el token del usuario activo
        # si no existe se ejecuta la comprobación del token de forma normal
        usuario = request.env['res.users'].sudo().browse(request.env.context.get('uid'))

        if not usuario.intrucciones_context:
            if answer_sudo and check_partner:
                if request.env.user._is_public() and answer_sudo.partner_id and not answer_token:
                    # paso por defecto el valor del context temporal del usuario a FALSE
                    usuario.sudo().write({"intrucciones_context": False, })
                    # las respuestas del usuario público no deben tener ningún socio_id; esto índica probablemente
                    # un problema de cookies
                    return 'answer_wrong_user'
                if not request.env.user._is_public() and answer_sudo.partner_id != request.env.user.partner_id:
                    # paso por defecto el valor del context temporal del usuario a FALSE
                    usuario.sudo().write({"intrucciones_context": False, })
                    # No coinciden los socios, probablemente un problema de cookies
                    return 'answer_wrong_user'
        # ------------------------------------------------------------
        # fin del cambio en el controller
        # ------------------------------------------------------------

        if answer_sudo and answer_sudo.deadline and answer_sudo.deadline < datetime.now():
            return 'answer_deadline'

        return True