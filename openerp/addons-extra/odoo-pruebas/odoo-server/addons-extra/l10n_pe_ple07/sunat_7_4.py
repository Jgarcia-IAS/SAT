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

class ple_7_4 (osv.Model):
    _name = "l10n_pe.ple_7_4"
    _inherit = "l10n_pe.ple"

    _columns= {
        'fiscal_year': fields.man2one('account.fiscal_year', 'Fiscal year', required=True, readonly=True, states={'draft':[('readonly',False)],}),
        'lines_ids': fields.one2many ('l10n_pe.ple_line_7_4', 'ple_7_4_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        # TODO
        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_7_4',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s0000" % (ple.fiscal_year.name),
                self.convert_str(r.catalog_2),
                self.convert_str(r.contract_number_3),
                self.convert_date (r.contract_date_4),
                self.convert_str(r.asset_code_5),
                self.convert_date (r.rent_start_date_6),
                self.convert_amount(r.pay_count_7),
                self.convert_amount(r.contract_total_amount_8),
                self.convert_str(r.operation_state_9),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_7_4.txt"

class ple_line_7_4 (osv.Model):
    _name = 'l10n_pe.ple_line_7_4'
    _inherit = 'l10n_pe.ple_line'
    
    _columns = {
        'ple_7_4_id': fields.many2one('l10n_pe.ple_7_4', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_7_4_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_7_4_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'catalog_2': fields.selection(_get_catalog_selection, "Catalog", size=1, required=True, help="Código del catálogo utilizado"),
        'contract_number_3': fields.text('Contract number', required=True, help="Número del contrato de arrendamiento financiero del Activo Fijo."),
        'contract_date_4': fields.date ('Contract date', required=True, help="Fecha del contrato de arrendamiento financiero del Activo Fijo"),
        'asset_code_5': fields.char('Asset Code', size=24, required=True, help="Código relacionado con el Activo Fijo"),
        'rent_start_date_6': fields.date ('Rent start date', required=True, help="Fecha de inicio del arrendamiento financiero del Activo Fijo"),
        'pay_count_7': fields.float('Payment count', digits=5, help="Número de cuotas pactadas"),
        'contract_total_amount_8': fields.float('Contract total amount', digits=(12,2), help="Monto total del contrato de arrendamiento financiero del Activo Fijo"),
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
        'operation_date_3': fields.date.context_today,
        'operation_state_7': '1',
    }
    
    def onchange_move_line_id (self, cr, uid, ids, move_line_id, context=None):
        vals = {}
        if move_line_id:
            aml_obj = self.pool.get('account.move.line')
            ml = aml_obj.browse (cr, uid, move_line_id, context=context)
            vals['account_id'] = ml.account_id.id
            vals['operation_date_3'] = ml.date
            vals['description_4'] = ml.name
            vals['debit_5'] = ml.debit
            vals['credit_6'] = ml.credit
            return {'value': vals}
        else:
            return False


class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('7_4', '7.4 AF Arrendamiento'))
        return sorted(rep_types, key=lambda e: e[0])
