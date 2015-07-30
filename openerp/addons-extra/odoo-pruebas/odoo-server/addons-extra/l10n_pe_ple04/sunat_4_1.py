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

class ple_4_1 (osv.Model):
    _name = "l10n_pe.ple_4_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_4_1', 'ple_4_1_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_4_1')
        
        ple = self.browse(cr, uid, ids[0], context=context)

        cmds = []
        for line in ple.lines_ids:
            cmds.append((2, line.id))
        if cmds:
            ple.write({'lines_ids': cmds}, context=context)
        ple.refresh()
        
        move_lines = self.get_move_lines (cr, uid, ple.period_id.id, '4_1', ple.company_id.id, context=context)
        
        for ml in move_lines:
            vals = {
                'ple_4_1_id': ple.id,
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
            'report_name': 'l10n_pe.sunat_4_1',
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
                self.convert_date (r.operation_date_3),
                self.convert_str(r.partner_doc_type_4),
                self.convert_str(r.partner_doc_number_5),
                self.convert_str(r.partner_name_6),
                self.convert_amount(r.total_amount_7),
                self.convert_amount(r.retention_8),
                self.convert_str(r.operation_state_9),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_4_1.txt"

class ple_line_4_1 (osv.Model):
    _name = 'l10n_pe.ple_line_4_1'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_02', context=context)

    _columns = {
        'ple_4_1_id': fields.many2one('l10n_pe.ple_4_1', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_4_1_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_4_1_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'operation_date_3': fields.date ('Operation date', required=True, help="Fecha de la operación"),
        'partner_doc_type_4': fields.selection(_get_doc_type_selection, "Partner Doc. type", required=True, size=3, help="Tipo de Documento de Identidad de la persona que prestó el servicio"),
        'partner_doc_number_5': fields.char("Partner's doc. number", size=15, required=True, help="Número de Documento de Identidad de la persona que prestó el servicio"),
        'partner_name_6': fields.char("Partner's name", size=60, required=True, required=True, help="Apellidos y Nombres de la persona que prestó el servicio"),
        'total_amount_7': fields.float('Debit', digits=(12,2), help="Monto Bruto"),
        'retention_8': fields.float('Credit', digits=(12,2), help="Retención efectuada"),
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
            # TODO

            return {'value': vals}
        else:
            return False

    def onchange_doc (self, cr, uid, ids, partner_doc_type, partner_doc_number, context=None):
        res = {}

        if partner_doc_type == '0':
            if (not partner_doc_number) or len (partner_doc_number) > 15:
                raise osv.except_osv (_('Value error'),
                       _('Document number should be alfanumeric, not longer than 15 characters! Please check!'))
        elif partner_doc_type == '1':
            if (not partner_doc_number) or len (partner_doc_number) != 8 or not partner_doc_number.isdigit():
                raise osv.except_osv (_('Value error'),
                       _('Libreta electoral or DNI should be numeric, exactly 8 numbers long! Please check!'))
        elif partner_doc_type == '4':
            if (not partner_doc_number) or len (partner_doc_number) > 12:
                raise osv.except_osv (_('Value error'),
                       _('Carnet de extranjeria should be alfanumeric, not longer than 12 characters! Please check!'))
        elif partner_doc_type == '6':
            if (not partner_doc_number) or (len (partner_doc_number) < 8 or len(partner_doc_number) > 11) or not partner_doc_number.isdigit():
                raise osv.except_osv (_('Value error'),
                       _('RUC should be numeric, 8-11 numbers long! Please check!'))
        elif partner_doc_type == '7':
            if (not partner_doc_number) or len (partner_doc_number) > 12:
                raise osv.except_osv (_('Value error'),
                       _('Pasaporte should be alfanumeric, not longer than 12 characters! Please check!'))
        elif partner_doc_type == 'A':
             if (not partner_doc_number) or len (partner_doc_number) != 15 or not partner_doc_number.isdigit():
                raise osv.except_osv (_('Value error'),
                       _('Cedula diplomatica should be numeric, exactly 15 numbers long! Please check!'))

        return res and {'value': res}

class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('4_1', '4.1 Retenciones'))
        return sorted(rep_types, key=lambda e: e[0])
