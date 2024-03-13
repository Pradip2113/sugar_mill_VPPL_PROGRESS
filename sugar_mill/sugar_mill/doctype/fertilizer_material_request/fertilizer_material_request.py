# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FertilizerMaterialRequest(Document):
	@frappe.whitelist()
	def opcost(self):
		self. fertilizer_material_template == self.vehicle_type
		doc=frappe.db.get_list('Fertilizer Material Template',filters={'name':self.fertilizer_material_template})
		for d in doc:
			doc1=frappe.get_doc('Fertilizer Material Template',d.name)
			if(self.fertilizer_material_template==d.name):
				for d1 in doc1.get("items"):
					self.append("items",{
							"items":d1.item_code,
							"item_name":d1.item_name,
							"qty":d1.qty,
							"rate":d1.rate,
							"uom":d1.uom,
							"description":d1.item_name,
							"gst_hsn_code":d1.hsn_code,
							"temp_qty":d1.qty,
							}
						)
     
	@frappe.whitelist()
	def labor(self):
		for d2 in self.get("items"):
			d2.qty = d2.temp_qty * self.labor_count

