import base64
import io
from odoo import models,fields
from datetime import date, datetime ,timedelta


class PayrollSummaryXlsx(models.AbstractModel):
    _name = 'report.payroll_summary.payroll_summary_report_xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, payslips):
        domain = []
        start_date = data.get('start_date')
        format_str = '%Y-%m-%d'
        datetime_obj = datetime.strptime(start_date, format_str).strftime('%Y-%B-%d')
        year = datetime_obj.split("-")[0]
        month = datetime_obj.split("-")[1]
        end_date =  data.get('end_date')
        end_datetime_obj = datetime.strptime(end_date, format_str).strftime('%Y-%B-%d')
        end_year = end_datetime_obj.split("-")[0]
        end_month = end_datetime_obj.split("-")[1]
        emp_id =  data.get('employee_name')
        structure_id = data.get('structure_id')
        domain += [('date_from','>=',start_date)]
        domain += [('date_to','<=',end_date)]
        sheet = workbook.add_worksheet('Payslips')
        bold = workbook.add_format({'bold': True})
        row = 0
        col = 1
        sheet.write(row, col, self.env.company.name, bold)
        row = 4
        col = 0
        dept = self.env['hr.department']
        dept_title =['S.No','Components']
        all_dept_total = ['Total']
        if data.get('report_type') == 'bank transfer':
            row_h = 1
            col_h = 1
            sheet.write(row_h + 1, col_h, 'Bank Transfer statement for the month ' + month + '-' + year,bold)
            title = [ 'S.No','Name',
                      'Employee Number',
                      'Bank Account Number',
                      'Net Pay',
                     ]
            for i in range(len(title)):
                sheet.set_column('T:T', 13)
                sheet.write(row, col + i , title[i] , bold)
            payslips = self.env['hr.payslip'].search(domain)
            total_net = 0
            s_no = 0
            for payslip in payslips:
                row += 1
                col = 0
                s_no = s_no + 1
                sheet.write(row, col,s_no)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.name)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.identification_id if payslip.employee_id.identification_id else ' ')
                col = col + 1
                sheet.write(row, col, payslip.employee_id.bank_account_id.acc_number if payslip.employee_id.bank_account_id.acc_number else ' ')
                col = col + 1
                rec = {}
                for line in payslip.line_ids :
                    if line.code == 'NET':
                        rec.update({"NET": round(line.total)})
                        total_net += round(line.total)
                num = len(title)
                for i in range(num):
                    col = 4
                    sheet.write(row, col, rec.get('NET'))
                    col = col + 1
            row += 1
            col = 1
            sheet.write(row, col, 'Grand Total', bold)
            num = len(title)
            for i in range(num):
                col = 4
                sheet.write(row, col, total_net, bold)
                col = col + 1
        elif data.get('report_type') == 'earnings deductions':
            row_h = 1
            col_h = 1
            sheet.write(row_h + 1, col_h, 'Earning & Deductions - for the month of ' + month + '-' + year,bold)
            title = [ 'S.No','Name',
                      'Employee Number',
                      data.get('earnings_deductions'),
                     ]
            for i in range(len(title)):
                sheet.set_column('T:T', 13)
                sheet.write(row, col + i , title[i] , bold)
            payslips = self.env['hr.payslip'].search(domain)
            total_gross = total_td =  0
            s_no = 0
            for payslip in payslips:
                row += 1
                col = 0
                s_no = s_no + 1
                sheet.write(row, col,s_no)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.name)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.identification_id if payslip.employee_id.identification_id else ' ')
                col = col + 1
                rec = {}
                for line in payslip.line_ids :
                    if line.code == data.get('earnings_deductions'):
                        rec.update({"EARNINGS_DEDUCTIONS": round(line.total)})
                        total_gross += round(line.total)
                num = len(title)
                for i in range(num):
                    col = 3
                    sheet.write(row, col, rec.get('EARNINGS_DEDUCTIONS'))
                    col = col + 1
            row += 1
            col = 1
            sheet.write(row, col, 'Grand Total', bold)
            num = len(title)
            for i in range(num):
                col = 3
                sheet.write(row, col, total_gross, bold)
                col = col + 1
        elif data.get('report_type') == 'pf summary':
            row_h = 1
            col_h = 1
            sheet.write(row_h + 1, col_h, 'PF Summary report for the month of ' + month + '-' + year,bold)
            title = [ 'S.No','Name',
                      'Employee Number',
                      'Basic Salary',
                      'PF Salary',
                      'PF Employee',
                      'PF Employer',
                     ]
            for i in range(len(title)):
                sheet.set_column('T:T', 13)
                sheet.write(row, col + i , title[i] , bold)
            payslips = self.env['hr.payslip'].search(domain)
            total_basic = total_pf_salary = total_epf = total_pf =  0
            s_no = 0
            pf_salary = 15000
            for payslip in payslips:
                row += 1
                col = 0
                s_no = s_no + 1
                sheet.write(row, col,s_no)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.name)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.identification_id if payslip.employee_id.identification_id else ' ')
                col = col + 1
                rec = {}
                for line in payslip.line_ids :
                    if line.code == 'BASIC':
                        rec.update({"BASIC": round(line.total)})
                        total_basic += round(line.total)
                    if line.code == 'BASIC':
                        rec.update({"PF_SALARY": pf_salary if round(line.total) > pf_salary else round(line.total) })
                        total_pf_salary += pf_salary if round(line.total) > pf_salary else round(line.total)
                    if line.code == 'EPF':
                        rec.update({"EPF": round(line.total)})
                        total_epf += round(line.total)
                    if line.code == 'PF':
                        rec.update({"PF": round(line.total)})
                        total_pf += round(line.total)
                num = len(title)
                for i in range(num):
                    col = 3
                    sheet.write(row, col, rec.get('BASIC'))
                    col = col + 1
                    sheet.write(row, col, rec.get('PF_SALARY'))
                    col = col + 1
                    sheet.write(row, col, rec.get('EPF'))
                    col = col + 1
                    sheet.write(row, col, rec.get('PF'))
                    col = col + 1
            row += 1
            col = 1
            sheet.write(row, col, 'Grand Total', bold)
            num = len(title)
            for i in range(num):
                col = 3
                sheet.write(row, col, total_basic, bold)
                col = col + 1
                sheet.write(row, col, total_pf_salary, bold)
                col = col + 1
                sheet.write(row, col, total_epf, bold)
                col = col + 1
                sheet.write(row, col, total_pf, bold)
                col = col + 1
        elif data.get('report_type') == 'ptax recovery':
            row_h = 1
            col_h = 1
            sheet.write(row_h + 1, col_h, 'PTax Recovery - for the month of ' + month + '-' + year,bold)
            title = [ 'S.No','Name',
                      'Employee Number',
                      'PTax Gross'
                      'PTax Amount',
                     ]
            for i in range(len(title)):
                sheet.set_column('T:T', 13)
                sheet.write(row, col + i , title[i] , bold)
            payslips = self.env['hr.payslip'].search(domain)
            total_gross = total_ptax =  0
            s_no = 0
            for payslip in payslips:
                row += 1
                col = 0
                s_no = s_no + 1
                sheet.write(row, col,s_no)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.name)
                col = col + 1
                sheet.write(row, col, payslip.employee_id.identification_id if payslip.employee_id.identification_id else ' ')
                col = col + 1
                rec = {}
                for line in payslip.line_ids :
                    if line.code == 'GROSS':
                        rec.update({"GROSS": round(line.total)})
                        total_gross += round(line.total)
                    if line.code == 'PT':
                        rec.update({"PT": round(line.total)})
                        total_ptax += round(line.total)
                num = len(title)
                for i in range(num):
                    col = 3
                    sheet.write(row, col, rec.get('GROSS'))
                    col = col + 1
                    sheet.write(row, col, rec.get('PT'))
                    col = col + 1
            row += 1
            col = 1
            sheet.write(row, col, 'Grand Total', bold)
            num = len(title)
            for i in range(num):
                col = 3
                sheet.write(row, col, total_gross, bold)
                col = col + 1
                sheet.write(row, col, total_ptax, bold)
                col = col + 1
        elif data.get('report_type') == 'department summary':
            row_h = 1
            col_h = 1
            sheet.write(row_h + 1, col_h, 'Department-wise Summary for the month of ' +month + '-' + year,bold)
            deps= self.env['hr.department'].search([])
            deps_no = self.env['hr.department'].search_count([])
            payslips = self.env['hr.payslip'].search(domain)
            basic = [1,'BASIC']
            hra = [2,'House Rent Allowance']
            lta = [3,'Leave Travel Allowance']
            spl =[4,'Special Allowance']
            fca =[5,'Food Coupon Allowance']
            sd = [6,'Standard Deduction']
            gross = [7,'Gross']
            pf = [8,'PF']
            pt = [9,'Professional Tax']
            it = [10,'Income Tax']
            fcd = [11,'Food Coupon Deduction']
            td = [12,'Total Deduction']
            net = [13,'NET']
            for dep in deps:
                dept_title.append(dep.name)
            for col_num, data in enumerate(dept_title):
                sheet.write(row + 1, col_num, data)
            row += 1
            rec = {}
            total_dept_basic = total_dept_hra = total_dept_lta = 0
            total_dept_pf = total_dept_ptax = total_dept_it = total_dept_fcd = 0
            total_dept_td = total_dept_net = 0
            total_dept_sd = total_dept_spl = total_dept_fca = 0
            total_dept_gross = total_dept_ptax = 0
            for dep in deps:
                total_basic = total_hra = total_lta = 0
                total_pf = total_ptax = total_it = total_fcd = 0
                total_td = total_net = 0
                total_sd = total_spl = total_fca = 0
                total_gross = total_ptax = 0
                dept_total = 0
                for payslip in payslips:
                    if payslip.employee_id.department_id.name == dep.name:
                        for line in payslip.line_ids :
                            if line.code == 'BASIC':
                                total_basic += round(line.total)
                                total_dept_basic += round(line.total)
                            if line.code == 'HRA':
                                total_hra += round(line.total)
                                total_dept_hra += round(line.total)
                            if line.code == 'LTA':
                                total_lta += round(line.total)
                                total_dept_lta += round(line.total)
                            if line.code == 'SPL':
                                total_spl += round(line.total)
                                total_dept_spl += round(line.total)
                            if line.code == 'FCA':
                                total_fca += round(line.total)
                                total_dept_fca += round(line.total)
                            if line.code == 'SD':
                                total_sd += round(line.total)
                                total_dept_sd += round(line.total)
                            if line.code == 'GROSS':
                                total_gross += round(line.total)
                                total_dept_gross += round(line.total)
                            if line.code == 'PF':
                                total_pf += round(line.total)
                                total_dept_pf += round(line.total)
                            if line.code == 'PT':
                                total_ptax += round(line.total)
                                total_dept_ptax += round(line.total)
                            if line.code == 'IT':
                                total_it += round(line.total)
                                total_dept_it += round(line.total)
                            if line.code == 'FCD':
                                total_fcd += round(line.total)
                                total_dept_fcd += round(line.total)
                            if line.code == 'TD':
                                total_td += round(line.total)
                                total_dept_td += round(line.total)
                            if line.code == 'NET':
                                total_net += round(line.total)
                                total_dept_net += round(line.total)
                basic.append(total_basic)
                hra.append(total_hra)
                lta.append(total_lta)
                spl.append(total_spl)
                fca.append(total_fca)
                sd.append(total_sd)
                gross.append(total_gross)
                pf.append(total_pf)
                pt.append(total_ptax)
                it.append(total_it)
                fcd.append(total_fcd)
                td.append(total_td)
                net.append(total_net)
                col_num = 0
                sheet.write_row(row + 1, col_num, basic)
                sheet.write_row(row + 2, col_num, hra)
                sheet.write_row(row + 3, col_num, lta)
                sheet.write_row(row + 4, col_num, spl)
                sheet.write_row(row + 5, col_num, fca)
                sheet.write_row(row + 6, col_num, sd)
                sheet.write_row(row + 7, col_num, gross)
                sheet.write_row(row + 8, col_num, pf)
                sheet.write_row(row + 9, col_num, pt)
                sheet.write_row(row + 10, col_num, it)
                sheet.write_row(row + 11, col_num, fcd)
                sheet.write_row(row + 12, col_num, td)
                sheet.write_row(row + 13, col_num, net)
            all_dept_total.append(total_dept_basic)
            all_dept_total.append(total_dept_hra)
            all_dept_total.append(total_dept_lta)
            all_dept_total.append(total_dept_spl)
            all_dept_total.append(total_dept_fca)
            all_dept_total.append(total_dept_sd)
            all_dept_total.append(total_dept_gross)
            all_dept_total.append(total_dept_pf)
            all_dept_total.append(total_dept_ptax)
            all_dept_total.append(total_dept_it)
            all_dept_total.append(total_dept_fcd)
            all_dept_total.append(total_dept_td)
            all_dept_total.append(total_dept_net)
            row = 5
            col_num = deps_no + 2
            sheet.write_column(row ,col_num,all_dept_total)
        elif data.get('report_type') == 'individual pay':
            domain += [('employee_id', '=', emp_id)]
            name = self.env['hr.employee'].search([('id','=',emp_id)]).name
            row_h = 1
            col_h = 1
            sheet.write(row_h + 1, col_h, 'Individual Pay Record - '+ name +' - ' + month + '-' + year + ' to ' + end_month + '-' + end_year,bold)
            payslips = self.env['hr.payslip'].search(domain,order="date_from")
            payslip_num = self.env['hr.payslip'].search_count(domain)
            basic = [1, 'BASIC']
            hra = [2, 'House Rent Allowance']
            lta = [3, 'Leave Travel Allowance']
            spl = [4, 'Special Allowance']
            fca = [5, 'Food Coupon Allowance']
            sd = [6, 'Standard Deduction']
            gross = [7, 'Gross']
            pf = [8, 'PF']
            pt = [9, 'Professional Tax']
            it = [10, 'Income Tax']
            fcd = [11, 'Food Coupon Deduction']
            td = [12, 'Total Deduction']
            net = [13, 'NET']
            total_dept_basic = total_dept_hra = total_dept_lta = 0
            total_dept_pf = total_dept_ptax = total_dept_it = total_dept_fcd = 0
            total_dept_td = total_dept_net = 0
            total_dept_sd = total_dept_spl = total_dept_fca = 0
            total_dept_gross = total_dept_ptax = 0
            dept_total = 0
            col = 2
            for payslip in payslips:
                date_from = payslip.date_from
                month = date_from.strftime("%B")
                year = date_from.strftime("%Y")
                sheet.write(row, col, month + '-' + year)
                col+= 1
                total_basic = total_hra = total_lta = 0
                total_pf = total_ptax = total_it = total_fcd = 0
                total_td = total_net = 0
                total_sd = total_spl = total_fca = 0
                total_gross = total_ptax = 0
                for line in payslip.line_ids:
                    if line.code == 'BASIC':
                        total_basic += round(line.total)
                        total_dept_basic += round(line.total)
                    if line.code == 'HRA':
                        total_hra += round(line.total)
                        total_dept_hra += round(line.total)
                    if line.code == 'LTA':
                        total_lta += round(line.total)
                        total_dept_lta += round(line.total)
                    if line.code == 'SPL':
                        total_spl += round(line.total)
                        total_dept_spl += round(line.total)
                    if line.code == 'FCA':
                        total_fca += round(line.total)
                        total_dept_fca += round(line.total)
                    if line.code == 'SD':
                        total_sd += round(line.total)
                        total_dept_sd += round(line.total)
                    if line.code == 'GROSS':
                        total_gross += round(line.total)
                        total_dept_gross += round(line.total)
                    if line.code == 'PF':
                        total_pf += round(line.total)
                        total_dept_pf += round(line.total)
                    if line.code == 'PT':
                        total_ptax += round(line.total)
                        total_dept_ptax += round(line.total)
                    if line.code == 'IT':
                        total_it += round(line.total)
                        total_dept_it += round(line.total)
                    if line.code == 'FCD':
                        total_fcd += round(line.total)
                        total_dept_fcd += round(line.total)
                    if line.code == 'TD':
                        total_td += round(line.total)
                        total_dept_td += round(line.total)
                    if line.code == 'NET':
                        total_net += round(line.total)
                        total_dept_net += round(line.total)
                basic.append(total_basic)
                hra.append(total_hra)
                lta.append(total_lta)
                spl.append(total_spl)
                fca.append(total_fca)
                sd.append(total_sd)
                gross.append(total_gross)
                pf.append(total_pf)
                pt.append(total_ptax)
                it.append(total_it)
                fcd.append(total_fcd)
                td.append(total_td)
                net.append(total_net)
            col_num = 0
            sheet.write_row(row + 1, col_num, basic)
            sheet.write_row(row + 2, col_num, hra)
            sheet.write_row(row + 3, col_num, lta)
            sheet.write_row(row + 4, col_num, spl)
            sheet.write_row(row + 5, col_num, fca)
            sheet.write_row(row + 6, col_num, sd)
            sheet.write_row(row + 7, col_num, gross)
            sheet.write_row(row + 8, col_num, pf)
            sheet.write_row(row + 9, col_num, pt)
            sheet.write_row(row + 10, col_num, it)
            sheet.write_row(row + 11, col_num, fcd)
            sheet.write_row(row + 12, col_num, td)
            sheet.write_row(row + 13, col_num, net)
            all_dept_total.append(total_dept_basic)
            all_dept_total.append(total_dept_hra)
            all_dept_total.append(total_dept_lta)
            all_dept_total.append(total_dept_spl)
            all_dept_total.append(total_dept_fca)
            all_dept_total.append(total_dept_sd)
            all_dept_total.append(total_dept_gross)
            all_dept_total.append(total_dept_pf)
            all_dept_total.append(total_dept_ptax)
            all_dept_total.append(total_dept_it)
            all_dept_total.append(total_dept_fcd)
            all_dept_total.append(total_dept_td)
            all_dept_total.append(total_dept_net)
            row = 4
            col_num = 2 + payslip_num
            sheet.write_column(row, col_num, all_dept_total)
        elif data.get('report_type') == 'monthly pay':
            print('structure_id',structure_id)
            rec = self.env['hr.payroll.structure'].search([('id', '=', structure_id)])
            domain += [('struct_id', '=', structure_id)]
            domain += [('state', 'in', ['verify', 'done', 'paid'])]
            row_h = 1
            col_h = 1
            sheet.write(row_h + 1, col_h, 'Monthly Payroll Summary - '+month + '-' + year, bold)
            #sheet.write(row + 1, col, month + '-' + year + '- Payroll Summary', bold)
            if rec.name == "Intership Stipend":
                title = ['S.No', 'Employee No', 'Employee Name',
                         'Bank Account Number',
                         'PAN', 'Stipend', 'Income Tax', 'Net Pay']
                # 'Gross','Total Deductions',
                for i in range(len(title)):
                    sheet.set_column('T:T', 13)
                    sheet.write(row, col + i, title[i], bold)
                payslips = self.env['hr.payslip'].search(domain).sorted(
                    key=lambda r: r.employee_id.identification_id if r.employee_id.identification_id else 'zzzzz')
                total_stipend = total_net = total_it = 0
                s_no = 0
                for payslip in payslips:
                    row += 1
                    col = 0
                    s_no = s_no + 1
                    sheet.write(row, col, s_no)
                    col = col + 1
                    sheet.write(row, col,
                                payslip.employee_id.identification_id if payslip.employee_id.identification_id else ' ')
                    col = col + 1
                    sheet.write(row, col, payslip.employee_id.name)
                    col = col + 1
                    sheet.write(row, col,
                                payslip.employee_id.bank_account_id.acc_number if payslip.employee_id.bank_account_id.acc_number else ' ')
                    col = col + 1
                    sheet.write(row, col,
                                payslip.employee_id.pan_card_number if payslip.employee_id.pan_card_number else ' ')
                    col = col + 1
                    rec = {}
                    for line in payslip.line_ids:
                        if line.code == 'STIPEND':
                            rec.update({"STIPEND": line.total})
                            total_stipend += line.total
                        if line.code == 'IT':
                            rec.update({"IT": line.total})
                            total_it += line.total
                        if line.code == 'NET':
                            rec.update({"NET": round(line.total)})
                            total_net += round(line.total)
                    num = len(title)
                    for i in range(num):
                        col = 5
                        sheet.set_column('T:T', 13)
                        sheet.write(row, col, rec.get('STIPEND'))
                        col = col + 1
                        sheet.write(row, col, rec.get('IT'))
                        col = col + 1
                        sheet.write(row, col, rec.get('NET'))
                        col = col + 1
                row += 1
                col = 2
                sheet.write(row, col, 'Grand Total', bold)
                num = len(title)
                for i in range(num):
                    col = 5
                    sheet.write(row, col, total_stipend, bold)
                    col = col + 1
                    sheet.write(row, col, total_it, bold)
                    col = col + 1
                    sheet.write(row, col, total_net, bold)
                    col = col + 1
            else:
                title = ['S.No', 'Employee No', 'Employee Name',
                         'Bank Account Number', 'PAN',
                         'Basic Pay', 'HRA',
                         'Leave Travel Alloance', 'Standard Deduction',
                         'Food Coupon (Allowance)', 'Onsite Allowance', 'Shift Allowance',
                         'Spl Allowance', 'Gross',
                         'Employee PF Contribution', 'Food Coupon (Deduction)',
                         'Income Tax', 'HR Deductions', 'Other Deductions',
                         'Professional Tax', 'Total Deductions', 'Net Pay',
                         ]
                for i in range(len(title)):
                    sheet.set_column('T:T', 13)
                    sheet.write(row, col + i, title[i], bold)
                payslips = self.env['hr.payslip'].search(domain).sorted(
                    key=lambda r: r.employee_id.identification_id if r.employee_id.identification_id else 'zzzzz')
                print('payslips',payslips)
                total_basic = total_stipend = total_hra = total_lta = total_sd = 0
                total_fca = total_onsite = total_shift = 0
                total_spl = total_gross = 0
                total_epf = total_fcd = total_it = 0
                total_hrd = total_other = total_pt = 0
                total_td = total_net = 0
                s_no = 0
                for payslip in payslips:
                    row += 1
                    col = 0
                    s_no = s_no + 1
                    sheet.write(row, col, s_no)
                    col = col + 1
                    sheet.write(row, col,
                                payslip.employee_id.identification_id if payslip.employee_id.identification_id else ' ')
                    col = col + 1
                    sheet.write(row, col, payslip.employee_id.name)
                    col = col + 1
                    sheet.write(row, col,
                                payslip.employee_id.bank_account_id.acc_number if payslip.employee_id.bank_account_id.acc_number else ' ')
                    col = col + 1
                    sheet.write(row, col,
                                payslip.employee_id.pan_card_number if payslip.employee_id.pan_card_number else ' ')
                    col = col + 1
                    rec = {}
                    for line in payslip.line_ids:
                        if line.code == 'BASIC':
                            rec.update({"BASIC": line.total})
                            total_basic += line.total
                        if line.code == 'HRA':
                            rec.update({"HRA": line.total})
                            total_hra += line.total
                        if line.code == 'LTA':
                            rec.update({"LTA": line.total})
                            total_lta += line.total
                        if line.code == 'SD':
                            rec.update({"SD": line.total})
                            total_sd += line.total
                        if line.code == 'FCA':
                            rec.update({"FCA": line.total})
                            total_fca += line.total
                        if line.code == 'ONSITE':
                            rec.update({"ONSITE": line.total})
                            total_onsite += line.total
                        if line.code == 'SHIFT':
                            rec.update({"SHIFT": line.total})
                            total_shift += line.total
                        if line.code == 'SPL':
                            rec.update({"SPL": line.total})
                            total_spl += line.total
                        if line.code == 'GROSS':
                            rec.update({"GROSS": line.total})
                            total_gross += line.total
                        if line.code == 'EPF':
                            rec.update({"EPF": line.total})
                            total_epf += line.total
                        if line.code == 'FCD':
                            rec.update({"FCD": line.total})
                            total_fcd += line.total
                        if line.code == 'IT':
                            rec.update({"IT": line.total})
                            total_it += line.total
                        if line.code == 'HRD':
                            rec.update({"HRD": line.total})
                            total_hrd += line.total
                        if line.code == 'OTHER':
                            rec.update({"OTHER": line.total})
                            total_other += line.total
                        if line.code == 'PT':
                            rec.update({"PT": line.total})
                            total_pt += line.total
                        if line.code == 'TD':
                            rec.update({"TD": line.total})
                            total_td += line.total
                        if line.code == 'NET':
                            rec.update({"NET": round(line.total)})
                            total_net += round(line.total)
                    num = len(title)
                    for i in range(num):
                        col = 5
                        sheet.set_column('T:T', 13)
                        sheet.write(row, col, rec.get('BASIC'))
                        col = col + 1
                        sheet.write(row, col, rec.get('HRA'))
                        col = col + 1
                        sheet.write(row, col, rec.get('LTA'))
                        col = col + 1
                        sheet.write(row, col, rec.get('SD'))
                        col = col + 1
                        sheet.write(row, col, rec.get('FCA'))
                        col = col + 1
                        sheet.write(row, col, rec.get('ONSITE'))
                        col = col + 1
                        sheet.write(row, col, rec.get('SHIFT'))
                        col = col + 1
                        sheet.write(row, col, rec.get('SPL'))
                        col = col + 1
                        sheet.write(row, col, rec.get('GROSS'))
                        col = col + 1
                        sheet.write(row, col, rec.get('EPF'))
                        col = col + 1
                        sheet.write(row, col, rec.get('FCD'))
                        col = col + 1
                        sheet.write(row, col, rec.get('IT'))
                        col = col + 1
                        sheet.write(row, col, rec.get('HRD'))
                        col = col + 1
                        sheet.write(row, col, rec.get('OTHER'))
                        col = col + 1
                        sheet.write(row, col, rec.get('PT'))
                        col = col + 1
                        sheet.write(row, col, rec.get('TD'))
                        col = col + 1
                        sheet.write(row, col, rec.get('NET'))
                        col = col + 1
                row += 1
                col = 2
                sheet.write(row, col, 'Grand Total', bold)
                num = len(title)
                for i in range(num):
                    col = 5
                    sheet.write(row, col, total_basic, bold)
                    col = col + 1
                    sheet.write(row, col, total_hra, bold)
                    col = col + 1
                    sheet.write(row, col, total_lta, bold)
                    col = col + 1
                    sheet.write(row, col, total_sd, bold)
                    col = col + 1
                    sheet.write(row, col, total_fca, bold)
                    col = col + 1
                    sheet.write(row, col, total_onsite, bold)
                    col = col + 1
                    sheet.write(row, col, total_shift, bold)
                    col = col + 1
                    sheet.write(row, col, total_spl, bold)
                    col = col + 1
                    sheet.write(row, col, total_gross, bold)
                    col = col + 1
                    sheet.write(row, col, total_epf, bold)
                    col = col + 1
                    sheet.write(row, col, total_fcd, bold)
                    col = col + 1
                    sheet.write(row, col, total_it, bold)
                    col = col + 1
                    sheet.write(row, col, total_hrd, bold)
                    col = col + 1
                    sheet.write(row, col, total_other, bold)
                    col = col + 1
                    sheet.write(row, col, total_pt, bold)
                    col = col + 1
                    sheet.write(row, col, total_td, bold)
                    col = col + 1
                    sheet.write(row, col, total_net, bold)
                    col = col + 1
































