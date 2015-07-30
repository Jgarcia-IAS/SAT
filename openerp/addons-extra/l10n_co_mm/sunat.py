# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2011 NUMA Extreme Systems (www.numaes.com) for Cubic ERP - Teradata SAC. (http://cubicerp.com).
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import base64

class sunat_file_save (osv.TransientModel):
    _name = 'l10n_pe.sunat_file_save'
    
    _columns = {
        'output_name': fields.char ('Output filename', size=128),
        'output_file': fields.binary ('Output file', readonly=True, filename="output_name"),    
    }

class ple (osv.AbstractModel):
    _name = "l10n_pe.ple"
    _inherit = ['mail.thread','ir.needaction_mixin']
    
    _columns = {
        'company_id': fields.many2one ('res.company', 'Company', required=True, readonly=True, states={'draft':[('readonly',False)],}),
        'period_id': fields.many2one ('account.period', 'Period', required=True, domain="[('company_id','=',company_id)]", readonly=True, states={'draft':[('readonly',False)],}),
        'journal_id': fields.many2one ('account.journal', 'Journal', domain="[('company_id','=',company_id)]", readonly=True, states={'draft':[('readonly',False)],}),
        'state' : fields.selection ([
                        ('draft', 'Draft'),
                        ('issued', 'Issued'),
                        ], 'State', readonly=True),
    }    

    _defaults = {
        'state': 'draft',
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'l10n_pe.ple', context=c),
    }

    _sql_constraints = [('report_name_unique','unique(company_id,period_id)',_('Only one report per company and period is allowed!'))]
    
    def onchange_state (self, cr, uid, ids, state, context=None):
        if ids and state:
            ple = self.browse (cr, uid, ids[0], context=context)
            if ple.state == 'issued':
                raise osv.except_osv (_('Action error'),
                       _('You can not get back to "draft" an issued report!'))
        return False

    def get_all_periods_up_to (self, cr, uid, period_id, context=None):
        period_obj = self.pool.get('account.period')
        period = period_obj.browse(cr, uid, period_id, context=context)
        period_ids = period_obj.search (cr, uid, 
                                        [('fiscalyear_id', '=', period.fiscalyear_id.id), ('date_start','<=',period.date_start)], 
                                        context=context)
        return period_ids
        
    def get_move_lines (self, cr, uid, period_id, report_type, 
                          company_id=None, account_ids=None, journal_ids=None, partner_ids=None, product_ids=None, context=None):
        conf_obj = self.pool.get('l10n_pe.ple_configuration')
        move_line_obj = self.pool.get('account.move.line')
        period_obj = self.pool.get('account.period')

        if isinstance(period_id, (int, long)):
            period_ids = [period_id]
        else:
            period_ids = period_id

        if not company_id:
            periods = period_obj.browse(cr, uid, period_ids, context=context)
            company_id = periods[0].company_id.id

        conf_ids = conf_obj.search(cr, uid, [('company_id', '=', company_id), ('report_type','=',report_type)], context=context)
        if conf_ids and len(conf_ids)==1:
            conf = conf_obj.browse(cr, uid, conf_ids[0], context=context)
            search_expr = [('move_id.state','=','posted')]

            search_expr += [('period_id','in', period_ids)]

            if partner_ids:
                search_expr += [('partner_id','in', partner_ids)]

            if product_ids:
                search_expr += [('product_id','in', product_ids)]

            if journal_ids:
                search_expr += [('journal_id','in', journal_ids)]
            elif conf.journals_ids:
                search_expr += [('journal_id','in', [j.id for j in conf.journals_ids])]

            if account_ids:
                search_expr += [('account_id','in', account_ids)]
            elif conf.accounts_ids:
                search_expr += [('account_id','in',[j.id for j in conf.accounts_ids or []])]

            move_line_ids = move_line_obj.search(cr, uid, search_expr, context=context)
            if move_line_ids:
                return move_line_obj.browse(cr, uid, move_line_ids, context=context)
            else:
                return []
        else:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            raise osv.except_osv (_('Configuration error'),
                   _('No data for report SUNAT %(report_type)s for company [%(company)s]!') % {
                           'report_type': report_type,
                           'company': company.name})

    def action_confirm (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
                
        ple = self.browse (cr, uid, ids[0], context=context)

        if ple.state == 'draft':
            ple.write ({'state': 'issued'}, context=context)
            
        return True
        
    def action_reload (self, cr, uid, ids, context=None):
        # To be defined by subclasses
        raise osv.except_osv (_('Action error'),
               _('Subclass has not implemented reload action!'))

    def action_report (self, cr, uid, ids, context=None):
        # To be defined by subclasses
        raise osv.except_osv (_('Action error'),
               _('Subclass has not implemented report action!'))
    
    def action_save_file (self, cr, uid, ids, context=None):
        sfs_obj = self.pool.get('l10n_pe.sunat_file_save')

        encoded_output_file = base64.encodestring('\n'.join(self.get_output_lines(cr, uid, ids, context=context)))

        vals = {
            'output_name': self.get_output_filename(cr, uid, ids, context=context),
            'output_file': encoded_output_file,        
        }
        
        sfs_id = sfs_obj.create (cr, uid, vals, context=context)
        
        return {
            'name':_("Save output file"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'l10n_pe.sunat_file_save',
            'res_id': sfs_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': "",
            'context': dict(context)
        }
    
    def convert_date (self, s):
        if s:
            return "%s/%s/%s" % (s[8:10], s[5:7], s[0:4])
        else:
            return "  /  /    "
    
    def convert_str (self, s):
        return s and str(s) or '-'
        
    def convert_amount (self, a):
        return a and str(a) or '0.00'
        
    def convert_qty (self, q):
        return q and str(q) or '0'
        
    def get_output_lines (self, cr, uid, ids, context=None):
        # To be defined by subclasses
        # It should return a list of strings, each of them representing an output line
        return []

    def get_output_filename (self):
        # To be defined by subclasses
        # It should return the name of the output file
        
        raise osv.except_osv (_('Action error'),
               _('Subclass has not implemented output filename action!'))

class ple_line(osv.AbstractModel):
    _name = 'l10n_pe.ple_line'
    
    _columns = {
        'sequence': fields.integer ('Sequence'),
        'move_line_id': fields.many2one('account.move.line', 'Accounting movement'),
        'account_id': fields.many2one('account.account', 'Account', domain="[('company_id','=',company_id)])"),
    }

class ple_configuration (osv.Model):
    _name = "l10n_pe.ple_configuration"
    
    def _get_report_type (self, cr, uid, context=None):
        return self.get_report_type(cr, uid, context=context)

    _columns = {
        'company_id': fields.many2one ('res.company', 'Company', required=True, on_delete='cascade'),
        'report_type': fields.selection (_get_report_type, 'Report type', required=True),
        'accounts_ids': fields.many2many ('account.account', 'l10n_pe_conf_account', 'conf_id', 'account_id', 'Target accounts', domain="[('company_id','=',company_id)]"),
        'journals_ids': fields.many2many ('account.journal', 'l10n_pe_conf_journal', 'conf_id', 'journal_id', 'Target journals', domain="[('company_id','=',company_id)]"),
    }    
    
    _defaults = {
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'l10n_pe.ple', context=c),
    }

    def get_report_type (self, cr, uid, context=None):
        # To be subclassed
        # Returns a list of tuples for the report type selection field
        
        return []

