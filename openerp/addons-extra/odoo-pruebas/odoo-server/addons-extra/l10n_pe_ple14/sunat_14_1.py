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
from openerp.tools.translate import _

class ple_14_1 (osv.Model):
    _name = "l10n_pe.ple_14_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_14_1', 'ple_14_1_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_14_1')

        #Remove existing lines
        ple = self.browse(cr, uid, ids[0], context=context)
        cmds = []
        for line in ple.lines_ids:
            cmds.append((2, line.id))
        if cmds:
            ple.write({'lines_ids': cmds}, context=context)
        ple.refresh()
        
        # Get the list of involved movements
        move_lines = self.get_move_lines (cr, uid, ple.period_id.id, '14_1', ple.company_id.id, context=context)

        for aml in move_lines:
            vals = {
                'ple_14_1_id': ple.id,
                'move_line_id': aml.id,
            }
            vals.update(ple_line_obj.onchange_move_line_id(cr, uid, [], aml.id, ple.company_id.id, context=context)['value'])
            ple_line_obj.create(cr, uid, vals, context=context)

        return True

    def action_renumber (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        next_seq = 1
        for line in sorted(ple.lines_ids, key=lambda l: l.payment_issued_date_3):
            line.write ({'sequence': next_seq}, context=context)
            next_seq += 1

        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_14_1',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            if not r.payment_issued_date_3:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Payment issued date is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if not r.payment_type_5:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Payment type is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if (r.payment_type_5 in ['00','03','05','06','07','08','11','12','13','14','15','16','18','19','23', \
                                   '26','28','30','34','35','36','37','55','56','87','88'] \
                or r.operation_state_27 == '2' \
                or (r.payment_type_5 in ['07','08','87','88','89','97','98'] and r.original_doc_type_24 in ['03','12','13','14','36']) \
                or r.export_amount_12>0 \
                ):
                if not r.partner_doc_type_9:
                    raise osv.except_osv (_('Value error'),
                           _('[Sequence: %d] Partner doc type is a mandatory field. It could not be blank! Please check it') % r.sequence)
                if not r.partner_doc_number_10:
                    raise osv.except_osv (_('Value error'),
                           _('[Sequence: %d] Partner doc number is a mandatory field. It could not be blank! Please check it') % r.sequence)
                if not r.partner_name_11:
                    raise osv.except_osv (_('Value error'),
                           _('[Sequence: %d] Partner name is a mandatory field. It could not be blank! Please check it') % r.sequence)

            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str(r.sequence),
                self.convert_date (r.payment_issued_date_3),
                self.convert_date (r.payment_due_date_4),
                self.convert_str(r.payment_type_5),
                self.convert_str(r.payment_sequence_6),
                self.convert_str(r.payment_number_7),
                self.convert_str(r.final_payment_number_8),
                self.convert_str(r.partner_doc_type_9),
                self.convert_str(r.partner_doc_number_10),
                self.convert_str(r.partner_name_11),
                self.convert_str(r.export_amount_12),
                self.convert_amount(r.export_tax_base_13),
                self.convert_amount(r.non_taxed_base_14),
                self.convert_amount(r.inafecta_base_15),
                self.convert_amount(r.isc_amount_16),
                self.convert_amount(r.igv_ipm_amount_17),
                self.convert_amount(r.ivap_base_18),
                self.convert_amount(r.ivap_amount_19),
                self.convert_amount(r.other_taxes_20),
                self.convert_amount(r.payment_total_amount_21),
                self.convert_amount(r.exchange_rate_22),
                self.convert_date (r.original_date_23),
                self.convert_str(r.original_doc_type_24),
                self.convert_str(r.original_sequence_25),
                self.convert_str(r.original_doc_number_26),
                self.convert_str(r.operation_state_27),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_14_1.txt"

class ple_line_14_1 (osv.Model):
    _name = 'l10n_pe.ple_line_14_1'
    _inherit = 'l10n_pe.ple_line'

    def _get_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_02', context=context)
    
    def _get_payment_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_10', context=context)
    
    _columns = {
        'ple_14_1_id': fields.many2one('l10n_pe.ple_14_1', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_14_1_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_14_1_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'payment_issued_date_3': fields.date("Payment's issue date", help="Fecha de emisión del Comprobante de Pago"),
        'payment_due_date_4': fields.date("Payment's due date", help="Fecha de Vencimiento o Fecha de Pago"),
        'payment_type_5': fields.selection(_get_payment_type_selection, "Payment type", help="Tipo de Comprobante de Pago o Documento, según SUNAT Tabla 10"),    
        'payment_sequence_6': fields.char("Payment sequence", size=20, help="Número serie del comprobante de pago o documento o número de serie de la maquina registradora"),
        'payment_number_7': fields.char("Payment number", size=20, help="Número del comprobante de pago o documento. En caso de optar por anotar el importe total de las operaciones realizadas diariamente, registrar el número inicial"),
        'final_payment_number_8': fields.char("Final payment number", size=20, help="En caso de optar por anotar el importe total de las operaciones realizadas diariamente, registrar el número final. "),
        'partner_doc_type_9': fields.selection(_get_doc_type_selection, "Doc. type", size=3, help="Tipo de Documento de Identidad del cliente"),
        'partner_doc_number_10': fields.char("Partner's doc. number", size=15, help="Número de Documento de Identidad del cliente"),
        'partner_name_11': fields.char("Partner's name", size=200, help="Apellidos y nombres, denominación o razón social  del cliente"),
        'export_amount_12': fields.float("Export amount", digits=(12,2), help="Valor facturado de la exportación"),
        'export_tax_base_13': fields.float("Export tax base", digits=(12,2), help="Base imponible de la operación gravada (3)"),
        'non_taxed_base_14': fields.float("Non taxed base", digits=(12,2), help="Importe total de la operación exonerada"),
        'inafecta_base_15': fields.float("Inafecta base", digits=(12,2), help="Importe total de la operación inafecta"),
        'isc_amount_16': fields.float("ISC amount", digits=(12,2), help="ISC, de ser el caso"),
        'igv_ipm_amount_17': fields.float("IGV/IPM amount", digits=(12,2), help="IGV y/o IPM (4)"),
        'ivap_base_18': fields.float("IVAP base", digits=(12,2), help="Base imponible de la operación gravada con el IVAP"),
        'ivap_amount_19': fields.float("IVAP amount", digits=(12,2), help="IVAP (5)"),
        'other_taxes_20': fields.float("Other taxes amount", digits=(12,2), help="Otros tributos y cargos que no forman parte de la base imponible"),
        'payment_total_amount_21': fields.float("Payment total amount", digits=(12,2), help="Importe total del comprobante de pago"),
        'exchange_rate_22': fields.float("Currency exchange rate", digits=(1,3), help="Tipo de cambio"),
        'original_date_23': fields.date("Original doc. date", help="Fecha de emisión del comprobante de pago o documento original que se modifica"),
        'original_doc_type_24': fields.selection(_get_payment_type_selection, "Original doc. type", help="Tipo del comprobante de pago o documento original que se modifica, según SUNAT Tabla 10"),
        'original_sequence_25': fields.char('Original sequence', size=20, help="Número de serie del comprobante de pago o documento original que se modifica"),
        'original_doc_number_26': fields.char('Original doc.number', size=20, help="Número del comprobante de pago o documento original que se modifica."),
        'operation_state_27': fields.selection ([
                                ('1', '1 - Este período'),
                                ('2', '2 - Inutilizado'),
                                ('9', '8 - Período previo, no registrado'),
                                ('9', '9 - Período previo, no registrado'),
                            ], 'Operation state', help="""
1. Obligatorio
2. Registrar '1' cuando la operación (ventas gravadas, exoneradas, inafectas y/o exportaciones) corresponde al periodo, así como a las Notas de Crédito y Débito emitidas en el periodo.
3. Registrar '2' cuando el documento ha sido inutilizado durante el periodo previamente a ser entregado, emitido o durante su emisión.
4. Registrar '8' cuando la operación (ventas gravadas, exoneradas, inafectas y/o exportaciones) corresponde a un periodo anterior y NO ha sido anotada en dicho periodo.
5. Registrar '9' cuando la operación (ventas gravadas, exoneradas, inafectas y/o exportaciones) corresponde a un periodo anterior y SI ha sido anotada en dicho periodo.                     
"""),
    }
    
    _order = 'sequence'
    
    _defaults = {
        'operation_state_27': '1',
    }
    
    def onchange_move_line_id (self, cr, uid, ids, move_line_id, company_id, context=None):
        vals = {}
        if move_line_id:
            aml_obj = self.pool.get('account.move.line')
            invoice_obj = self.pool.get('account.invoice')
            conf_obj = self.pool.get('l10n_pe.ple_configuration')
            currency_obj = self.pool.get('res.currency')
            
            conf_ids = conf_obj.search(cr, uid, [('report_type', '=', '14_1'), ('company_id', '=', company_id)], context=context)
            if not conf_ids:
                raise osv.except_osv (_('Configuration error'),
                       _('No configuration found for SUNAT report 14.1! Please check it'))
            conf = conf_obj.browse(cr, uid, conf_ids[0], context=context)

            ml = aml_obj.browse (cr, uid, move_line_id, context=context)
            vals['payment_issued_date_3'] = ml.date
            vals['payment_due_date_4'] = ml.date_maturity or ml.date
            vals['payment_type_5'] = ml.journal_id.sunat_payment_type
            s = ml.ref.split('-')
            vals['payment_sequence_6'] = len(s)>1 and s[0] or ''
            vals['payment_number_7'] = len(s)>1 and s[1] or s[0]
            vals['final_payment_number_8'] = 0.0
            vals['partner_doc_type_9'] = ml.partner_id and ml.partner_id.doc_type
            vals['partner_doc_number_10'] = ml.partner_id and ml.partner_id.doc_number
            vals['partner_name_11'] = ml.partner_id and ml.partner_id.name

            invoice_ids = invoice_obj.search(cr, uid, [('name', '=', ml.move_id.name)], context=context)
            
            vals['export_amount_12'] = 0.0
            vals['export_tax_base_13'] = 0.0
            vals['non_taxed_base_14'] = 0.0
            vals['inafecta_base_15'] = 0.0
            vals['isc_amount_16'] = 0.0
            vals['igv_ipm_amount_17'] = 0.0
            vals['ivap_base_18'] = 0.0
            vals['ivap_amount_19'] = 0.0
            vals['other_taxes_20'] = 0.0
            vals['payment_total_amount_21'] = ml.debit or ml.credit
            
            if invoice_ids:
                invoice = invoice_obj.browse(cr, uid, invoice_ids[0], context=context)
                inafecta_total = 0.0
                isc_total = 0.0
                igv_total = 0.0
                ivap_base_total = 0.0
                ivap_total = 0.0
                other_total = 0.0
                for line in invoice.tax_line:
                    if line.tax_code_id in conf.inafecta_taxes:
                        inafecta_total += line.tax_amount
                    elif line.tax_code_id in conf.isc_taxes:
                        isc_total += line.tax_amount
                    elif line.tax_code_id in conf.igv_taxes:
                        igv_total += line.tax_amount
                    elif line.tax_code_id in conf.ivap_taxes:
                        ivap_total += line.tax_amount
                        ivap_base_total += line.base_amount
                    else:
                        other_total += line.tax_amount
                vals['export_amount_12'] = invoice.amount_untaxed
                vals['export_tax_base_13'] = invoice.amount_untaxed
                vals['non_taxed_base_14'] = 0.0
                vals['inafecta_base_15'] = inafecta_total
                vals['isc_amount_16'] = isc_total
                vals['igv_ipm_amount_17'] = igv_total
                vals['ivap_base_18'] = ivap_base_total
                vals['ivap_amount_19'] = ivap_total
                vals['other_taxes_20'] = other_total
                vals['payment_total_amount_21'] = invoice.amount_total

                from_currency_id = currency_obj.search(cr, uid, [('name','=','USD')], context=context)[0]
                to_currency_id = currency_obj.search(cr, uid, [('name','=','PEN')], context=context)[0]
                vals['exchange_rate_22'] = currency_obj.compute(cr, uid, 
                                                                from_currency_id, 
                                                                to_currency_id, 
                                                                1.0,
                                                                context=dict(context, date=ml.maturity_date or ml.date))
            return {'value': vals}
        else:
            return False

    def onchange_doc (self, cr, uid, ids, partner_doc_type, partner_doc_number, context=None):
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

    _columns = {
        'inafecta_taxes': fields.many2many('account.tax.code', 'ple14_1_inafecta_taxes', 'conf_id', 'tax_code_id', 'Inafecta taxes codes'),
        'isc_taxes': fields.many2many('account.tax.code', 'ple14_1_isc_taxes', 'conf_id', 'tax_code_id', 'ISC taxes codes'),
        'igv_taxes': fields.many2many('account.tax.code', 'ple14_1_igv_taxes', 'conf_id', 'tax_code_id', 'IGV taxes codes'),
        'ivap_taxes': fields.many2many('account.tax.code', 'ple14_1_ivap_taxes', 'conf_id', 'tax_code_id', 'IVAP taxes codes'),
    }

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('14_1', '14.1 Ventas e Ingresos'))
        return sorted(rep_types, key=lambda e: e[0])
