##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

class account_tax(osv.osv):
	_name = 'account.tax'
	_inherit = 'account.tax'
	_columns = {
		'in_order': fields.boolean('Incluir en pedido de venta', help='Si esta chequeado se incluye en el calculo de impuestos en la orden o pedido'),
	}
    
	_defaults = {
	'in_order' : 0,
    }

account_tax()


class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
        'is_taxed' : fields.boolean('Es gravado con IVA', help="Especificar si al producto se le aplica IVA"),
    }
    
    _defaults = {
	    'is_taxed' : True,
	}
product_product()

class account_tax_category(osv.Model):
    _inherit = 'account.tax.category'

    _columns = {
        'type': fields.selection([('IVA', 'Impuesto a las Ventas - IVA'), ('RTE', 'Retencion en la Fuente'), ('RVA', 'Retencion de IVA'), ('CRE', 'Impuesto a la Equidad - CREE'),('ICA', 'Industria y Comercio - ICA'),('RCA', 'Retencion de ICA')], 'Tipo de impuesto', required=True, help="El tipo de impuesto agrupa por categoria los impuestos para totalizarlos por tipo"),                
    }     
     
    _defaults = {
	    'type' : 'IVA',
	}    

