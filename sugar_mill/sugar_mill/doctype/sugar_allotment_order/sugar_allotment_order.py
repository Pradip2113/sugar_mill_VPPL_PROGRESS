# Copyright (c) 2024, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SugarAllotmentOrder(Document):
	
	def before_save(self):
		self.iuom_conversion_calculation()
		# self.quantity_calculation()
  				
	@frappe.whitelist()
	def update_conversion_factors(self):
		for item in self.get("items"):
			if item.item_code:
				conversion_factor = frappe.get_value('UOM Conversion Detail', {'parent':item.item_code,'uom':item.uom},"conversion_factor")
				item.conversion_factor = conversion_factor
				item.stock_qty = float(item.conversion_factor or 0)*float(item.qty or 0)
			
							
	@frappe.whitelist()
	def get_item_uom(self):
		for item in self.get("items"):
			if item.item_code:
				suom = frappe.get_value('Item', {'name': item.item_code}, "sales_uom")
				if(suom):
					item.uom =suom
				else:
					uom = frappe.get_value('Item', {'name':item.item_code},"stock_uom")					
					item.uom =uom


	@frappe.whitelist()
	def get_raw_materials(self):
		if self.release_order:
			doc_name = frappe.get_value('Quota', {'name': self.release_order, 'docstatus': 1}, "name")
			if doc_name:
				doc = frappe.get_doc('Quota', doc_name)
				self.reference_number = doc.reference_number
				self.reference_date = doc.reference_date
				self.total_quantity = doc.total_quantity
				for d in doc.get("items"):
					self.append('items', {
						"item_code": d.item_code,
						"item_name": d.item_name,
						"qty": d.quantity,
						"stock_uom": d.stock_uom,
						"uom": self.get_sales_uom(d.item_code),
						"conversion_factor": d.conversion_factor,
						"stock_qty": d.stock_qty,
					})

	@frappe.whitelist()
	def get_sales_uom(self, item_code):
		uom = frappe.get_value('Item', {'name': item_code}, "sales_uom")
		# frappe.throw(str(uom))
		if uom:
			# frappe.msgprint('hiii')
			return uom
		else:
			releaseuom = frappe.get_value('Quota', {'name': self.release_order, 'docstatus': 1}, "name")
			if releaseuom:
				doc1 = frappe.get_doc('Quota', releaseuom)
				for quota_item in doc1.get("items"):
					if quota_item.item_code == item_code:
						return quota_item.uom
			else:
				default_uom = frappe.get_value('Item', {'name': item_code}, "stock_uom")
				return default_uom
		return None

	@frappe.whitelist()
	def iuom_conversion_calculation(self):
		for item in self.get("items"):
			if item.item_code:
				conversion_factor = frappe.get_value('UOM Conversion Detail', {'parent':item.item_code,'uom':item.uom},"conversion_factor")
				item.conversion_factor = conversion_factor
				item.stock_qty = float(item.conversion_factor or 0)*float(item.qty or 0)
    

