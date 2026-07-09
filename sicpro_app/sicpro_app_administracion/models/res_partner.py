# -*- coding: utf-8 -*-

import base64
import collections
import datetime
import hashlib
import pytz
import threading
import re

import requests
from collections import defaultdict
from lxml import etree
from random import randint
from werkzeug import urls

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class Partner(models.Model):
    _inherit = "res.partner"

    # modifico el orden del partner para que salga el nombre primero y después el proceso
    def _get_contact_name(self, partner, name):
        return "%s, %s" % (name, partner.commercial_company_name or partner.sudo().parent_id.name)