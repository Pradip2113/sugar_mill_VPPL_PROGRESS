# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HandTGroup(Document):
	@frappe.whitelist()
	def update_value(self):
		if not self.doc_name:
			branch_doc = frappe.get_all("Branch",
												filters={"name": self.branch},
												fields={"group_count_no",},)
			if branch_doc:
				c_counter = (branch_doc[0].group_count_no)
				value = str(c_counter+1)
				self.doc_name = value
				# frappe.throw(value)
			else:
				frappe.throw("Please select Plant")
   
	@frappe.whitelist()
	def before_save(self):
		# frappe.throw(str(int(self.name)-1)+" "+str(frappe.get_value("Branch", self.branch , "group_count_no")))
		# if not self.doc_name:
		# 	frappe.throw("Please Refresh the page and try again")
		if str(int(self.name)-1)== str(frappe.get_value("Branch", self.branch , "group_count_no")):
			frappe.db.set_value('Branch', self.branch , 'group_count_no', self.doc_name)
  
	@frappe.whitelist()
	def on_trash(self):
		if str(self.name) == str(frappe.get_value("Branch", self.branch , "group_count_no")):
			h=frappe.get_all('H and T Group', order_by='CAST(name AS UNSIGNED) DESC' ,limit =2)
			frappe.db.set_value('Branch', self.branch , 'group_count_no', str((h[1].name)))
		