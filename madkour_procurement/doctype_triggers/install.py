import frappe
from frappe import _

def after_install():
    script = """
frappe.ui.form.on('Material Request', {
    assign_all: function (frm) {
        frm.doc.items.forEach(function (item) {
            // Toggle the "assign" field in each child table row between 0 and 1
            frappe.model.set_value(item.doctype, item.name, 'assign', item.assign === 1 ? 0 : 1);
        });
        frm.refresh_field('items'); // Refresh the child table to reflect the changes
    }
});

frappe.ui.form.on('Material Request', {
    refresh(frm) {
        frm.set_query('assign', function() {
            return {
                query: 'frappe.core.doctype.user.user.user_query',
                filters: {
                    'role_profile_name': ['in', ['Buyer', 'Buyers Manager']]
                }
            };
        });
    }
});
            """
    doc = frappe.get_doc({
        "doctype": "Client Script",
        "name": "MR",
        "dt": "Material Request",
        "view": "Form",
        "module": "Madkour Procurement",
        "enabled": 1,
        "script": script
    })
    doc.insert(ignore_permissions=True)



    #Requester field
    doc_requester_field = frappe.get_doc({
    "doctype": "Custom Field",
    "name": "Material Request-requester",
    "fieldtype": "Link",
    "module": "Madkour Procurement",
    "dt": "Material Request",
    "options": "Employee",
    "label": "Requester",
    "fieldname": "requester",
    "insert_after": "requester_name",
    "reqd": 1,
    "is_system_generated": 1
    }).insert(ignore_permissions=True)

    #Direct manager field
    doc_requester_field = frappe.get_doc({
        "doctype": "Custom Field",
        "fieldtype": "Link",
        "dt": "Material Request",
        "options": "Employee",
        "module": "Madkour Procurement",
        "label": "Direct manager",
        "fieldname": "direct_manager",
        "insert_after": "requester_mobile",
        "fetch_from": "requester.reports_to",
        "length": 0,
        "read_only": 1,
        "is_system_generated": 1
    })
    doc_requester_field.insert(ignore_permissions=True)

    #Edit requester name field
    rq = frappe.db.sql("""
        select name from `tabCustom Field`
        where dt = 'Material Request'
        and fieldname = 'requester_name'
        """,as_dict = 1)[0].name
    
    doc_edit_requester_field = frappe.get_doc('Custom Field', rq)
    doc_edit_requester_field.fetch_from = "requester.employee_name"
    doc_edit_requester_field.read_only = 1
    doc_edit_requester_field.save(ignore_permissions=True)


    #Edit requester mobile field
    rq = frappe.db.sql("""
        select name from `tabCustom Field`
        where dt = 'Material Request'
        and fieldname = 'requester_mobile'
        """,as_dict = 1)[0].name
    
    doc_edit_requester_mobile = frappe.get_doc('Custom Field', rq)
    doc_edit_requester_mobile.fetch_from = "requester.cell_number"
    doc_edit_requester_mobile.read_only = 1
    doc_edit_requester_mobile.save(ignore_permissions=True)


    #Assign field
    doc_assign_field = frappe.get_doc({
        "doctype": "Custom Field",
        "fieldtype": "Link",
        "dt": "Material Request",
        "options": "User",
        "label": "Assign",
        "module": "Madkour Procurement",
        "fieldname": "assign",
        "insert_after": "project",
        "length": 0,
        "is_system_generated": 1
    })
    doc_assign_field.insert(ignore_permissions=True)

    #Assign field
    doc_description_field = frappe.get_doc({
        "doctype": "Custom Field",
        "fieldtype": "Text",
        "dt": "Material Request",
        "label": "Description",
        "module": "Madkour Procurement",
        "fieldname": "description",
        "insert_after": "assign",
        "length": 0,
        "mandatory_depends_on": "assign",
        "is_system_generated": 1
    })
    doc_description_field.insert(ignore_permissions=True)
    
    #Assign all field
    doc_assign_all_field = frappe.get_doc({
        "doctype": "Custom Field",
        "fieldtype": "Check",
        "dt": "Material Request",
        "label": "Assign all",
        "module": "Madkour Procurement",
        "fieldname": "assign_all",
        "insert_after": "assign",
        "is_system_generated": 1
    })
    doc_assign_all_field.insert(ignore_permissions=True)


    #Assign field in child table
    doc_assignch_field = frappe.get_doc({
        "doctype": "Custom Field",
        "dt": "Material Request Item",
        "label": "Assign",
        "module": "Madkour Procurement",
        "fieldtype": "Check",
        "fieldname": "assign",
        "is_system_generated": 1
    })
    doc_assignch_field.insert(ignore_permissions=True)


    #Edit buyer field in child table
    rq = frappe.db.sql("""
        select name from `tabCustom Field`
        where dt = 'Material Request Item'
        and fieldname = 'buyer'
        """,as_dict = 1)[0].name
    
    doc_buyer_field = frappe.get_doc('Custom Field', rq)
    doc_buyer_field.options = ""
    doc_buyer_field.save(ignore_permissions=True)

    frappe.msgprint("Your message after installation.")

def before_install():
    pass