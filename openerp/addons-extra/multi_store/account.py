# -*- coding: utf-8 -*-
from openerp import models, fields 

class account_journal(models.Model):
    _inherit = 'account.journal'

    store_ids = fields.Many2many(
        'res.store', 'res_store_journal_rel', 'journal_id', 'store_id',
        'Store', help="""Users that are not of this store, can see this\
        journals records but can not post or modify any entry on them.""")


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    store_id = fields.Many2one(
        'res.store', 'Sucursal', required = True ,
         help="""  Sucursal. """)

    _defaults = {
        'store_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).store_id.id,
    }


class account_voucher(models.Model):
    _inherit = 'account.voucher'

    store_id = fields.Many2one(
        'res.store', 'Sucursal', required = True ,
         help="""  Sucursal. """)

    _defaults = {
        'store_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).store_id.id,
    }
