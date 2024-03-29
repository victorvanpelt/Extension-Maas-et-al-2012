from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']



mturk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'A Study about Corporate Taxation',
    'description': 'During this study you will be asked to assess corporate tax strategies',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 20,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # Masters
        {
            'QualificationTypeId': "2F1QJWKUDD8XADTFD2Q0G6UTO95ALH",
            'Comparator': "Exists",
        },
        # Only US
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
        # At least 500 HITs approved
        {
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [500]
        },
        # At least 95% of HITs approved
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [95]
        },
        ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.50,
    'participation_fee': 0.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'maas_replication',
        'display_name': "Maas Replication",
        'num_demo_participants': 3,
        'app_sequence': ['biasjesse', 'payment_info'],
        'extension': 0
    },
    {
        'name': 'maas_extension',
        'display_name': "Maas Extension",
        'num_demo_participants': 3,
        'app_sequence': ['biasjesse', 'payment_info'],
        'extension': 1
    },
    {
        'name': 'epq',
        'display_name': "Ex-post Questionnaire",
        'num_demo_participants': 1,
        'app_sequence': ['epq'],
    },
    {
        'name': 'bret',
        'display_name': "Bomb Risk Elicitation Task",
        'num_demo_participants': 1,
        'app_sequence': ['bret', 'payment_info'],
    },
    {
        'name': 'maas_replication_all',
        'display_name': "Maas Replication, Bret, EPQ",
        'num_demo_participants': 3,
        'app_sequence': ['biasjesse', 'bret', 'epq', 'payment_info'],
        'extension': 0
    },
    {
        'name': 'maas_extension_all',
        'display_name': "Maas Extension, Bret, EPQ",
        'num_demo_participants': 3,
        'app_sequence': ['biasjesse', 'bret', 'epq', 'payment_info'],
        'extension': 1
    },
]

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
POINTS_DECIMAL_PLACES = 2
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2

ROOMS = [
    dict(
        name= 'CenterLab',
        display_name= 'Room for CenterLab',
        participant_label_file= 'centerlablabels.txt',
        use_secure_urls= True,
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
"""

SECRET_KEY = '91959382821233'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']