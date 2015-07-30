# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2011 NUMA Extreme Systems (www.numaes.com) 
#                    for Cubic ERP - Teradata SAC. (http://cubicerp.com).
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
from openerp.tools.translate import _

class account_account(osv.Model):
    _inherit = "account.account"

    def _get_financial_catalog_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_22', context=context)
    
    _columns = {
        'bank_account_id': fields.many2one("res.partner.bank", "Related bank account", on_delete="restrict"),
        'sunat_financial_catalog': fields.selection(_get_financial_catalog_selection, "Financial catalog", 
                                                    help="Catálogo de estados financieros, according to SUNAT Table 22"),    
    }

class journal(osv.Model):
    _inherit = "account.journal"
    
    def _get_payment_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_01', context=context)
    
    def _get_payment_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_10', context=context)
    
    def _get_customs_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_11', context=context)
    
    def _get_operation_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_12', context=context)
    
    _columns = {
        'sunat_payment_code': fields.selection(_get_payment_code_selection, "Payment code", 
                                               help="Medio de pago, according to SUNAT Table 01"),    
        'sunat_payment_type': fields.selection(_get_payment_type_selection, "Payment type", 
                                               help="Tipo de comprobante de pago o documento, according to SUNAT Table 10"),    
        'sunat_customs_code': fields.selection(_get_customs_code_selection, "Customs code", 
                                               help="Código de aduana, according to SUNAT Table 11"),    
        'sunat_operation_type': fields.selection(_get_operation_type_selection, "Operation type", 
                                                 help="Tipo de operación, according to SUNAT Table 12"),    
    }
    
class res_partner_bank(osv.Model):
    _inherit = "res.bank"

    def _get_bank_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_03', context=context)
    
    _columns = {
        'sunat_bank_code': fields.selection(_get_bank_code_selection, "Bank code", 
                                            help="Entidad financiera, according to SUNAT Table 03"),    
    }

class res_currency(osv.Model):
    _inherit = "res.currency"

    def _get_sunat_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_04', context=context)
    
    _columns = {
        'sunat_code': fields.selection(_get_sunat_code_selection, "SUNAT code", 
                                       help="Tipo de moneda, according to SUNAT Table 04"),    
    }

