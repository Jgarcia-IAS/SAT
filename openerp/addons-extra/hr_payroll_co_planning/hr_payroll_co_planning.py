# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2013 Interconsulting S.A. e Innovatecsa SAS.  (http://interconsulting.com.co).
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
from openerp.osv import fields, osv

from openerp.tools.translate import _
from datetime import datetime
import openerp.addons.decimal_precision as dp
from dateutil import relativedelta
import warning 
class planning(osv.osv):

    _name= 'planning.planning'
    _description = 'Planeacion de puestos de trabajo'

    _columns = {
        'name' : fields.char ('Nombre', size=100, required = True),
        'date_start': fields.date('Fecha de inicio',select=True),
        'date_end': fields.date('Fecha final',select=True),
        'state': fields.selection([('draft','Borrador'),('posted','Confirmado') ,('closed','Cerrado')], 'Status', required=True, readonly=True, track_visibility='onchange', help='La planeacion tiene 3 estados Borrador, Enviado y Trasmitida'),
        'planning_planning_line_ids': fields.one2many('planning.planning.line', 'planning_id', 'Planeacion de Puestos de trabajo'),
        'planning_planning_line_update_ids': fields.one2many('planning.planning.line.update', 'planning_id', 'Planeacion de Puestos de trabajo'),
        'department_id' : fields.many2one ('hr.department','Departamento', help="Departamento de la empresa o sucursal" , required = True),

    }
    _defaults = {
        'state': 'draft',
        'date_start': lambda *a: time.strftime('%Y-%m-01'),
        'date_end': lambda *a: str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],

    }


    def close_planning(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'closed'}, context=context)

    def open_planning(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'posted'}, context=context)


    def planning_run(self, cr, uid, ids, context=None):
        cr.execute("""select * from fnc_generar_planeacion(%s)""", ids)
#        return self.pool.get('warning').info(cr, uid, title='Export imformation', message=' products Created,  products Updated')

        return [i[0] for i in cr.fetchall()]

    def planning_confirm(self, cr, uid, ids, context=None):
        cr.execute("""select * from fnc_confirmar_planeacion(%s)""", ids)
        self.write(cr, uid, ids, {'state': 'posted'}, context=context)
        return [i[0] for i in cr.fetchall()]

    def planning_enviar(self, cr, uid, ids, context=None):
        cr.execute("""select * from fnc_enviar_planeacion(%s)""", ids)
        return [i[0] for i in cr.fetchall()]


class workstation(osv.osv):
    _name= 'workstation.workstation'
    _description = 'Puestos de trabajo'

    _columns = {        
        'code' : fields.char ('Codigo', size=10, required = True),
        'name' : fields.char ('Nombre', size=100, required = True),
        'partner_id' : fields.many2one ('res.partner','Empresa', help="Empresa relacionada" , required = True),
        'department_id' : fields.many2one ('hr.department','Departamento', help="Departamento de la empresa o sucursal" , required = True),
        'employee_ids':fields.many2many('hr.employee', 'employee_user_rel', 'user_id', 'employee_id', 'Empleados'),
        'empleado_turnos_ids': fields.one2many('empleado_turnos.empleado_turnos', 'empleado_turnos_id', 'Working Time'),
        'date_start': fields.date('Fecha de inicio',select=True),
        'date_end': fields.date('Fecha final',select=True),
        'active': fields.boolean('Active', help="Si el campo no está activo, No se tomara en cuenta para la planeación de la nomina"),
        'tipo_de_turno_id' : fields.many2one ('tipo_de_turno.tipo_de_turno','Tipo de turno', help="Tipo de trno"),
        'turnos_sugeridos_ids': fields.one2many('turnos_sugeridos.turnos_sugeridos', 'turnos_sugeridos_id', 'Turnos sugeridos'),

    }

    _defaults = {
        'active': True,
    }



class turnos(osv.osv):
    _name= 'turnos.turnos'
    _description = 'turnos'

    _columns = {        
        'code' : fields.char ('Codigo', size=10, required = True),
        'name' : fields.char ('Nombre', size=100, required = True),
        'turnos_id':fields.many2one('workstation.workstation', 'Puestos de trabajo',  ondelete ='cascade', select = True),
        'start_time': fields.float('Start Time'),
        'end_time': fields.float('End Time'),
    }



class tipo_de_turno(osv.osv):
    _name= 'tipo_de_turno.tipo_de_turno'
    _description = 'tipo_de_turno'

    _columns = {
        'code' : fields.char ('Codigo', size=10, required = True),
        'name' : fields.char ('Nombre', size=100, required = True),
    }




