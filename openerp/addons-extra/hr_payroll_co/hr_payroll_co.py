# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.techreceptives.com>)
#    Special Credit and Thanks to Thymbra Latinoamericana S.A.
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
#/#############################################################################

import time
from openerp.osv import fields, orm, osv, expression
from openerp.tools.translate import _
from datetime import datetime
import openerp.addons.decimal_precision as dp

class hr_payslip_run(orm.Model):
    _inherit = 'hr.payslip.run'

    _columns = {        
       'liquida' : fields.boolean('Liquidación', help="Indica si se ejecuta una estructura para liquidacion de contratos y vacaciones"),
       'struct_id':fields.many2one('hr.payroll.structure', 'Estructura salarial', help="Defina la estructura salarial que se usará para la liquidacion de contratos y vacaciones"),   
       'date_prima' : fields.date ('Fecha de liquidación de prima'),
       'date_cesantias' : fields.date ('Fecha de liquidación de cesantías'),
       'date_vacaciones' : fields.date ('Fecha de liquidación de vacaciones'),
       'dias_vacaciones': fields.float('Días tomados de vacaciones', digits_compute=dp.get_precision('Payroll')),
       'date_intereses' : fields.date ('Fecha de liquidación de intereses a las cesantías'),
       'date_liquidacion' : fields.date ('Fecha de liquidación contrato'),
    }

    _defaults = {
        'liquida': False,
    }

class hr_contract_setting(orm.Model):
    _name= 'hr.contract.setting'
    _description = 'Configuracion nomina'

    _columns = {
        'contrib_id' : fields.many2one ('hr.contribution.register','Concepto', help="Concepto de aporte"),
        'partner_id' : fields.many2one ('res.partner','Entidad', help="Entidad relacionada"),
        'account_debit_id' : fields.many2one('account.account', 'Cuenta deudora'),
        'account_credit_id' : fields.many2one('account.account', 'Cuenta acreedora'),
        'contract_id' : fields.many2one('hr.contract', 'Riesgos', required=True, ondelete='cascade', select=True),        
    }

class hr_employee(orm.Model):
    _inherit = 'hr.employee' 
    
    _sql_constraints = [('emp_identification_uniq', 'unique(identification_id)', 'La cedula debe ser unica. La cedula ingresada ya existe'),
                       ]

class hr_department_salary_rule(orm.Model):
    _name = 'hr.department.salary.rule'
    _description = 'Cuentas contables por departamento'

    _columns = {
        'department_id' : fields.many2one('hr.department', 'Departamento', required=True, ondelete='cascade', select=True),
        'salary_rule_id' : fields.many2one('hr.salary.rule', 'Regla salarial', required=True),
        'account_debit_id' : fields.many2one('account.account', 'Cuenta deudora'),
        'account_credit_id' : fields.many2one('account.account', 'Cuenta acreedora'),       
    } 
    
    _sql_constraints = [('department_rule_uniq', 'unique(department_id, salary_rule_id)', 'La regla debe ser unica por departamento. La regla ingresada ya existe'),
                       ]   

class hr_department(orm.Model):
    _inherit = 'hr.department'

    _columns = {
        'account_analytic_id': fields.many2one('account.analytic.account','Cuenta analítica',required=True),   
        'salary_rule_ids' : fields.one2many('hr.department.salary.rule', 'department_id', 'Reglas salariales'),
    }
    
class hr_salary_rule(orm.Model):
    _inherit = 'hr.salary.rule'

    _columns = {        
       'acumula' : fields.boolean('Acumula', help="Indica si el valor se acumula para liquidación de contratos"),
       'type_distri' : fields.selection([('na','No aplica'), ('hora','Horas reportadas'),('dpto','Por contrato'),('novedad','Por novedades')],'Tipo distribución', required=True),
       'register_credit_id':fields.many2one('hr.contribution.register', 'Registro contribución crédito', help="Identificación del movimiento cédito de la regla salarial"),   
    }

    _defaults = {
        'acumula': False,
        'type_distri' : 'na',
    }

