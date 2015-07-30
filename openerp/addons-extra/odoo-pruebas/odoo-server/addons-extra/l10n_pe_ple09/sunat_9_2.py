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

class ple_9_2 (osv.Model):
    _name = "l10n_pe.ple_9_2"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_9_2', 'ple_9_2_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_9_2')
        stock_move_obj = self.pool.get('stock.move')
        conf_obj = self.pool.get('l10n_pe.ple_configuration')
        
        ple = self.browse(cr, uid, ids[0], context=context)

        conf_ids = conf_obj.search(cr, uid, [('report_type', '=', '9_2'), ('company_id', '=', ple.company_id.id)], context=context)
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
        
        move_ids = stock_move_obj.search(cr, uid, ['|',('location_id','in',conf.consigner_locations), ('location_dest_id','in',conf.consigner_locations),
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
                vals['receiver_doc_number_16'] = partner and partner.doc_number
                vals['receiver_name_17'] = partner and partner.name
                vals['quantity_sent_18'] = 0.0
                vals['quantity_received_19'] = initial_stock[product]
                vals['quantity_sold_20'] = 0.0
                
                ple_line_obj.create(cr, uid, vals, context=context)

            for m in sorted(moves, key=lambda m: m.date):
                src = m.location_id.id in conf.consignee_locations
                dst = m.location_dest_id.id in conf.consignee_locations
                vals = {
                    'ple_12_1_id': ple.id,
                }
                if src and not dst:
                    outgoing_moves[m.product_id] += m.product_qty
                    final_stock[m.product_id] -= m.product_qty
                    vals['quantity_sent_18'] = m.product_qty
                elif dst and not src:
                    incoming_moves[m.product_id] += m.product_qty
                    final_stock[m.product_id] += m.product_qty
                    if m.purchase_line_id:
                        vals['quantity_sold_20'] = m.product_qty
                    else:
                        vals['quantity_received_19'] = m.product_qty
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
                vals['payment_doc_id_13'] = m.purchase_line_id and m.purchase_line_id.order_id.number.split('-')[0] or False
                vals['payment_number_14'] = m.purchase_line_id and m.purchase_line_id.order_id.number.split('-')[1] or False
                vals['send_received_date_15'] = m.date
                vals['receiver_doc_number_16'] = partner and partner.doc_number
                vals['receiver_name_17'] = partner and partner.name
                
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
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_9_2',
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
                self.convert_str(r.sending_number_10),
                self.convert_str(r.issued_doc_type_11),
                self.convert_date (r.issued_doc_on_12),
                self.convert_str(r.payment_doc_id_13),
                self.convert_str(r.payment_number_14),
                self.convert_date(r.send_received_date_15),
                self.convert_str(r.sender_doc_number_16),
                self.convert_str(r.sender_name_17),
                self.convert_amount(r.quantity_received_18),
                self.convert_amount(r.quantity_given_back_19),
                self.convert_amount(r.quantity_sold_20),
                self.convert_str(r.operation_state_21),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_9_2.txt"

class ple_line_9_2 (osv.Model):
    _name = 'l10n_pe.ple_line_9_2'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_catalog_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_13', context=context)
    
    def _get_asset_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_05', context=context)
    
    def _get_doc_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_10', context=context)
    
    def _get_uom_code_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_06', context=context)

    _columns = {
        'ple_9_2_id': fields.many2one('l10n_pe.ple_9_2', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_9_2_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_9_2_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'catalog_2': fields.selection(_get_catalog_selection, "Catalog", size=1, required=True, help="Código del catálogo utilizado"),
        'asset_type_3': fields.selection(_get_asset_type_selection, "Asset type", size=2, required=True, help="Tipo de existencia"),
        'asset_id_4': fields.char('Asset identification', size=24, required=True, help="Código de la existencia"),
        'asset_name_6': fields.char('Asset name', size=80, help="Nombre de la existencia"),
        'uom_code_7': fields.selection(_get_uom_code_selection, "UOM type", size=3, required=True, help="Código de la unidad de medida"),
        'sent_on_8': fields.date ('Sent on', required=True, help="Fecha de emisión de la guía de remisión emitido por el consignador"),
        'sending_id_9': fields.integer('Sending id', 
                            help="Serie de la guía de remisión emitido por el consignador, con la que se reciben los bienes o se devuelven al consignador los bienes no vendidos"),
        'sending_number_10': fields.integer('Sending number', required=True,
                            help="Número de la guía de remisión emitido por el consignador, con la que se reciben los bienes o se devuelven al consignador los bienes no vendidos"),
        'issued_doc_type_11': fields.selection(_get_doc_type_selection, "Doc. type", size=3, required=True, help="Tipo de Comprobante de Pago o Documento emitido por el consignador"),
        'issued_doc_on_12': fields.date ('Issued on', required=True, help="Fecha de emisión del comprobante emitido por el consignatario, por la venta de los bienes recibidos en consignación"),
        'payment_doc_id_13': fields.char('Payment doc. id', size=20, required=True, help="Serie del Comprobante de Pago emitido por el consignatario, por la venta de los bienes recibidos en consignación"),
        'payment_number_14': fields.char('Payment number', size=20, required=True, help="Número del Comprobante de Pago emitido por el consignatario, por la venta de los bienes recibidos en consignación"),
        'send_received_date_15': fields.date('Send/received date', required=True, help="Fecha de recepción, devolución o venta del bien"),
        'sender_doc_number_16': fields.char("Sender's doc. number", size=15, help="Número de RUC del consignador"),
        'sender_name_17': fields.char('Sender name', size=20, required=True, help="Apellidos y Nombres, Denominación o Razón Social del consignador"),
        'quantity_received_18': fields.float('Quantity received', digits=(12,2), help="Cantidad de bienes recibidos en consignación (la primera tupla corresponde al saldo inicial)"),
        'quantity_given_back_19': fields.float('Quantity given back', digits=(12,2), help="Cantidad de bienes devueltos al consignador"),
        'quantity_sold_20': fields.float('Quantity sold', digits=(12,2), help="Cantidad de bienes vendidos por el consignatario"),
        'operation_state_21': fields.selection ([
                                ('1', '1'),
                                ('8', '8'),
                                ('9', '9'),
                            ], 'Operation state', required=True, help="""
Registrar '1' cuando la operación corresponde al periodo, 
'8' cuando la operación corresponde a un periodo anterior y NO ha sido anotada en dicho periodo o
'9' cuando la operación corresponde a un periodo anterior y SI ha sido anotada en dicho periodo."""),
    }

    _defaults = {
        'operation_state_21': '1',    
    }
    
    def onchange_doc (self, cr, uid, ids, partner_doc_number, context=None):
        res = {}

        if (not partner_doc_number) or (len (partner_doc_number) < 8 or len(partner_doc_number) > 11) or not partner_doc_number.isdigit():
            raise osv.except_osv (_('Value error'),
                       _('RUC should be numeric, 8-11 numbers long! Please check!'))

        return res and {'value': res}
        
class ple_configuration (osv.Model):
    _inherit = "l10n_pe.ple_configuration"

    _columns = {
        'consigner_locations': fields.many2many('stock.location', 'ple9_1_stock_locations', 'conf_id', 'location_id', 'Consigner Stock locations to consider'),
    }

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('9_2', '9.2 Bienes recibidos en consignación'))
        return sorted(rep_types, key=lambda e: e[0])

