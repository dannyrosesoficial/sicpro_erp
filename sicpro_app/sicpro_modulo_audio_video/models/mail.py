# -*- coding: utf-8 -*-

from odoo.tools import mail
from lxml.html import clean

mail.safe_attrs = clean.defs.safe_attrs | frozenset(
    ['style',
     'data-o-mail-quote',  # quote detection
     'data-oe-model', 'data-oe-id', 'data-oe-field', 'data-oe-type',
     'data-oe-expression', 'data-oe-translation-id', 'data-oe-nodeid',
     'data-publish', 'data-id', 'data-res_id', 'data-interval',
     'data-member_id', 'data-scroll-background-ratio', 'data-view-id',
     'data-class', 'controls'
     ]
)
