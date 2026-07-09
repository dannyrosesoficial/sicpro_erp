# -*- coding: utf-8 -*-

import logging

from odoo import SUPERUSER_ID, api

logger = logging.getLogger(__name__)


def set_default_map_settings(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    user_model = env["res.users"]
    users = user_model.search([("context_map_website_id", "=", False)])
    logger.info("Updating user settings for maps...")
    users.write(
        {
            "context_map_website_id": user_model._default_map_website().id,
            "context_route_map_website_id": (
                user_model._default_route_map_website().id
            ),
        }
    )
    # Update the starting partner this way that is faster
    cr.execute(
        """
        UPDATE res_users
        SET context_route_start_partner_id = partner_id
        WHERE context_route_start_partner_id IS NULL;
        """
    )
