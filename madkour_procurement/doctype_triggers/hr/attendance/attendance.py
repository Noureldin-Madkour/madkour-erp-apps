from __future__ import unicode_literals
import frappe
from frappe import _
import datetime
from frappe.utils import getdate
from frappe.utils import add_to_date


@frappe.whitelist()
def before_insert(doc, method=None):
    pass


@frappe.whitelist()
def after_insert(doc, method=None):
    pass


@frappe.whitelist()
def onload(doc, method=None):
    pass


@frappe.whitelist()
def before_validate(doc, method=None):
    pass


@frappe.whitelist()
def validate(doc, method=None):
    pass

@frappe.whitelist()
def flexible(doc, chechin, late):
    get_out_time = frappe.db.sql(f"""
        select distinct `tabEmployee Checkin`.time, `tabEmployee Checkin`.log_type,`tabEmployee Checkin`.shift
        from `tabEmployee Checkin`
        where `tabEmployee Checkin`.employee = '{doc.employee}'
        and date(`tabEmployee Checkin`.time) = '{chechin.time.date()}'
        and `tabEmployee Checkin`.log_type = 'OUT'
    """,as_dict = 1)

    s = str(chechin.time.time())
    e = str(get_out_time[0].time.time())

    time_IN = datetime.datetime.strptime(s, "%H:%M:%S")
    time_OUT = datetime.datetime.strptime(e, "%H:%M:%S")

    delta_time = (time_OUT - time_IN)//3600

    time_hours = delta_time.total_seconds()
    if time_hours < 8:
        extra_salary = frappe.get_doc(
        {
            "doctype": "Extra Salary",
            "company": "EGEU",
            "employee": doc.employee,
            "time_check_in": chechin.time.time(),
            "salary_component": late.salary_component,
            "amount": -1,
            "payroll_date": doc.attendance_date,
            "overwrite_salary_structure_amount": 1,
            "deduct_full_tax_on_selected_payroll_date": 0,
            "posted": 0,
        }
    )
    extra_salary.submit()
    frappe.msgprint("Extra Salary has been created a flexible")