class hr_salary_rule_category(orm.Model):
    _inherit = 'hr.salary.rule.category'

    _columns = {        
        'type' : fields.selection([('Devengado','Devengado'),('Deducción','Deducción')],'Tipo'),
    }

class hr_contract_deduction(orm.Model):
    _name= 'hr.contract.deduction'
    _description = 'Deducciones o pagos periodicas'

    _columns = {        
        'input_id' :fields.many2one ('hr.rule.input','Entrada', required=True, help="Entrada o parametro asociada a la regla salarial"), 
        'type' : fields.selection([('P','Prestamo empresa'),('A','Ahorro'),('S','Seguro'),('L','Libranza'),('E','Embargo'),('R','Retencion'),('O','Otros')],'Tipo deduccion', required=True),
        'period' : fields.selection([('limited','Limitado'),('indefinite','Indefinido')],'Periodo', required=True),
        'amount' : fields.float('Valor', help="Valor de la cuota o porcentaje segun formula de la regla salarial", required=True),
        'total_deduction' : fields.float('Total', help="Total a descontar"),
        'total_accumulated' : fields.float('Acumulado', help="Total pagado o acumulado del concepto"),
        'date' : fields.date('Fecha', select=True, help="Fecha del prestamo u obligacion"),
        'show_voucher' : fields.boolean('Mostrar', help="Indica si se muestra o no en el comprobante de nomina"),
        'contract_id' : fields.many2one('hr.contract', 'Deduciones', required=True, ondelete='cascade', select=True),
    }

    _defaults = {
        'type': "O",
        'period': "indefinite",
        'amount' : 0,
        'total_deduction': 0,
        'total_accumulated' : 0,
        'show_voucher': False,
    }
     
class hr_contract_risk(orm.Model):
    _name= 'hr.contract.risk'
    _description = 'Riesgos profesionales'
    
    _columns = {
        'code' : fields.char ('Codigo', size=10, required = True),
        'name' : fields.char ('Nombre', size=100, required = True),
        'percent': fields.float('Porcentaje', required = True, help="porcentaje del riesgo profesional"),
        'date' : fields.date ('Fecha vigencia'),
    }
    
    _defaults = {
      'percent' : 0.00,          
    }

class hr_payslip_deduction_line(orm.Model):
    '''
    Detail of deduction
    '''
    _name = 'hr.payslip.deduction.line'
    _description = 'Detalle de deducciones'
    _order = 'employee_id, contract_id, deduction_id'

    _columns = {
        'slip_id':fields.many2one('hr.payslip', 'Pay Slip', required=True, ondelete='cascade'),
        'deduction_id':fields.many2one('hr.contract.deduction', 'Deducciones', required=True),
        'employee_id':fields.many2one('hr.employee', 'Employee', required=True),
        'contract_id':fields.many2one('hr.contract', 'Contract', required=True, select=True),
        'amount': fields.float('Valor', digits_compute=dp.get_precision('Payroll')),
        'total_deduction' : fields.float('Total', digits_compute=dp.get_precision('Payroll'), help="Total a descontar"),
        'total_accumulated' : fields.float('Acumulado', digits_compute=dp.get_precision('Payroll'), help="Total pagado o acumulado del concepto", readonly=True),
        'date' : fields.date('Fecha', select=True, digits_compute=dp.get_precision('Payroll'), help="Fecha del prestamo u obligacion"),
        'show_voucher' : fields.boolean('Mostrar', digits_compute=dp.get_precision('Payroll'), help="Indica si se muestra o no en el comprobante de nomina"),
    }
    
    _defaults = {
        'amount': 0,
        'total_deduction' : 0,
        'total_accumulated' : 0,
    }

class hr_contract_acumulados(orm.Model):
    '''
    Detalle acumulados del contrato
    '''
    _name = 'hr.contract.acumulados'
    _description = 'Acumulados del contrato'
    _order = 'period_id, salary_rule_id'

    _columns = {    
        'period_id' : fields.many2one('account.period', required=True, string='Periodo'),        
        'salary_rule_id' : fields.many2one('hr.salary.rule', required=True, string='Regla salarial'),        
        'amount' : fields.float('Valor', required=True),
        'contract_id' : fields.many2one('hr.contract', 'Liquidacion', required=True, ondelete='cascade', select=True),
    }
    
    _defaults = {
        'amount': 0,
    }


