from __future__ import unicode_literals
import frappe
from frappe import _


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

    if doc.select == "عرض":
        flag_powder = 0
        flag_liquid = 0
        count_powder = 0
        count_liquid = 0
        customer_group = frappe.db.get_value(
            "Customer", {"name": doc.customer}, ["customer_group"]
        )
        if customer_group not in ("موظفي الشركة","أونلاين", "مودرن تريد"):
            for item in doc.items:

                item_group = frappe.db.get_value(
                        "Item", {"name": item.item_code}, ["item_group"]
                    )

                item_parent = frappe.db.get_value(
                    "Item Group", {"name": item_group}, ["parent_item_group"]
                )

                # frappe.throw(str(float(doc.total) * 0.10))

                if (
                    item_parent == "شيفى ميكس - بودر"
                    or item_parent == "منتجات بودر"
                    or item_parent == "منتجات السوائل"
                    or item_parent == "شيفى ميكس - سوائل"
                ):
                    if (
                        item_parent == "شيفى ميكس - بودر"
                        or item_parent == "منتجات بودر"
                    ):
                        flag_powder = 1
                    elif (
                        item_parent == "منتجات السوائل"
                        or item_parent == "شيفى ميكس - سوائل"
                    ):
                        flag_liquid = 1
                    else:
                        frappe.throw("احد المنتجات خارج العرض")

        else:
            frappe.throw("انت من ضمن المجموعات الخارجة من العرض")

        if flag_liquid == 1:
            if doc.total_qty >= 1 and doc.total_qty <= 10:
                if doc.total_free_items <= (0.10 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 10% من قيمة المنتجات)"
                    )

            if doc.total_qty > 10 and doc.total_qty <= 26:
                if doc.total_free_items <= (0.115 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 11.5% من قيمة المنتجات)"
                    )

            if doc.total_qty > 26 and doc.total_qty <= 75:
                if doc.total_free_items <= (0.133 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 13.3% من قيمة المنتجات)"
                    )

            if doc.total_qty > 75 and doc.total_qty <= 100:
                if doc.total_free_items <= (0.15 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 15% من قيمة المنتجات)"
                    )

            if doc.total_qty > 100 and doc.total_qty <= 300:
                if doc.total_free_items <= (0.17 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 17% من قيمة المنتجات)"
                    )

            if doc.total_qty > 300 and doc.total_qty <= 500:
                if doc.total_free_items <= (0.18 * doc.total):
                    pass
                else:
                    frappe.throw("لقد تعديت الحد الاقصي")

            if doc.total_qty > 500 and doc.total_qty <= 800:
                if doc.total_free_items <= (0.19 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 19% من قيمة المنتجات)"
                    )

        if flag_powder == 1:
            if doc.total_qty >= 1 and doc.total_qty <= 10:
                if float(doc.total_free_items) <= float((doc.total) * 0.10):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 10% من قيمة المنتجات)"
                    )

            if doc.total_qty > 10 and doc.total_qty <= 25:
                if float(doc.total_free_items) <= (0.12 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 12% من قيمة المنتجات)"
                    )

            if doc.total_qty > 25 and doc.total_qty <= 75:
                if float(doc.total_free_items) <= (0.133 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 13.3% من قيمة المنتجات)"
                    )

            if doc.total_qty > 75 and doc.total_qty <= 100:
                if float(doc.total_free_items) <= (0.15 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 15% من قيمة المنتجات)"
                    )

            if doc.total_qty > 100 and doc.total_qty <= 400:
                if float(doc.total_free_items) <= (0.18 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 18% من قيمة المنتجات)"
                    )

            if doc.total_qty > 400 and doc.total_qty <= 600:
                if float(doc.total_free_items) <= (0.20 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 20% من قيمة المنتجات)"
                    )

            if doc.total_qty > 600 and doc.total_qty <= 800:
                if float(doc.total_free_items) <= (0.22 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 22% من قيمة المنتجات)"
                    )

            if doc.total_qty > 800 and doc.total_qty <= 1000:
                if float(doc.total_free_items) <= (0.24 * doc.total):
                    pass
                else:
                    frappe.throw(
                        "لقد تعديت الحد الاقصي (السعر تعدى 24% من قيمة المنتجات)"
                    )

        create_stock_ledger_entry(doc)
        create_gl_entry(doc)

