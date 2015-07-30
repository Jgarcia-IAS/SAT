# -*- coding: utf-8 -*-
# from openerp.osv import osv, fields

import openerp
from openerp.osv import osv, fields
from openerp import addons
import logging
from openerp.tools.translate import _
from openerp import tools


class svhr_hr_employee(osv.Model):
    _inherit = "hr.employee"

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    def _get_default_image(self, cr, uid, context=None):
        image_path = addons.get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))



    _columns = {
        # page informacion personal
        'sv_dep_nac': fields.many2one('res.country.state', 'Departamento Nacimiento'),
        'sv_ciu_nac': fields.char('Ciudad Nacimiento', size=38),
        'sv_tel_per': fields.char('Teléfono Personal', size=30),
        'sv_num_cel': fields.char('Número de Celular', size=30),
        'sv_cor_elec': fields.char('Correo Electrónico', size=30),
        'sv_profesion': fields.char('Profesión, ocupación u oficio', size=40),
        'sv_ano_exp': fields.date('Experiencia Laboral', size=30),
        'sv_tipo_doc': fields.selection([('cedula', 'Cédula de Ciudadanía'), ('ced_ext', 'Cédula de Extranjería')], "Tipo de Documento"),
        'sv_doc_expedida': fields.char('Expedido en', size=30),
        'sv_hr_banco': fields.selection([('DAVIVIENDA', 'DAVIVIENDA'), ('BANCOLOMBIA', 'BANCOLOMBIA'), ('OTRO', 'OTRO')], "Banco"),
        # Page Configuracion RRHH
        'sv_funcionalidad': fields.selection([('admin', 'Administrativo'), ('opera', 'Operativo')], "Funcionalidad"),
        # Page Documentacion
            # Libreta militar
        'sv_lib': fields.boolean('Libreta Militar', required=False),
        'sv_tipo_lib': fields.selection([('pri_cla', 'Primera Clase'), ('seg_cla', 'Segunda Clase')], "Tipo de Libreta Militar"),
        'sv_num_lib': fields.char('Número de Libreta Militar', size=30),
        'sv_num_dis': fields.char('Número de Distrito', size=38),
            # Licencia de conduccion
        'sv_num_lic': fields.char('Número de Licencia', size=30),
        'sv_tipo_cat': fields.selection([('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('C1', 'C2'), ('C2', 'C2'), ('C3', 'C3')], "Tipo de Licencia Conducción"),
        'sv_veh': fields.boolean('Tiene Vehiculo', required=False),
            # Referencias
        'sv_ref_ids': fields.many2many('svhr.recomendaciones', 'svhr_hr_employee'),
            # Experiencia
        'sv_exp_id': fields.one2many('svhr.experiencia', 'sv_exp_ids', 'Experiencia'),
        # Page Informacion Privada
            # Vivienda
        'sv_casa_propia': fields.boolean('Vive en casa propia', required=False),
        'sv_nom_arr': fields.char('Nombre del arrendador', size=30),
        'sv_val_men': fields.char('Costo del alquiler', size=30),
        'sv_tel_arr': fields.char('Telefono del arrendador', size=30),
        'sv_tie_viv': fields.char('Tiempo de anteguedad', size=30),
        'sv_cas_fam': fields.selection([('no', 'No'), ('si', 'Si')], "Es casa familiar"),
            # Lugares de recidencia
        'sv_otra_ciu': fields.selection([('no', 'No'), ('si', 'Si')], "A vivido en otra ciudad"),
        'sv_ciudad': fields.char('Ciudad', size=30),
        'sv_viv_otra': fields.selection([('no', 'No'), ('si', 'Si')], "Aceptaria vivir en otra ciudad"),
            # Informacion familiar
        'sv_conyugue': fields.boolean('Tiene cónyuge', required=False),
        'sv_nom_cony': fields.char('Nombre', size=40),
        'sv_tbr_cony': fields.boolean('Trabaja Actualmente', required=False),
        'sv_nom_emp': fields.char('¿En qué empresa?', size=40),
        'sv_cat_emp': fields.selection([('empleado', 'Empleado'), ('independiente', 'Independiente')], "Trabaja como"),
        'sv_tip_contr': fields.selection([('indefinido', 'Indefinido'), ('fijo', 'Fijo')], "Tipo de Contrato"),
                # Personas bajo su responsabilidad
        'sv_per_dependan': fields.boolean('Tiene personas bajo su responsabilidad', required=False),
        'sv_num_depe': fields.char('¿Cuanto?', size=20),
        'sv_nom_depe': fields.text('Nombre'),
                # Hijos
        'sv_hijos': fields.boolean('Tiene hijos', required=False),
        'sv_val_hij': fields.char('¿Cuanto?', size=40),
        'sv_nom_hij': fields.text('Sus nombres por favor'),
        # Page Informacion Academica
                # Primaria
        'sv_nivel_primaria': fields.boolean('Primaria', required=False),
        'sv_niv_pri': fields.char('Año', required=False),
        'sv_inst_pri': fields.char('Institucion ?', required=False),
               # Secundaria
        'sv_nivel_secundaria': fields.boolean('Secundaria', required=False),
        'sv_niv_sec': fields.char('Año', required=False),
        'sv_inst_sec': fields.char('Institucion ?', required=False),
               # Tecnico
        'sv_nivel_tecnico': fields.boolean('Tecnico', required=False),
        'sv_niv_tec': fields.char('Semestre?', required=False),
        'sv_inst_tec': fields.char('Institucion ?', required=False),
        'sv_nom_tec': fields.char('Nombre del tecnico', required=False),
               # Tecnologo
        'sv_nivel_tecnologo': fields.boolean('Tecnologo', required=False),
        'sv_niv_tgia': fields.char('Semestre?', required=False),
        'sv_inst_tgia': fields.char('Institucion ?', required=False),
        'sv_nom_tgia': fields.char('Nombre del tecnologo', required=False),
               # Profesional
        'sv_nivel_profesional': fields.boolean('Profesional', required=False),
        'sv_niv_prof': fields.char('Semestre?', required=False),
        'sv_inst_prof': fields.char('Universidad', required=False),
        'sv_nom_prof': fields.char('Nombre de la carrera', required=False),
               # Posgrados
        'sv_nivel_posgrado': fields.boolean('Posgrado', required=False),
        'sv_niv_posg': fields.char('Semestre?', required=False),
        'sv_inst_posg': fields.char('Universidad', required=False),
        'sv_nom_posg': fields.char('Nombre del Posgrado', required=False),
               # Cursos
        'sv_nivel_curso': fields.boolean('Curso', required=False),
        'sv_niv_curs': fields.char('Año o semestre?', required=False),
        'sv_inst_curs': fields.char('Institucion', required=False),
        'sv_nom_curs': fields.char('Nombre del Curso', required=False),
        # Page Informacion Dactilar
        'sv_inf_dact': fields.binary(""),
        'sv_fec_dact': fields.date(''),
        'sv_inf_foto1': fields.binary(""),
        'sv_fec_foto1': fields.date(''),
        'sv_inf_foto2': fields.binary(""),
        'sv_fec_foto2': fields.date(''),
        'sv_pas_judi1': fields.binary(""),
        'sv_fec_judi1': fields.date(''),
        'sv_pas_judi2': fields.binary(""),
        'sv_fec_judi2': fields.date(''),
}


class svhr_recomendaciones(osv.Model):
    _name = "svhr.recomendaciones"
    _columns = {
        'sv_tipo': fields.selection([('laboral', 'Laboral'), ('personal', 'Personal')], "Tipo de referencia"),
        'sv_name': fields.char('Nombre', size=40),
        'sv_tele': fields.char('Telefono', size=20),
        'sv_celu': fields.char('Celular', size=20),
        'sv_dire': fields.char('Direccion', size=40),
        'sv_rela': fields.char('Relacion', size=40),
        'sv_acti': fields.char('Actividad', size=40),
        'sv_pare': fields.char('Parentesco', size=40),
        'sv_emp': fields.char('Nombre de la empresa', size=40),
        }


class svhr_experiencia(osv.Model):
    _name = "svhr.experiencia"
    _columns = {
        'sv_empresa': fields.char('Nombre de la empresa', size=40),
        'sv_nit': fields.char('Nit de la empresa', size=40),
        'sv_jefe': fields.char('Nombre del jefe inmediato', size=40),
        'sv_num_emp': fields.char('Numero de la empresa', size=40),
        'sv_num_jefe': fields.char('Numero del Jefe inmediato', size=40),
        'sv_dire': fields.char('Direccion de la empresa', size=40),
        'sv_fecha_ini': fields.date('Fecha ingreso'),
        'sv_fecha_ret': fields.date('Fecha retiro'),
        'sv_mot_ret': fields.char('Motivo retiro', size=80),
        'sv_exp_ids': fields.many2one('hr.employee', 'Experiencia'),
        }
