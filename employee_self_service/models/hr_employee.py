from odoo import models, fields, _, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    tds_count = fields.Integer("TDS", compute="compute_tds_count")

    def compute_tds_count(self):
        for rec in self:
            if rec.id:
                rec.tds_count = self.env['employee.tds'].search_count([('employee_id', '=', rec.id)])
            else:
                rec.tds_count = 0

    def action_tds_self_service(self):
        return {
            'name': _('TDS Details'),
            'type': 'ir.actions.act_window',
            'res_model': 'employee.tds',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }

    def action_tax_self_service(self):
        return {
            'name': _('Tax Details'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee.tax',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }

    def action_time_off_dashboard_self_service(self):
        return {
            'name': _('Time Off Dashboard'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }
