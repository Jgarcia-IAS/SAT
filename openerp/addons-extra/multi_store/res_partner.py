# -*- coding: utf-8 -*-
from openerp import models, fields

class res_partner(models.Model):
    _inherit = 'res.partner'

    store_ids = fields.Many2many(
        'res.store', 'res_store_partner_rel', 'partner_id', 'store_id',
        'Sucursal', help="""Users that are not of this store, can see this\
        partner records but can not post or modify any entry on them.""")

