{
    'name': "HR Experience",
    'summary': """Hiring Model""",
    'description': """
        Hiring the certificated in the right place
    """,
    'author': "Danyah",
    'version': '0.1',
    'depends': ['base', 'hr','hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'wizard/add_experince_view.xml',
        'views/hr_experience_views.xml',
        'views/hr_experience_main.xml',

    ],

}
