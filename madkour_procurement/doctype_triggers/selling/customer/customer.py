from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):

     last_code = frappe.db.sql(""" select max(code) as max from `tabCustomer` """, as_dict=1)
     for x in last_code:
         doc.code = int(x.max) + 1

@frappe.whitelist()
def after_insert(doc, method=None):
    doc.mobile_no = doc.mobile2

@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    doc.mobile_no = doc.mobile2

@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
