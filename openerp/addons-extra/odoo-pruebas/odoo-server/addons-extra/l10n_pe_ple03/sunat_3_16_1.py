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

class ple_3_16_1 (osv.Model):
    _name = "l10n_pe.ple_3_16_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'total_capital_2': fields.float('Total capital', digits=(12,2), help="Importe del Capital Social o Participaciones Sociales al cierre del ejercicio o periodo que corresponda"),
        'nominal_per_share_3': fields.float('Nominal value per share', digits=(12,2), help="Valor nominal por acción o participación social"),
        'share_count_4': fields.float('Share count', digits=(12,2), help="Número de acciones o participaciones sociales suscritas"),
        'operation_state_5': fields.selection ([
                                ('1', '1'),
                                ('8', '8'),
                                ('9', '9'),
                            ], 'Operation state', required=True, help="""
Registrar '1' cuando la operación corresponde al periodo, 
'8' cuando la operación corresponde a un periodo anterior y NO ha sido anotada en dicho periodo o
'9' cuando la operación corresponde a un periodo anterior y SI ha sido anotada en dicho periodo."""),
    }

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_3_16_1',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        elements = [
            "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
            self.convert_amount(ple.total_capital_2),
            self.convert_amount(ple.nominal_per_share_3),
            self.convert_amount(ple.share_count_4),
            self.convert_str(r.operation_state_5),
        ]
        res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_3_16_1.txt"

class ple_line_3_16_1(osv.Model):
    _name = 'l10n_pe.ple_line_3_16_1'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_02', context=context)
    
    def _get_share_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_16', context=context)
    
    _columns = {
        'ple_3_16_1_id': fields.many2one('l10n_pe.ple_3_16_1', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_3_16_1_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_3_16_1_id', 'company_id', string='Company', type="many2one", relation="res.company"),
        'share_amount_2': fields.float('Share Amount', digits=(12,2), help="Importe del Capital Social o Participaciones Sociales al cierre del ejercicio o periodo que corresponda"),
        'share_amount_unit_3': fields.float('Share Amount Unit', digits=(12,2), help="Valor nominal por acción o participación social"),
        'share_count_suscribed_4': fields.float('Share Count Suscribed', digits=(12,2), help="Número de acciones o participaciones sociales suscritas"),
        'share_count_payed_5': fields.float('Share Count Payed', digits=(12,2), help="Número de acciones o participaciones sociales pagadas"),
        'operation_state_6': fields.selection ([
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
        'operation_state_6': '1',
    }
    
    def onchange_partner_id (self, cr, uid, ids, period_id, context=None):
        vals = {}
        ple_3_16_1_obj = self.pool.get('l10n_pe.ple_3_16_1')
        period_obj = self.pool.get('account.period')
        partner_obj = self.pool.get('res.partner')
        
        lines = ple_3_16_1_obj.get_move_lines(cr, uid,
                                            ple_3_16_1_obj.get_all_periods_up_to(period_id, context=context),
                                            '3_16_1',
                                            context=context)
        lines.sort(key=lambda l: (l.period_id.date_start))
        
        initial_balance = 0.0
        final_balance = 0.0
        initial_quantity = 0.0
        final_quantity = 0.0
        period = period_obj.browse(cr, uid, period_id, context=context)
        if lines:
            for l in lines:
                if l.date_start >= period.date_start:
                    final_balance += (l.credit - l.debit)
                    final_quantity += l.product_qty
                else:
                    initial_balance += (l.credit - l.debit)
                    initial_quantity += l.product_qty
                if (not first_move_date) or first_move_date > l.date:
                    first_move_date = l.date
            final_balance += initial_balance
            final_quantity += initial_quantity

        vals['share_amount_2'] = final_balance
        vals['share_amount_unit_3'] = final_balance / final_quantity
        vals['share_count_suscribed_4'] = final_quantity
        vals['share_count_payed_5'] = final_quantity
        return {'value': vals}