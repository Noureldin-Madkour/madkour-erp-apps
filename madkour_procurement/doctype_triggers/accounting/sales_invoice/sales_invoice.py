import frappe
from frappe import _
import requests
import time
import json



@frappe.whitelist()
def before_insert(doc, metho):
    pass

@frappe.whitelist()
def after_insert(doc, metho):
    pass

@frappe.whitelist()
def onload(doc, metho):
    pass


@frappe.whitelist()
def before_validate(doc, metho):
    pass


@frappe.whitelist()
def validate(doc, metho):
    pass


@frappe.whitelist()
def on_submit(doc, metho):
    pass




@frappe.whitelist()
def on_cancel(doc, metho):
    pass

@frappe.whitelist()
def before_save(doc, metho):
    pass

@frappe.whitelist()
def before_cancel(doc, metho):
    pass


@frappe.whitelist()
def on_update(doc, metho):
    pass

