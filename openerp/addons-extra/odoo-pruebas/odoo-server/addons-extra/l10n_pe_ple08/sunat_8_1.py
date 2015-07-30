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

class ple_8_1 (osv.Model):
    _name = "l10n_pe.ple_8_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_8_1', 'ple_8_1_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_8_1')

        #Remove existing lines
        ple = self.browse(cr, uid, ids[0], context=context)
        cmds = []
        for line in ple.lines_ids:
            cmds.append((2, line.id))
        if cmds:
            ple.write({'lines_ids': cmds}, context=context)
        ple.refresh()
        
        # Get the list of involved movements
        move_lines = self.get_move_lines (cr, uid, [ple.period_id.id], '8_1', ple.company_id.id, context=context)

        for aml in move_lines:
            vals = {
                'ple_8_1_id': ple.id,
                'move_line_id': aml.id,
            }
            vals.update(ple_line_obj.onchange_move_line_id(cr, uid, [], aml.id, ple.company_id.id,context=context)['value'])
            ple_line_obj.create(cr, uid, vals, context=context)

        return True

    def action_renumber (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        next_seq = 1
        for line in sorted(ple.lines_ids, key=lambda l: l.issued_date_3):
            line.write ({'sequence': next_seq}, context=context)
            next_seq += 1

        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_8_1',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            if not r.issued_date_3:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Payment issued date is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if not r.type_5:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Document type is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if not r.sequence_6:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Document sequence is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if (r.type_5 in ['00','03','05','06','07','08','11','12','13','14','15','16','18','19','22','23', \
                                   '26','28','30','34','35','36','37','55','56','87','88','91','97','98'] \
                or (r.type_5 in ['07','08','87','88','89','97','98'] and r.original_doc_type_25 in ['03','12','13','14','36']) \
                or r.tax_base_13>0 \
                ):
                if not r.supplier_doc_type_10:
                    raise osv.except_osv (_('Value error'),
                           _('[Sequence: %d] Partner doc type is a mandatory field. It could not be blank! Please check it') % r.sequence)
                if not r.supplier_doc_number_11:
                    raise osv.except_osv (_('Value error'),
                           _('[Sequence: %d] Partner doc number is a mandatory field. It could not be blank! Please check it') % r.sequence)
                if not r.supplier_name_12:
                    raise osv.except_osv (_('Value error'),
                           _('[Sequence: %d] Partner name is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if not r.original_issued_date_24:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Original issue date is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if not r.original_doc_type_25:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Original doc. type is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if r.type_5 in ['07','08','87','88','97','98'] \
               and not r.original_sequence_26:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Original sequence is a mandatory field. It could not be blank! Please check it') % r.sequence)
            if not r.operation_state_32:
                raise osv.except_osv (_('Value error'),
                       _('[Sequence: %d] Original doc.number is a mandatory field. It could not be blank! Please check it') % r.sequence)

            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str(r.sequence),
                self.convert_date (r.issued_date_3),
                self.convert_date (r.due_date_4),
                self.convert_str(r.type_5),
                self.convert_str(r.sequence_6),
                self.convert_str(r.dua_dsi_year_7),
                self.convert_str(r.tax_doc_number_8),
                self.convert_amount(r.amount_9),
                self.convert_str(r.supplier_doc_type_10),
                self.convert_str(r.supplier_doc_number_11),
                self.convert_str(r.supplier_name_12),
                self.convert_amount(r.tax_base_13),
                self.convert_amount(r.tax_amount_14),
                self.convert_amount(r.tax_base_15),
                self.convert_amount(r.tax_amount_16),
                self.convert_amount(r.tax_base_17),
                self.convert_amount(r.tax_amount_18),
                self.convert_amount(r.tax_base_19),
                self.convert_amount(r.tax_amount_20),
                self.convert_amount(r.tax_amount_21),
                self.convert_amount(r.total_amount_22),
                self.convert_amount(r.currency_exchange_rate_23),
                self.convert_date (r.original_issued_date_24),
                self.convert_str(r.original_doc_type_25),
                self.convert_str(r.original_sequence_26),
                self.convert_str(r.original_doc_number_27),
                self.convert_str(r.doc_number_28),
                self.convert_date (r.deposit_date_29),
                self.convert_str(r.retention_mark_31 and '1' or '0'),
                self.convert_date (r.operation_state_32),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_8_1.txt"

class ple_line_8_1 (osv.Model):
    _name = 'l10n_pe.ple_line_8_1'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_02', context=context)
    
    def _get_payment_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_10', context=context)
    
    _columns = {
        'ple_8_1_id': fields.many2one('l10n_pe.ple_8_1', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_8_1_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_8_1_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'issued_date_3': fields.date("Issued on", help="Fecha de emisión del comprobante de pago o documento"),
        'due_date_4': fields.date("Due date", help="Fecha de emisión del comprobante de pago o documento"),
        'type_5': fields.selection(_get_payment_type_selection, "Doc. type", help="Tipo de Comprobante de Pago o Documento, según SUNAT Tabla 10"),    
        'sequence_6': fields.char("Doc. sequence", size=20, help="Serie del comprobante de pago o documento. En los casos de la Declaración Única de Aduanas (DUA) o de la Declaración Simplificada de Importación (DSI) se consignará el código de la dependencia Aduanera."),
        'dua_dsi_year_7': fields.integer("DUA/DSI (YYYY)", help="Año de emisión de la DUA o DSI"),
        'tax_doc_number_8': fields.char("Tax payment doc", help="Número del comprobante de pago o documento o número de orden del formulario físico o virtual donde conste el pago del impuesto, tratándose de liquidaciones de compra, utilización de servicios prestados por no domiciliados u otros, número de la DUA, de la DSI, de la Liquidación de cobranza u otros documentos emitidos por SUNAT que acrediten el crédito fiscal en la importación de bienes."),
        'amount_9': fields.float("Final amount", help="En caso de optar por anotar el importe total de las operaciones diarias que no otorguen derecho a crédito fiscal en forma consolidada, registrar el número final (2)."),
        'supplier_doc_type_10': fields.selection(_get_doc_type_selection, "Supplier's doc.type", size=3, help="Tipo de Documento de Identidad del proveedor"),
        'supplier_doc_number_11': fields.char("Supplier's doc.number", size=15, help="Número de RUC del proveedor o número de documento de Identidad, según corresponda."),
        'supplier_name_12': fields.char("Supplier's name", size=200, help="Apellidos y nombres, denominación o razón social  del proveedor. En caso de personas naturales se debe consignar los datos en el siguiente orden: apellido paterno, apellido materno y nombre completo."),
        'tax_base_13': fields.float("Tax base 13", digits=(12,2), help="Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas exclusivamente a operaciones"),
        'tax_amount_14': fields.float("Tax amount 14", digits=(12,2), help="Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal"),
        'tax_base_15': fields.float("Tax base 15", digits=(12,2), help="Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas a operaciones gravadas y/o de exportación y a operaciones no gravadas"),
        'tax_amount_16': fields.float("Tax amount 16", digits=(12,2), help="Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal"),
        'tax_base_17': fields.float("Tax base 17", digits=(12,2), help="Base imponible de las adquisiciones gravadas que no dan derecho a crédito fiscal y/o saldo a favor por exportación, por no estar destinadas a operaciones gravadas y/o de exportación."),
        'tax_amount_18': fields.float("Tax amount 18", digits=(12,2), help="Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal"),
        'tax_base_19': fields.float("Tax base 19", digits=(12,2), help="Valor de las adquisiciones no gravadas"),
        'tax_amount_20': fields.float("Tax amount 20", digits=(12,2), help="Monto del Impuesto Selectivo al Consumo en los casos en que el sujeto pueda utilizarlo como deducción."),
        'tax_amount_21': fields.float("Other taxes", digits=(12,2), help="Otros tributos y cargos que no formen parte de la base imponible."),
        'total_amount_22': fields.float("Total amount", digits=(12,2),help="Importe total de las adquisiciones registradas según comprobante de pago."),
        'currency_exchange_rate_23': fields.float("Exchange rate", digits=(1,3), help="Tipo de cambio (3)."),
        'original_issued_date_24': fields.date("Original issue date", help="Fecha de emisión del comprobante de pago que se modifica (4)."),
        'original_doc_type_25': fields.selection(_get_payment_type_selection, "Original doc.type", help="Tipo de comprobante de pago que se modifica (4). SUNAT Tabla 10"),
        'original_sequence_26': fields.char('Original sequence', size=20, help="Número de serie del comprobante de pago que se modifica (4)."),
        'original_doc_number_27': fields.char('Original doc.number', size=20, help="Número del comprobante de pago que se modifica (4)."),
        'doc_number_28': fields.char("Doc.number w/o Address", size=20, help="Número del comprobante de pago emitido por sujeto no domiciliado (5)."),
        'deposit_date_29': fields.date("Detraction deposit date", help="Fecha de emisión de la Constancia de Depósito de Detracción (6)"),
        'deposit_number_30': fields.char("Detraction number", help="Número de la Constancia de Depósito de Detracción (6)"),                                     
        'retention_mark_31': fields.boolean("Retention mark", help="Marca del comprobante de pago sujeto a retención"),
        'operation_state_32': fields.selection ([
                                ('1', '1 - Este período'),
                                ('6', '6 - Período previo (dentro del año)'),
                                ('7', '7 - Período previo (fuera del año)'),
                                ('9', '9 - Ajuste período anterior'),
                            ], 'Operation state', help="""
1. Obligatorio
2. Registrar '1' cuando se anota el Comprobante de Pago o documento en el periodo que se emitió o que se pagó el impuesto, según corresponda.
3. Registrar '6' cuando la fecha de emisión del Comprobante de Pago o de pago del impuesto es anterior al periodo de anotación y esta se produce dentro de los doce meses siguientes a la emisión o pago del impuesto, según corresponda.
4. Registrar '7' cuando la fecha de emisión del Comprobante de Pago o pago del impuesto es anterior al periodo de anotación y esta se produce luego de los doce meses siguientes a la emisión o pago del impuesto, según corresponda.
5. Registrar '9' cuando se realice un ajuste en la anotación de la información de una operación registrada en un periodo anterior.                           
"""),
    }
    
    _order = 'sequence'
    
    _defaults = {
        'operation_state_32': '1',
    }
    
    def onchange_move_line_id (self, cr, uid, ids, move_line_id, company_id, context=None):
        vals = {}
        if move_line_id:
            aml_obj = self.pool.get('account.move.line')
            invoice_obj = self.pool.get('account.invoice')
            conf_obj = self.pool.get('l10n_pe.ple_configuration')
            currency_obj = self.pool.get('res.currency')
            
            conf_ids = conf_obj.search(cr, uid, [('report_type', '=', '8_1'), ('company_id', '=', company_id)], context=context)
            if not conf_ids:
                raise osv.except_osv (_('Configuration error'),
                       _('No configuration found for SUNAT report 8.1! Please check it'))
            conf = conf_obj.browse(cr, uid, conf_ids[0], context=context)

            ml = aml_obj.browse (cr, uid, move_line_id, context=context)
            vals['issued_date_3'] = ml.date
            vals['due_date_4'] = ml.date_maturity or ml.date
            vals['type_5'] = ml.journal_id.sunat_payment_type
            s = ml.ref.split('-')
            vals['sequence_6'] = len(s)>1 and s[0] or ''
            vals['tax_doc_number_8'] = len(s)>1 and s[1] or s[0] 
            vals['amount_9'] = ml.debit or ml.credit
            vals['supplier_doc_type_10'] = ml.partner_id and ml.partner_id.doc_type
            vals['supplier_doc_number_11'] = ml.partner_id and ml.partner_id.doc_number
            vals['supplier_name_12'] = ml.partner_id and ml.partner_id.name

            invoice_ids = invoice_obj.search(cr, uid, [('name', '=', ml.move_id.name)], context=context)
            
            vals['tax_base_13']   = 0.0
            vals['tax_amount_14'] = 0.0
            vals['tax_base_16']   = 0.0
            vals['tax_amount_17'] = 0.0
            vals['tax_base_18']   = 0.0
            vals['tax_amount_19'] = 0.0
            vals['tax_amount_20'] = 0.0
            vals['currency_exchange_rate_23'] = 0.0
            
            if invoice_ids:
                invoice = invoice_obj.browse(cr, uid, invoice_ids[0], context=context)
                base_13_total = 0.0
                amount_14_total = 0.0
                base_15_total = 0.0
                amount_16_total = 0.0
                base_17_total = 0.0
                amount_18_total = 0.0
                amount_20_total = 0.0
                other_total = 0.0
                for line in invoice.tax_line:
                    if line.tax_code_id in conf.base_13_tax_code:
                        base_13_total += line.base
                    elif line.tax_code_id in conf.amount_14_tax_code:
                        amount_14_total += line.tax_amount
                    if line.tax_code_id in conf.base_15_tax_code:
                        base_15_total += line.base
                    elif line.tax_code_id in conf.amount_16_tax_code:
                        amount_16_total += line.tax_amount
                    if line.tax_code_id in conf.base_17_total:
                        base_17_total += line.base
                    elif line.tax_code_id in conf.amount_18_tax_code:
                        amount_18_total += line.tax_amount
                    elif line.tax_code_id in conf.amount_20_tax_code:
                        amount_20_total += line.tax_amount
                    else:
                        other_total += line.tax_amount
                vals['tax_base_13']   = base_13_total
                vals['tax_amount_14'] = amount_14_total
                vals['tax_base_16']   = base_15_total
                vals['tax_amount_17'] = amount_16_total
                vals['tax_base_18']   = base_17_total
                vals['tax_amount_19'] = amount_18_total
                vals['tax_amount_20'] = amount_20_total
                vals['tax_amount_21'] = other_total

                vals['amount_9'] = invoice.amount_untaxed

                from_currency_id = currency_obj.search(cr, uid, [('name','=','USD')], context=context)[0]
                to_currency_id = currency_obj.search(cr, uid, [('name','=','PEN')], context=context)[0]
                vals['currency_exchange_rate_23'] = currency_obj.compute(cr, uid, 
                                                                from_currency_id, 
                                                                to_currency_id, 
                                                                1.0,
                                                                context=dict(context, date=ml.maturity_date or ml.date))
            return {'value': vals}
        else:
            return False

class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    _columns = {
        'base_13_tax_code': fields.many2many('account.tax.code', 'ple8_1_base_13_tax_code', 'conf_id', 'tax_code_id', 'Base 13 tax codes', 
                                             help="Código de impuesto de Base imponible de las adquisiciones gravadas que dan derecho a "
                                                  "crédito fiscal y/o saldo a favor por exportación, destinadas exclusivamente a operaciones gravadas y/o de exportación"),
        'amount_14_tax_code': fields.many2many('account.tax.code', 'ple8_1_amount_14_tax_code', 'conf_id', 'tax_code_id', 'Amount 14 tax codes', 
                                             help="Código de impuestos para el Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal"),
        'base_15_tax_code': fields.many2many('account.tax.code', 'ple8_1_base_15_tax_code', 'conf_id', 'tax_code_id', 'Base 15 tax codes', 
                                             help="Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a "
                                                  "favor por exportación, destinadas a operaciones gravadas y/o de exportación y a operaciones no gravadas"),
        'amount_16_tax_code': fields.many2many('account.tax.code', 'ple8_1_amount_16_tax_code', 'conf_id', 'tax_code_id', 'Amount 16 tax codes', 
                                             help="Código de impuestos para el Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal"),
        'base_17_tax_code': fields.many2many('account.tax.code', 'ple8_1_base_17_tax_code', 'conf_id', 'tax_code_id', 'Base 17 tax codes', 
                                             help="Base imponible de las adquisiciones gravadas que no dan derecho a crédito fiscal y/o saldo a "
                                                  "favor por exportación, por no estar destinadas a operaciones gravadas y/o de exportación."),
        'amount_18_tax_code': fields.many2many('account.tax.code', 'ple8_1_amount_18_tax_code', 'conf_id', 'tax_code_id', 'Amount 18 tax codes', 
                                             help="Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal"),
        'amount_20_tax_code': fields.many2many('account.tax.code', 'ple8_1_amount_20_tax_code', 'conf_id', 'tax_code_id', 'Amount 20 tax codes', 
                                             help="Monto del Impuesto Selectivo al Consumo en los casos en que el sujeto pueda utilizarlo como deducción."),
    }

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('8_1', '8.1 Compras'))
        return sorted(rep_types, key=lambda e: e[0])
