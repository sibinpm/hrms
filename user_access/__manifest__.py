{
    'name': 'User Access Groups',
    'summary': """New access groups are added in this module""",
    'version': '15.0.0.1 10-june',
    'description': """New access groups are added in this module""",
    'author': 'PMCS',
    "license": "AGPL-3",
    'sequence': 10,
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'Tools',
    'depends': ['base', 'hr'],
    'data': [
        'security/user_access.xml',
        # 'security/ir.model.access.csv',
        'data/access.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
