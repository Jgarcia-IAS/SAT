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
    'name': 'account_vat_declaration',
    'version': '0.1',
    "author": "I.A.S. Ingenieria, Aplicaciones y Software",
    "website": "http://www.ias.com.co",
    'description': """
        Account VAT Declaration
        
        Powered by Cubic ERP http://cubicERP.com
        
        Cubic ERP Adds:
         - Support to base_table
         - filter by journal code in lines
         - Other fixes
         - Migrated to v7.0
         - Multicompany
    """,
    'depends': [
        'account',
        'base_table',
    ],
    'init_xml': [
    ],
    'demo_xml': [
    ],
    'update_xml': [
        'account_vat_declaration_view.xml',
        'workflow/account_vat_decl.xml',
        'wizard/account_vat_declaration_wizard_view.xml',
    ],
    'active': False,
    'installable': True,
}
