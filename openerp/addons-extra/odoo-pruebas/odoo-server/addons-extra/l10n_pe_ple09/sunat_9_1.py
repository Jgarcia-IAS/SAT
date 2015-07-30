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
from datetime import timedelta, date

class ple_9_1 (osv.Model):
    _name = "l10n_pe.ple_9_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_9_1', 'ple_9_1_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_9_1')
        stock_move_obj = self.pool.get('stock.move')
        conf_obj = self.pool.get('l10n_pe.ple_configuration')
        
        ple = self.browse(cr, uid, ids[0], context=context)

        conf_ids = conf_obj.search(cr, uid, [('report_type', '=', '9_1'), ('company_id', '=', ple.company_id.id)], context=context)
        if not conf_ids:
            raise osv.except_osv (_('Configuration error'),
                   _('No configuration found for SUNAT report 9.1! Please check it'))
        conf = conf_obj.browse(cr, uid, conf_ids[0], context=context)
        
        cmds = []
        for line in ple.lines_ids:
            cmds.append((2, line.id))
        if cmds:
            ple.write({'lines_ids': cmds}, context=context)
        ple.refresh()
        
        move_ids = stock_move_obj.search(cr, uid, ['|',('location_id','in',conf.consignee_locations), ('location_dest_id','in',conf.consignee_locations),
                                                   ('company_id','=', ple.company_id.id),
                                                   ('date','>=', ple.period_id.date_start),('date','<=',ple.period_id.date_stop),
                                                   ('state','=', 'done')], context=context)
        if move_ids:
            moves = stock_move_obj.browse(cr, uid, move_ids, context=context)

            products = list(set([m.product_id for m in moves]))

            initial_stock = {}
            
            initial_date = ple.period_id.date_start
            previous_day = date(int(initial_date[0:4]), int(initial_date[5:7]), int(initial_date[9:11])) - timedelta(days=1)
            previous_date = previous_day.strftime("%Y-%m-%d")
            for product in products:
                initial_stock[product] = product.get_product_available(context=dict(context, 
                                                                                    location=conf.stock_locations,
                                                                                    to_date=previous_date))
            final_stock = {product: initial_stock[product] for product in products}
            incoming_moves = {product: 0 for product in products}
            outgoing_moves = {product: 0 for product in products}
            
            partner = None
            for m in moves:
                if m.partner_id:
                    partner = m.partner_id
                    break

            for product in products:
                vals = {
                    'ple_9_1_id': ple.id,
                }
                vals['quantity_sent_19'] = initial_stock[product]

                vals['catalog_2'] = product.sunat_valuation_method
                vals['asset_type_3'] = product.categ_id and product.categ_id.sunat_inventory_type
                vals['asset_id_4'] = product.code
                vals['asset_name_6'] = product.code.name
                vals['uom_type_7'] = product.uom_id.sunat_code
                vals['sent_on_8'] = ple.period_id.date_start
                vals['doc_id_9'] = False
                vals['doc_id_10'] = False
                vals['issued_doc_type_11'] = False
                vals['issued_doc_on_12'] = ple.period_id.date_start
                vals['payment_doc_id_13'] = False
                vals['payment_number_14'] = False
                vals['send_received_date_15'] = False
                vals['receiver_doc_type_16'] = partner and partner.doc_type
                vals['receiver_doc_number_17'] = partner and partner.doc_number
                vals['receiver_name_18'] = partner and partner.name
                vals['quantity_sent_19'] = initial_stock[product]
                vals['quantity_received_20'] = 0.0
                vals['quantity_sold_21'] = 0.0
                
                ple_line_obj.create(cr, uid, vals, context=context)

            for m in sorted(moves, key=lambda m: m.date):
                src = m.location_id.id in conf.consignee_locations
                dst = m.location_dest_id.id in conf.consignee_locations
                vals = {
                    'ple_12_1_id': ple.id,
                }
                if src and not dst:
                    outgoing_moves[m.product_id] += product_qty
                    final_stock[m.product_id] -= product_qty
                    vals['quantity_received_20'] = product_qty
                elif dst and not src:
                    incoming_moves[m.product_id] += product_qty
                    final_stock[m.product_id] += product_qty
                    if m.picking_id and m.picking_id.sale_id:
                        vals['quantity_sold_21'] = product_qty
                    else:
                        vals['quantity_sent_19'] = product_qty
                else:
                    # It is an internal move
                    continue

                vals['catalog_2'] = m.product_id.sunat_valuation_method
                vals['asset_type_3'] = m.product_id.categ_id and m.product.categ_id.sunat_inventory_type
                vals['asset_id_4'] = m.product_id.code
                vals['asset_name_6'] = m.product_id.code.name
                vals['uom_type_7'] = m.product_id.uom_id.sunat_code
                vals['sent_on_8'] = ple.period_id.date_start
                vals['doc_id_9'] = m.picking_id and m.picking_id.name.split('-')[0] or False
                vals['doc_id_10'] = m.picking_id and m.picking_id.name.split('-')[1] or m.name
                vals['issued_doc_type_11'] = m.picking_id and m.picking_id.sunat_doc_type or False
                vals['issued_doc_on_12'] = m.date
                vals['payment_doc_id_13'] = m.picking_id and m.picking_id.sale_id and m.picking_id.sale_id.number.split('-')[0] or False,
                vals['payment_number_14'] = m.picking_id and m.picking_id.sale_id and m.picking_id.sale_id.number.split('-')[1] or False,
                vals['send_received_date_15'] = False
                vals['receiver_doc_type_16'] = partner and partner.doc_type
                vals['receiver_doc_number_17'] = partner and partner.doc_number
                vals['receiver_name_18'] = partner and partner.name
                
                ple_line_obj.create(cr, uid, vals, context=context)

        self.action_renumber(cr, uid, ids, context=context)
        
        return True

    def action_renumber (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        next_seq = 1
        for line in sorted(ple.lines_ids, key=lambda l: l.send_received_date_15):
            line.write ({'sequence': next_seq}, context=context)
            next_seq += 1

        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_9_1',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str(r.catalog_2),
                self.convert_str(r.asset_type_3),
                self.convert_str(r.asset_id_4),
                self.convert_str(r.sequence),
                self.convert_str(r.asset_name_6),
                self.convert_str(r.uom_code_7),
                self.convert_date (r.sent_on_8),
                self.convert_str(r.sending_id_9),
                self.convert_str(r.sending_id_10),
                self.convert_str(r.issued_doc_type_11),
                self.convert_date (r.issued_doc_on_12),
                self.convert_str(r.payment_doc_id_13),
                self.convert_str(r.payment_number_14),
                self.convert_date(r.send_received_date_15),
                self.convert_str(r.receiver_doc_type_16),
                self.convert_str(r.receiver_doc_number_17),
                self.convert_str(r.receiver_name_18),
                self.convert_amount(r.quantity_sent_19),
                self.convert_amount(r.quantity_received_20),
                self.convert_amount(r.quantity_sold_21),
                self.convert_str(r.operation_state_22),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_9_1.txt"

class ple_line_9_1 (osv.Model):
    _name = 'l10n_pe.ple_line_9_1'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_catalog_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_13', context=context)
    
    def _get_asset_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_05', context=context)
    
    def _get_issued_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_10', context=context)
    
    def _get_uom_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_06', context=context)

    def _get_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_02', context=context)

    _columns = {
        'ple_9_1_id': fields.many2one('l10n_pe.ple_9_1', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_9_1_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_9_1_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'catalog_2': fields.selection(_get_catalog_selection, "Catalog", size=1, required=True, help="Código del catálogo utilizado"),
        'asset_type_3': fields.selection(_get_asset_type_selection, "Asset type", size=2, required=True, help="Tipo de existencia"),
        'asset_id_4': fields.char('Asset identification', size=24, required=True, help="Código de la existencia"),
        'asset_name_6': fields.char('Asset name', size=80, help="Nombre de la existencia"),
        'uom_code_7': fields.selection(_get_uom_code_selection, "UOM code", size=3, required=True, help="Código de la unidad de medida"),
        'sent_on_8': fields.date ('Sent on', required=True, help="Fecha de emisión de la guía de remisión emitido por el consignador"),
        'sending_id_9': fields.integer('Sending serial', 
                            help="Serie de la guía de remisión emitido por el consignador, con la que entrega los bienes al consignatario o se recibe los bienes no vendidos por el consignatario"),
        'sending_id_10': fields.integer('Sending number', required=True,
                            help="Número de la guía de remisión emitido por el consignador, con la que entrega los bienes al consignatario o se recibe los bienes no vendidos por el consignatario"),
        'issued_doc_type_11': fields.selection(_get_issued_doc_type_selection, "Doc. type", size=3, required=True, help="Tipo de Comprobante de Pago o Documento emitido por el consignador"),
        'issued_doc_on_12': fields.date ('Issued on', required=True, help="Fecha de emisión del comprobante emitido por el consignador"),
        'payment_doc_id_13': fields.char('Payment doc. id', size=20, required=True, help="Serie del Comprobante de Pago emitido por el consignador"),
        'payment_number_14': fields.char('Payment number', size=20, required=True, help="Número del Comprobante de Pago emitido por el consignador"),
        'send_received_date_15': fields.date('Send/received date', required=True, help="Fecha de entrega o devolución del bien"),
        'receiver_doc_type_16': fields.selection(_get_doc_type_selection, "Receiver Doc. type", required=True, size=3, help="Tipo de documento de identidad del consignatario"),
        'receiver_doc_number_17': fields.char("Receiver's doc. number", size=15, help="Número de RUC del consignatario o del documento de identidad"),
        'receiver_name_18': fields.char('Receiver name', size=20, required=True, help="Apellidos y Nombres, Denominación o Razón Social del consignatario"),
        'quantity_sent_19': fields.float('Quantity sent', digits=(12,2), help="Cantidad de bienes entregados en consignación (la primera tupla corresponde al saldo inicial)"),
        'quantity_received_20': fields.float('Quantity received', digits=(12,2), help="Cantidad de bienes devueltos por el consignatario"),
        'quantity_sold_21': fields.float('Quantity sold', digits=(12,2), help="Cantidad de bienes vendidos"),
        'operation_state_22': fields.selection ([
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
        'operation_state_22': '1',
    }

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
        'consignee_locations': fields.many2many('stock.location', 'ple9_1_stock_locations', 'conf_id', 'location_id', 'Consignee Stock locations to consider'),
    }

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('9_1', '9.1 Bienes entregados en consignación'))
        return sorted(rep_types, key=lambda e: e[0])
