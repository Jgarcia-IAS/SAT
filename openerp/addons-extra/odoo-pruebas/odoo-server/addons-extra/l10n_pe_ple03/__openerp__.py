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
    "name": "Peruvian Accounting Localization - PLE03",
    "version": "1.0",
    "description": """
Programa de Libros Electrónicos

3. Libro de Inventarios y Balances
    """,
    "author": "NUMA Extreme Systems for Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Localisation/Profile",
    "depends": [
        "account",
        "account_asset",
	    "l10n_pe",
	    "base_translate_tools",
	    "base_table",
        "l10n_pe_ple",
        "product",
	],
    "data":[
          "security/ir.model.access.csv",
          "security/security.xml",
#          "sunat_3_1_view.xml",
#          "sunat_3_2_view.xml",
#          "sunat_3_3_view.xml",
#          "sunat_3_4_view.xml",
#          "sunat_3_5_view.xml",
#          "sunat_3_6_view.xml",
#          "sunat_3_7_view.xml",
#          "sunat_3_8_view.xml",
#          "sunat_3_9_view.xml",
#          "sunat_3_11_view.xml",
#          "sunat_3_12_view.xml",
#          "sunat_3_13_view.xml",
#          "sunat_3_14_view.xml",
#          "sunat_3_15_view.xml",
#          "sunat_3_16_1_view.xml",
#          "sunat_3_16_2_view.xml",
#          "sunat_3_17_view.xml",
#          "sunat_3_18_view.xml",
#          "sunat_3_19_view.xml",
#          "sunat_3_20_view.xml",
#          "sunat_3_21_view.xml",
#          "sunat_3_22_view.xml",
#          "sunat_3_23_view.xml",
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
