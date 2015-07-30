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

class ple_12_1 (osv.Model):
    _name = "l10n_pe.ple_12_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'lines_ids': fields.one2many ('l10n_pe.ple_line_12_1', 'ple_12_1_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1
        ple_line_obj = self.pool.get('l10n_pe.ple_line_12_1')
        stock_move_obj = self.pool.get('stock.move')
        conf_obj = self.pool.get('l10n_pe.ple_configuration')
        
        ple = self.browse(cr, uid, ids[0], context=context)

        conf_ids = conf_obj.search(cr, uid, [('report_type', '=', '12_1'), ('company_id', '=', ple.company_id.id)], context=context)
        if not conf_ids:
            raise osv.except_osv (_('Configuration error'),
                   _('No configuration found for SUNAT report 12.1 (used also by 13.1)! Please check it'))
        conf = conf_obj.browse(cr, uid, conf_ids[0], context=context)
        
        cmds = []
        for line in ple.lines_ids:
            cmds.append((2, line.id))
        if cmds:
            ple.write({'lines_ids': cmds}, context=context)
        ple.refresh()
        
        move_ids = stock_move_obj.search(cr, uid, ['|',('location_id','in',conf.stock_locations), ('location_dest_id','in',conf.stock_locations),
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

            for product in products:
                vals = {
                    'ple_12_1_id': ple.id,
                }
                vals['input_qty_13'] = initial_stock[product]

                vals['catalog_3'] = product.sunat_valuation_method
                vals['asset_type_4'] = product.categ_id and product.categ_id.sunat_inventory_type
                vals['asset_id_5'] = product.code
                vals['issued_on_6'] = ple.period_id.date_start
                vals['doc_type_7'] = False
                vals['doc_id_8'] = False
                vals['doc_id_9'] = False
                vals['op_type_10'] = False
                vals['description_11'] = 'Stock inicial del período'
                vals['uom_code_12'] = product.uom_id and product.uom_id.sunat_code
                
                ple_line_obj.create(cr, uid, vals, context=context)

            for m in sorted(moves, key=lambda m: m.date):
                src = m.location_id.id in conf.stock_locations
                dst = m.location_dest_id.id in conf.stock_locations
                vals = {
                    'ple_12_1_id': ple.id,
                }
                if src and not dst:
                    outgoing_moves[m.product_id] += m.product_qty
                    final_stock[m.product_id] -= m.product_qty
                    vals['output_qty_14'] = m.product_qty
                elif dst and not src:
                    incoming_moves[m.product_id] += m.product_qty
                    final_stock[m.product_id] += m.product_qty
                    vals['input_qty_13'] = m.product_qty
                else:
                    # It is an internal move
                    continue

                vals['catalog_3'] = m.product_id.sunat_valuation_method
                vals['asset_type_4'] = m.product_id.categ_id and m.product.categ_id.sunat_inventory_type
                vals['asset_id_5'] = m.product_id.code
                vals['issued_on_6'] = m.date
                vals['doc_type_7'] = m.picking_id and m.picking_id.sunat_doc_type or False
                vals['doc_id_8'] = m.picking_id and m.picking_id.name.split('-')[0] or False
                vals['doc_id_9'] = m.picking_id and m.picking_id.name.split('-')[1] or False
                vals['op_type_10'] = m.picking_id and m.picking_id.sunat_op_type or False
                vals['description_11'] = m.picking_id and m.picking_id.name or '<sin referencia>'
                vals['uom_code_12'] = m.product_id.uom_id and m.product_id.uom_id.sunat_code
                
                ple_line_obj.create(cr, uid, vals, context=context)

        self.action_renumber(cr, uid, ids, context=context)
        
        return True

    def action_renumber (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        next_seq = 1
        for line in sorted(ple.lines_ids, key=lambda l: l.issued_on_6):
            line.write ({'sequence': next_seq}, context=context)
            next_seq += 1

        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_12_1',
            'datas': {},
        }

    def get_output_lines (self, cr, uid, ids, context=None):

        assert ids and len(ids)==1

        ple = self.browse (cr, uid, ids[0], context=context)

        res = []
        for r in ple.lines_ids:
            elements = [
                "%s%s00" % (ple.period_id.date_start[0:4], ple.period_id.date_start[5:7]),
                self.convert_str("%04d%03d" % (r.annex_2, r.sequence)),
                self.convert_str(r.catalog_3),
                self.convert_str(r.asset_type_4),
                self.convert_str(r.asset_id_5),
                self.convert_date(r.issued_on_6),
                self.convert_str(r.doc_type_7),
                self.convert_str(r.doc_id_8),
                self.convert_str(r.doc_id_9),
                self.convert_str(r.op_type_10),
                self.convert_str(r.description_11),
                self.convert_str(r.uom_code_12),
                self.convert_amount(r.input_qty_13),
                self.convert_amount(r.output_qty_14),
                self.convert_str(r.operation_state_15),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_12_1.txt"

class ple_line_12_1 (osv.Model):
    _name = 'l10n_pe.ple_line_12_1'
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

    def _get_op_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_12', context=context)
    
    _columns = {
        'ple_12_1_id': fields.many2one('l10n_pe.ple_12_1', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_12_1_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_12_1_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'annex_2': fields.integer('Annex', required=True, digits=4, help="""Código de establecimiento anexo:
1. Los cuatro primeros dígitos son obligatorios y corresponden al código de establecimiento anexo según el Registro Único de Contribuyentes")
2. De la posición 5 a la 7 se registrara un correlativo (secuencia)"""),
        'catalog_3': fields.selection(_get_catalog_selection, "Catalog", size=1, required=True, help="Código del catálogo utilizado"),
        'asset_type_4': fields.selection(_get_asset_type_selection, "Asset type", size=2, required=True, help="Tipo de existencia"),
        'asset_id_5': fields.char('Asset identification', size=24, required=True, help="Código de la existencia"),
        'issued_on_6': fields.date('Issued on', required=True, 
                                 help="Fecha de emisión del documento de traslado, comprobante de pago, documento interno o similar"),
        'doc_type_7': fields.selection(_get_doc_type_selection, "Doc. type", size=2, required=True, 
                                       help="Tipo del documento de traslado, comprobante de pago, documento interno o similar"),
        'doc_id_8': fields.char('Doc. identification', size=20, required=True, 
                                help="Número de serie del documento de traslado, comprobante de pago, documento interno o similar"),
        'doc_id_9': fields.char('Doc. identification (2)', size=20, required=True, 
                                help="Número de serie del documento de traslado, comprobante de pago, documento interno o similar"),
        'op_type_10': fields.selection(_get_op_type_selection, "Operation type", size=2, required=True, help="Tipo de operación efectuada"),
        'description_11': fields.char('Asset description', size=80, help="Descripción de la existencia"),
        'uom_code_12': fields.selection(_get_uom_code_selection, "UOM code", size=3, required=True, help="Código de la unidad de medida"),
        'input_qty_13': fields.float('Input quantity', digits=(12,2), help="Entradas de las unidades físicas (la primera tupla corresponde al saldo inicial)"),
        'output_qty_14': fields.float('Output quantity', digits=(12,2), help="Salidas de las unidades físicas"),
        'operation_state_15': fields.selection ([
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
        'issued_on_6': fields.date.context_today,
        'operation_state_15': '1',
    }
    
class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    _columns = {
        'stock_locations': fields.many2many('stock.location', 'ple12_1_stock_locations', 'conf_id', 'location_id', 'Stock locations to consider'),
    }

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('12_1', '12.1 Inventario físico'))
        return sorted(rep_types, key=lambda e: e[0])

