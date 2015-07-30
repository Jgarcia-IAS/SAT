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
    "name": "Colombian Accounting Localization Basics  by I.A.S. INGENIERÍA, APLICACIONES Y SOFTWARE",
    "version": "1.0",
    "description": """
Profile and basics to colombian accounting localization
    
Localización contable y tributaria básica para Colombia
    """,
    "author": "I.A.S. Ingenieria, Aplicaciones y Software",
    "website": "http://www.ias.com.co",
    "category": "Localisation/Profile",
    "depends": [
	    "account_chart",
        "account_payment",
	    "l10n_co_chart",
        "l10n_co_vat",
	    "base_translate_tools",
	    "base_table",
	],
    "data":[
	    "account_data.xml",
        "account_report.xml",
        "invoice_view.xml",
	],
    "demo_xml": [
	],
    "update_xml": [
	],
    "active": False,
    "installable": True,
    "certificate" : "",
    'images': [],
}
