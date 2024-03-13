# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FarmerList(Document):
	@frappe.whitelist()    
	def fetchbranch(self):
		for i in self.bank_details:
			doc1=frappe.db.get_list('Bank Master',filters={'bank_name':i.bank_name},fields={'name','bank_name','branch','ifsc_code'})
			for d in doc1:
				i.branchifsc_code = d.ifsc_code
	
	def before_save(self):
		aadhar_list = frappe.get_all('Farmer List', filters={'aadhaar_number': self.aadhaar_number, 'name': ['!=', self.name]},fields ={'name','supplier_name'})
		if aadhar_list:
			frappe.throw(f"Aadhar number must be unique aadhar Exist for vendor '{aadhar_list[0].supplier_name}'")
  
		existing_supplier = frappe.get_all('Supplier', filters={'name': self.name})
		if len(existing_supplier)==0:
			m=frappe.new_doc('Supplier')
			m.supplier_type=self.supplier_type
			m.supplier_name=self.supplier_name
			m.supplier_group=self.supplier_group
			m.branch = self.branch
			m.insert()
			doc = frappe.db.get_all("Supplier", fields=["name"], order_by="creation DESC", limit=1)
			frappe.db.set_value("Supplier", doc[0].name, "name", self.name)
	# ------------------------------------------------------------------------------------------------------------------------------------
			k=frappe.new_doc('Customer')
			k.customer_type=self.supplier_type
			k.customer_name=self.supplier_name
			k.customer_group=self.supplier_group
			k.branch = self.branch
			k.territory="India"
			k.insert()
			moc = frappe.db.get_all("Customer", fields=["name"], order_by="creation DESC", limit=1)
			frappe.db.set_value("Customer", moc[0].name, "name", self.name)
	# ------------------------------------------------------------------------------------------------------------------------------------
			q=frappe.new_doc('Address')
			q.address_type="Billing"
			q.address_title=self.name 
			q.country="India"
			q.gst_category="Unregistered"
			q.pincode=self.pin_code
			q.address_line1 =self.village
			q.address_line2 =self.taluka
			q.city=self.circle_office
			q.state=self.state
			q.append(
							"links",
							{
								"link_doctype": "Supplier",
								"link_name": self.name,
								"link_title": "",
								
							},
						)
			q.append(
							"links",
							{
								"link_doctype": "Customer",
								"link_name": self.name,
								"link_title": "",
								
							},
						)
			q.insert()
	
			qoc=frappe.db.get_all("Address", fields=["name"], order_by="creation DESC", limit=1)
			frappe.db.set_value("Supplier", self.name, "supplier_primary_address", qoc[0].name)
			frappe.db.set_value("Supplier", self.name, "primary_address", f"{self.village}\n{self.taluka}\n{self.circle_office}\n{self.state}\n India")
			frappe.db.set_value("Customer",self.name, "customer_primary_address", qoc[0].name)
			frappe.db.set_value("Customer", self.name, "primary_address", f"{self.village}\n{self.taluka}\n{self.circle_office}\n{self.state}\n India") 
		else:
			frappe.db.set_value("Supplier", self.name, "supplier_type", self.supplier_type)
			frappe.db.set_value("Supplier", self.name, "supplier_name", self.supplier_name)
			frappe.db.set_value("Supplier", self.name, "supplier_group", self.supplier_group)
			frappe.db.set_value("Supplier", self.name, "branch", self.branch)
			frappe.db.set_value("Supplier", self.name, "primary_address", f"{self.village}\n{self.taluka}\n{self.circle_office}\n{self.state}\n India")
   
			frappe.db.set_value("Customer", self.name, "customer_name", self.supplier_name)
			frappe.db.set_value("Customer", self.name, "customer_group", self.supplier_group)
			frappe.db.set_value("Customer", self.name, "branch", self.branch)
			frappe.db.set_value("Customer", self.name, "territory", "India")
			frappe.db.set_value("Customer", self.name, "primary_address", f"{self.village}\n{self.taluka}\n{self.circle_office}\n{self.state}\n India") 
   
			frappe.db.set_value("Address",self.name+"-Billing" , "address_line1", self.village)
			frappe.db.set_value("Address", self.name+"-Billing", "address_line2", self.taluka)
			frappe.db.set_value("Address", self.name+"-Billing", "city", self.circle_office)
			frappe.db.set_value("Address", self.name+"-Billing", "state", self.state)
			frappe.db.set_value("Address", self.name+"-Billing", "country", "India")
			frappe.db.set_value("Address", self.name+"-Billing", "pincode", self.pin_code)
			
		# frappe.msgprint(f"हा VENDOR, {self.name} या ID सह सेव्ह केला आहे.")
  
	def on_trash(self):
		frappe.delete_doc("Supplier", self.name)
		frappe.delete_doc("Customer", self.name)
  
	@frappe.whitelist()
	def validation_to_bank_details(self):
		checked_row_1 = None
		for d in self.get("bank_details"):
			if d.farmer and d.farmer == 1: 
				if checked_row_1 is None:
					checked_row_1 = d
				else:
					d.farmer = 0 
     
     
		checked_row_2 = None
		for d in self.get("bank_details"):
			if d.harvester and d.harvester == 1: 
				if checked_row_2 is None:
					checked_row_2 = d
				else:
					d.harvester = 0 
     
     
		checked_row_3 = None
		for d in self.get("bank_details"):
			if d.transporter and d.transporter == 1: 
				if checked_row_3 is None:
					checked_row_3 = d
				else:
					d.transporter = 0 
     
