# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2011 NUMA Extreme Systems (www.numaes.com) for Cubic ERP - Teradata SAC. (http://cubicerp.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp.osv import fields, osv

class ple_3_9 (osv.Model):
    _name = "l10n_pe.ple_3_9"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_3_9', 'ple_3_9_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_3_9')

        #Remove existing lines
        ple = self.browse(cr, uid, ids[0], context=context)
        cmds = []
        for line in ple.lines_ids:
            cmds.append((2, line.id))
        if cmds:
            ple.write({'lines_ids': cmds}, context=context)
        ple.refresh()
        
        # Get the list of involved movements
        period_ids = self.get_all_periods_up_to (cr, uid, ids, ple.period_id.id)
        move_lines = self.get_move_lines (cr, uid, period_ids, '3_9', ple.company_id.id, context=context)

        #Get the list of involved accounts
        account_ids = list(set([aml.account_id.id for aml in move_lines]))
        #Get the list of involved products
        product_ids = list(set([aml.product_id.id for aml in move_lines]))
        
        for product_id in product_ids:
            vals = {
                'ple_3_9_id': ple.id,
                'product_id': product_id,
                'account_id': account_ids and account_ids[0],
            }
            vals.update(ple_line_obj.onchange_account_id(cr, uid, [], account_ids and account_ids[0], context=context)['value'])
            vals.update(ple_line_obj.onchange_product_id(cr, uid, [], product_id, ple.period_id.id, context=context)['value'])
            ple_line_obj.create(cr, uid, vals, context=context)

        return True

    def action_renumber (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        next_seq = 1
        for line in sorted(ple.lines_ids, key=lambda l: l.operation_date_3):
            line.write ({'sequence': next_seq}, context=context)
            next_seq += 1

        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_3_9',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str(r.sequence),
                self.convert_date (r.start_date_3),
                self.convert_str(r.account_code_4),
                self.convert_str(r.product_description_5),
                self.convert_amount(r.accounting_value_6),
                self.convert_amount(r.acumulated_dep_7),
                self.convert_str(r.operation_state_8),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_3_9.txt"

class ple_line_3_9 (osv.Model):
    _name = 'l10n_pe.ple_line_3_9'
    _inherit = 'l10n_pe.ple_line'
    
    _columns = {
        'ple_3_9_id': fields.many2one('l10n_pe.ple_3_9', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_3_9_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_3_9_id', 'company_id', string='Company', type="many2one", relation="res.company"),
        'product_id': fields.many2one('product.product', 'Product', on_delete="restrict"),

        'start_date_3': fields.date ('Start date', required=True, help="Fecha de inicio de la operación"),
        'account_code_4': fields.char("Account code", size=24, help="Código de la cuenta contable asociada a la obligación y desagregado en subcuentas al nivel máximo de dígitos utilizado, según la estructura 3.21"),
        'product_description_5': fields.char("Product description", size=40, help="Descripción del intangible"),
        'accounting_value_6': fields.float('Accounting value', digits=(12,2), help="Valor contable del intangible"),
        'acumulated_dep_7': fields.float('Acumulated depreciation', digits=(12,2), help="Amortización contable acumulada"),
        'operation_state_8': fields.selection ([
                                ('1', '1'),
                                ('8', '8'),
                                ('9', '9'),
                            ], 'Operation state', required=True, help="""
Registrar '1' cuando la operación corresponde al periodo, 
'8' cuando la operación corresponde a un periodo anterior y NO ha sido anotada en dicho periodo o
'9' cuando la operación corresponde a un periodo anterior y SI ha sido anotada en dicho periodo."""),
    }
    
    _order = 'sequence'
    
    _defaults = {
        'operation_state_8': '1',
    }
    
    def onchange_product_id (self, cr, uid, ids, product_id, period_id, context=None):
        vals = {}
        if product_id:
            ple_3_9_obj = self.pool.get('l10n_pe.ple_3_9')
            product_obj = self.pool.get('product.product')
            
            lines = ple_3_9_obj.get_move_lines(cr, uid,
                                                ple_3_9_obj.get_all_periods_up_to(period_id, context=context),
                                                '3_9',
                                                product_id=product_id,
                                                context=context)
            lines.sort(key=lambda l: (l.period_id.date_start))
            
            initial_balance = 0.0
            initial_qty = 0.0
            final_balance = 0.0
            final_qty = 0.0
            period = period_obj.browse(cr, uid, period_id, context=context)
            if lines:
                for l in lines:
                    if l.date_start >= period.date_start:
                        final_balance += (l.credit - l.debit)
                        final_quantity += l.product_qty
                    else:
                        initial_balance += (l.credit - l.debit)
                        final_quantity += l.product_qty
                final_balance += initial_balance
                final_quantity += initial_quantity

            product = product_obj.browse(cr, uid, product_id, context=context)
            vals['product_description_5'] = product.name
            vals['accounting_value_6'] = final_balance
            vals['acumulated_dep_7'] = product.standard_price and product.sunat_acum_depreciation * final_balance / product.standard_price or 0.0
            return {'value': vals}
        else:
            return False

    def onchange_account_id (self, cr, uid, ids, account_id, context=None):
        vals = {}
        if account_id:
            account_obj = self.pool.get('account.account')
            account = account_obj.browse(cr, uid, account_id, context=context)
            vals['account_code_4'] = account.code
            return {'value': vals}
        else:
            return False

class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('3_9', '3.9 Saldo de Cuentas de intangibles'))
        return sorted(rep_types, key=lambda e: e[0])