class product_category(osv.Model):
    _inherit = "product.category"

    def _get_sunat_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_05', context=context)

    def _get_sunat_inventory_type(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for pc in self.read(cr, uid, ids, ['sunat_code', 'parent_id'], context=context):
            if pc['sunat_code']:
                res[pc['id']] = pc['sunat_code']
            elif pc['parent_id']:
                parent = self.browse(cr, uid, pc['parent_id'] [0], context=context)
                res[pc['id']] = parent.sunat_inventory_type
            else:
                res[pc['id']] = False
        return res
        
    def _get_sunat_inventory_display_type(self, cr, uid, ids, fields, args, context=None):
        res = {}
        vals = self._get_sunat_inventory_type(cr, uid, ids, fields, args, context=context)
        selection = {}
        for x in self._get_sunat_code_selection(cr, uid, context=context): selection[x[0]]=x[1] 
        for k in vals.keys():
            if vals[k]:
                res[k] = selection[vals[k]]
            else:
                res[k] = ''
        return res
        
    _columns = {
        'sunat_code': fields.selection(_get_sunat_code_selection, "SUNAT inventory type code", 
                                       help="Tipo de existencia, according to SUNAT Table 05"),    
        'sunat_inventory_type': fields.function(_get_sunat_inventory_type, string="Inventory type", type="char", 
                                                 help="SUNAT code, for this category or the first in parent's chain"),
        'sunat_inventory_display_type': fields.function(_get_sunat_inventory_display_type, string="Inventory type", type="char", 
                                                 help="SUNAT code, for this category or the first in parent's chain"),
    }

class product_uom(osv.Model):
    _inherit = "product.uom"
        
    def _get_sunat_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_06', context=context)

    _columns = {
        'sunat_code': fields.selection(_get_sunat_code_selection, "SUNAT code", 
                                       help="Tipo de existencia, according to SUNAT Table 06"),    
    }

class product_template(osv.Model):
    _inherit = "product.template"

    def _get_sunat_valuation_method_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_13', context=context)

    def _get_sunat_title_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_15', context=context)

    def _get_sunat_share_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_16', context=context)

    def _get_sunat_asset_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_18', context=context)

    def _get_sunat_asset_state_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_19', context=context)

    def _get_sunat_asset_depreciation_method_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_20', context=context)

    _columns = {
        'sunat_title_type': fields.selection(_get_sunat_title_type_selection, "SUNAT title type", 
                                             help="Tipo de título, according to SUNAT Table 15"),    
        'sunat_share_type': fields.selection(_get_sunat_share_type_selection, "SUNAT share type", 
                                             help="Tipo de acciones o participaciones, according to SUNAT Table 16"),    
        'sunat_valuation_method': fields.selection(_get_sunat_valuation_method_selection, "SUNAT valuation method", 
                                                   help="Método de valuación, according to SUNAT Table 13"),
        'sunat_asset_type': fields.selection(_get_sunat_asset_type_selection, "SUNAT asset type", 
                                             help="Tipo de activo fijo, according to SUNAT Table 18"),    
        'sunat_asset_state': fields.selection(_get_sunat_asset_state_selection, "SUNAT asset state", 
                                             help="Estado del activo fijo, according to SUNAT Table 19"),    
        'sunat_depreciation_method': fields.selection(_get_sunat_asset_depreciation_method_selection, "SUNAT depreciation method", 
                                             help="Método de depreciación, according to SUNAT Table 20"),    
    }

class product_product(osv.Model):
    _inherit = "product.product"
    
    _columns = {
        'sunat_nominal_value': fields.float('Title/share nominal value x unit', digits=(14,2)),
        'sunat_acum_depreciation': fields.float('Acumulated depreciaton x unit', digits=(14,2)),
    }

class stock_picking(osv.Model):
    _inherit = "stock.picking"
    
    def _get_sunat_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_10', context=context)

    def _get_sunat_op_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_12', context=context)

    _columns = {
        'sunat_doc_type': fields.selection(_get_sunat_doc_type_selection, "SUNAT document type", 
                                             help="Tipo de documento, according to SUNAT Table 10"),    
        'sunat_op_type': fields.selection(_get_sunat_op_type_selection, "SUNAT operation type", 
                                             help="Tipo de operación, according to SUNAT Table 12"),    
    }
class res_company(osv.Model):
    _inherit = "res.company"

    def _get_sunat_accounting_plan_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_17', context=context)

    _columns = {
        'sunat_accounting_plan': fields.selection(_get_sunat_accounting_plan_selection, "SUNAT accounting plan", 
                                             help="Plan de cuentas, according to SUNAT Table 17"),    
    }

class account_asset_category(osv.Model):
    _inherit = "account.asset.category"

    def _get_sunat_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_13', context=context)

    _columns = {
        'sunat_code': fields.selection(_get_sunat_code_selection, "SUNAT code", 
                                       help="Catálogo de existencias, according to SUNAT Table 13"),    
    }

class account_asset_asset(osv.Model):
    _inherit = "account.asset.asset"

    def _get_sunat_asset_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_18', context=context)

    def _get_sunat_asset_state_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_19', context=context)

    def _get_sunat_asset_depreciation_method_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_20', context=context)

    _columns = {
        'sunat_asset_type': fields.selection(_get_sunat_asset_type_selection, "SUNAT asset type", 
                                             help="Tipo de activo fijo, according to SUNAT Table 18"),    
        'sunat_asset_state': fields.selection(_get_sunat_asset_state_selection, "SUNAT asset state", 
                                             help="Estado del activo fijo, according to SUNAT Table 19"),    
        'sunat_depreciation_method': fields.selection(_get_sunat_asset_depreciation_method_selection, "SUNAT depreciation method", 
                                             help="Método de depreciación, according to SUNAT Table 20"),    
    }

class account_analytic_account(osv.Model):
    _inherit = "account.analytic.account"

    def _get_sunat_production_grouping_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_21', context=context)

    _columns = {
        'sunat_production_grouping': fields.selection(_get_sunat_production_grouping_selection, "SUNAT production grouping", 
                                             help="Código de agrupamiento del costo de producción valorizado anual, according to SUNAT Table 21"),    
    }

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    def _get_doc_types (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_02', context=context)
    
    _columns = {
        'doc_type': fields.selection (_get_doc_types, 'Document type'),
        'doc_number': fields.char('Document Number',32,select=1),
    }
    _sql_constraints = [('doc_number_unique','unique(doc_number)','The document number must be unique!'),]
    
    def vat_change(self, cr, uid, ids, value, context=None):
        res = super (res_partner, self).vat_change(cr, uid, ids, value, context=context)
        if not res:
            res = {'value':{}}
            
        res['value']['doc_type'] = '6'
        res['value']['doc_number'] = value and value[2:]
        return res

    def onchange_is_company (self, cr, uid, ids, is_company, doc_type, context=None):
        res = super (res_partner, self).onchange_type(cr, uid, ids, is_company, context=context)
        res['value']['doc_type'] = is_company and '6' or '1'
#        if is_company and doc_type != '6':
#            raise osv.except_osv (_('Value error'),
#                   _('Companies should be identified by RUC only! Please check!'))
        return res
        
    def onchange_doc (self, cr, uid, ids, doc_type, doc_number, is_company, context=None):
        res = {'value':{},'warning':{}}

        if doc_number and is_company and (doc_type != '6'):
            res['warning']['title'] = _('Value error')
            res['warning']['message'] = _('Companies should be identified by RUC only! Please check!')
            
        if doc_number and doc_type == '0':
            if (not doc_number) or len (doc_number) > 15:
                res['warning']['title'] = _('Value error')
                res['warning']['message'] = _('Document number should be alfanumeric, not longer than 15 characters! Please check!')
        elif doc_number and doc_type == '1':
            if (not doc_number) or len (doc_number) != 8 or not doc_number.isdigit():
                res['warning']['title'] = _('Value error')
                res['warning']['message'] = _('Libreta electoral or DNI should be numeric, exactly 8 numbers long! Please check!')
        elif doc_number and doc_type == '4':
            if (not doc_number) or len (doc_number) > 12:
                res['warning']['title'] = _('Value error')
                res['warning']['message'] = _('Carnet de extranjeria should be alfanumeric, not longer than 12 characters! Please check!')
        elif doc_number and doc_type == '6':
            if (not doc_number) or (len (doc_number) < 8 or len (doc_number) > 11) or not doc_number.isdigit():
                res['warning']['title'] = _('Value error')
                res['warning']['message'] = _('RUC should be numeric, 8-11 numbers long! Please check!')
            res['value']['vat'] = doc_number and 'PE' + doc_number
                       
        elif doc_number and doc_type == '7':
            if (not doc_number) or len (doc_number) > 12:
                res['warning']['title'] = _('Value error')
                res['warning']['message'] = _('Pasaporte should be alfanumeric, not longer than 12 characters! Please check!')
        elif doc_number and doc_type == 'A':
            if (not doc_number) or len (doc_number) != 15 or not doc_number.isdigit():
                res['warning']['title'] = _('Value error')
                res['warning']['message'] = _('Cedula diplomatica should be numeric, exactly 15 numbers long! Please check!')

        return res
        
