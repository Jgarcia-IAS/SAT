# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 I.A.S. INGENIERÍA, APLICACIONES Y SOFTWARE Johan Alejandro Olano (<http:http://www.ias.com.co).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv
class res_partner(osv.osv):
    _inherit = 'res.partner'

    def onchange_nomenclature(self, cr, uid, ids, nomenclature, nomenclature_text, nomenclature_1, nomenclature_text_1, nomenclature_2, nomenclature_text_2,nomenclature_3,nomenclature_text_3, context=None):
        res = {'value':{}}
        res['value']['street3'] = (nomenclature and (nomenclature+' ') or '') + (nomenclature_text and (nomenclature_text+' ') or '') + (nomenclature_1 and (nomenclature_1+' ') or '') + (nomenclature_text_1 and (nomenclature_text_1+' ') or '')  + (nomenclature_2 and (nomenclature_2+' ') or '') + (nomenclature_text_2 and (nomenclature_text_2+' ') or '') + (nomenclature_3 and (nomenclature_3+' ') or '') + (nomenclature_text_3 and (nomenclature_text_3+' ') or '')
        return res

    _columns = {

        'nomenclature': fields.selection([('CR', 'CR'),
        ('CL', 'CL'),('AV','AV'),('DG' ,'DG'),('TV','TV'),('AK','AK'),('AC','AC'),('AUT','AUT'),
         ('CRT','CRT'),('CRV','CRV'),('CON','CON'),('CONJ','CONJ'),('UN','UN'),('UR','UR'),('URB','URB'),('BRR','BRR'),('MZ','MZ'),('AP','AP'),('TO','TO'),
        ('BL','BL'),('P','P'),('CA','CA'),('CC','CC'),('LC','LC')
        ],size=22),
        'nomenclature_text': fields.char(size=22),
        'nomenclature_1':fields.selection([('CR', 'CR'),
        ('CL', 'CL'),('AV','AV'),('DG' ,'DG'),('TV','TV'),('AK','AK'),('AC','AC'),('AUT','AUT'),
         ('CRT','CRT'),('CRV','CRV'),('CON','CON'),('CONJ','CONJ'),('UN','UN'),('UR','UR'),('URB','URB'),('BRR','BRR'),('MZ','MZ'),('AP','AP'),('TO','TO'),
        ('BL','BL'),('P','P'),('CA','CA'),('CC','CC'),('LC','LC')
        ],size=22),
        'nomenclature_text_1': fields.char(size=22),
        'nomenclature_2':fields.selection([('CR', 'CR'),
        ('CL', 'CL'),('AV','AV'),('DG' ,'DG'),('TV','TV'),('AK','AK'),('AC','AC'),('AUT','AUT'),
         ('CRT','CRT'),('CRV','CRV'),('CON','CON'),('CONJ','CONJ'),('UN','UN'),('UR','UR'),('URB','URB'),('BRR','BRR'),('MZ','MZ'),('AP','AP'),('TO','TO'),
        ('BL','BL'),('P','P'),('CA','CA'),('CC','CC'),('LC','LC')
        ],size=22),
        'nomenclature_text_2': fields.char(size=22),
        'nomenclature_3':fields.selection([('CR', 'CR'),
        ('CL', 'CL'),('AV','AV'),('DG' ,'DG'),('TV','TV'),('AK','AK'),('AC','AC'),('AUT','AUT'),
         ('CRT','CRT'),('CRV','CRV'),('CON','CON'),('CONJ','CONJ'),('UN','UN'),('UR','UR'),('URB','URB'),('BRR','BRR'),('MZ','MZ'),('AP','AP'),('TO','TO'),
        ('BL','BL'),('P','P'),('CA','CA'),('CC','CC'),('LC','LC')
        ],size=22),
        'nomenclature_text_3': fields.char(size=22),
        'street3':fields.char(),




    }


