# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class account_move(osv.osv):
    _name = "account.move"
    _inherit = "account.move"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con este movimiento"),

        }

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con este movimiento"),

        }
class account_move_line(osv.osv):
    _name = "account.move.line"
    _inherit = "account.move.line"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT',
#             store=True,related = 'move_id.ot', 
            help="Orden de trabajo relacionada con esta orden de compras"),

        }



class purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con esta orden de compras"),

        }

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        invoice_vals = super(purchase_order,self)._prepare_inv_line(cr, uid, account_id, order_line, context=context)
        invoice_vals.update({'ot': order_line.ot.id})
        print "-----------------------"
        print order_line.ot
        return invoice_vals






class purchase_order_line(osv.osv):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
#                  store=True,related = 'order_id.ot',
            help="Orden de trabajo relacionada con esta orden de compras"),

        }



class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con esta Factura de proveedor o Factura de cliente"),

        }

                
    def action_move_create(self, cr, uid, ids, context=None):
        ret = super(account_invoice, self).action_move_create(cr, uid, ids, context=None)
        if ret:
            for inv in self.browse(cr, uid, ids):
                move_line_ids = []

                for move_line in inv.move_id.line_id:
                    move_line_ids.append(move_line.id)
                    aml_obj = self.pool.get("account.move.line")
                    print "------ction_move_create---------"

                    if inv.type in ('out_invoice', 'out_refund'):
                        aml_obj.write(cr, uid, move_line_ids, {'ot': inv.ot.id})
                    else: 

                        for line in inv.invoice_line:
                           if line.product_id.id == move_line.product_id.id:
                                aml_obj.write(cr, uid, move_line.id, {'ot': line.ot.id})
 
        return ret




class account_invoice_line(osv.osv):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"
    _columns = {
            'ot': fields.many2one('mrp.repair', string='OT', 
#                  store=True,related = 'invoice_id.ot',
                  help="Orden de trabajo relacionada con esta Factura de proveedor o Factura de cliente"
             ),
        }

 
   



class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con esta Factura de proveedor o Factura de cliente"),

        }
    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        invoice_vals = super(sale_order,self)._prepare_invoice(cr, uid, order, line_ids, context=context)

        invoice_vals.update({'ot': order.ot.id})

        return invoice_vals




class sale_order_line(osv.osv):
    _name = "sale.order.line"
    _inherit = "sale.order.line"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
                  store=True,related = 'order_id.ot',
                  help="Orden de trabajo relacionada con esta Factura de proveedor o Factura de cliente"),

        }
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
 
        invoice_vals = super(sale_order_line,self)._prepare_order_line_invoice_line(cr, uid,  line,account_id, context=context)
        invoice_vals.update({'ot': line.ot.id})
        return invoice_vals


class hr_expense_expense(osv.osv):
    _name = "hr.expense.expense"
    _inherit = "hr.expense.expense"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
             help="Orden de trabajo relacionada con este gasto"),

        }

    def line_get_convert(self, cr, uid, x, part, date, context=None):
        invoice_vals = super(hr_expense_expense,self).line_get_convert(cr, uid, x, part, date, context=context)
        invoice_vals.update({'ot': x.get('ot', False)})
        return invoice_vals

    def move_line_get_item(self, cr, uid, line, context=None):
        invoice_vals = super(hr_expense_expense,self).move_line_get_item(cr, uid, line, context=context)
        invoice_vals.update({'ot':line.ot.id,})
        return invoice_vals


class hr_expense_line(osv.osv):
    _name = "hr.expense.line"
    _description = "Expense Line"

    _inherit = "hr.expense.line"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
#                  store=True,related = 'expense_id.ot',
             help="Orden de trabajo relacionada con este gasto"),

        }

class account_bank_statement(osv.osv):
    _inherit = 'account.bank.statement'
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
             help="Orden de trabajo relacionada con este gasto"),

        }
    def _prepare_move_line_vals(self, cr, uid, st_line, move_id, debit, credit, currency_id=False,
                amount_currency=False, account_id=False, partner_id=False, context=None):

        invoice_vals = super(account_bank_statement,self)._prepare_move_line_vals( cr, uid, st_line, move_id, debit, credit, currency_id,
                amount_currency, account_id, partner_id, context=context)

        invoice_vals.update({'ot': st_line.ot.id})

        return invoice_vals


class account_bank_statement_line(osv.osv):
    _inherit = 'account.bank.statement.line'

    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
#                  store=True,related = 'statement_id.ot',
             help="Orden de trabajo relacionada con este gasto"),

        }

#===================================================================================