@frappe.whitelist()
def create_gl_entry(doc):
    for item in doc.free_items:
        if doc.set_warehouse:
            account = frappe.db.get_value(
                "Warehouse", {"name": doc.set_warehouse}, ["account"]
            )
        else:
            frappe.throw("Please choose a warehouse")
        new_doc = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": doc.posting_date,
                "account": "3111 - Cost of Goods Sold - EGEU",
                "debit": item.qty * item.rate,
                "credit": 0,
                "account_currency": "EGP",
                'cost_center' : item.cost_center,
                "debit_in_account_currency": item.qty * item.rate,
                "credit_in_account_currency": 0,
                "against": account,
                "remarks": "صنف داخل عرض",
                "voucher_type": "Delivery Note",
                "voucher_no": doc.name,
                "is_opening": "No",
                "is_advanced": "No",
                "company": "EGEU",
                "fiscal_year": "2023",
            }
        )
        new_doc.insert(ignore_permissions=True)
        new_doc1 = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": doc.posting_date,
                "account": account,
                "debit": 0,
                "credit": item.qty * item.rate,
                "account_currency": "EGP",
                "debit_in_account_currency": 0,
                'cost_center' : item.cost_center,
                "credit_in_account_currency": item.qty * item.rate,
                "against": "3111 - Cost of Goods Sold - EGEU",
                "remarks": "صنف داخل عرض",
                "voucher_type": "Delivery Note",
                "voucher_no": doc.name,
                "is_opening": "No",
                "is_advanced": "No",
                "company": "EGEU",
                "fiscal_year": "2023",
            }
        )
        new_doc1.insert(ignore_permissions=True)


@frappe.whitelist()
def create_stock_ledger_entry(doc):
    for item in doc.free_items:
        if doc.set_warehouse:
            val_rate, actual_qty, name = frappe.db.get_value(
                "Bin",
                {"item_code": item.item_code, "warehouse": doc.set_warehouse},
                ["valuation_rate","actual_qty", "name"],
            )
        else:
            frappe.throw("Please choose a warehouse")

        new_doc = frappe.get_doc(
            {
                "doctype": "Stock Ledger Entry",
                "item_code": item.item_code,
                "warehouse": doc.set_warehouse,
                "posting_date": doc.posting_date,
                "posting_time": doc.posting_time,
                "voucher_type": "Delivery Note",
                "voucher_no": doc.name,
                "voucher_detail_no": item.barcode,
                "actual_qty": -1 * item.qty * item.conversion_factor,
                "qty_after_transaction": item.actual_qty - item.qty,
                "incoming_rate": val_rate,
                "outgoing_rate": val_rate,
                "valuation_rate": val_rate,
                "stock_value": val_rate * ( item.actual_qty - item.qty),
                "stock_value_difference": val_rate * (-1 *item.actual_qty - item.qty),
                "company": "EGEU",
                "stock_uom": item.uom,
                "fiscal_year": "2023",
            }
        )
        new_doc.insert(ignore_permissions=True)

@frappe.whitelist()
def on_cancel(doc, method=None):
    if doc.select == "عرض":
        if doc.free_items != []:
            voucher_name = doc.name

            if frappe.db.exists({"doctype": "Stock Ledger Entry", "voucher_no": voucher_name}):
                name = frappe.db.get_value(
                    "Stock Ledger Entry", {"voucher_no": voucher_name}, ["name"]
                )
                stock_ledger = frappe.get_doc("Stock Ledger Entry", name)
                stock_ledger.is_cancelled = True
                stock_ledger.save(ignore_permissions=True)

            if frappe.db.exists({"doctype": "GL Entry", "voucher_no": voucher_name}):
                namegl = frappe.db.get_value(
                    "GL Entry", {"voucher_no": voucher_name}, ["name"]
                )
                gl = frappe.get_doc("GL Entry", namegl)
                gl.is_cancelled = 1
                gl.save(ignore_permissions=True)
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    total = 0
    for item in doc.free_items:
        total += item.qty * item.rate

    doc.total_free_items = total
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
