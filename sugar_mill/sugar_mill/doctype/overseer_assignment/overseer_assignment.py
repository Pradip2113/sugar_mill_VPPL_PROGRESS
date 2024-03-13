# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OverseerAssignment(Document):
    
	@frappe.whitelist()
	def before_save(self):
		self.for_overseer()
		self.for_fieldman()
  

	@frappe.whitelist()
	def for_overseer(self):
		list=[]
		doc = frappe.db.get_list("User Permission",
												filters={"user": self.overseer,},
												fields=["for_value","name"],)
		for d in self.get("circle_office_table_os"):
			list.append(d.circle_office)
		values_in_first_list = set(item['for_value'] for item in doc)
		items_not_in_first_list = set([value for value in list if value not in values_in_first_list])
		filtered_list = [item for item in doc if item['for_value'] not in list]
		# frappe.throw(str(items_not_in_first_list))
		for x in items_not_in_first_list:
			user_permission = frappe.new_doc('User Permission')
			user_permission.user = self.overseer
			user_permission.allow = 'Circle Office'
			user_permission.for_value = x
			user_permission.insert()
			user_permission.save()
   
		for m in filtered_list:
			doc = frappe.db.get_list("User Permission",
												filters={"user": self.overseer, "for_value": m.for_value},
												fields=["name"],)
			for k in doc:
				permission_doc = frappe.get_doc("User Permission", k.name)
				if permission_doc:
					permission_doc.delete()
		
	
	@frappe.whitelist()
	def for_fieldman(self):
		fieldman_list = []
		for do in self.get('circle_office_table_os'):
			list=[]
			doc = frappe.db.get_list("User Permission",
													filters={"user": do.field_man,},
													fields=["for_value","name"],)

			list.append(do.circle_office)
			values_in_first_list = set(item['for_value'] for item in doc)
			items_not_in_first_list = [value for value in list if value not in values_in_first_list]
			filtered_list = [item for item in doc if item['for_value'] not in list]
			
			for x in list:
				user_permission = frappe.new_doc('User Permission')
				user_permission.user = do.field_man
				user_permission.allow = 'Circle Office'
				user_permission.for_value = x
				user_permission.insert()
				user_permission.save()
	
			# for m in filtered_list:
			# 	doc = frappe.db.get_list("User Permission",
			# 										filters={"user": do.field_man, "for_value": m.for_value},
			# 										fields=["name"],)
			# 	for k in doc:
			# 		permission_doc = frappe.get_doc("User Permission", k.name)
			# 		if permission_doc:
			# 			permission_doc.delete()
		 

	@frappe.whitelist()
	def on_trash(self):
		for m in self.get("circle_office_table_os"):
			doc = frappe.db.get_list("User Permission",
												filters={"user": self.overseer, "for_value": m.circle_office},
												fields=["name"],)
			for k in doc:
				permission_doc = frappe.get_doc("User Permission", k.name)
				if permission_doc:
					permission_doc.delete()
 
 
			doc_1 = frappe.db.get_list("User Permission",
												filters={"user": m.field_man, "for_value": m.circle_office},
												fields=["name"],)
			for k_1 in doc_1:
				permission_doc_1 = frappe.get_doc("User Permission", k_1.name)
				if permission_doc_1:
					permission_doc_1.delete()
 
 
 
