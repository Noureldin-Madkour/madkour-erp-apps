from __future__ import unicode_literals
import frappe
from frappe import _
from collections import defaultdict


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
    total = 0
    stock_balance = 0
    if doc.stock_entry_type == 'Material Transfer':
        for item in doc.items:
            total += item.basic_amount

        warehouse = doc.items[0].t_warehouse
        credit = frappe.db.get_value("Warehouse",{"name":warehouse},["credit_limit"])
        warehouses = frappe.get_all(
        "Warehouse", fields=["name", "parent_warehouse"]
        )
        parent_warehouse = {d.name: d.parent_warehouse for d in warehouses}

        filters = {"warehouse": warehouse}
        bin_data = frappe.get_all(
        "Bin",
        fields=["sum(stock_value) as stock_value", "warehouse"],
        filters=filters,
        group_by="warehouse",
        )

        # warehouse_wise_stock_value = defaultdict(float)
        # for row in bin_data:
        #     if not row.stock_value:
        #         continue
        # frappe.msgprint(str(stock_balance + float(total)))
        if(stock_balance + float(total) > credit):
            frappe.throw("لا يمكن تخطي حدود السحب")
        # warehouse_wise_stock_value[row.warehouse] = row.stock_value
        # if len(bin_data) != 0:
        #     stock_balance = float(bin_data[0]['stock_value'])
        #     if credit < stock_balance + float(total):
        #         frappe.throw("لا يمكن تخطي حدود السحب")



@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass

@frappe.whitelist()
def get_item_allow_sales_true():
    frappe.msgprint('sssssssss')
    return frappe.db.sql("""
    SELECT name
    FROM `tabItem`
    """,as_dict=1)