class empleado_turnos(osv.osv):
    _name= 'empleado_turnos.empleado_turnos'
    _description = 'empleado_turnos'

    _columns = {
        'empleado_turnos_id': fields.many2one('workstation.workstation', 'Puestos de trabajo',  ondelete ='cascade', select = True),
        'employee_id' : fields.many2one ('hr.employee','Empleado', help="Empleado"),
        'turno_id' : fields.many2one ('turnos.turnos','Turno', help="Turno"),

    }


  
class turnos_sugeridos(osv.osv):
    _name= 'turnos_sugeridos.turnos_sugeridos'
    _description = 'turnos_sugeridos'

    _columns = {
        'turnos_sugeridos_id': fields.many2one('workstation.workstation', 'Puestos de trabajo',  ondelete ='cascade', select = True , required=True),
        'turno_id' : fields.many2one ('turnos.turnos','Turno', help="Turno" ,required=True),
        'dias_id' : fields.many2one ('dias.dias','Dia', help="Dia" , required=True),
        'start_time': fields.float('Start Time' , required=True),
        'end_time': fields.float('End Time', required=True),
    }



class planning_planning_line(osv.osv):
    _name= 'planning.planning.line'
    _description = 'planning_planning_line'

    _columns = {
        'planning_id': fields.many2one('planning.planning', 'Planeacion de puestos de trabajo',  ondelete ='cascade', select = True),
        'partner_id' : fields.many2one ('res.partner','Empresa', help="Empresa relacionada"),
        'department_id' : fields.many2one ('hr.department','Departamento', help="Departamento de la empresa o sucursal" , required = True),
        'workstation_id': fields.many2one('workstation.workstation', 'Puestos de trabajo',  ondelete ='cascade', select = True),
        'turno_id' : fields.many2one ('turnos.turnos','Turno', help="Turno"),
        'employee_id' : fields.many2one ('hr.employee','Empleado', help="Empleado"),
        'date_start': fields.datetime('Fecha de inicio',select=True),
        'date_end': fields.datetime('Fecha final',select=True),
        'state': fields.selection([('draft','Unposted'),('posted','Posted') ,('cancel','Cancel'),('executed','Executed')], 'Status', required=True, readonly=True, help='La planeacion tiene 3 estados Borrador, Enviado y Trasmitida'),
        'hours_total': fields.float('Total'),
        'hours_d': fields.float('HD'),
        'hours_n': fields.float('HN'),
        'hours_f_d': fields.float('HFD'),
        'hours_f_n': fields.float('HFN'),
    }

    _defaults = {
        'state': 'draft',
    }

class planning_planning_line_update(osv.osv):
    _name= 'planning.planning.line.update'
    _description = 'planning_planning_line_update'

    _columns = {
        'planning_id': fields.many2one('planning.planning', 'Planeacion de puestos de trabajo',  ondelete ='cascade', select = True),
        'partner_id' : fields.many2one ('res.partner','Empresa', help="Empresa relacionada"),
        'department_id' : fields.many2one ('hr.department','Departamento', help="Departamento de la empresa o sucursal" , required = True),
        'workstation_id': fields.many2one('workstation.workstation', 'Puestos de trabajo',  ondelete ='cascade', select = True),
        'turno_id' : fields.many2one ('turnos.turnos','Turno', help="Turno"),
        'employee_id' : fields.many2one ('hr.employee','Empleado', help="Empleado"),
        'date_start': fields.datetime('Fecha de inicio',select=True),
        'date_end': fields.datetime('Fecha final',select=True),
        'state': fields.selection([('added','Adicionado'),('modify','Modificado') ,('cancel','Anulado'),('even','Sin cambio')], 'Status', required=True, readonly=True, help='La planeacion tiene 3 estados Borrador, Enviado y Trasmitida'),
        'hours_total': fields.float('Total'),
        'hours_d': fields.float('HD'),
        'hours_n': fields.float('HN'),
        'hours_f_d': fields.float('HFD'),
        'hours_f_n': fields.float('HFN'),
    }

    _defaults = {
        'state': 'added',
    }

class dias(osv.osv):
    _name= 'dias.dias'
    _description = 'dias'

    _columns = {
        'code' : fields.char ('Codigo', size=10, required = True),
        'name' : fields.char ('Nombre', size=100, required = True),

    }


 
