{
    'name': 'Talento Humano Servagro',
    'version': '1.1.3',
    'description': """
       Modulo de extension de Recursos Humanos para Servagro Ltda.
    """,
    'author': 'Servagro',
    'website': 'http://www.servagroltda.com',
    'depends': ['base_setup', 'hr'],
     'data': [
              'security/svhr_security.xml',
              'security/ir.model.access.csv',
              'svhr_view.xml',
              'svhr_rec_view.xml',
              'svhr_exp_view.xml',
              ],
     'demo': [],
    'installable': True,
    'auto_install': False,
}
