# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#     Copyright (C) 2013 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
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
from openerp.tools.translate import _ 
import time


class etl_server(osv.Model):
    _name = 'etl.server'
    _description = 'ETL Server'
    _columns = {
            'name': fields.char('Name', size=128, required=True, translate=True, select=True),
            'type': fields.selection([('odbc','ODBC'), ('xmlrpc','XML-RPC')], 'Server Type'),
            'str_connection': fields.char('String Connection', size=2048),
            'active': fields.boolean('Active'),     
        }
    _defaults = {
            'active' : True,
        }


class etl_source(osv.Model):
    _name = 'etl.source'
    _description = 'ETL Source'
    _columns = {
            'name': fields.char('Name', size=256, required=True, translate=True, select=True),
            'server_id': fields.many2one('etl.server',string='Server'),
            'query': fields.text('Query'),
            'pk_definition': fields.char('PK Definition',1024),
            'state': fields.selection([('draft','Draft'),('active','Active'),('cancel','Cancel')],'State'),     
        }
    _defaults = {
            'state' : 'draft',
        }


class etl_mapping(osv.Model):
    _name = 'etl.mapping'
    _description = 'ETL Mapping'
    _columns = {
            'name': fields.char('Name', size=512, required=True, translate=True, select=True),
            'source_id': fields.many2one('etl.source',string='Source'),
            'pk_source': fields.char('PK Source',512,help="Primary Key in the source of data"),
            'model_id': fields.many2one('ir.model',string='Model'),
            'id_model': fields.integer('Id of Model'),
            'state': fields.selection([('inserted','Inserted'),('updated','Updated'),('deleted','Deleted')],'State'),
            'mapping_job_ids': fields.one2many('etl.mapping.job','mapping_id',string='Mapping Job'),
        }
    _defaults = {
            'state' : 'inserted',
        }


class etl_mapping_job(osv.Model):
    _name = 'etl.mapping.job'
    _description = 'ETL Mapping Job'
    _columns = {
            'name': fields.char('Name', size=512, required=True, translate=True, select=True),
            'mapping_id': fields.many2one('etl.mapping',string='Mapping'),
            'job_id': fields.many2one('etl.job',string='Job'),
            'date': fields.date('Date'),
            'last_log': fields.text('Last Log'),
            'state': fields.selection([('new','New'),('ok','Ok'),('fail','Fail')],'State'),     
        }
    _defaults = {
            'state' : 'new',
        }


class etl_job(osv.Model):
    _name = 'etl.job'
    _description = 'ETL Job'
    _columns = {
            'name': fields.char('Name', size=512, required=True, translate=True, select=True),
            'mapping_job_ids': fields.one2many('etl.mapping.job','job_id',string='Mapping Job'),
            'date': fields.date('Date'),
            'state': fields.selection([('new','New'),('ok','Ok'),('fail','Fail')],'State'),     
        }
    _defaults = {
            'state' : 'new',
        }

