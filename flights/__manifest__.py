# -*- coding: utf-8 -*-
{
    'name': "flights",

    'summary': """
        Base module to manage flights and related data""",

    'description': """
        Base module to manage flights and related data
    """,

    'author': "Apexive Studio LLC, Ivan Elizaryev",
    'website': "https://apexive.com",
    'license': "Other OSI approved licence",  # MIT

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Industries',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'contacts',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/flight_wizard_views.xml',
        'wizard/flight_export_wizard_views.xml',
        'views/views.xml',
        'views/flight_aerodrome_views.xml',
        'views/templates.xml',
        'data/flight_flight_param_type_data.xml',
        'data/flight_crew_role_data.xml',
        'data/flight_event_kind_data.xml',
        'data/flight_aircraft_class_data.xml',
        'data/flight_aircraft_model_tag_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
