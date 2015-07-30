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

class ple_10_3 (osv.Model):
    _name = "l10n_pe.ple_10_3"
    _inherit = "l10n_pe.ple"

    _columns= {
        'period_id': fields.many2one ('account.period', 'Period', readonly=True),
        'fiscal_year_1': fields.many2one('account.fiscalyear', 'Fiscal year', required=True, help="""
1. Obligatorio
3. AAAA >= 2010
4. Se entiende que la información es a partir del 01 de enero del ejercicio o desde el inicio de actividades, cuando corresponda
                                     """),
        'lines_ids': fields.one2many ('l10n_pe.ple_line_10_3', 'ple_10_3_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        #TODO
        
        return True

    def action_report (self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_10_3',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s0000" % (ple.fiscal_year_1.name),
                self.convert_str(r.process_code_2),
                self.convert_str(r.process_description_3),
                self.convert_amount(r.direct_material_cost_4),
                self.convert_amount(r.direct_labor_cost_5),
                self.convert_amount(r.direct_other_direct_costs_6),
                self.convert_amount(r.indirect_production_costs_7),
                self.convert_amount(r.indirect_labor_costs_8),
                self.convert_amount(r.indirect_other_costs_9),
                self.convert_amount(r.initial_in_process_inventory_10),
                self.convert_amount(r.final_in_process_inventory_11),
                self.convert_str(r.grouping_code_12),
                self.convert_str(r.operation_state_13),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_10_3.txt"

class ple_line_10_3 (osv.Model):
    _name = 'l10n_pe.ple_line_10_3'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_grouping_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_21', context=context)
    
    _columns = {
        'ple_10_3_id': fields.many2one('l10n_pe.ple_10_3', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_10_3_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_10_3_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'account_id': fields.many2one('account.account', 'Account', help="Account to summarize costs"),

        'process_code_2': fields.char('Process code', size=10, required=True, 
                                      help="Código de identificación del Proceso informado (La información podrá agruparse optativamente por proceso productivo, línea de producción, producto o proyecto)"),
        'process_description_3': fields.char('Process description', size=100, required=True, 
                                      help="Descripción del Proceso informado"),
        'direct_material_cost_4': fields.float('Direct material costs',  digits=(12,2),
                                                help="Costo de Materiales y Suministros Directos"),
        'direct_labor_cost_5': fields.float('Direct labor costs',  digits=(12,2),
                                                help="Costo de la Mano de Obra Directa"),
        'direct_other_direct_costs_6': fields.float('Other direct costs',  digits=(12,2),
                                                help="Otros Costos Directos"),
        'indirect_production_costs_7': fields.float('Indirect production costs',  digits=(12,2),
                                                help="Gastos de Producción Indirectos: Materiales y Suministros Indirectos"),
        'indirect_labor_costs_8': fields.float('Indirect labor costs',  digits=(12,2),
                                                help="Gastos de Producción  Indirectos:Mano de Obra Indirecta"),
        'indirect_other_costs_9': fields.float('Indirect other costs',  digits=(12,2),
                                                help="Otros Gastos de Producción Indirectos"),
        'initial_in_process_inventory_10': fields.float('Initial in process inventory',  digits=(12,2),
                                                help="Inventario inicial de productos en proceso"),
        'final_in_process_inventory_11': fields.float('Final in process inventory',  digits=(12,2),
                                                help="Inventario final de productos en proceso"),
        'grouping_code_12': fields.selection(_get_grouping_code_selection, 'Grouping code', required=True,
                                             help="Código de agrupamiento del costo de producción valorizado anual"),
        'operation_state_13': fields.selection ([
                                ('1', '1'),
                                ('8', '8'),
                                ('9', '9'),
                            ], 'Operation state', required=True, help="""
Registrar '1' cuando la operación corresponde al periodo, 
'8' cuando la operación corresponde a un periodo anterior y NO ha sido anotada en dicho periodo o
'9' cuando la operación corresponde a un periodo anterior y SI ha sido anotada en dicho periodo."""),
    }

    _defaults = {
        'operation_state_13': '1',    
    }
    
    def onchange_account_id (self, cr, uid, ids, account_id, period_id, context=None):
        vals = {}
        
        if account_id:
            #TODO
            pass
            return {'value': vals}
        else:
            return False

class ple_configuration (osv.Model):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('10_3', '10.3 Costo producción anual valorizado'))
        return sorted(rep_types, key=lambda e: e[0])

