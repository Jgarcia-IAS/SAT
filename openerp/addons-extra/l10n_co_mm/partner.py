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

from osv import osv, fields
from tools.translate import _

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
        
#    def create (self, cr, uid, vals, context=None):
#        new_vals = vals.copy()
#        if vals.get('doc_number',False) and not vals.get('doc_number',False):
#            new_vals['doc_number'] = vals['doc_number']
#        return super (res_partner, self).create (cr, uid, new_vals, context=context)
        
#    def write (self, cr, uid, ids, vals, context=None):
#        new_vals = vals.copy()
#        if vals.get('doc_number') and not vals.get('doc_number'):
#            new_vals['doc_number'] = vals['doc_number']
#        return super (res_partner, self).write (cr, uid, ids, new_vals, context=context)
        
res_partner()
