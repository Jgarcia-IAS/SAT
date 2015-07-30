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

class ple_3_23 (osv.Model):
    _name = "l10n_pe.ple_3_23"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_3_23', 'ple_3_23_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_3_23',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str(r.note_nomber_2),
                self.convert_str(r.note_description_3),
                self.convert_str(r.note_contents_4),
                self.convert_str(r.operation_state_5),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_3_23.txt"

class ple_line_3_23 (osv.Model):
    _name = 'l10n_pe.ple_line_3_23'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_catalog_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_22', context=context)
    
    _columns = {
        'ple_3_23_id': fields.many2one('l10n_pe.ple_3_23', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_3_23_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_3_23_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'note_nomber_2': fields.integer("Note number", required=True, size=3, help="Número de la nota"),
        'note_description_3': fields.char("Note description", size=100, required=True, help="Descripción de la nota"),
        'note_contents_4': fields.text("Note contents", required=True, help="Contenido de la nota"),
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

class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('3_23', '3.23 Notas de los estados financieros'))
        return sorted(rep_types, key=lambda e: e[0])
