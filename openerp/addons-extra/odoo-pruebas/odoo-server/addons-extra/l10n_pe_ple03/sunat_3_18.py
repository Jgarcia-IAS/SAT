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

class ple_3_18 (osv.Model):
    _name = "l10n_pe.ple_3_18"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_3_18', 'ple_3_18_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        #TODO
        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_3_18',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str(r.account_code_2),
                self.convert_amount(r.initial_debt_3),
                self.convert_amount(r.initial_credit_4),
                self.convert_amount(r.acum_debt_movements_5),
                self.convert_amount(r.acum_credit_movements_6),
                self.convert_str(r.operation_state_7),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_3_18.txt"

class ple_line_3_18 (osv.Model):
    _name = 'l10n_pe.ple_line_3_18'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_catalog_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_10', context=context)
    
    _columns = {
        'ple_3_18_id': fields.many2one('l10n_pe.ple_3_18', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_3_18_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_3_18_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'catalog_code_2': fields.selection(_get_catalog_code_selection, "Catalog code", required=True, size=3, help="Código del catálogo utilizado"),
        'account_code_3': fields.char("Account code", size=40, required=True, help="Código de la Cuenta Contable y/o Partida"),
        'balance_4': fields.float('Balance', digits=(12,2), help="Saldo del Rubro Contable"),
        'operation_state_5': fields.selection ([
                                ('1', '1'),
                                ('8', '8'),
                                ('9', '9'),
                            ], 'Operation state', required=True, help="""
Registrar '1' cuando la operación corresponde al periodo, 
'8' cuando la operación corresponde a un periodo anterior y NO ha sido anotada en dicho periodo o
'9' cuando la operación corresponde a un periodo anterior y SI ha sido anotada en dicho periodo."""),
    }
    
    _order = 'sequence'
    
    _defaults = {
        'operation_state_5': '1',
    }

    def onchange_account_id (self, cr, uid, ids, account_id, context=None):
        vals = {}
        if move_line_id:
            account_obj = self.pool.get('account.account')
            account = account_obj.browse (cr, uid, account_id, context=context)
            vals['account_code_3'] = account.code
            return {'value': vals}
        else:
            return False

class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('3_18', '3.18 Estado de flujos de Efectivo'))
        return sorted(rep_types, key=lambda e: e[0])
