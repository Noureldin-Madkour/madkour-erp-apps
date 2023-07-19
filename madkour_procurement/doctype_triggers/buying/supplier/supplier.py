from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    last_code = frappe.db.sql(""" select max(supplier_code) as max FROM `tabSupplier`; """, as_dict=1)
    current_code = 0
    if last_code and last_code[0]['max']:
        current_code = int(last_code[0]['max']) + 1
    doc.supplier_code   = current_code
    
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
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
