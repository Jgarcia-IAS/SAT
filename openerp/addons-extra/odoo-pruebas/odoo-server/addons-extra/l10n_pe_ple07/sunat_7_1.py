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

class ple_7_1 (osv.Model):
    _name = "l10n_pe.ple_7_1"
    _inherit = "l10n_pe.ple"

    _columns= {
        'fiscal_year': fields.man2one('account.fiscal_year', 'Fiscal year', required=True, readonly=True, states={'draft':[('readonly',False)],}),
        'lines_ids': fields.one2many ('l10n_pe.ple_line_7_1', 'ple_7_1_id', 'Lines', readonly=True, states={'draft':[('readonly',False)],}),
    }

    def action_reload (self, cr, uid, ids, context=None):
        #TODO
        return True

    def action_report (self, cr, uid, ids, context=None):
        assert ids and len(ids)==1

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_pe.sunat_7_1',
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
                self.convert_str(r.asset_code_3),
                self.convert_str(r.asset_type_4),
                self.convert_str(r.asset_account_code_5),
                self.convert_str(r.asset_state_6),
                self.convert_str(r.asset_description_7),
                self.convert_str(r.asset_brand_8),
                self.convert_str(r.asset_model_9),
                self.convert_str(r.asset_id_10),
                self.convert_amount(r.initial_amount_11),
                self.convert_amount(r.acquired_amount_12),
                self.convert_amount(r.improvements_amount_13),
                self.convert_amount(r.write_off_amount_14),
                self.convert_amount(r.other_amount_15),
                self.convert_amount(r.revaluation_amount_16),
                self.convert_amount(r.reorg_amount_17),
                self.convert_amount(r.other_reorg_amount_18),
                self.convert_amount(r.inflation_amount_19),
                self.convert_date (r.acquisition_date_20),
                self.convert_date (r.use_start_date_21),
                self.convert_str(r.depreciation_type_22),
                self.convert_str(r.dep_type_change_doc_23),
                self.convert_amount(r.dep_percentage_24),
                self.convert_amount(r.acum_dep_prev_25),
                self.convert_amount(r.dep_wo_rev_26),
                self.convert_amount(r.dep_dt_write_off_27),
                self.convert_amount(r.other_dep_28),
                self.convert_amount(r.rev_dep_29),
                self.convert_amount(r.reorg_dep_30),
                self.convert_amount(r.other_rev_dep_31),
                self.convert_amount(r.inflation_dep_32),
                self.convert_str(r.operation_state_33),
            ]
            res.append('|'.join(elements))
        return res

    def get_output_filename (self, cr, uid, ids, context=None):
        return "sunat_7_1.txt"