@frappe.whitelist()
def on_submit(doc, method=None):

    get_checkin = frappe.db.sql(
        f"""
                                select distinct `tabEmployee Checkin`.name, `tabEmployee Checkin`.time, `tabEmployee Checkin`.log_type,`tabEmployee Checkin`.shift
                                from `tabEmployee Checkin`
                                where `tabEmployee Checkin`.employee = '{doc.employee}'
                                and `tabEmployee Checkin`.log_type = 'IN'
                                and `tabEmployee Checkin`.shift IS NOT NULL
                                order by `tabEmployee Checkin`.time desc
                                """,
        as_dict=1,
    )
    for chechin in get_checkin:
        if frappe.db.exists({"doctype": "Payroll Policy", "shift_type": chechin.shift}):
            pp = frappe.get_last_doc(
                "Payroll Policy", filters={"shift_type": chechin.shift}
            )
        else:
            frappe.throw("Something went wrong")

        for late in pp.late_table:

            d = (datetime.datetime.min + late.from_time).time()
            d2 = (datetime.datetime.min + late.to_time).time()
            if chechin.time.date() == getdate(doc.attendance_date):

                if chechin.time.time() >= d and chechin.time.time() <= d2:
                    if not pp.repeat_late == 1:
                        if pp.is_flexible == 1:
                            flexible(doc, chechin, late)
                        else:
                            extra_salary = frappe.get_doc(
                                {
                                    "doctype": "Extra Salary",
                                    "company": "EGEU",
                                    "employee": doc.employee,
                                    "time_check_in": chechin.time.time(),
                                    "salary_component": late.salary_component,
                                    "amount": late.deduct_value_hours,
                                    "payroll_date": doc.attendance_date,
                                    "overwrite_salary_structure_amount": 1,
                                    "deduct_full_tax_on_selected_payroll_date": 0,
                                    "posted": 0,
                                }
                            )
                            extra_salary.submit()
                            frappe.msgprint("Extra Salary has been created")
                    else:
                        if pp.is_flexible == 1:
                            flexible(doc, chechin, late)
                        else:
                            ex_salary = frappe.db.sql(
                                f"""
                                select *
                                from `tabExtra Salary`
                                where employee = '{doc.employee}'
                                and salary_component = '{late.salary_component}'
                                and time_check_in between '{late.from_time}' and '{late.to_time}'
                                ORDER BY
                                `tabExtra Salary`.payroll_date DESC,
                                `tabExtra Salary`.creation DESC LIMIT 1
                            """,
                                as_dict=1,
                            )
                            if ex_salary:
                                if ex_salary[0].amount * 2 >= late.maximum_deduct_value:
                                    value = late.maximum_deduct_value
                                else:
                                    value = ex_salary[0].amount * 2
                                extra_salary = frappe.get_doc(
                                    {
                                        "doctype": "Extra Salary",
                                        "company": "EGEU",
                                        "employee": doc.employee,
                                        "time_check_in": chechin.time.time(),
                                        "salary_component": late.salary_component,
                                        "amount": value,
                                        "payroll_date": doc.attendance_date,
                                        "overwrite_salary_structure_amount": 1,
                                        "deduct_full_tax_on_selected_payroll_date": 0,
                                        "posted": 0,
                                    }
                                )
                                extra_salary.submit()
                                frappe.msgprint("Extra Salary has been Updated")
                            else:
                                extra_salary = frappe.get_doc(
                                    {
                                        "doctype": "Extra Salary",
                                        "company": "EGEU",
                                        "employee": doc.employee,
                                        "time_check_in": chechin.time.time(),
                                        "salary_component": late.salary_component,
                                        "amount": late.deduct_value_hours,
                                        "payroll_date": doc.attendance_date,
                                        "overwrite_salary_structure_amount": 1,
                                        "deduct_full_tax_on_selected_payroll_date": 0,
                                        "posted": 0,
                                    }
                                )
                                extra_salary.submit()
                                frappe.msgprint("Extra Salary has been created")

    if frappe.db.exists({"doctype": "Payroll Policy", "shift_type": doc.shift}):
        pp = frappe.get_last_doc(
            "Payroll Policy", filters={"shift_type": doc.shift}
        )
        if pp.over_time_component:
            overtimes = frappe.db.sql(
                f"""
                                            select distinct `tabEmployee Checkin`.time, `tabEmployee Checkin`.log_type,`tabEmployee Checkin`.shift
                                            from `tabEmployee Checkin`
                                            where `tabEmployee Checkin`.employee = '{doc.employee}'
                                            and `tabEmployee Checkin`.log_type = 'OUT'
                                            order by `tabEmployee Checkin`.time desc
                                            """,
                as_dict=1,
            )
            for overtime in overtimes:
                if frappe.db.exists(
                    {"doctype": "Payroll Policy", "shift_type": overtime.shift}
                ):
                    pp = frappe.get_last_doc(
                        "Payroll Policy", filters={"shift_type": overtime.shift}
                    )
                    if pp.over_time_component:
                        pp_end_time = datetime.datetime.strptime(pp.end_time, "%H:%M:%S")
                        over_time_in_str = str(overtime.time.time())
                        time_out = datetime.datetime.strptime(over_time_in_str, "%H:%M:%S")
                        time_in_mins = time_out - pp_end_time
                        time_in_mins = (time_in_mins.total_seconds()) / 60
                        if time_in_mins > 0:
                            if overtime.time.date() == getdate(doc.attendance_date):
                                extra_salary = frappe.get_doc(
                                    {
                                        "doctype": "Extra Salary",
                                        "company": "EGEU",
                                        "employee": doc.employee,
                                        "time_check_in": overtime.time.time(),
                                        "salary_component": pp.over_time_component,
                                        "amount": time_in_mins,
                                        "payroll_date": doc.attendance_date,
                                        "overwrite_salary_structure_amount": 1,
                                        "deduct_full_tax_on_selected_payroll_date": 0,
                                        "posted": 0,
                                    }
                                )
                                extra_salary.submit()
                                frappe.msgprint("Overtime has been created in Extra Salary")
                else:
                    frappe.throw("Something went wrong")

    if doc.status == "Absent":
        if frappe.db.exists({"doctype": "Payroll Policy", "shift_type": doc.shift}):
            pp = frappe.get_last_doc(
                "Payroll Policy", filters={"shift_type": doc.shift}
            )
            if pp.absent_salary_component:
                extra_salary = frappe.get_doc(
                    {
                        "doctype": "Extra Salary",
                        "company": "EGEU",
                        "employee": doc.employee,
                        "salary_component": pp.absent_salary_component,
                        "amount": 1,
                        "payroll_date": doc.attendance_date,
                        "overwrite_salary_structure_amount": 1,
                        "deduct_full_tax_on_selected_payroll_date": 0,
                        "posted": 0,
                    }
                )
                extra_salary.submit()
                frappe.msgprint("Absents has been created in Extra Salary")
                extra_salary = frappe.get_doc(
                    {
                        "doctype": "Extra Salary",
                        "company": "EGEU",
                        "employee": doc.employee,
                        "salary_component": pp.penalty_salary_component,
                        "amount": 1,
                        "payroll_date": doc.attendance_date,
                        "overwrite_salary_structure_amount": 1,
                        "deduct_full_tax_on_selected_payroll_date": 0,
                        "posted": 0,
                    }
                )
                extra_salary.submit()
                frappe.msgprint("Absents has been created in Extra Salary again")

@frappe.whitelist()
def on_cancel(doc, method=None):
    pass


@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass


@frappe.whitelist()
def before_save(doc, method=None):
    pass


@frappe.whitelist()
def before_cancel(doc, method=None):
    pass


@frappe.whitelist()
def on_update(doc, method=None):
    pass
