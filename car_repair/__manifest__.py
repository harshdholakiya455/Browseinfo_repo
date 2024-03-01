{
    'name': 'Car Repair',
    'version': '17.0',
    'description': '''custom module ''',

    'depends': ['base','mail','sale','purchase'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/car_detail_view.xml',
        'views/car_view.xml',
        'views/product_inherit.xml',
        'data/mail_send.xml',
        'data/scheduled_mail.xml',
        'data/scheduled_actions.xml',
        'report/car_report_filter.xml',
        'report/car_repair_reports.xml',
        'wizard/send_mail_view.xml',
        'wizard/car_report_wizard.xml',
        


    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
