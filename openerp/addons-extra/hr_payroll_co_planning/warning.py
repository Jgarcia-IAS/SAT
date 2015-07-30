# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2013 Interconsulting S.A. e Innovatecsa SAS.  (http://interconsulting.com.co).
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

WARNING_TYPES = [('warning','Warning'),('info','Information'),('error','Error')]

class warning(osv.osv):
 _name = 'warning'
 _description = 'warning'
 _columns = {
   'type': fields.selection(WARNING_TYPES, string='Type', readonly=True),
   'title': fields.char(string="Title", size=100, readonly=True),
   'message': fields.text(string="Message", readonly=True),
 } 
 _req_name = 'title'

 def _get_view_id(self, cr, uid):
    """Get the view id
    @return: view id, or False if no view found
    """
    res = self.pool.get('ir.model.data').get_object_reference(cr, uid,'hr_payroll_co_planning','warning_form')
    return res and res[1] or False

 def message(self, cr, uid, id, context):
     message = self.browse(cr, uid, id)
     message_type = [t[1]for t in WARNING_TYPES if message.type == t[0]][0] 
     print '%s: %s' % (_(message_type), _(message.title))
     res = {
        'name': '%s: %s' % (_(message_type), _(message.title)),
        'view_type': 'form',
        'view_mode': 'form',
        'view_id': self._get_view_id(cr, uid),
        'res_model': 'warning',
        'domain': [],
        'context': context,
        'type': 'ir.actions.act_window',
        'target': 'new',
        'res_id': message.id
     } 
     return res

 def warning(self, cr, uid, title, message, context=None):
     id = self.create(cr, uid, {'title': title, 'message': message, 'type': 'warning'})
     res = self.message(cr, uid, id, context)
     return res

 def info(self, cr, uid, title, message, context=None):
     id = self.create(cr, uid, {'title': title, 'message': message, 'type': 'info'})
     res = self.message(cr, uid, id, context)
     return res

 def error(self, cr, uid, title, message, context=None):
     id = self.create(cr, uid, {'title': title, 'message': message, 'type': 'error'})
     res = self.message(cr, uid, id, context)
     return res
