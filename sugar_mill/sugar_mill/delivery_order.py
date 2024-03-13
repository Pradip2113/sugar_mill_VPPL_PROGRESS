import frappe
                
@frappe.whitelist()
def get_raw_materials(sales_entry):
    deli_or = {}

    if sales_entry:
        doc_name = frappe.get_value('Sugar Allotment Order', {'name': sales_entry, 'docstatus': 1}, "name")
        if doc_name:
            doc = frappe.get_doc('Sugar Allotment Order', doc_name)
            deli_or['sale_type'] = doc.sale_type
            deli_or['reference_number'] = doc.reference_number
            deli_or['quota'] = doc.release_order
            deli_or['reference_date'] = doc.reference_date
            deli_or['items'] = []

            for d in doc.get("items"):
                # frappe.throw(str(d.rate))
                item_data = {
                    "item_code": d.item_code,
                    "item_name": d.item_name,
                    "item_group":d.item_group,
                    "qty": d.qty,
                    "stock_uom": d.stock_uom,
                    "uom": d.uom,
                    "season":d.season,
                    "rate": float(d.rate),
                }
                deli_or['items'].append(item_data)
                # frappe.throw(str(deli_or))
    return deli_or
