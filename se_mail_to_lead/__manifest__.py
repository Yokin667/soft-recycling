# See LICENSE file for full copyright and licensing details.

{
    'name': 'Generate Lead/Opportunity from email body',
    'summary': "Create lead automatically with custom configurable fields labels on setting.",
    'version': '12.0.0.1.0',
    'category': 'CRM',
    'author': 'Jupical Technologies Pvt Ltd.',
    'maintainer': 'Jupical Technologies Pvt. Ltd.',
    'contributors':['Anil Kesariya <anil.r.kesariya@gmail.com>'],
    'website': 'http://www.jupical.com',
    'live_test_url': 'http://jupical.com/contactus',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
