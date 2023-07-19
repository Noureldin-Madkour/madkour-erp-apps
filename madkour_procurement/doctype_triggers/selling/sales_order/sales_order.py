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
    delivery_date = doc.delivery_date
    for item in doc.items:
        item.delivery_date = delivery_date
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

@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
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
