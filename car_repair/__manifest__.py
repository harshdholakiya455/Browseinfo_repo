{
    'name': 'Car Repair',
    'version': '17.0',
    'description': '''custom module ''',

    'depends': ['base','mail','sale', 'product'],
    'data': [
        'security/security_group.xml',
        'security/security_access.xml',
        'security/ir.model.access.csv',
        'views/car_detail_view.xml',
        'views/car_view.xml',
        'views/product_inherit.xml',
        'views/res_config_settings_views.xml',
        'data/scheduled_actions.xml',
        'report/car_report_filter.xml',
        'report/car_repair_reports.xml',
        'report/report_layout.xml',
        'wizard/send_mail_view.xml',
        'wizard/car_report_wizard.xml',
        'data/mail_send.xml',
        'data/scheduled_mail.xml',
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