class hr_contract_liquidacion(orm.Model):
    '''
    Detalle liquidacion de contrato
    '''
    _name = 'hr.contract.liquidacion'
    _description = 'Detalle liquidacion de contrato'
    _order = 'contract_id, sequence'

    _columns = {
        'sequence': fields.integer('Secuencia', required=True),
        'type' : fields.selection([('P','Pago'),('D','Descuento')],'Tipo', required=True),
        'name' : fields.char ('Concepto', size=100, required = True),
        'dias': fields.float('Días', required = True),
        'amount' : fields.float('Valor', required=True),
        'contract_id' : fields.many2one('hr.contract', 'Liquidacion', required=True, ondelete='cascade', select=True),
    }
    
    _defaults = {
        'amount': 0,
        'dias' : 1.0,
    }

class hr_contract_analytic(orm.Model):
    _name= 'hr.contract.analytic'
    _description = 'Distribucion por cuenta analitica'

    _columns = {
        'percent' : fields.float('Porcentaje', required=True),
        'account_analytic_id': fields.many2one('account.analytic.account','Cuenta analítica',required=True),   
        'contract_id' : fields.many2one('hr.contract', 'Cuenta analitica', required=True, ondelete='cascade', select=True),        
    }
    
    _defaults = {
        'percent': 0.00,
    }    
    
    
