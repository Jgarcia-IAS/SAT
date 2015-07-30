# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2012 Cubic ERP - Teradata SAC. (http://cubicerp.com).
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

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    _columns = {
            'nit': fields.char('NIT', size=9),
            'nit_validate': fields.char('CV', size=1),
            'nit_complete': fields.char('NIT Completo', size=11),


        }


    def verification_nit(self, cr, uid, ids, nit, nit_validate, context=None):
        res = {'value':{}}
        res['value']['vat'] = (nit and ('CO'+nit) or '') + (nit_validate and (nit_validate+'') or '')
        res['value']['nit_complete'] = (nit and (''+nit) or '') + (nit_validate and ('-'+nit_validate+'') or '')
        return res



    def nit_complete(self, cr, uid, ids, nit, nit_validate, context=None):
        res = {'value':{}}
        res['value']['vat'] = (nit and ('CO'+nit) or '') + (nit_validate and (nit_validate+'') or '')
        res['value']['nit_complete'] = (nit and (''+nit) or '') + (nit_validate and ('-'+nit_validate+'') or '')
        return res

res_partner()
