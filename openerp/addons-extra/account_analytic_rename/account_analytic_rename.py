# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Interconsulting S.A e Innovatecsa SAS.
#    (<http://www.interconsulting.com.co).
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
from openerp.osv import osv, fields
#from openerp.tools import debug
from openerp.tools.translate import _

class account_analytic_pais(osv.osv):
	_name = "account.analytic.pais"
	_columns = {
		'name': fields.char('Name',size=100),
		'code': fields.char('Code',size=4),
	}
class account_analytic_aeropuerto(osv.osv):
	_name = "account.analytic.aeropuerto"
	_columns = {
		'name': fields.char('Name',size=100),
		'code': fields.char('Code',size=4),
	}
class account_analytic_cliente(osv.osv):
	_name = "account.analytic.cliente"
	_columns = {
		'name': fields.char('Name',size=100),
		'code': fields.char('Code',size=4),
	}
class account_analytic_unidad_de_negocio(osv.osv):
	_name = "account.analytic.unidad_de_negocio"
	_columns = {
		'name': fields.char('Name',size=100),
		'code': fields.char('Code',size=4),
	}
class account_analytic_servicio(osv.osv):
	_name = "account.analytic.servicio"
	_columns = {
		'name': fields.char('Name',size=100),
		'code': fields.char('Code',size=4),
	}


class account_analytic_account(osv.osv):
	_name = "account.analytic.account"
	_inherit = "account.analytic.account"


        def _get_default_full_name(self, cr, uid, ids, name, arg, context=None):
            records=self.browse(cr,uid,ids)
            result = dict((x,'') for x in ids)

            for r in records:
                if(r.pais and r.aeropuerto and r.cliente and r.unidad_de_negocio and r.servicio):
                  result[r.id] = "%s %s %s %s %s" % \
                     (r.pais.code + '/' or '', r.aeropuerto.code + '/' or '',
                      r.cliente.code + '/' or '', r.unidad_de_negocio.code + '/' or '',
                      r.servicio.code + '/' or ''
                     )

                  cr.execute(""" UPDATE account_analytic_account SET name = %s  || '/'  || %s || '/'  || %s || '/'  || %s || '/'  || %s WHERE id = %s""" , (r.pais.code, r.aeropuerto.code,r.cliente.code,r.unidad_de_negocio.code,r.servicio.code,r.id,))
                

            return result


	
	def name_get(self, cr, uid, ids, context=None):
		if not ids:
			return []
		res = []
		for obj_account in self.browse(cr,uid,ids):
			data = []
			account = obj_account.parent_id
			while account:
				data.insert(0,(account.full_name or account.name))
				account = account.parent_id
			data.append(obj_account.name)
			data = '/'.join(data)
			res.append((obj_account.id, data))  
		return res
		
	_columns = {
                'full_name': fields.function(_get_default_full_name, type='char', string='Full Name', size=24 , track_visibility='always'),
                'pais': fields.many2one('account.analytic.pais', 'País'),
                'aeropuerto': fields.many2one('account.analytic.aeropuerto', 'Aeropuerto'),
                'cliente': fields.many2one('account.analytic.cliente', 'Cliente'),
                'unidad_de_negocio': fields.many2one('account.analytic.unidad_de_negocio', 'Unidad de negocio'),
                'servicio': fields.many2one('account.analytic.servicio', 'Servicio'),
	}

#        _defaults = {
#
#            'full_name': _get_default_full_name,
#        }

account_analytic_account()
