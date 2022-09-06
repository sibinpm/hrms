import datetime
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_round
from odoo.exceptions import UserError, ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    current_leave_id = fields.Many2one('hr.leave.type', compute='_compute_current_leave',
                                       string="Current Time Off Type",
                                       groups="hr.group_hr_user,user_access.group_self_service_employee")

    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.",
                          groups="hr.group_hr_user,user_access.group_self_service_employee",
                          copy=False)

    first_contract_date = fields.Date(compute='_compute_first_contract_date',
                                      groups="hr.group_hr_user,user_access.group_self_service_employee",
                                      store=True)
    address_home_id = fields.Many2one(
        'res.partner', 'Address',
        help='Enter here the private address of the employee, not the one linked to your company.',
        groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    birthday = fields.Date('Date of Birth',
                           groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)
    identification_id = fields.Char(string='Identification No',
                                    groups="hr.group_hr_user,user_access.group_self_service_employee",tracking=True)
    bank_account_id = fields.Many2one(
        'res.partner.bank', 'Bank Account Number',
        domain="[('partner_id', '=', address_home_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        groups="hr.group_hr_user,user_access.group_self_service_employee",
        tracking=True,
        help='Employee bank salary account')



class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HrPayslip, self).create(vals_list)
        if self.env.user.user_has_groups('user_security_groups.group_user_director'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_managers'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_employee'):
            raise UserError(_('You do not have access rights to run this option!'))
        return res

    def write(self, vals):
        res = super(HrPayslip, self).write(vals)
        if self.env.user.user_has_groups('user_security_groups.group_user_director'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_managers'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_employee'):
            raise UserError(_('You do not have access rights to run this option!'))
        return res

    def unlink(self):
        res = super(HrPayslip, self).unlink()
        if self.env.user.user_has_groups('user_security_groups.group_user_director'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_managers'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_employee'):
            raise UserError(_('You do not have access rights to run this option!'))
        return res
