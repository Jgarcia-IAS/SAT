# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
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
    "name": "Colombian Accounting Localization - Magnetic Mediums",
    "version": "1.0",
    "description": """
Medios magneticos para Colombia
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Localisation/Profile",
    "depends": [

         "account_asset",
         "analytic",
         "base_vat",
         "stock",
         "l10n_pe",
         "l10n_pe_vat",
	     "base_translate_tools",
	     "base_table",
         "base_person",
	],
    "data":[
          "security/ir.model.access.csv",
          "security/security.xml",
          "sunat_view.xml",
          "table_view.xml",
          "base.table.csv",
          "base.element.csv",
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
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
