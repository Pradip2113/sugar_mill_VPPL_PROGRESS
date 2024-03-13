# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HandTContract(Document):
	@frappe.whitelist()
	def on_submit(self):
		if self.vehicle_type == "BULLOCK CART" or self.vehicle_type == "TRACTOR CART" or self.vehicle_type == "TRUCK":
#   ----------------------------------------------------------------------------------------
			moc = frappe.new_doc("Vehicle Registration")
			moc.h_and_t_contract = self.name
			moc.vehicle_number = self.vehicle_no
			moc.gang_type = self.gang_type
			moc.contractor_name = self.transporter_name
			moc.vehicle_type = self.vehicle_type
			moc.total_numbers_of_vehicle = self.total_vehicle
			moc.transporter_code = self.transporter_code
			moc.ht_no = self.old_no
			moc.season = self.season
			moc.trolly__1 = self.trolly_1
			moc.trolly_2 = self.trolly_2

			doc=frappe.db.get_list("Branch",filters={"branch" : self.plant},fields=["name","cart_no"])
			pre_cart_no=int(float(doc[0].get("cart_no")))
			if self.vehicle_type == 'BULLOCK CART':
				for i in range(pre_cart_no+1,int(self.total_vehicle)+pre_cart_no+1):
					vehicle_detail = moc.append("vehicle_details_tab", {})
					vehicle_detail.cart_no=i if self.vehicle_type != 'TRACTOR CART' else None
					vehicle_detail.trolly_1 = self.trolly_1
					vehicle_detail.trolly_2 = self.trolly_2
					vehicle_detail.driver_name = self.transporter_code
					vehicle_detail.season = self.season
					vehicle_detail.h_t_cont = self.name
					vehicle_detail.harvester_code = self.harvester_code
			else:
				vehicle_detail = moc.append("vehicle_details_tab", {})
				vehicle_detail.cart_no=i if self.vehicle_type != 'TRACTOR CART' else None
				vehicle_detail.trolly_1 = self.trolly_1
				vehicle_detail.trolly_2 = self.trolly_2
				vehicle_detail.driver_name = self.transporter_code
				vehicle_detail.season = self.season
				vehicle_detail.h_t_cont = self.name
				vehicle_detail.harvester_code = self.harvester_code
				
			moc.save()
			if self.vehicle_type != 'TRACTOR CART':
				frappe.db.set_value("Branch",doc[0].get("name"),"cart_no",int(self.total_vehicle)+pre_cart_no)
		frappe.set_value("H T Master", self.old_no , "hts" , self.season)

	@frappe.whitelist()
	def before_cancel(self):
     
		doc = frappe.get_all('H T Master', filters={'name':self.old_no}, fields=["name","hts"])
		for j in doc:
			if(self.season == j.hts):
				frappe.set_value("H T Master", j.name , "hts" , None)
				
 
