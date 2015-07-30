# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 I.A.S. INGENIERÍA, APLICACIONES Y SOFTWARE Johan Alejandro Olano (<http:http://www.ias.com.co).
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
    'name': 'Contabilidad Colombia Extra  by I.A.S. INGENIERÍA, APLICACIONES Y SOFTWARE',
    'version': '1.0',
    "author": "I.A.S. Ingenieria, Aplicaciones y Software",
    "website": "http://www.ias.com.co",
    'category': 'Account',
    'depends': ['account','sale','l10n_mx_account_tax_category','stock'],
    'demo': [],
    'description': """
Este módulo permite adicionar funcionalidades para la localización Colombiana
=============================================================================
Collaborators:
   - Johan Alejandro Olano <jolano@ias.com.co>

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
