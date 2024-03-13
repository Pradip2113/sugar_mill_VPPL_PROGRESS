# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import get_datetime

class TripSheet(Document):
	# @frappe.whitelist()
	# def hdata(self):
	# 	doc = frappe.get_all('H and T Contract', filters={'name': self.transporter_code}, fields={'name','gang_type','vehicle_no','transporter_code','harvester_code','transporter_name','harvester_name','trolly_1','trolly_2','total_vehicle','vehicle_type'})
	# 	for s in doc:
	# 		# self.transporter_name = s.transporter_name
	# 		# self.transporter = s.transporter_code
	# 		# self.harvester_code = s.harvester_code
	# 		# self.harvester_name = s.harvester_name
	# 		self.vehicle_type = s.vehicle_type
	# 		self.vehicle_number = s.vehicle_no
	# 		self.tolly_1 = s.trolly_1
	# 		self.tolly_2 = s.trolly_2
	# 		# self.gang_type = s.gang_type
   
	@frappe.whitelist()
	def carthdata(self):
		vehireg = frappe.get_all('Vehicle Registration item',filters={'cart_no': self.cartno}, fields={'parent','driver_name','cart_no','season'})
		for m in vehireg:
			htget = frappe.get_all('H and T Contract', filters={'name': m.parent}, fields={'name','gang_type','vehicle_no','circle','old_no','new_h_t_no','transporter_name','harvester_code','harvester_name','vehicle_type','transporter_code'})
			for j in htget:
				self.old_transporter_code=j.old_no
				self.vehicle_type=j.vehicle_type
				self.transporter_name=j.transporter_name
				self.transporter_code=j.name
				self.transporter = j.transporter_code
				self.harvesting_code__ht=j.name 
				self.harvester_code_old=j.old_no
				self.harvester_name_h=j.harvester_name
				self.gang_type = j.gang_type
				self.harvester_code = j.harvester_code
				self.harvester_name = j.harvester_name	
		if (self.cartno == 0 or self.cartno == ""):
			self.transporter_code = None
			self.vehicle_type = None
			self.transporter_name = None
			self.transporter = None
			self.harvesting_code__ht = None
			self.harvester_name_h = None
		
				
	def before_save(self):
		doc=frappe.db.get_list("Branch",filters={"branch" : self.branch},
											fields=["name","trip_sheet_no"])
		if int(self.tripsheet_no) == 0:
			trip_sheet_no_value = float(doc[0].get("trip_sheet_no"))
			self.tripsheet_no = int(trip_sheet_no_value)
			frappe.db.set_value("Branch", doc[0].get("name"), "trip_sheet_no", self.tripsheet_no)

   
		datetime_value = get_datetime(self.creation)
		value = frappe.get_value('H and T Contract',self.transporter_code,'last_cane_weight_entry')
		if value:
			branch_setting_time = get_datetime(frappe.get_value('Branch',self.branch,'trip_sheet_time'))
			if( datetime_value-value)<=(branch_setting_time):
				frappe.throw(f'Your are not allow to create "Trip Sheet" because {self.transporter_code} have not complited {branch_setting_time}  time set by agricultural Department come after {branch_setting_time-(datetime_value-value)} time')


	@frappe.whitelist()
	def get_transporter_info(self):
		doc=frappe.get_doc("H and T Contract",self.transporter_code)
		self.old_transporter_code=doc.old_no
		self.vehicle_type=doc.vehicle_type
		self.transporter_name=doc.transporter_name

		
		
  
@frappe.whitelist()
def cartlist(cartno):
    vehireg = frappe.get_all('Vehicle Registration item', filters={'cart_no': cartno}, fields={'parent','driver_name','cart_no','season'})

    for m in vehireg:
        htget = frappe.get_all('H and T Contract', filters={'name': m.parent,'vehicle_type':"BULLOCK CART"}, fields={'name','gang_type','circle','old_no','transporter_name','harvester_code','harvester_name','vehicle_type','transporter_code'})
        
        for j in htget:
            cartinfo = {
                "name":j.name,
                "h_t_no":j.old_no,
                "transporter": j.transporter_code,
                "transporter_name": j.transporter_name,
                "transporter_code": j.name, 
                "harvester": j.harvester_code,
                "harvester_code":j.name,
                # "harvester_vendor_code":frappe.get_value("Farmer List",j.harvester_code,"existing_supplier_code"),
                "harvester_name": j.harvester_name,
                "vehicle_type": j.vehicle_type,
                "gang_type": j.gang_type
            }
            
            # cartinfo_list.append(cartinfo)

    return cartinfo
