# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AdvanceRequest(Document):
	@frappe.whitelist()
	def fetch_amount(self):
		doc1 = frappe.get_all('Season Wise Advance Item', 
				# filters={'season': self.season,'plant':self.plant,'vehicle_type':self.vehicle_type,'gang_type':self.gang_type},
				fields=["name", "advance","gang_type","vehicle_type","plant","season"])
		for n in doc1:
			for d in self.items:
				if n.gang_type == d.gang and n.vehicle_type == d.vehicle_type:
					if n.vehicle_type == 'BULLOCK CART':
						d.sacn_limit = n.advance * d.vehicle_cart
						
					else:
						d.sacn_limit = n.advance
					
					doc_if_present= frappe.get_all("Advance Request item",
                                            filters={"code_no": d.code_no},
                                            fields={"sanction_amount", "name","parent"},)
					if(doc_if_present):
						if (doc_if_present[0].parent) != self.name:
							if (doc_if_present[0].sanction_amount):
								d.prv_scan_amt= (doc_if_present[0].sanction_amount)
        
	@frappe.whitelist()
	def paid_amount(self):
		total = 0.0
		for h in self.items:
			if h.per_cart_amount >0 and h.vehicle_cart>0:
				h.sanction_amount = h.per_cart_amount * h.vehicle_cart
				total = h.sacn_limit - h.sanction_amount - h.prv_scan_amt
				h.bal_amt = total
			
			
   
	@frappe.whitelist()
	def before_save(self):
		# self.auto_100_row_add_in_child_table()
  
		if self.items:
			for k in self.items:
				# k.prv_scan_amt  = k.prv_scan_amt  + k.sanction_amount
				if k.sacn_limit  < k.prv_scan_amt :
					frappe.throw("Exceeding the Limit ......")
						
     
     
	# @frappe.whitelist()
	# def amount(self):
	# 	pass
     
		# doc = frappe.get_all('H and T Contract',
        #                filters={'season': self.season,'plant':self.plant,'vehicle_type':self.vehicle_type,'gang_type':self.gang_type},
        #                fields=["name","h_and_t_group","total_vehicle","circle","gang_type","vehicle_type","plant","season","transporter_name","group_leader_name"])
		# for m in doc:
		# 	if not any(d.get("code_no") == m['name'] for d in self.items):
		# 		self.append("items", {
		# 				"code_no": m["name"],
		# 				"name1": m["transporter_name"],
		# 				"circle": m["circle"],
		# 				"group_leader": m["group_leader_name"],
		# 				"gang": m["gang_type"],
		# 				"vehicle_cart": m["total_vehicle"],
		# 				"vehicle_type": m["vehicle_type"],
		# 				"gang": m["gang_type"],
		# 			})
		# doc1 = frappe.get_all('Season Wise Advance Item', 
        #                 filters={'season': self.season,'plant':self.plant,'vehicle_type':self.vehicle_type,'gang_type':self.gang_type},
        #                 fields=["name", "advance","gang_type","vehicle_type","plant","season"])
		# for n in doc1:
		# 	for d in self.items:
		# 		if n.gang_type == d.gang and n.vehicle_type == d.vehicle_type:
		# 			d.sacn_limit = n.advance
		# 			frappe.msgprint(str(n.advance))

    

    
    
    
	# @frappe.whitelist()
	# def auto_100_row_add_in_child_table(self):
	# 	if self.items:
	# 		for _ in range(50):
	# 			self.append(
	# 						"items",
	# 						{
	# 							"bal_amt": "",
							
	# 						},
	# 					)
			
    
    

	
	# @frappe.whitelist()
	# def fetch_amount(self):
	# 	doc = frappe.get_all('Season Wise Advance Item', filters={'season': self.season,'plant':self.plant,'vehicle_type':self.vehicle_type,'gang_type':self.gang_type},fields=["name", "advance","gang_type","vehicle_type","plant","season"])
	# 	for s in doc:
	# 		self.amount_limit = s.advance
		
	# # @frappe.whitelist()
	# # def paid_amount(self):
	# 	# total=0.0
	# 	# doc=frappe.db.get_list('Advance Request', filters={'contractor_name': self.contractor_name},fields={'name','paid_amount_till_today'})
	# 	# for d in doc:
	# 	# 	doc1=frappe.get_doc('Advance Request',d.name)
	# 	# 	total=total+doc1.paid_amount_till_today
	# 	# self.paid_amount_till_today=total
	# 	# frappe.msgprint(str(total))
  
	# @frappe.whitelist()
	# def before_save(self):
	# 	if self.amount_limit < self.amount_to_be_paid+self.paid_amount_till_today:
	# 		frappe.throw("Exceeding the Limit ......")
      
      
      
	# # 		self.limit_amount = s.advance
	# # 	total=0.0
	# # 	doc=frappe.db.get_list('Advance Request', filters={'contractor_name': self.contractor_name},fields={'name','advance_amount'})
	# # 	for d in doc:
	# # 		doc1=frappe.get_doc('Advance Request',d.name)
	# # 		total=total+doc1.advance_amount
	# # 	self.paid_amount=total
  
  
	# # def before_save(self):
	# # 	if self.limit_amount < self.advance_amount+self.paid_amount:
	# # 		frappe.throw("Exceeding the Limit ......")
		
