##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2013 Opensystem Colombia (<http://opensystem.co>).
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
{
    'name': 'Contabilidad Colombia Extra',
    'version': '1.0',
    'author': 'Opensystem Colombia SAS y Aliados',
    'category': 'Account',
    'depends': ['account','sale','l10n_mx_account_tax_category'],
    'demo': [],
    'description': """
Este módulo permite adicionar funcionalidades para la localización Colombiana
=============================================================================

Las funcionalidades implementadas son:
-----------------------------------------------
    * Parametrizar y filtrar por tipo de comprobante de ingreso o egreso
    * Parametrizar el impuesto si se calcula o no en el pedido de venta
    * 
    * 
    """,
    'data': [
       'account_tax_view.xml', 
       'account_journal_view.xml', 
       'sale_order_view.xml',
       'partner_view.xml',
       'account_invoice_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'images': [],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