class ple_line_7_1 (osv.Model):
    _name = 'l10n_pe.ple_line_7_1'
    _inherit = 'l10n_pe.ple_line'
    
    def _get_catalog_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_13', context=context)
    
    def _get_asset_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_18', context=context)
    
    def _get_asset_state_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_19', context=context)
    
    def _get_depreciation_type_selection (self, cr, uid, context=None):
        bt_obj = self.pool.get('base.element')
    
        return bt_obj.get_as_selection(cr, uid, 'PE.SUNAT.TABLA_20', context=context)
    
    _columns = {
        'ple_7_1_id': fields.many2one('l10n_pe.ple_7_1', 'PLE', on_delete='cascade'),
        'state': fields.related ('ple_7_1_id', 'state', string='State', type="char"),
        'company_id': fields.related ('ple_7_1_id', 'company_id', string='Company', type="many2one", relation="res.company"),

        'catalog_2': fields.selection(_get_catalog_selection, "Catalog", size=1, required=True, help="Código del catálogo utilizado"),
        'asset_code_3': fields.char('Asset Code', size=24, required=True, help="Código relacionado con el Activo Fijo"),
        'asset_type_4': fields.selection(_get_asset_type_selection, "Asset type", size=1, required=True, help="Código del tipo de Activo Fijo"),
        'asset_account_code_5': fields.char('Asset Account Code', size=24, required=True, help="Código de la Cuenta Contable del Activo Fijo, desagregada hasta el nivel máximo de dígitos utilizado "),
        'asset_state_6': fields.selection(_get_asset_state_selection, "Asset state", size=1, required=True, help="Estado del Activo Fijo"),
        'asset_description_7': fields.char('Asset description', size=40, required=True, help="Descripción del Activo Fijo"),
        'asset_brand_8': fields.char('Asset brand', size=20, required=True, help="Marca del Activo Fijo"),
        'asset_model_9': fields.char('Asset model', size=20, required=True, help="Modelo del Activo Fijo"),
        'asset_id_10': fields.char('Asset id', size=20, required=True, help="Número de serie y/o placa del Activo Fijo"),
        'initial_amount_11': fields.float('Initial amount', digits=(12,2), help="Importe del saldo inicial del Activo Fijo"),
        'acquired_amount_12': fields.float('Acquired amount', digits=(12,2), help="Importe de las adquisiciones o adiciones de Activo Fijo"),
        'improvements_amount_13': fields.float('Improvements amount', digits=(12,2), help="Importe de las mejoras del Activo Fijo"),
        'write_off_amount_14': fields.float('Write off amount', digits=(12,2), help="Importe de los retiros y/o bajas del Activo Fijo"),
        'other_amount_15': fields.float('Other amount', digits=(12,2), help="Importe por otros ajustes en el valor del Activo Fijo"),
        'revaluation_amount_16': fields.float('Revaluation amount', digits=(12,2), help="Valor de la revaluación voluntaria efectuada"),
        'reorg_amount_17': fields.float('Reorg. amount', digits=(12,2), help="Valor de la revaluación efectuada por reorganización de sociedades"),
        'other_reorg_amount_18': fields.float('Other reorg. amount', digits=(12,2), help="Valor de otras revaluaciones efectuada"),
        'inflation_amount_19': fields.float('Inflation amount', digits=(12,2), help="Importe del valor del ajuste por inflación del Activo Fijo"),
        'acquisition_date_20': fields.date ('Acquisition date', required=True, help="Fecha de adquisición del Activo Fijo"),
        'use_start_date_21': fields.date ('Use start date', required=True, help="Fecha de inicio del Uso del Activo Fijo"),
        'depreciation_type_22': fields.selection(_get_depreciation_type_selection, "Depreciation type", size=1, required=True, help="Código del Método aplicado en el cálculo de la depreciación"),
        'dep_type_change_doc_23': fields.char('Dep. doc. change id', size=20, required=True, help="Número de documento de autorización para cambiar el método de la depreciación"),
        'dep_percentage_24': fields.float('Depreciation percentage', digits=(7,2), help="Porcentaje de la depreciación"),
        'acum_dep_prev_25': fields.float('Acumulated dep. previous', digits=(12,2), help="Depreciación acumulada al cierre del ejercicio anterior."),
        'dep_wo_rev_26': fields.float('Depreciation w/o revaluation', digits=(12,2), help="Valor de la depreciación del ejercicio sin considerar la revaluación"),
        'dep_dt_write_off_27': fields.float('Dep. due to write off', digits=(12,2), help="Valor de la depreciación del ejercicio relacionada con los retiros y/o bajas del Activo Fijo"),
        'other_dep_28': fields.float('Other depreciation', digits=(12,2), help="Valor de la depreciación relacionada con otros ajustes"),
        'rev_dep_29': fields.float('Revaluation depreciation', digits=(12,2), help="Valor de la depreciación de la revaluación voluntaria efectuada"),
        'reorg_dep_30': fields.float('Reorg.depreciation', digits=(12,2), help="Valor de la depreciación de la revaluación efectuada por reorganización de sociedades"),
        'other_rev_dep_31': fields.float('Other rev. depreciation', digits=(12,2), help="Valor de la depreciación de otras revaluaciones efectuadas"),
        'inflation_dep_32': fields.float('Inflation depreciation', digits=(12,2), help="Valor del ajuste por inflación de la depreciación"),
        'operation_state_33': fields.selection ([
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
        'operation_state_7': '1',
    }
    

class ple_configuration (osv.osv):
    _inherit = "l10n_pe.ple_configuration"

    def get_report_type (self, cr, uid, context=None):
        rep_types = super(ple_configuration, self).get_report_type(cr, uid, context=context)
        rep_types.append (('7_1', '7.1 Detalle de los activos fijos'))
        return sorted(rep_types, key=lambda e: e[0])
