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

class ple_3_13 (osv.Model):
    _name = "l10n_pe.ple_3_13"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_3_13', 'ple_3_13_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_3_13')

        #Remove existing lines
        ple = self.browse(cr, uid, ids[0], context=context)
        cmds = []
        for line in ple.lines_ids:
            cmds.append((2, line.id))
        if cmds:
            ple.write({'lines_ids': cmds}, context=context)
        ple.refresh()
        
        # Get the list of involved movements
        period_ids = self.get_all_periods_up_to (cr, uid, ids, ple.period_id.id)
        move_lines = self.get_move_lines (cr, uid, period_ids, '3_13', ple.company_id.id, context=context)

        #Get the list of involved partners per account
        tuples = list(set([(aml.account_id.id, aml.partner_id.id) for aml in move_lines]))

        for t in tuples:
            vals = {
                'ple_3_13_id': ple.id,
                'account_id': t[0],
                'partner_id': t[1],
            }
            vals.update(ple_line_obj.onchange_account_partner_id(cr, uid, [], account_id, partner_id, ple.period_id.id, context=context)['value'])
            ple_line_obj.create(cr, uid, vals, context=context)

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
            'report_name': 'l10n_pe.sunat_3_13',
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
                self.convert_str(r.partner_doc_type_3),
                self.convert_str(r.partner_doc_number_4),
                self.convert_str(r.partner_name_5),
                self.convert_date (r.operation_date_6),
                self.convert_str(r.account_code_7),
                self.convert_amount(r.amount_8),
                self.convert_str(r.operation_state_9),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_3_13.txt"

class ple_line_3_13 (osv.Model):
    _name = 'l10n_pe.ple_line_3_13'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_02', context=context)
    
    _columns = {
        'ple_3_13_id': fields.many2one('l10n_pe.ple_3_13', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_3_13_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_3_13_id', 'company_id', string='Company', type="many2one", relation="res.company"),
        'partner_id': fields.many2one('res.partner', 'Partner', on_delete="restrict"),

        'partner_doc_type_3': fields.selection(_get_doc_type_selection, "Doc. type", required=True, size=3, help="Tipo de Documento de Identidad del cliente"),
        'partner_doc_number_4': fields.char("Partner's doc. number", size=15, help="Número de Documento de Identidad del cliente"),
        'payment_date_5': fields.date ('Payment date', required=True, help="Fecha de emisión del Comprobante de Pago"),
        'partner_name_6': fields.char("Partner's name", size=60, required=True, help="Apellidos y Nombres, Denominación o Razón Social del cliente"),
        'account_code_7': fields.char("Account code", size=24, help="Código de la cuenta contable asociada a la obligación y desagregado en subcuentas al nivel máximo de dígitos utilizado, según la estructura 3.21"),
        'amount_8': fields.float('Amount', digits=(12,2), help="Monto de cada cuenta por cobrar del cliente"),
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
        'operation_state_9': '1',
    }
    
    def onchange_account_partner_id (self, cr, uid, ids, account_id, partner_id, period_id, context=None):
        vals = {}
        if account_id and partner_id:
            ple_3_13_obj = self.pool.get('l10n_pe.ple_3_13')
            period_obj = self.pool.get('account.period')
            partner_obj = self.pool.get('res.partner')
            account_obj = self.pool.get('account.account')
            
            lines = ple_3_13_obj.get_move_lines(cr, uid,
                                                ple_3_13_obj.get_all_periods_up_to(period_id, context=context),
                                                '3_13',
                                                partner_ids=[partner_id],
                                                account_ids=[account_id],
                                                context=context)
            lines.sort(key=lambda l: (l.period_id.date_start))
            
            initial_balance = 0.0
            final_balance = 0.0
            first_move_date = None
            period = period_obj.browse(cr, uid, period_id, context=context)
            if lines:
                for l in lines:
                    if l.date_start >= period.date_start:
                        final_balance += (l.credit - l.debit)
                    else:
                        initial_balance += (l.credit - l.debit)
                    if (not first_move_date) or first_move_date > l.date:
                        first_move_date = l.date
                final_balance += initial_balance

            partner = partner_obj.browse(cr, uid, partner_id, context=context)
            account = account_obj.browse(cr, uid, account_id, context=context)
            vals['partner_doc_type_3'] = partner.doc_type
            vals['partner_doc_number_4'] = partner.doc_number
            vals['partner_name_6'] = partner.name
            vals['payment_date_5'] = False
            vals['account_code_7'] = account.code
            vals['amount_8'] = -final_balance
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

 
class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('3_13', '3.13 Cuentas por pagar diversas'))
        return sorted(rep_types, key=lambda e: e[0])
