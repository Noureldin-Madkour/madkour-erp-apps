from __future__ import unicode_literals
import frappe
from frappe import _
import datetime

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
def on_submit(doc, method=None):
    pass
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    
    for item in doc.items:
        if item.custom_assign == 1 and doc.custom_assign_to:
            # Create ToDo doctype for this material request
            current_user = frappe.session.user
            current_user_full_name = frappe.get_value("User", current_user, "full_name")

            todo_doc = frappe.get_doc({
                'doctype': 'ToDo',
                'status': 'Open',
                'priority': 'Medium',
                'date': datetime.date.today(),
                'allocated_to': doc.custom_assign_to,
                'description': doc.custom_description,
                'reference_type': 'Material Request',
                'reference_name': doc.name,
                'assigned_by': current_user,
                'assigned_by_full_name': current_user_full_name
            })
            todo_doc.insert()

            user = frappe.db.sql(f"""
                SELECT CONCAT_WS(' ', first_name, middle_name, last_name) AS full_name
                FROM `tabUser`
                WHERE name = '{doc.custom_assign_to}'
            """, as_dict=1)[0]
            full_name = user.get('full_name')
            full_name = full_name.title()
            item.buyer = full_name
            item.custom_assign = 0
            doc.custom_assign_to = ''
            doc.custom_as = 0

@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