#  -------------------------------------------------------------------------------------------
	@frappe.whitelist()
	def on_update_after_submit(self):
		if self.vehicle_type == "BULLOCK CART" or self.vehicle_type == "TRACTOR CART" or self.vehicle_type == "TRUCK":
			frappe.db.set_value("Vehicle Registration", str(self.season)+"-"+str(self.name), "contractor_name",self.h_and_t_group)
			frappe.db.set_value("Vehicle Registration",str(self.season)+"-"+str(self.name), "transporter_code",self.transporter_code)
			frappe.db.set_value("Vehicle Registration",str(self.season)+"-"+str(self.name), "vehicle_number",self.vehicle_no)
			# frappe.db.set_value("Vehicle Registration",str(self.season)+"-"+str(self.name), "contractor_name",self.harvester_code)
			frappe.db.set_value("Vehicle Registration",str(self.season)+"-"+str(self.name), "vehicle_type",self.vehicle_type)
			frappe.db.set_value("Vehicle Registration",str(self.season)+"-"+str(self.name), "total_numbers_of_vehicle",self.total_vehicle)
			frappe.db.set_value("Vehicle Registration",str(self.season)+"-"+str(self.name), "transporter_code",self.transporter_code)
			frappe.db.set_value("Vehicle Registration",str(self.season)+"-"+str(self.name), "season",self.season)
			self.changing_the_no_of_chart_after_updating()
	@frappe.whitelist()
	def eeeuu(self):
		if self.vehicle_type == "BULLOCK CART" or self.vehicle_type == "TRACTOR CART":
			chil = frappe.get_all("Vehicle Registration item", fields=["name","cart_no"])
			for m in chil:
				frappe.db.set_value("Vehicle Registration item", m.name, "cart_no",m.name)
   
	@frappe.whitelist()
	def changing_the_no_of_chart_after_updating(self):
		if self.vehicle_type == "BULLOCK CART" or self.vehicle_type == "TRACTOR CART" or self.vehicle_type == "TRUCK":
			doc = frappe.get_all('Vehicle Registration item', filters={'parent': str(self.season) + "-" + str(self.name)}, fields=["name", "idx"], order_by="name DESC")
			no_doc_remove =len(doc)-int(self.total_vehicle)
			no_doc_insert = int(self.total_vehicle) - len(doc)
			if no_doc_remove>0:
				moc = frappe.get_all('Vehicle Registration item', filters={'parent': str(self.season) + "-" + str(self.name)}, fields=["name", "idx"], order_by="name DESC", limit=no_doc_remove)
				for m in moc:
					frappe.delete_doc('Vehicle Registration item', m.name)

			if no_doc_insert>0:
				for i in range(int(no_doc_insert)):
					new_doc = frappe.new_doc('Vehicle Registration item')
					new_doc.parent = str(self.season) + "-" + str(self.name)
					new_doc.parentfield = "vehicle_details_tab"
					new_doc.parenttype = "Vehicle Registration"
					new_doc.idx = len(doc)+i+1
					new_doc.insert(ignore_permissions=True)
		
	@frappe.whitelist()    
	def oldhandtcode(self):
			doc1=frappe.db.get_list('H T Master',
                           filters={'name':self.old_no},
                           fields={'name','plant','company_name','contract_type','advance','circle','transporter_code','harvester_code','village_tra','transporter_name',
                                   'harvester_name','transportor_commission','harvester_retantion_','tds','hts'})
			for d in doc1:
				if self.season == d.hts:
					frappe.msgprint("This Contract Already Registor")
					self.company_name = ""
					self.contract_type = ""
					self.advance =""
					self.circle = ""
					self.transporter_code = ""
					self.harvester_code = ""
					self.village_tra = ""
					self.transporter_name = ""
					self.harvester_name = ""
					self.transportor_commission = ""
					self.harvester_retantion_ = ""
					self.tds = ""
				else:
				# self.plant = d.plant,
					self.company_name = d.company_name
					self.contract_type = d.contract_type
					self.advance = d.advance
					self.circle = d.circle
					self.transporter_code = d.transporter_code
					self.harvester_code = d.harvester_code
					self.village_tra = d.village_tra
					self.transporter_name = d.transporter_name
					self.harvester_name = d.harvester_name
					self.transportor_commission = d.transportor_commission
					self.harvester_retantion_ = d.harvester_retantion_
					self.tds = d.tds
			
	@frappe.whitelist()    
	def get_bank_details(self):
		self.transporter_info(self.transporter_code,"Transporter")
		entity_types = [self.transporter_code]
		for i in entity_types:
			doc =frappe.db.get_list('Farmer List', filters={'name':i}, fields={'name'})
			for index in doc:
				chart_table = frappe.get_all("Bank Details", filters={"parent": index['name']},fields=["farmer","bank_and_branch","harvester","transporter","branch","branchifsc_code","account_number","status","is_active","created_datename"])
				for d in chart_table:
					self.append(
						"bank_details",
						{
							"farmer": d.farmer,
							"harvester": d.harvester,
							"transporter": d.transporter,
							"branch": d.branch,
							"bank_name": d.bank_and_branch,
							"branchifsc_code": d.branchifsc_code,
							"account_number": d.account_number,
							"status": d.status,
							"is_active": d.is_active,
							"created_datename": d.created_datename
						}
					)
    
    
	@frappe.whitelist()
	def transporter_info(self,code,type):
		if code:
			doc=frappe.db.get_all('Farmer List', filters={'name':code}, fields={'name',"supplier_name"})
			for i in doc:
				self.append(
						"diesel_calculation",
						{
							"diesel_id": i.name,
							"diesel_owner_is":type,
							"diesel_owner": i.supplier_name,
						}
					)
				break
        
    
		

				