class mrp_repair(osv.osv):
    _name = 'mrp.repair'
    _inherit = 'mail.thread'
    _description = 'Repair Order'

    def _amount_untaxed(self, cr, uid, ids, field_name, arg, context=None):
        """ Calculates untaxed amount.
        @param self: The object pointer
        @param cr: The current row, from the database cursor,
        @param uid: The current user ID for security checks
        @param ids: List of selected IDs
        @param field_name: Name of field.
        @param arg: Argument
        @param context: A standard dictionary for contextual values
        @return: Dictionary of values.
        """
        res = {}
        cur_obj = self.pool.get('res.currency')

        for repair in self.browse(cr, uid, ids, context=context):
            res[repair.id] = 0.0
            for line in repair.operations:
                res[repair.id] += line.price_subtotal
            for line in repair.fees_lines:
                res[repair.id] += line.price_subtotal

            for line in repair.compras:
                res[repair.id] += line.amount_total

            cur = repair.pricelist_id.currency_id
            res[repair.id] = cur_obj.round(cr, uid, cur, res[repair.id])
        return res

    def _amount_tax(self, cr, uid, ids, field_name, arg, context=None):
        """ Calculates taxed amount.
        @param field_name: Name of field.
        @param arg: Argument
        @return: Dictionary of values.
        """
        res = {}
        #return {}.fromkeys(ids, 0)
        cur_obj = self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for repair in self.browse(cr, uid, ids, context=context):
            val = 0.0
            cur = repair.pricelist_id.currency_id
            for line in repair.operations:
                #manage prices with tax included use compute_all instead of compute
                if line.to_invoice:
                    tax_calculate = tax_obj.compute_all(cr, uid, line.tax_id, line.price_unit, line.product_uom_qty, line.product_id, repair.partner_id)
                    for c in tax_calculate['taxes']:
                        val += c['amount']
            for line in repair.fees_lines:
                if line.to_invoice:
                    tax_calculate = tax_obj.compute_all(cr, uid, line.tax_id, line.price_unit, line.product_uom_qty, line.product_id, repair.partner_id)
                    for c in tax_calculate['taxes']:
                        val += c['amount']

            for line in repair.compras:
                val += line.amount_tax
                print line.amount_tax
                print "------------------------------------------------"

            res[repair.id] = cur_obj.round(cr, uid, cur, val)
        return res

    def _amount_total(self, cr, uid, ids, field_name, arg, context=None):
        """ Calculates total amount.
        @param field_name: Name of field.
        @param arg: Argument
        @return: Dictionary of values.
        """
        res = {}
        untax = self._amount_untaxed(cr, uid, ids, field_name, arg, context=context)
        tax = self._amount_tax(cr, uid, ids, field_name, arg, context=context)
        cur_obj = self.pool.get('res.currency')
        for id in ids:
            repair = self.browse(cr, uid, id, context=context)
            cur = repair.pricelist_id.currency_id
            res[id] = cur_obj.round(cr, uid, cur, untax.get(id, 0.0) + tax.get(id, 0.0))
        return res

    def _get_default_address(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        partner_obj = self.pool.get('res.partner')
        for data in self.browse(cr, uid, ids, context=context):
            adr_id = False
            if data.partner_id:
                adr_id = partner_obj.address_get(cr, uid, [data.partner_id.id], ['default'])['default']
            res[data.id] = adr_id
        return res

    def _get_lines(self, cr, uid, ids, context=None):
        return self.pool['mrp.repair'].search(cr, uid, [('operations', 'in', ids)], context=context)

    def _get_fee_lines(self, cr, uid, ids, context=None):
        return self.pool['mrp.repair'].search(cr, uid, [('fees_lines', 'in', ids)], context=context)


    def _get_compras_lines(self, cr, uid, ids, context=None):
        return self.pool['mrp.repair'].search(cr, uid, [('compras', 'in', ids)], context=context)
    

    def get_ventas_lines(self, cr, uid, ids, fields, args, context=None):
        line_obj = self.pool.get('account.invoice')
        res = {}
        for script in self.browse(cr, uid, ids):
            args = [('ot', '=', script.id), ('type', '=', 'out_invoice' )]
            if script.ir_filter_ventas_id:
                args += eval(script.ir_filter_ventas_id.domain)
            line_ids = line_obj.search(cr, uid, args)
            res[script.id] = line_ids
        return res

    def set_ventas_lines(self, cr, uid, id, name, value, inv_arg, context):
        line_obj = self.pool.get('account.invoice')
        for line in value:
             if line[0] == 1: # one2many Update
                line_id = line[1]
                line_obj.write(cr, uid, [line_id], line[2])
        return True

    def get_compras_lines(self, cr, uid, ids, fields, args, context=None):
        line_obj = self.pool.get('account.invoice')
        res = {}
        for script in self.browse(cr, uid, ids):
            args = [('ot', '=', script.id), ('invoice_id.type', '=', 'in_invoice' )]
            if script.ir_filter_compras_id:
                args += eval(script.ir_filter_compras_id.domain)
            line_ids = line_obj.search(cr, uid, args)
            res[script.id] = line_ids
        return res

    def set_compras_lines(self, cr, uid, id, name, value, inv_arg, context):
        line_obj = self.pool.get('account.invoice')
        for line in value:
             if line[0] == 1: # one2many Update
                line_id = line[1]
                line_obj.write(cr, uid, [line_id], line[2])
        return True


    _columns = {
        'name': fields.char('Repair Reference', required=True, states={'confirmed': [('readonly', True)]}, copy=False),
        'product_id': fields.many2one('product.product', string='Product to Repair', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'product_qty': fields.float('Product Quantity', digits_compute=dp.get_precision('Product Unit of Measure'),
                                    required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'partner_id': fields.many2one('res.partner', 'Partner', select=True, help='Choose partner for whom the order will be invoiced and delivered.', states={'confirmed': [('readonly', True)]}),
        'address_id': fields.many2one('res.partner', 'Delivery Address', domain="[('parent_id','=',partner_id)]", states={'confirmed': [('readonly', True)]}),
        'default_address_id': fields.function(_get_default_address, type="many2one", relation="res.partner"),
        'state': fields.selection([
            ('draft', 'Quotation'),
            ('cancel', 'Cancelled'),
            ('confirmed', 'Confirmed'),
            ('under_repair', 'Under Repair'),
            ('ready', 'Ready to Repair'),
            ('2binvoiced', 'To be Invoiced'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Repaired')
            ], 'Status', readonly=True, track_visibility='onchange', copy=False,
            help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed repair order. \
            \n* The \'Confirmed\' status is used when a user confirms the repair order. \
            \n* The \'Ready to Repair\' status is used to start to repairing, user can start repairing only after repair order is confirmed. \
            \n* The \'To be Invoiced\' status is used to generate the invoice before or after repairing done. \
            \n* The \'Done\' status is set when repairing is completed.\
            \n* The \'Cancelled\' status is used when user cancel repair order.'),
        'location_id': fields.many2one('stock.location', 'Current Location', select=True, required=True, readonly=True, states={'draft': [('readonly', False)], 'confirmed': [('readonly', True)]}),
        'location_dest_id': fields.many2one('stock.location', 'Delivery Location', readonly=True, required=True, states={'draft': [('readonly', False)], 'confirmed': [('readonly', True)]}),
        'lot_id': fields.many2one('stock.production.lot', 'Repaired Lot', domain="[('product_id','=', product_id)]", help="Products repaired are all belonging to this lot"),
        'date_ot': fields.date('Fecha apertura', required=True, help="Fecha de la apertura de la orden de trabajo."),
        'guarantee_limit': fields.date('Warranty Expiration', help="The warranty expiration limit is computed as: last move date + warranty defined on selected product. If the current date is below the warranty expiration limit, each operation and fee you will add will be set as 'not to invoiced' by default. Note that you can change manually afterwards.", states={'confirmed': [('readonly', True)]}),
        'operations': fields.one2many('mrp.repair.line', 'repair_id', 'Operation Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True),

        'stock_move_ids': fields.one2many('stock.move', 'ot', 'Movimientos de inventario', readonly=True, states={'draft': [('readonly', False)]}, copy=False  ),

        'caja_menor': fields.one2many('account.bank.statement.line', 'ot', 'Caja menor  Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True  ),
        'gastos_empleados': fields.one2many('hr.expense.line', 'ot', 'Gastos empleados  Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True  ),
        'compras': fields.one2many('account.invoice.line', 'ot', 'Compras Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True,   ),
        'ventas': fields.one2many('account.invoice', 'ot', 'Ventas Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True   ),
        'ir_filter_ventas_id': fields.many2one('ir.filters', 'Ventas Filter', domain=[('ot', '=', 'account.invoice'), ('type', '=', 'out_invoice' )]),
        'view_ventas_ids': fields.function(get_ventas_lines, fnct_inv=set_ventas_lines, string='Lines', relation="account.invoice", method=True, type="one2many"),
        'ir_filter_compras_id': fields.many2one('ir.filters', 'Compras Filter', domain=[('ot', '=', 'account.invoice.line'), ('invoice_id.type', '=', 'in_invoice' )]),
        'view_compras_ids': fields.function(get_compras_lines, fnct_inv=set_compras_lines, string='Lines', relation="account.invoice", method=True, type="one2many"),


        'pricelist_id': fields.many2one('product.pricelist', 'Pricelist', help='Pricelist of the selected partner.'),
        'partner_invoice_id': fields.many2one('res.partner', 'Invoicing Address'),
        'invoice_method': fields.selection([
            ("none", "No Invoice"),
            ("b4repair", "Before Repair"),
            ("after_repair", "After Repair")
           ], "Invoice Method",
            select=True, required=True, states={'draft': [('readonly', False)]}, readonly=True, help='Selecting \'Before Repair\' or \'After Repair\' will allow you to generate invoice before or after the repair is done respectively. \'No invoice\' means you don\'t want to generate invoice for this repair order.'),
        'invoice_id': fields.many2one('account.invoice', 'Invoice', readonly=True, track_visibility="onchange", copy=False),
        'move_id': fields.many2one('stock.move', 'Move', readonly=True, help="Move created by the repair order", track_visibility="onchange", copy=False),
        'fees_lines': fields.one2many('mrp.repair.fee', 'repair_id', 'Fees', readonly=True, states={'draft': [('readonly', False)]}, copy=True),
        'journal_id': fields.many2one('account.journal', 'Diaio cargos',states={'draft': [('readonly', False)]}, readonly=True, required=True),
        'internal_notes': fields.text('Internal Notes'),
        'quotation_notes': fields.text('Quotation Notes'),
        'company_id': fields.many2one('res.company', 'Company'),
        'invoiced': fields.boolean('Invoiced', readonly=True, copy=False),
        'repaired': fields.boolean('Repaired', readonly=True, copy=False),
        'amount_untaxed': fields.function(_amount_untaxed, string='Untaxed Amount',
            store={
                'mrp.repair': (lambda self, cr, uid, ids, c={}: ids, ['operations', 'fees_lines'], 10),
                'mrp.repair.line': (_get_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),
                'mrp.repair.fee': (_get_fee_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),
                'mrp.repair.compras': (_get_compras_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),

            }),
        'amount_tax': fields.function(_amount_tax, string='Taxes',
            store={
                'mrp.repair': (lambda self, cr, uid, ids, c={}: ids, ['operations', 'fees_lines'], 10),
                'mrp.repair.line': (_get_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),
                'mrp.repair.fee': (_get_fee_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),
                'mrp.repair.compras': (_get_compras_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),

            }),
        'amount_total': fields.function(_amount_total, string='Total',
            store={
                'mrp.repair': (lambda self, cr, uid, ids, c={}: ids, ['operations', 'fees_lines'], 10),
                'mrp.repair.line': (_get_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),
                'mrp.repair.fee': (_get_fee_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),
                'mrp.repair.compras': (_get_compras_lines, ['price_unit', 'price_subtotal', 'product_id', 'tax_id', 'product_uom_qty', 'product_uom'], 10),

            }),
    }


    def _default_stock_location(self, cr, uid, context=None):
        try:
            warehouse = self.pool.get('ir.model.data').get_object(cr, uid, 'stock', 'warehouse0')
            return warehouse.lot_stock_id.id
        except:
            return False

    _defaults = {
        'state': lambda *a: 'draft',
        'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'mrp.repair'),
        'invoice_method': lambda *a: 'b4repair',
        'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'mrp.repair', context=context),
        'pricelist_id': lambda self, cr, uid, context: self.pool.get('product.pricelist').search(cr, uid, [('type', '=', 'sale')])[0],
        'product_qty': 1.0,
        'location_id': _default_stock_location,



    }

    _sql_constraints = [
        ('name', 'unique (name)', 'The name of the Repair Order must be unique!'),
    ]




    def onchange_product_id(self, cr, uid, ids, product_id=None):
        """ On change of product sets some values.
        @param product_id: Changed product
        @return: Dictionary of values.
        """
        product = False
        if product_id:
            product = self.pool.get("product.product").browse(cr, uid, product_id)
        return {'value': {
                    'guarantee_limit': False,
                    'lot_id': False,
                    'product_uom': product and product.uom_id.id or False,
                }
        }

    def onchange_product_uom(self, cr, uid, ids, product_id, product_uom, context=None):
        res = {'value': {}}
        if not product_uom or not product_id:
            return res
        product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
        uom = self.pool.get('product.uom').browse(cr, uid, product_uom, context=context)
        if uom.category_id.id != product.uom_id.category_id.id:
            res['warning'] = {'title': _('Warning'), 'message': _('The Product Unit of Measure you chose has a different category than in the product form.')}
            res['value'].update({'product_uom': product.uom_id.id})
        return res

    def onchange_location_id(self, cr, uid, ids, location_id=None):
        """ On change of location
        """
        return {'value': {'location_dest_id': location_id}}

    def button_dummy(self, cr, uid, ids, context=None):
        return True

    def onchange_partner_id(self, cr, uid, ids, part, address_id):
        """ On change of partner sets the values of partner address,
        partner invoice address and pricelist.
        @param part: Changed id of partner.
        @param address_id: Address id from current record.
        @return: Dictionary of values.
        """
        part_obj = self.pool.get('res.partner')
        pricelist_obj = self.pool.get('product.pricelist')
        if not part:
            return {'value': {
                        'address_id': False,
                        'partner_invoice_id': False,
                        'pricelist_id': pricelist_obj.search(cr, uid, [('type', '=', 'sale')])[0]
                    }
            }
        addr = part_obj.address_get(cr, uid, [part], ['delivery', 'invoice', 'default'])
        partner = part_obj.browse(cr, uid, part)
        pricelist = partner.property_product_pricelist and partner.property_product_pricelist.id or False
        return {'value': {
                    'address_id': addr['delivery'] or addr['default'],
                    'partner_invoice_id': addr['invoice'],
                    'pricelist_id': pricelist
                }
        }

    def action_cancel_draft(self, cr, uid, ids, *args):
        """ Cancels repair order when it is in 'Draft' state.
        @param *arg: Arguments
        @return: True
        """
        if not len(ids):
            return False
        mrp_line_obj = self.pool.get('mrp.repair.line')
        for repair in self.browse(cr, uid, ids):
            mrp_line_obj.write(cr, uid, [l.id for l in repair.operations], {'state': 'draft'})
        self.write(cr, uid, ids, {'state': 'draft'})
        return self.create_workflow(cr, uid, ids)

    def action_confirm(self, cr, uid, ids, *args):
        """ Repair order state is set to 'To be invoiced' when invoice method
        is 'Before repair' else state becomes 'Confirmed'.
        @param *arg: Arguments
        @return: True
        """
        mrp_line_obj = self.pool.get('mrp.repair.line')
        for o in self.browse(cr, uid, ids):
            if (o.invoice_method == 'b4repair'):
                self.write(cr, uid, [o.id], {'state': '2binvoiced'})
            else:
                self.write(cr, uid, [o.id], {'state': 'confirmed'})
                for line in o.operations:
                    if line.product_id.track_production:
                        raise osv.except_osv(_('Warning!'), _("Serial number is required for operation line with product '%s'") % (line.product_id.name))
                mrp_line_obj.write(cr, uid, [l.id for l in o.operations], {'state': 'confirmed'})
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        """ Cancels repair order.
        @return: True
        """
        mrp_line_obj = self.pool.get('mrp.repair.line')
        for repair in self.browse(cr, uid, ids, context=context):
            if not repair.invoiced:
                mrp_line_obj.write(cr, uid, [l.id for l in repair.operations], {'state': 'cancel'}, context=context)
            else:
                raise osv.except_osv(_('Warning!'), _('Repair order is already invoiced.'))
        return self.write(cr, uid, ids, {'state': 'cancel'})

    def wkf_invoice_create(self, cr, uid, ids, *args):
        self.action_invoice_create(cr, uid, ids)
        return True
        
    def action_fees_create(self, cr, uid, ids, group=False, context=None):
		
        res = {}
        invoices_group = {}
        inv_line_obj = self.pool.get('account.invoice.line')
        inv_obj = self.pool.get('account.invoice')
        repair_line_obj = self.pool.get('mrp.repair.line')
        repair_fee_obj = self.pool.get('mrp.repair.fee')
        move_pool = self.pool.get('account.move')
        line_ids = []
        period_pool = self.pool.get('account.period')
        
        for repair in self.browse(cr, uid, ids, context=context):
            res[repair.id] = False
            if repair.state in ('draft', 'cancel') or repair.invoice_id:
                continue
            if not (repair.partner_id.id and repair.partner_invoice_id.id):
                raise osv.except_osv(_('No partner!'), _('You have to select a Partner Invoice Address in the repair form!'))
            comment = repair.quotation_notes
            
            if repair.journal_id:
                for fee in repair.fees_lines:
                    if fee.to_invoice:
                        if group:
                            name = repair.name + '-' + fee.name
                        else:
                            name = fee.name
                        if not fee.product_id:
                            raise osv.except_osv(_('Warning!'), _('No product defined on Fees!'))

                        if fee.product_id.property_account_expense:
                            account_credit_id = fee.product_id.property_account_expense.id
                        elif fee.product_id.categ_id.property_account_expense_categ:
                            account_credit_id = fee.product_id.categ_id.property_account_expense_categ.id
                        else:
                            raise osv.except_osv(_('Error!'), _('No existe cuenta de gasto para producto "%s".') % fee.product_id.name)
                            
                        if fee.product_id.property_account_income:
                            account_debit_id = fee.product_id.property_account_income.id
                        elif fee.product_id.categ_id.property_account_income_categ:
                            account_debit_id = fee.product_id.categ_id.property_account_income_categ.id
                        else:
                            raise osv.except_osv(_('Error!'), _('No existe cuenta de ingreso/inventario para producto "%s".') % fee.product_id.name)
                            
                        search_periods = period_pool.find(cr, uid, fee.date_fee, context=context)
                        period_id = search_periods[0]
                        name = _('Orden de trabajo %s') % (repair.name)
                        move = {
							'narration': name,
							'date' : fee.date_fee,
							'ref': repair.name,
							'journal_id': repair.journal_id.id,
							'period_id': period_id,
						}
						
			debit_line = (0, 0, {
							'name': fee.product_id.name,
							'date': fee.date_fee,
							'partner_id': repair.partner_id.id,
							'account_id': debit_account_id,
							'journal_id': repair.journal_id.id,
							'period_id': period_id,
							'debit': fee.price_subtotal,
							'credit': 0.0,
							'analytic_account_id': False,
							'tax_code_id': False,
							'tax_amount': 0.0,
			})
			line_ids.append(debit_line)
						
                        credit_line = (0, 0, {
							'name': fee.product_id.name,
							'date': fee.date_fee,
							'partner_id': repair.partner_id.id,
							'account_id': debit_account_id,
							'journal_id': repair.journal_id.id,
							'period_id': period_id,
							'debit': 0.0,
							'credit': fee.price_subtotal,
							'analytic_account_id': False,
							'tax_code_id': False,
							'tax_amount': 0.0,
			})
			line_ids.append(credit_line)

                        invoice_fee_id = inv_line_obj.create(cr, uid, {
                            'invoice_id': inv_id,
                            'name': name,
                            'origin': repair.name,
                            'account_id': account_id,
                            'quantity': fee.product_uom_qty,
                            'invoice_line_tax_id': [(6, 0, [x.id for x in fee.tax_id])],
                            'uos_id': fee.product_uom.id,
                            'product_id': fee.product_id and fee.product_id.id or False,
                            'price_unit': fee.price_unit,
                            'price_subtotal': fee.product_uom_qty * fee.price_unit
                        })
                        repair_fee_obj.write(cr, uid, [fee.id], {'invoiced': True, 'invoice_line_id': invoice_fee_id})
                        
                        move.update({'line_id': line_ids})
			move_id = move_pool.create(cr, uid, move, context=context)
			#self.write(cr, uid, [slip.id], {'move_id': move_id, 'period_id' : period_id}, context=context)
						
                #res[repair.id] = inv_id
        return res
        
    def action_invoice_create(self, cr, uid, ids, group=False, context=None):
        """ Creates invoice(s) for repair order.
        @param group: It is set to true when group invoice is to be generated.
        @return: Invoice Ids.
        """
        res = {}
        invoices_group = {}
        inv_line_obj = self.pool.get('account.invoice.line')
        inv_obj = self.pool.get('account.invoice')
        repair_line_obj = self.pool.get('mrp.repair.line')
        repair_fee_obj = self.pool.get('mrp.repair.fee')
        move_pool = self.pool.get('account.move')
        line_ids = []
        period_pool = self.pool.get('account.period')
        
        for repair in self.browse(cr, uid, ids, context=context):
            res[repair.id] = False
            if repair.state in ('draft', 'cancel') or repair.invoice_id:
                continue
            if not (repair.partner_id.id and repair.partner_invoice_id.id):
                raise osv.except_osv(_('No partner!'), _('You have to select a Partner Invoice Address in the repair form!'))
            comment = repair.quotation_notes
            
            if repair.journal_id:
                for fee in repair.fees_lines:
                    if fee.to_invoice:
                        if group:
                            name = repair.name + '-' + fee.name
                        else:
                            name = fee.name
                        if not fee.product_id:
                            raise osv.except_osv(_('Warning!'), _('No product defined on Fees!'))

                        if fee.product_id.property_account_expense:
                            account_credit_id = fee.product_id.property_account_expense.id
                        elif fee.product_id.categ_id.property_account_expense_categ:
                            account_credit_id = fee.product_id.categ_id.property_account_expense_categ.id
                        else:
                            raise osv.except_osv(_('Error!'), _('No existe cuenta de gasto para producto "%s".') % fee.product_id.name)
                            
                        if fee.product_id.property_account_income:
                            account_debit_id = fee.product_id.property_account_income.id
                        elif fee.product_id.categ_id.property_account_income_categ:
                            account_debit_id = fee.product_id.categ_id.property_account_income_categ.id
                        else:
                            raise osv.except_osv(_('Error!'), _('No existe cuenta de ingreso/inventario para producto "%s".') % fee.product_id.name)
                            
                        search_periods = period_pool.find(cr, uid, fee.date_fee, context=context)
                        period_id = search_periods[0]
                        name = _('Orden de trabajo %s') % (repair.name)
                        move = {
							'narration': name,
							'date' : fee.date_fee,
							'ref': repair.name,
							'journal_id': repair.journal_id.id,
							'period_id': period_id,
						}
						
			debit_line = (0, 0, {
							'name': fee.product_id.name,
							'date': fee.date_fee,
							'partner_id': repair.partner_id.id,
							'account_id': account_debit_id,
							'journal_id': repair.journal_id.id,
							'period_id': period_id,
							'debit': fee.price_subtotal,
							'credit': 0.0,
							'analytic_account_id': False,
							'tax_code_id': False,
							'tax_amount': 0.0,
							'ot': repair.id,
			})
			line_ids.append(debit_line)
						
                        credit_line = (0, 0, {
							'name': fee.product_id.name,
							'date': fee.date_fee,
							'partner_id': repair.partner_id.id,
							'account_id': account_credit_id,
							'journal_id': repair.journal_id.id,
							'period_id': period_id,
							'debit': 0.0,
							'credit': fee.price_subtotal,
							'analytic_account_id': False,
							'tax_code_id': False,
							'tax_amount': 0.0,
							'ot': repair.id,
			})
			line_ids.append(credit_line)

                       
                        move.update({'line_id': line_ids})
			move_id = move_pool.create(cr, uid, move, context=context)
        return res

    def action_repair_ready(self, cr, uid, ids, context=None):
        """ Writes repair order state to 'Ready'
        @return: True
        """
        for repair in self.browse(cr, uid, ids, context=context):
            self.pool.get('mrp.repair.line').write(cr, uid, [l.id for
                    l in repair.operations], {'state': 'confirmed'}, context=context)
            self.write(cr, uid, [repair.id], {'state': 'ready'})
        return True

    def action_repair_start(self, cr, uid, ids, context=None):
        """ Writes repair order state to 'Under Repair'
        @return: True
        """
        repair_line = self.pool.get('mrp.repair.line')
        for repair in self.browse(cr, uid, ids, context=context):
            repair_line.write(cr, uid, [l.id for
                    l in repair.operations], {'state': 'confirmed'}, context=context)
            repair.write({'state': 'under_repair'})
        return True

    def action_repair_end(self, cr, uid, ids, context=None):
        """ Writes repair order state to 'To be invoiced' if invoice method is
        After repair else state is set to 'Ready'.
        @return: True
        """
        for order in self.browse(cr, uid, ids, context=context):
            val = {}
            val['repaired'] = True
            if (not order.invoiced and order.invoice_method == 'after_repair'):
                val['state'] = '2binvoiced'
            elif (not order.invoiced and order.invoice_method == 'b4repair'):
                val['state'] = 'ready'
            else:
                pass
            self.write(cr, uid, [order.id], val)
        return True

    def wkf_repair_done(self, cr, uid, ids, *args):
        self.action_repair_done(cr, uid, ids)
        return True

    def action_repair_done(self, cr, uid, ids, context=None):
        """ Creates stock move for operation and stock move for final product of repair order.
        @return: Move ids of final products
        """
        res = {}
        move_obj = self.pool.get('stock.move')
        repair_line_obj = self.pool.get('mrp.repair.line')
        for repair in self.browse(cr, uid, ids, context=context):
            move_ids = []
            for move in repair.operations:
                move_id = move_obj.create(cr, uid, {
                    'origin': repair.name,
                    'name': move.name,
                    'product_id': move.product_id.id,
                    'restrict_lot_id': move.lot_id.id,
                    'product_uom_qty': move.product_uom_qty,
                    'product_uom': move.product_uom.id,
                    'partner_id': repair.address_id and repair.address_id.id or False,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    'state': 'assigned',
                    'ot': repair.id,
                })
                move_ids.append(move_id)
                repair_line_obj.write(cr, uid, [move.id], {'move_id': move_id, 'state': 'done'}, context=context)
            move_id = move_obj.create(cr, uid, {
                'origin': repair.name,
                'name': repair.name,
                'product_id': repair.product_id.id,
                'product_uom': repair.product_uom.id or repair.product_id.uom_id.id,
                'product_uom_qty': repair.product_qty,
                'partner_id': repair.address_id and repair.address_id.id or False,
                'location_id': repair.location_id.id,
                'location_dest_id': repair.location_dest_id.id,
                'restrict_lot_id': repair.lot_id.id,
                'ot': repair.id,
            })
            move_ids.append(move_id)
            move_obj.action_done(cr, uid, move_ids, context=context)
            self.write(cr, uid, [repair.id], {'state': 'done', 'move_id': move_id}, context=context)
            res[repair.id] = move_id
        return res


class ProductChangeMixin(object):
    def product_id_change(self, cr, uid, ids, pricelist, product, uom=False,
                          product_uom_qty=0, partner_id=False, guarantee_limit=False, context=None):
        """ On change of product it sets product quantity, tax account, name,
        uom of product, unit price and price subtotal.
        @param pricelist: Pricelist of current record.
        @param product: Changed id of product.
        @param uom: UoM of current record.
        @param product_uom_qty: Quantity of current record.
        @param partner_id: Partner of current record.
        @param guarantee_limit: Guarantee limit of current record.
        @return: Dictionary of values and warning message.
        """
        result = {}
        warning = {}
        ctx = context and context.copy() or {}
        ctx['uom'] = uom

        if not product_uom_qty:
            product_uom_qty = 1
        result['product_uom_qty'] = product_uom_qty

        if product:
            product_obj = self.pool.get('product.product').browse(cr, uid, product, context=ctx)
            if partner_id:
                partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
                result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, partner.property_account_position, product_obj.taxes_id, context=ctx)

            result['name'] = product_obj.display_name
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id or False
            if not pricelist:
                warning = {
                    'title': _('No Pricelist!'),
                    'message':
                        _('You have to select a pricelist in the Repair form !\n'
                        'Please set one before choosing a product.')
                }
            else:
                price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                            product, product_uom_qty, partner_id, context=ctx)[pricelist]

                if price is False:
                    warning = {
                        'title': _('No valid pricelist line found !'),
                        'message':
                            _("Couldn't find a pricelist line matching this product and quantity.\n"
                            "You have to change either the product, the quantity or the pricelist.")
                     }
                else:
                    result.update({'price_unit': price, 'price_subtotal': price * product_uom_qty})

        return {'value': result, 'warning': warning}


class mrp_repair_line(osv.osv, ProductChangeMixin):
    _name = 'mrp.repair.line'
    _description = 'Repair Line'

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        """ Calculates amount.
        @param field_name: Name of field.
        @param arg: Argument
        @return: Dictionary of values.
        """
        res = {}
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.to_invoice and line.price_unit * line.product_uom_qty or 0
            cur = line.repair_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
        return res

    _columns = {
        'name': fields.char('Description', required=True),
        'repair_id': fields.many2one('mrp.repair', 'Repair Order Reference', ondelete='cascade', select=True),
        'type': fields.selection([('add', 'Add'), ('remove', 'Remove')], 'Type', required=True),
        'to_invoice': fields.boolean('To Invoice'),
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'invoiced': fields.boolean('Invoiced', readonly=True, copy=False),
        'price_unit': fields.float('Unit Price', required=False, digits_compute=dp.get_precision('Product Price')),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute=dp.get_precision('Account')),
        'tax_id': fields.many2many('account.tax', 'repair_operation_line_tax', 'repair_operation_line_id', 'tax_id', 'Taxes'),
        'product_uom_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'invoice_line_id': fields.many2one('account.invoice.line', 'Invoice Line', readonly=True, copy=False),
        'location_id': fields.many2one('stock.location', 'Source Location', required=True, select=True),
        'location_dest_id': fields.many2one('stock.location', 'Dest. Location', required=True, select=True),
        'move_id': fields.many2one('stock.move', 'Inventory Move', readonly=True, copy=False),
        'lot_id': fields.many2one('stock.production.lot', 'Lot'),
        'state': fields.selection([
                    ('draft', 'Draft'),
                    ('confirmed', 'Confirmed'),
                    ('done', 'Done'),
                    ('cancel', 'Cancelled')], 'Status', required=True, readonly=True, copy=False,
                    help=' * The \'Draft\' status is set automatically as draft when repair order in draft status. \
                        \n* The \'Confirmed\' status is set automatically as confirm when repair order in confirm status. \
                        \n* The \'Done\' status is set automatically when repair order is completed.\
                        \n* The \'Cancelled\' status is set automatically when user cancel repair order.'),
    }
    _defaults = {
        'state': lambda *a: 'draft',
        'product_uom_qty': lambda *a: 1,
    }

    def onchange_operation_type(self, cr, uid, ids, type, guarantee_limit, company_id=False, context=None):
        """ On change of operation type it sets source location, destination location
        and to invoice field.
        @param product: Changed operation type.
        @param guarantee_limit: Guarantee limit of current record.
        @return: Dictionary of values.
        """
        if not type:
            return {'value': {
                'location_id': False,
                'location_dest_id': False
                }}
        location_obj = self.pool.get('stock.location')
        warehouse_obj = self.pool.get('stock.warehouse')
        location_id = location_obj.search(cr, uid, [('usage', '=', 'production')], context=context)
        location_id = location_id and location_id[0] or False

        if type == 'add':
            # TOCHECK: Find stock location for user's company warehouse or
            # repair order's company's warehouse (company_id field is added in fix of lp:831583)
            args = company_id and [('company_id', '=', company_id)] or []
            warehouse_ids = warehouse_obj.search(cr, uid, args, context=context)
            stock_id = False
            if warehouse_ids:
                stock_id = warehouse_obj.browse(cr, uid, warehouse_ids[0], context=context).lot_stock_id.id
            to_invoice = (guarantee_limit and datetime.strptime(guarantee_limit, '%Y-%m-%d') < datetime.now())

            return {'value': {
                'to_invoice': to_invoice,
                'location_id': stock_id,
                'location_dest_id': location_id
                }}
        scrap_location_ids = location_obj.search(cr, uid, [('scrap_location', '=', True)], context=context)

        return {'value': {
                'to_invoice': False,
                'location_id': location_id,
                'location_dest_id': scrap_location_ids and scrap_location_ids[0] or False,
                }}


class mrp_repair_fee(osv.osv, ProductChangeMixin):
    _name = 'mrp.repair.fee'
    _description = 'Repair Fees Line'

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        """ Calculates amount.
        @param field_name: Name of field.
        @param arg: Argument
        @return: Dictionary of values.
        """
        res = {}
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.to_invoice and line.price_unit * line.product_uom_qty or 0
            cur = line.repair_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
        return res

    _columns = {
        'repair_id': fields.many2one('mrp.repair', 'Repair Order Reference', required=True, ondelete='cascade', select=True),
        'name': fields.char('Description', select=True, required=True),
        'product_id': fields.many2one('product.product', 'Product'),
        'product_uom_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
        'price_unit': fields.float('Unit Price', required=True),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute=dp.get_precision('Account')),
        'tax_id': fields.many2many('account.tax', 'repair_fee_line_tax', 'repair_fee_line_id', 'tax_id', 'Taxes'),
        'invoice_line_id': fields.many2one('account.invoice.line', 'Invoice Line', readonly=True, copy=False),
        'to_invoice': fields.boolean('To Invoice'),
        'invoiced': fields.boolean('Invoiced', readonly=True, copy=False),
        'date_fee': fields.date('Fecha', required=True, help="Fecha de la labor."),
        'user_id': fields.many2one('res.users', 'Responsable', help="Usuario responsable del servicio"),
        
    }

    _defaults = {
        'to_invoice': lambda *a: True,
#        'date_fee': lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
    }




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

