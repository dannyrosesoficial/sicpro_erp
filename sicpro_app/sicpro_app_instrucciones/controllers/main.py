# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
import logging
from datetime import datetime
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request

_logger = logging.getLogger(__name__)


class Instrucciones(Survey):

    def _check_validity(self, survey_sudo, answer_sudo, answer_token,
                        ensure_token=True, check_partner=True):

        if not survey_sudo:
            return 'survey_wrong'

        if answer_token and not answer_sudo:
            return 'token_wrong'

        if not answer_sudo and ensure_token:
            return 'token_required'

        if not answer_sudo and survey_sudo.access_mode == 'token':
            return 'token_required'

        if survey_sudo.users_login_required and request.env.user._is_public():
            return 'survey_auth'

        if not survey_sudo.active and (
            not answer_sudo or not answer_sudo.test_entry):
            return 'survey_closed'

        if (
            not survey_sudo.page_ids and survey_sudo.questions_layout == 'page_per_section') or not survey_sudo.question_ids:
            return 'survey_void'

        # --- LÓGICA PERSONALIZADA SICPRO ---
        # Usamos el campo técnico en el usuario para decidir si saltamos la validación
        is_instruccion = request.env.user.sudo().intrucciones_context

        if not is_instruccion:
            # Si NO es una instrucción de SICPRO, aplicamos la validación de socio original de Odoo
            if answer_sudo and check_partner:
                if request.env.user._is_public() and answer_sudo.partner_id and not answer_token:
                    return 'answer_wrong_user'
                if not request.env.user._is_public() and answer_sudo.partner_id != request.env.user.partner_id:
                    return 'answer_wrong_user'
        else:
            _logger.info(
                "SICPRO: Saltando validación de partner para la encuesta %s",
                survey_sudo.title)
        # --- FIN LÓGICA SICPRO ---

        if answer_sudo and answer_sudo.deadline and answer_sudo.deadline < datetime.now():
            return 'answer_deadline'

        return True