class hr_contract (orm.Model):
    _name = "hr.contract"
    _inherit = "hr.contract"
    _columns = {
        'analytic_ids' : fields.one2many('hr.contract.analytic', 'contract_id', 'Cuentas analíticas'),
        'setting_ids' : fields.one2many('hr.contract.setting', 'contract_id', 'Configuración'),
        'deduction_ids' : fields.one2many('hr.contract.deduction', 'contract_id', 'Deducciones'),
        'liquidacion_ids' : fields.one2many('hr.contract.liquidacion', 'contract_id', 'Liquidación'),
        'acumulado_ids' : fields.one2many('hr.contract.acumulados', 'contract_id', 'Acumulados'),
        'risk_id' : fields.many2one('hr.contract.risk', required=True, string='Riesgo profesional'),
        'date_prima' : fields.date ('Fecha de liquidación de prima'),
        'date_cesantias' : fields.date ('Fecha de liquidación de cesantías'),
        'date_vacaciones' : fields.date ('Fecha de liquidación de vacaciones'),
        'dias_vacaciones': fields.float('Días tomados de vacaciones', digits_compute=dp.get_precision('Payroll')),
        'date_intereses' : fields.date ('Fecha de liquidación de intereses a las cesantías'),
        'date_liquidacion' : fields.date ('Fecha de liquidación contrato'),
        'dias_sancion': fields.float('Sansiones en días', digits_compute=dp.get_precision('Payroll')),
        'prestamos': fields.float('Préstamos y anticipos', digits_compute=dp.get_precision('Payroll')),
        'distribuir' : fields.boolean('Distribuir por cuenta analítica', help="Indica si al calcula la nómina del contrato se distribuye por centro de costo"),
        'factor': fields.float('Factor salarial', required=True),
        'parcial': fields.boolean('Tiempo parcial'),
        'pensionado': fields.boolean('Pensionado'),
        'condicion': fields.float('Condición anterior', digits_compute=dp.get_precision('Payroll')),
        'compensacion': fields.float('Compensación', digits_compute=dp.get_precision('Payroll')),


    }
    
    _defaults = {
        'dias_sancion': 0.00,
        'dias_vacaciones' : 0.00,
        'distribuir' : False,
        'parcial' : False,
        'pensionado' : False,
        'factor': 0.00,
        'condicion': 0.00,
        'compensacion': 0.00,
    }
    
    def _check_percent_100(self, cr, uid, ids, context=None):
        for c in self.browse(cr,uid, ids, context=context):
           if c.analytic_ids:
              total = 0.00
              for cc in c.analytic_ids:		
        	total = total + cc.percent
              
              if total <> 100.00:
        	return False
        return True
        		
    _constraints = [
           (_check_percent_100, 'Error!\nLa distribucion de cuentas analiticas debe sumar el 100%.', ['analytic_ids']),
    ]
    
    def calcular_prima(self, cr, uid, ids, date_liquidacion, date_prima,context=None):
        
        #Elimina calculos previos
        liq_obj = self.pool.get('hr.contract.liquidacion')
        unlink_ids = []
        unlink_ids = liq_obj.search(cr, uid, [('contract_id', '=', ids[0]),('sequence','=','1')]) 
        liq_obj.unlink(cr, uid, unlink_ids)

        for cont in self.browse(cr, uid, ids, context=context):
          
          #------------  PRIMA ------------------
          
          #valida fecha de liquidacion de contrato
          if not date_liquidacion:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de contrato"))

          #la fecha de liquidacion debe ser mayor que la de inicio de contrato
          day_start = datetime.strptime(cont.date_start,"%Y-%m-%d")
          day_end = datetime.strptime(date_liquidacion,"%Y-%m-%d")
          if (day_end - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de contrato debe ser mayor a la fecha de inicio del mismo"))
          
          #calcula prima
          if not date_prima:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de prima"))
		   
          #la fecha de liquidacion prima debe ser mayor que la de inicio de contrato
          day_to = datetime.strptime(date_prima,"%Y-%m-%d")
          if (day_to - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de prima debe ser mayor a la fecha de inicio del contrato"))
                    
          dias = (day_end - day_to).days + 1
          aux_transporte = 0.00
          promedio_salario_var = 0.00
          total_prima = round(((cont.wage + aux_transporte + promedio_salario_var) * dias)/360,0)   
          
          args = {
            'type':'P',
            'name':'Prima',
            'dias': dias,
            'amount':total_prima, 
            'contract_id': cont.id,
            'sequence': 1,
          }
          
          liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)          
			
          return total_prima

    def calcular_cesantias(self, cr, uid, ids, date_liquidacion, date_cesantias, context=None):
        
        #Elimina calculos previos
        liq_obj = self.pool.get('hr.contract.liquidacion')
        unlink_ids = []
        unlink_ids = liq_obj.search(cr, uid, [('contract_id', '=', ids[0]),('sequence','=','2')]) 
        liq_obj.unlink(cr, uid, unlink_ids)

        for cont in self.browse(cr, uid, ids, context=context):
          
          #------------  CESANTIAS ------------------
          
          #valida fecha de liquidacion de contrato
          if not date_liquidacion:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de contrato."))

          #la fecha de liquidacion debe ser mayor que la de inicio de contrato
          day_start = datetime.strptime(cont.date_start,"%Y-%m-%d")
          day_end = datetime.strptime(date_liquidacion,"%Y-%m-%d")
          if (day_end - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de contrato debe ser mayor a la fecha de inicio del mismo"))
          
          #calcula cesantias
          if not date_cesantias:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de cesantías."))
		   
          #la fecha de liquidacion cesantias debe ser mayor que la de inicio de contrato
          day_to = datetime.strptime(date_cesantias,"%Y-%m-%d")
          if (day_to - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de cesantías debe ser mayor a la fecha de inicio del contrato"))
             
          dias = (day_end - day_to).days + 1   
          aux_transporte = 0.00
          promedio_salario_var = 0.00
          total_cesantias = round(((cont.wage + aux_transporte + promedio_salario_var) * dias)/360,0)   
          
          args = {
            'type':'P',
            'name':'Cesantías',
            'dias': dias,
            'amount':total_cesantias, 
            'contract_id': cont.id,
            'sequence': 2,
          }          
          
          liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)          
			
          return total_cesantias
    
    def calcular_intereses(self, cr, uid, ids, date_liquidacion, date_cesantias, date_intereses, context=None):
        
        #Elimina calculos previos
        liq_obj = self.pool.get('hr.contract.liquidacion')
        unlink_ids = []
        unlink_ids = liq_obj.search(cr, uid, [('contract_id', '=', ids[0]),('sequence','=','3')]) 
        liq_obj.unlink(cr, uid, unlink_ids)

        for cont in self.browse(cr, uid, ids, context=context):
          
          #------------  INTERESES DE CESANTIAS ------------------
          
          #valida fecha de liquidacion de contrato
          if not date_liquidacion:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de contrato."))

          #la fecha de liquidacion debe ser mayor que la de inicio de contrato
          day_start = datetime.strptime(cont.date_start,"%Y-%m-%d")
          day_end = datetime.strptime(date_liquidacion,"%Y-%m-%d")
          if (day_end - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de contrato debe ser mayor a la fecha de inicio del mismo"))
          
          #calcula intereses
          if not date_intereses:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de intereses de cesantías."))
		   
          #la fecha de liquidacion intereses cesantias debe ser mayor que la de inicio de contrato
          day_to = datetime.strptime(date_intereses,"%Y-%m-%d")
          if (day_to - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de intereses de cesantías debe ser mayor a la fecha de inicio del contrato"))
             
          #Calcula primero el cesantias
          total_cesantias = self.calcular_cesantias(cr, uid, ids, date_liquidacion, date_cesantias, context=context)
             
          dias = (day_end - day_to).days + 1   
          total_intereses = round((total_cesantias * dias * 0.12)/360,0)   
          
          args = {
            'type':'P',
            'name':'Intereses de cesantías',
            'dias': dias,
            'amount':total_intereses, 
            'contract_id': cont.id,
            'sequence': 3,
          }          
          
          liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)          
			
          return total_intereses

    def calcular_vacaciones(self, cr, uid, ids, date_liquidacion, date_vacaciones, context=None):
        
        #Elimina calculos previos
        liq_obj = self.pool.get('hr.contract.liquidacion')
        unlink_ids = []
        unlink_ids = liq_obj.search(cr, uid, [('contract_id', '=', ids[0]),('sequence','=','4')]) 
        liq_obj.unlink(cr, uid, unlink_ids)

        for cont in self.browse(cr, uid, ids, context=context):
          
          #------------  CESANTIAS ------------------
          
          #valida fecha de liquidacion de contrato
          if not date_liquidacion:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de contrato."))

          #la fecha de liquidacion debe ser mayor que la de inicio de contrato
          day_start = datetime.strptime(cont.date_start,"%Y-%m-%d")
          day_end = datetime.strptime(date_liquidacion,"%Y-%m-%d")
          if (day_end - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de contrato debe ser mayor a la fecha de inicio del mismo"))
          
          #calcula vacaciones
          if not date_vacaciones:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de vacaciones."))
		   
          #la fecha de liquidacion vacaciones debe ser mayor que la de inicio de contrato
          day_to = datetime.strptime(date_vacaciones,"%Y-%m-%d")
          if (day_to - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de vacaciones debe ser mayoy a la fecha de inicio del contrato"))
	
	  promedio_salario_var = 0.00
	  dias = ((15*((day_end - day_to).days - cont.dias_sancion)/360)) - cont.dias_vacaciones	  
          total_vacaciones = round(((cont.wage + promedio_salario_var)/30) * dias,0)   
          
          args = {
            'type':'P',
            'name':'Vacaciones',
            'dias': dias,
            'amount':total_vacaciones, 
            'contract_id': cont.id,
            'sequence': 4,
          }          
          
          liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)          
			
          return total_vacaciones

    
    def calcular_liquidacion(self, cr, uid, ids, context=None):
        
        #Elimina calculos previos
        liq_obj = self.pool.get('hr.contract.liquidacion')
        unlink_ids = []
        unlink_ids = liq_obj.search(cr, uid, [('contract_id', '=', ids[0])]) 
        liq_obj.unlink(cr, uid, unlink_ids)

        for cont in self.browse(cr, uid, ids, context=context):
          
          #------------  PAGOS ------------------
          
          #valida fecha de liquidacion de contrato
          if not cont.date_liquidacion:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de contrato."))

          #la fecha de liquidacion debe ser mayor que la de inicio de contrato
          day_start = datetime.strptime(cont.date_start,"%Y-%m-%d")
          day_end = datetime.strptime(cont.date_liquidacion,"%Y-%m-%d")
          if (day_end - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de contrato debe ser mayoy a la fecha de inicio del mismo"))
          
          #------------------------------
          #calcula prima
          if not cont.date_prima:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de prima."))
		   
          #la fecha de liquidacion prima debe ser mayor que la de inicio de contrato
          day_to = datetime.strptime(cont.date_prima,"%Y-%m-%d")
          if (day_to - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de prima debe ser mayoy a la fecha de inicio del contrato"))
                    
          dias = (day_end - day_to).days + 1
          aux_transporte = 0.00
          promedio_salario_var = 0.00
          total_prima = round(((cont.wage + aux_transporte + promedio_salario_var) * dias)/360,0)   
          
          args = {
            'type':'P',
            'name':'Prima',
            'dias': dias,
            'amount':total_prima, 
            'contract_id': cont.id,
            'sequence': 1,
          }
          
          liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)          
	
	  #------------------------------
          #calcula cesantias
          if not cont.date_cesantias:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de cesantías."))
		   
          #la fecha de liquidacion cesantias debe ser mayor que la de inicio de contrato
          day_to = datetime.strptime(cont.date_cesantias,"%Y-%m-%d")
          if (day_to - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de cesantías debe ser mayoy a la fecha de inicio del contrato"))
             
          dias = (day_end - day_to).days + 1   
          total_cesantias = round(((cont.wage + aux_transporte + promedio_salario_var) * dias)/360,0)   
          
          args = {
            'type':'P',
            'name':'Cesantías',
            'dias': dias,
            'amount':total_cesantias, 
            'contract_id': cont.id,
            'sequence': 2,
          }
          
          liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)          

	  #------------------------------	
          #calcula intereses
          if not cont.date_intereses:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de intereses de cesantías."))
		   
          #la fecha de liquidacion intereses cesantias debe ser mayor que la de inicio de contrato
          day_to = datetime.strptime(cont.date_intereses,"%Y-%m-%d")
          if (day_to - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de intereses de cesantías debe ser mayoy a la fecha de inicio del contrato"))
             
          dias = (day_end - day_to).days + 1   
          total_intereses = round((total_cesantias * dias * 0.12)/360,0)   
          
          args = {
            'type':'P',
            'name':'Intereses de cesantías',
            'dias': dias,
            'amount':total_intereses, 
            'contract_id': cont.id,
            'sequence': 3,
          }
          
          liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)          
	
	  #------------------------------
          #calcula vacaciones
          if not cont.date_vacaciones:
             raise osv.except_osv(_('Error!'),_("Debe ingresar fecha de liquidación de vacaciones."))
		   
          #la fecha de liquidacion vacaciones debe ser mayor que la de inicio de contrato
          day_to = datetime.strptime(cont.date_vacaciones,"%Y-%m-%d")
          if (day_to - day_start).days <= 0:
             raise osv.except_osv(_('Error!'),_("La fecha de liquidación de vacaciones debe ser mayoy a la fecha de inicio del contrato"))
	
	  dias = ((15*((day_end - day_to).days - cont.dias_sancion)/360)) - cont.dias_vacaciones	  
          total_vacaciones = round(((cont.wage + promedio_salario_var)/30) * dias,0)   
          
          args = {
            'type':'P',
            'name':'Vacaciones',
            'dias': dias,
            'amount':total_vacaciones, 
            'contract_id': cont.id,
            'sequence': 4,
          }
          
          liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)  
          
          #------------  DEDUCCIONES ------------------
          
          args = {
	    'type':'D',
	    'name':'Préstamos y anticipos',
	    'dias': 0,
	    'amount':cont.prestamos*(-1), 
	    'contract_id': cont.id,
	    'sequence': 5,
	  }
	            
	  liq_id = liq_obj.create(cr, uid, args, context=context)
          liq_obj.write(cr, uid, liq_id, args, context=context)  
		
          return True

class hr_payslip_analytic(orm.Model):
    _name= 'hr.payslip.analytic'
    _description = 'Distribucion regla por cuenta analitica'
    _order = 'salary_rule_id'
    _columns = {
        'salary_rule_id': fields.many2one('hr.salary.rule','Regla salarial',required=True),   
        'account_analytic_id': fields.many2one('account.analytic.account','Cuenta analítica',required=True),   
        'percent' : fields.float('Porcentaje', required=True),
        'slip_id' : fields.many2one('hr.payslip', 'Nómina', required=True, ondelete='cascade', select=True),        
    }
    
    _defaults = {
        'percent': 0.00,
    }        
    
    _sql_constraints = [('rule_analytic_uniq', 'unique(slip_id, salary_rule_id, account_analytic_id)', 'La distribucion para la misma regla y cuenta analitica debe ser unica'),
                       ]   

class hr_payslip (orm.Model):
    _name = "hr.payslip"
    _inherit = "hr.payslip"
    
    _columns = {
        'liquida' : fields.boolean('Liquidación', help="Indica si se ejecuta una estructura para liquidacion de contratos y vacaciones"),
        'deduction_line_ids': fields.one2many('hr.payslip.deduction.line', 'slip_id', 'Detalle deducciones', readonly=True),
        'analytic_ids': fields.one2many('hr.payslip.analytic', 'slip_id', 'Distribucion cuentas analiticas'),
        'date_prima' : fields.date ('Fecha de liquidación de prima'),
	'date_cesantias' : fields.date ('Fecha de liquidación de cesantías'),
	'date_vacaciones' : fields.date ('Fecha de liquidación de vacaciones'),
	'dias_vacaciones': fields.float('Días tomados de vacaciones', digits_compute=dp.get_precision('Payroll')),
	'date_intereses' : fields.date ('Fecha de liquidación de intereses a las cesantías'),
        'date_liquidacion' : fields.date ('Fecha de liquidación contrato'),
    } 
    
    _defaults = {
        'liquida': False,
    }
    
    def _check_percent_100(self, cr, uid, ids, context=None):
        for c in self.browse(cr,uid, ids, context=context):
           if c.analytic_ids:
              
              total = 100.00
              cuenta = 0
              for cc in c.analytic_ids:
		
                if cuenta <> cc.salary_rule_id.id:
                   if total <> 100.00:
        	      return False
                   cuenta = cc.salary_rule_id.id
                   total = 0.00
                
        	total = total + cc.percent
              
              if total <> 100.00:
        	return False
        return True
        		
    _constraints = [
           (_check_percent_100, 'Error!\nLa distribucion de cuentas analiticas debe sumar el 100%.', ['analytic_ids']),
    ]

    def get_inputs(self, cr, uid, contract_ids, date_from, date_to, context=None):
        res = []
        contract_obj = self.pool.get('hr.contract')
        rule_obj = self.pool.get('hr.salary.rule')
        deduction_obj = self.pool.get('hr.contract.deduction')

        structure_ids = contract_obj.get_all_structures(cr, uid, contract_ids, context=context)
        rule_ids = self.pool.get('hr.payroll.structure').get_all_rules(cr, uid, structure_ids, context=context)       
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]
        day_from = datetime.strptime(date_from,"%Y-%m-%d")
        day_to = datetime.strptime(date_to,"%Y-%m-%d")


        for contract in contract_obj.browse(cr, uid, contract_ids, context=context):
            for rule in rule_obj.browse(cr, uid, sorted_rule_ids, context=context):
                if rule.input_ids:
                    for input in rule.input_ids:
                        #Determina si existe un posible(s) valor(es) para la entrada
                        amount = 0
                        deduction_ids = deduction_obj.search(cr, uid, [('contract_id', '=',contract.id),('input_id','=',input.id)], context=context)
                        if len(deduction_ids) > 0:
                            for reg in deduction_obj.browse(cr, uid, deduction_ids, context=context):             
                                #Si es un prestamo valida que no se exceda el valor total
                                if reg.period == 'limited' :
                                    if (reg.total_accumulated + reg.amount) > reg.total_deduction:
                                        amount = reg.total_deduction - reg.total_accumulated
                                    else:
                                        amount = amount + reg.amount
                                else:
                                    amount = amount + reg.amount
                                        
                        inputs = {
                             'name': input.name,
                             'code': input.code,
                             'amount' : amount,
                             'contract_id': contract.id,
                        }
                        res += [inputs]
        return res

class hr_rule_input(orm.Model):
    _inherit = 'hr.rule.input' 
    
    _sql_constraints = [('code_uniq', 'unique(code)', 'El codigo debe ser unico. El codigo ingresado ya existe'),
                       ]

class hr_novedades(orm.Model):
    _name= 'hr.novedades'
    _description = 'Novedades de nómina'
    
    def _input_name(self, cr, uid, ids, args, args2, context=None):
        obj_model = self.pool.get('hr.rule.input')
        res = False
        novedad_record = self.browse(cr, uid, ids[0], context=context)
        data_id = obj_model.search(cr, uid, [('code', '=', novedad_record.code)])
        if data_id:
            res = obj_model.browse(cr, uid, data_id[0], context=context).name
        return res

    def _partner_name(self, cr, uid, ids, args, args2, context=None):
        obj_model = self.pool.get('hr.employee')
        res = False
        novedad_record = self.browse(cr, uid, ids[0], context=context)
        data_id = obj_model.search(cr, uid, [('identification_id', '=', novedad_record.identification_id)])
        if data_id:
            res = obj_model.browse(cr, uid, data_id[0], context=context).name_related
        return res

    
    _columns = {
        #'input_id' : fields.many2one ('hr.rule.input','Novedad', required=False, help="Código o nombre de la novedad"),
        'code': fields.char ('Codigo', required = True),
        'date_from' : fields.date ('Fecha desde', required = True),
        'date_to' : fields.date ('Fecha hasta', required = True),
        #'employee_id' : fields.many2one ('hr.employee','Empleado', required=False, domain=[('active','=','true')],help="Cédula o nombre completo del empleado"),
        'identification_id' : fields.char ('Cédula',required = True),
        'value': fields.float('Valor', required = True),
        'account_analytic_id': fields.many2one('account.analytic.account','Cuenta analítica'),   
    }
    
    _sql_constraints = [('novedad_uniq', 'unique(code, date_from, date_to, identification_id, account_analytic_id)', 'La novedad debe ser única para el período y cédula'),
                       ]   
    _defaults = {
      'value' : 0.00,                
    }
    
    def _check_code_novedad(self, cr, uid, ids, context=None):
        print 'ids ',ids
        for cod in self.browse(cr,uid, ids, context=context):
          if cod.code:
             cr.execute("""  SELECT * FROM hr_rule_input as p
	                                 WHERE p.code = '%s'
	                         """ % (cod.code))	     
	     cant = len(cr.fetchall())                    
             if cant > 0:
               return True      
             else:
               return False
          else:
             return False
        return True

    def _check_cedula_novedad(self, cr, uid, ids, context=None):
        print 'ids ',ids
        for cod in self.browse(cr,uid, ids, context=context):
          if cod.identification_id:
             cr.execute("""  SELECT * FROM hr_employee as p
                             INNER JOIN resource_resource as r ON (r.id = p.resource_id)
	                                 WHERE r.active = True AND p.identification_id = '%s'
	                         """ % (cod.identification_id))	     
	     cant = len(cr.fetchall())                    
             if cant > 0:
               return True      
             else:
               return False
          else:
             return False
        return True

            		
    _constraints = [
       (_check_code_novedad, 'Error!\nDebe ingresar el codigo de la novedad o el ingresado no existe', ['code']),
       (_check_cedula_novedad, 'Error!\nDebe ingresar la cedula o el empleado no esta activo', ['identification_id']),
    ]
   
