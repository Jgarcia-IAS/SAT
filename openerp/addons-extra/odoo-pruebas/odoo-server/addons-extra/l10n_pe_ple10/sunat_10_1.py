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

class ple_10_1 (osv.Model):
    _name = "l10n_pe.ple_10_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'period_id': fields.many2one ('account.period', 'Period', readonly=True),
        'fiscal_year_1': fields.many2one('account.fiscalyear', 'Fiscal year', required=True,
                                     help="""
1. Obligatorio
3. AAAA >= 2010
4. Se entiende que la información es a partir del 01 de enero del ejercicio o desde el inicio de actividades, cuando corresponda
                                     """),
        'initial_products_2': fields.float('Initial terminated products', digits=(12,2), help="Costo del inventario inicial de productos terminados contable"),
        'initial_mfg_cost_3': fields.float('Initial mfg cost products', digits=(12,2), help="Costo de producción de productos terminados contable"),
        'final_products_4': fields.float('Final terminated products', digits=(13,2), 
                                         help="Costos del inventario final de productos terminados disponibles para la venta contable"),
        'adjustment_5': fields.float('Adjustments', digits=(13,2), help="Ajustes diversos contables"),
        'operation_state_6': fields.selection ([
                                ('1', '1'),
                                ('8', '8'),
                                ('9', '9'),
                            ], 'Operation state', required=True, help="""
Registrar '1' cuando la operación corresponde al periodo, 
'8' cuando la operación corresponde a un periodo anterior y NO ha sido anotada en dicho periodo o
'9' cuando la operación corresponde a un periodo anterior y SI ha sido anotada en dicho periodo."""),
    }

    _defaults = {
        'operation_state_6': '1',
    }
    
    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        #TODO
        
        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_10_1',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        elements = [
            self.convert_str("%4s0000" % ple.fiscal_year_1.name),
            self.convert_amount(ple.initial_products_2),
            self.convert_amount(ple.initial_mfg_cost_3),
            self.convert_amount(ple.final_products_4),
            self.convert_amount(ple.adjustment_5),
            self.convert_str(ple.operation_state_6),
        ]
        res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_10_1.txt"

class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('10_1', '10.1 Costos de venta anual'))
        return sorted(rep_types, key=lambda e: e[0])
