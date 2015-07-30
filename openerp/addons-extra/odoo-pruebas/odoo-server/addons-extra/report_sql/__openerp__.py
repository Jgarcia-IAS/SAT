# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Interconsulting S.A e Innovatecsa SAS.
#    (<http://www.interconsulting.com.co).
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
    "name": "Report execute SQL sentence",
    "version": "1.0",
    "description": """
This module execute a sql query over de database and export it into excel file. 

    """,
    "author": "Interconsulting S.A. e Innovatecsa SAS.",
    "website": "http://www.interconsulting.com.co",
    'images' : ['static/description/icon.png',
                'static/description/sql01.jpg',
                'static/description/sql02.jpg',
                'static/description/sql03.jpg',
                'static/description/sql04.jpg',
                'static/description/sql05.jpg',
                'static/description/sql06.jpg',
                'static/description/sql05_06.jpg',
],
    "category": "Financial",
    "depends": [

			],
	"data":[
		    "report_view.xml",
			],
    "demo_xml": [
			],
    "active": False,
    "installable": True,
    "certificate" : "",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
