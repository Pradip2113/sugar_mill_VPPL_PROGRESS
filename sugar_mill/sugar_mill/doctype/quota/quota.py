# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Quota(Document):

 	# To get value conversion factor from item 
	@frappe.whitelist()
	def conversion_factors(self):
		for item in self.get("items"):
			if item.item_code:
				conversion_factor = frappe.get_value('UOM Conversion Detail', {'parent':item.item_code,'uom':item.uom},"conversion_factor")
				item.conversion_factor = conversion_factor
				item.stock_qty = float(item.conversion_factor or 0)*float(item.quantity or 0)
  
	# get item uom from item  
	@frappe.whitelist()
	def get_uom_item(self):
		for item in self.get("items"):
			if item.item_code:
				uom = frappe.get_value('Item', {'name':item.item_code},"stock_uom")					
				item.uom =uom
	


						