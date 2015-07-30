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

class ple_3_19 (osv.Model):
    _name = "l10n_pe.ple_3_19"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_3_19', 'ple_3_19_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        #TODO
        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_3_19',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str(r.catalog_code_2),
                self.convert_str(r.account_code_3),
                self.convert_amount(r.capital_4),
                self.convert_amount(r.investments_5),
                self.convert_amount(r.additional_capital_6),
                self.convert_amount(r.non_effective_results_7),
                self.convert_amount(r.legal_reserves_8),
                self.convert_amount(r.other_reserves_9),
                self.convert_amount(r.acum_results_10),
                self.convert_amount(r.convertion_differences_11),
                self.convert_amount(r.equity_adjustments_12),
                self.convert_amount(r.net_year_result_13),
                self.convert_amount(r.reval_excess_14),
                self.convert_amount(r.result_15),
                self.convert_str(r.operation_state_16),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_3_19.txt"

class ple_line_3_19 (osv.Model):
    _name = 'l10n_pe.ple_line_3_19'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_catalog_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_10', context=context)
    
    _columns = {
        'ple_3_19_id': fields.many2one('l10n_pe.ple_3_19', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_3_19_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_3_19_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'catalog_code_2': fields.selection(_get_catalog_code_selection, "Catalog code", required=True, size=3, help="Código del catálogo utilizado"),
        'account_code_3': fields.char("Account code", size=40, required=True, help="Código de la Cuenta Contable y/o Partida"),
        'capital_4': fields.float('Capital', digits=(12,2), help="Capital"),
        'investments_5': fields.float('Investments', digits=(12,2), help="Acciones de Inversión"),
        'additional_capital_6': fields.float('Additional capital', digits=(12,2), help="Capital Adicional"),
        'non_effective_results_7': fields.float('Non effective results', digits=(12,2), help="Resultados no Realizados"),
        'legal_reserves_8': fields.float('Legal reserves', digits=(12,2), help="Reservas Legales"),
        'other_reserves_9': fields.float('Other reserves', digits=(12,2), help="Otras Reservas"),
        'acum_results_10': fields.float('Acum. results', digits=(12,2), help="Resultados Acumulados"),
        'convertion_differences_11': fields.float('Convertion differences', digits=(12,2), help="Diferencias de Conversión"),
        'equity_adjustments_12': fields.float('Equity adjustments', digits=(12,2), help="Ajustes al Patrimonio"),
        'net_year_result_13': fields.float('Net year result', digits=(12,2), help="Resultado Neto del Ejercicio"),
        'reval_excess_14': fields.float('Reval excess', digits=(12,2), help="Excedente de Revaluación"),
        'result_15': fields.float('Result', digits=(12,2), help="Resultado del Ejercicio"),
        'operation_state_16': fields.selection ([
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
        'operation_state_16': '1',
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
        rep_types.append (('3_19', '3.19 Cambios en Patrimonio neto'))
        return sorted(rep_types, key=lambda e: e[0])
