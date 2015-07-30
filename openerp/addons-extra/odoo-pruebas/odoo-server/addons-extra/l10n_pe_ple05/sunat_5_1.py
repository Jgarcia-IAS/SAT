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

class ple_5_1 (osv.Model):
    _name = "l10n_pe.ple_5_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_5_1', 'ple_5_1_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_5_1')
        
        ple = self.browse(cr, uid, ids[0], context=context)

        cmds = []
        for line in ple.lines_ids:
            cmds.append((2, line.id))
        if cmds:
            ple.write({'lines_ids': cmds}, context=context)
        ple.refresh()
        
        move_lines = self.get_move_lines (cr, uid, ple.period_id.id, '5_1', ple.company_id.id, context=context)
        
        for ml in move_lines:
            vals = {
                'ple_5_1_id': ple.id,
                'move_line_id': ml.id,
            }
            vals.update(ple_line_obj.onchange_move_line_id(cr, uid, [], ml.id, context=context)['value'])
            ple_line_obj.create(cr, uid, vals, context=context)

        self.action_renumber(cr, uid, ids, context=context)
        
        return True

    def action_renumber (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        next_seq = 1
        for line in sorted(ple.lines_ids, key=lambda l: l.operation_date_3):
            line.write ({'sequence': next_seq}, context=context)
            next_seq += 1

        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_5_1',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str(r.sequence),
                self.convert_str(r.account_plan_code_3),
                self.convert_str(r.account_code_4),
                self.convert_date (r.operation_date_5),
                self.convert_str(description_6),
                self.convert_amount(r.debit_7),
                self.convert_amount(r.credit_8),
                self.convert_str(r.operation_state_9),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_5_1.txt"

class ple_line_5_1 (osv.Model):
    _name = 'l10n_pe.ple_line_5_1'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_account_plan_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_17', context=context)
    
    _columns = {
        'ple_5_1_id': fields.many2one('l10n_pe.ple_5_1', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_5_1_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_5_1_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'account_plan_code_3': fields.selection(_get_account_plan_code_selection, "Account plan code", size=2, required=True, help="Código del Plan de Cuentas utilizado por el deudor tributario"),
        'account_code_4': fields.char('Account code', size=24, required=True, help="Código de la cuenta contable asociada desagregado en subcuentas al nivel máximo de dígitos utilizado, según la estructura 3.21"),
        'operation_date_5': fields.date ('Operation date', required=True, help="Fecha de la operación"),
        'description_6': fields.char('Description', size=100, required=True, help="Glosa o descripción de la naturaleza de la operación registrada, de ser el caso."),
        'debit_7': fields.float('Debit', digits=(12,2), help="Movimientos del Debe"),
        'credit_8': fields.float('Credit', digits=(12,2), help="Movimientos del Haber"),
        'operation_state_9': fields.selection ([
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
        'operation_date_5': fields.date.context_today,
        'operation_state_9': '1',
    }
    

class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('5_1', '5.1 Libro Diario'))
        return sorted(rep_types, key=lambda e: e[0])