@frappe.whitelist()
def vendor_code(docname):
    doc = frappe.get_doc("Farmer List", docname)
    field_value_exist = frappe.get_value("Farmer List", doc.name, 'existing_supplier_code')
    if field_value_exist:
        # Field has a value
        return "Field has a value"
    else:
        field_name = 'existing_supplier_code'
        field_value = doc.name[3:]
        frappe.db.set_value('Farmer List', doc.name, field_name, field_value)
        
        # def reload_doc():
        #     frappe.get_doc('Farmer List', doc.name).reload()
        
        # frappe.enqueue(reload_doc, queue='default', timeout=1)
        return "Field value updated"
 
@frappe.whitelist()
def role():
    list=frappe.get_all("Has Role",filters={"parenttype": "User", "parent": frappe.session.user},fields=["role"],)
    if list:
        return list[0].role


  
	# @frappe.whitelist()
	# def aadhaar_number_vali(self):
	# 	if len(str(self.aadhaar_number)) != 12 and len(str(self.aadhaar_number)) != 0 :
	# 		frappe.throw("Input number must be exactly 12 digits.")
			
      
		# frappe.msgprint(doc[0].name)frappe.delete_doc("Crop Sampling", c.name)
		# frappe.msgprint(moc[0].name)
		# frappe.msgprint(qoc[0].name)




	# @frappe.whitelist()
	# def update_docs(self):
	# 	frappe.db.set_value("Supplier", self.name, "supplier_type", self.supplier_type)
	# 	frappe.db.set_value("Supplier", self.name, "supplier_name", self.supplier_name)
	# 	frappe.db.set_value("Supplier", self.name, "supplier_group", self.supplier_group)
	# 	frappe.db.set_value("Supplier", self.name, "address_line1", self.village)
	# 	frappe.db.set_value("Supplier", self.name, "address_line2", self.taluka)
	# 	frappe.db.set_value("Supplier", self.name, "city", self.circle_office)
	# 	frappe.db.set_value("Supplier", self.name, "state", self.state)
	# 	frappe.db.set_value("Supplier", self.name, "country", "India")
	# 	frappe.db.set_value("Supplier", self.name, "pincode", self.pin_code)

	# 	frappe.db.set_value("Customer", self.name, "customer_name", self.supplier_name)
	# 	frappe.db.set_value("Customer", self.name, "customer_group", self.supplier_group)
	# 	frappe.db.set_value("Customer", self.name, "territory", "India")
	# 	frappe.db.set_value("Customer", self.name, "address_line1", self.village)
	# 	frappe.db.set_value("Customer", self.name, "address_line2", self.taluka)
	# 	frappe.db.set_value("Customer", self.name, "city", self.circle_office)
	# 	frappe.db.set_value("Customer", self.name, "state", self.state)
	# 	frappe.db.set_value("Customer", self.name, "country", "India")
	# 	frappe.db.set_value("Customer", self.name, "pincode", self.pin_code)
		
		
@frappe.whitelist()
def filterfarmerlist(village, name):
    try:
        village = str(village) + '%'
        name = '%' + str(name) + '%'
        data=[]
        data = frappe.db.sql(
            '''SELECT supplier_name, village, name, circle_office, existing_supplier_code, workflow_state
               FROM `tabFarmer List`
               WHERE village LIKE %s
               AND supplier_name LIKE %s 
               LIMIT 20
            ''', (village, name), as_dict=True)

        if data is not None:
            return data
        else:
            return []
    except Exception as e:
        frappe.log_error("Error in filterfarmerlist: " + str(e))
        return []


	
