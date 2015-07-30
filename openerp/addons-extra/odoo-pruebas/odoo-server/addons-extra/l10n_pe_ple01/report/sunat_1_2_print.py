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

import time

from openerp.report import report_sxw

class sunat_1_2_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(sunat_1_2_report, self).__init__(cr, uid, name, context)
        self.localcontext.update( {
            'get_banks': self.get_banks,
            'time': time,
        })
        self.context = context

    def get_banks(self, ple):
        be_obj = self.pool.get("base.element")
        banks = []
        src = sorted(ple.lines_ids, key=lambda l: (l.bank_code_3, l.bank_number_4, l.sequence))

        lines = []
        current_bank = None
        current_account = None
        for l in src:
            if (current_bank == None) or current_bank != l.bank_code_3 or current_account != l.bank_number_4:
                if current_bank != None:
                    be = be_obj.get_element(self.cr, self.uid, "PE.SUNAT.TABLA_03", current_bank, 'element_char')
                    banks.append({'bank_code': current_bank, 
                                  'bank_name': be and be[0] or '<desconocido>',
                                  'bank_number': current_account or '<desconocido>',
                                  'lines': lines})
                lines = []
                current_bank = l.bank_code_3
                current_account = l.bank_number_4
            lines.append(l)
        if current_bank != None:
            be = be_obj.get_element(self.cr, self.uid, "PE.SUNAT.TABLA_03", current_bank, 'element_char')
            banks.append({'bank_code': current_bank, 
                          'bank_name': be and be[0] or '<desconocido>',
                          'bank_number': current_account or '<desconocido>',
                          'lines': lines})
        return banks

report_sxw.report_sxw('report.l10n_pe.sunat_1_2', 'l10n_pe.ple_1_2',
    'addons/l10n_pe_ple01/report/sunat_1_2.rml', parser=sunat_1_2_report, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
