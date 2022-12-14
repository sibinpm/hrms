{
    'name': 'Employee Self Services',
    'summary': """This module allows a employee to access his/her own records in employee and income tax related records""",
    'version': '15.0.0.2 10-june',
    'description': """This module allows a employee to access his/her own records in employee and income tax related records""",
    'author': 'PMCS',
    "license": "AGPL-3",
    'sequence': 10,
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'Accounting, Tools',
    'depends': ['base', 'hr', 'Itax_calculation_master', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/employee_tax.xml',
        'views/hr_payslip.xml',
        'views/hr_employee.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
