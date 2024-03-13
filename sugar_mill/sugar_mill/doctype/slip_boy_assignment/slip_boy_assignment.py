# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SlipBoyAssignment(Document):

	@frappe.whitelist()
	def before_save(self):
		
		list=[]
		doc = frappe.db.get_list("User Permission",
												filters={"user": self.slip_boy,},
												fields=["for_value","name"],)
		
		for d in self.get("village_table_sb"):
			list.append(d.village)
		values_in_first_list = set(item['for_value'] for item in doc)
		items_not_in_first_list = [value for value in list if value not in values_in_first_list]
		filtered_list = [item for item in doc if item['for_value'] not in list]
		
		for x in items_not_in_first_list:
			user_permission = frappe.new_doc('User Permission')
			user_permission.user = self.slip_boy
			user_permission.allow = 'Route'
			user_permission.for_value = x
			user_permission.insert()
			user_permission.save()

		self.circleoffice()
  
		for m in filtered_list:
			doc = frappe.db.get_list("User Permission",
												filters={"user": self.slip_boy, "for_value": m.for_value},
												fields=["name"],)
			
			for k in doc:
				if k.name:
					permission_doc = frappe.get_doc("User Permission", k.name)
					frappe.msgprint(str(permission_doc))
					if permission_doc:
						permission_doc.delete()

		# demo = frappe.db.get_list("User Permission",
		# 										filters={"user": self.slip_boy ,"allow":"Circle Office"},
		# 										fields=["for_value","name"],)
		
			


	@frappe.whitelist()
	def on_trash(self):
		for m in self.get("village_table_sb"):
			doc = frappe.db.get_list("User Permission",
												filters={"user": self.slip_boy, "for_value": m.village},
												fields=["name"],)
			for k in doc:
				permission_doc = frappe.get_doc("User Permission", k.name)
				if permission_doc:
					permission_doc.delete()
		doc1 = frappe.db.get_list("User Permission",
												filters={"user": self.slip_boy, "for_value": self.circle_office},
												fields=["name"],)
		for kt in doc1:
			permission_doc = frappe.get_doc("User Permission", kt.name)
			if permission_doc:
				permission_doc.delete()
     
     
	@frappe.whitelist()
	def circleoffice(self):
		moc = frappe.db.get_all("User Permission",
												filters={"user": self.slip_boy,"allow":'Circle Office'},
												fields=["for_value","name"],)
		
		for m in moc:
			
			if m.name:
				userdoc=frappe.get_doc("User Permission",m.name)
				userdoc.delete()


		doc=frappe.get_all("Slip Boy Assignment",filters={"slip_boy":self.slip_boy ,'name':['!=',self.name]},fields=["circle_office"])
		
		for d in doc:
			user_permission = frappe.new_doc('User Permission')
			user_permission.user = self.slip_boy
			user_permission.allow = 'Circle Office'
			user_permission.for_value = d.circle_office
			user_permission.insert()
			user_permission.save()

		user_permission = frappe.new_doc('User Permission')
		user_permission.user = self.slip_boy
		user_permission.allow = 'Circle Office'
		user_permission.for_value = self.circle_office
		user_permission.insert()
		user_permission.save()
		



	# s=frappe.new_doc('User Permission')
	# s.user=doc.user
	# s.allow="Village"
	# s.for_value=doc.village
	# s.insert()