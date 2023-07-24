import frappe
from frappe import _


def after_install():
    script = """
            frappe.ui.form.on('Material Request', {
                refresh(frm) {
                    // your code here
                }
            })
            """
    doc = frappe.get_doc({
        "doctype": "Client Script",
        "name": "MR",
        "dt": "Material Request",
        "view": "Form",
        "script": script
    })
    
    doc.insert(ignore_permissions=True)