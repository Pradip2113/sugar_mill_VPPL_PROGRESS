# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DieselSale(Document):
	
	@frappe.whitelist()
	def salesinvoice(self):
		debet_account_name,cost_center=self.get_debet_account()
		if not debet_account_name:
			frappe.throw("Please add the debet account in Diesel Sale Setting in Branch")
		if not cost_center:
			frappe.throw("Please add the cost centre in Diesel Sale Setting in Branch")
		doc = frappe.new_doc('Sales Invoice')
		doc.customer =self.party_name 
		doc.sale_type="Diesel Sale"
		doc.naming_series='ACC-SINV-.YYYY.-'
		doc.posting_date=self.date
		doc.branch=self.plant
		doc.due_date=self.date
		doc.debit_to=debet_account_name
		doc.cost_center=cost_center
		for i in self.get("diseal_sale_item"):
			doc.append(
					"items",
					{
						"item_code": i.item_code,
						"qty": i.qty,
						"rate": i.rate,
						"amount": ((i.amount)),
					},)
		doc.run_method("set_missing_values")
		doc.run_method("calculate_taxes_and_totals")
		doc.insert()
		doc.diesel_sale_ref=self.name
		doc.docstatus=1
		doc.save()
		
  
	@frappe.whitelist()
	def get_item_rate(self,item_code,index):
		item_price = frappe.get_all(
			doctype="Item Price",
			filters={"item_code": item_code, "selling": True},
			fields=["price_list_rate"],
			order_by="creation desc",
		)
		if item_price:
			self.get("diseal_sale_item")[index-1].rate=float(item_price[0]["price_list_rate"])
			self.get("diseal_sale_item")[index-1].amount=self.get("diseal_sale_item")[index-1].rate*self.get("diseal_sale_item")[index-1].qty
		else:
			self.get("diseal_sale_item")[index-1].rate=0

	@frappe.whitelist()
	def get_debet_account(self):
		debet_account_name=""
		cost_center=""
		debet_account_name,cost_center = frappe.get_value(
			"Branch",
			{"name": self.plant},
			["debit_to_","cost_center_for_diesel"]
		)
		return debet_account_name,cost_center

	@frappe.whitelist()
	def get_customer_name(self):
		type_code=""
		type_name=""
		if(self.harvester):
			type_code="harvester_code"
			type_name="harvester_name"
		if(self.transporter):
			type_code="transporter_code"
			type_name="transporter_name"
		if(type_code=="" or type_code==""):
			frappe.throw("Please select the type of Customer")
		customer_id,customer_name=frappe.get_value("H and T Contract",{"name":self.contract_id},[type_code,type_name])
		self.party_name=customer_id
		self.customer_name=customer_name
		diesel_sale_item = frappe.get_value(
			"Branch",
			{"name": self.plant},
			"diesel_sale_item"
		)
		if(not diesel_sale_item):
			frappe.throw("Please set the diesel item in Branch")
		self.get_diesel_info()
		self.append("diseal_sale_item",{
			"item_code":diesel_sale_item,
			"qty":self.total_diesel_allocation_remaining
		})
		self.get_item_rate(diesel_sale_item,0)
		

	@frappe.whitelist()
	def get_diesel_info(self):
		ton_value_on_diesel_allocate, diesel_allocation_value_har, diesel_allocation_per_km = frappe.get_value("Branch",{"name":self.plant},["total_ton_value_from_which_diesel_will_allocate", "diesel_allocation_amount_per_ton", "diesel_allocation_amount_per_km"])
		if(not ton_value_on_diesel_allocate):
			frappe.throw("Please Enter Total TON Value From Which Diesel Will Allocate in Branch")
		if(not diesel_allocation_value_har):
			frappe.throw("Please Enter How Much Diesel Will Allocate (in Liter) in Branch")
		if(not diesel_allocation_per_km):
			frappe.throw("Please Enter Diesel Allocation Per KM (in Liter) in Branch")
		if(self.transporter):
			doc=frappe.get_doc("H and T Contract",self.contract_id)
			child_table=doc.get("diesel_calculation")
			if(child_table):
				for i in child_table:
					if(len(child_table)>0 and i.customer_type=='Transporter'):
						self.total_distance_in_km=i.remaining/diesel_allocation_per_km
						self.total_diesel_allocated=i.total_sold
						self.total_allocated=self.total_distance_in_km*diesel_allocation_per_km
						self.total_diesel_allocation_remaining=i.remaining
						break
 
		if(self.harvester):
			doc=frappe.get_doc("H and T Contract",self.contract_id)
			child_table=doc.get("diesel_calculation")
			for i in child_table:
				if(len(child_table)>0 and i.customer_type=='Harvester'):
					liter_value_per_ton=diesel_allocation_value_har/ton_value_on_diesel_allocate
					self.total__weight_in_ton=i.remaining/liter_value_per_ton
					self.total_diesel_allocated=i.total_sold
					self.total_allocated=self.total__weight_in_ton*liter_value_per_ton
					self.total_diesel_allocation_remaining=i.remaining
					break
 
	@frappe.whitelist()
	def set_diesel_sale_value(self):
		ton_value_on_diesel_allocate, diesel_allocation_value_har, diesel_allocation_per_km = frappe.get_value("Branch",{"name":self.plant},["total_ton_value_from_which_diesel_will_allocate", "diesel_allocation_amount_per_ton", "diesel_allocation_amount_per_km"])
		if(not ton_value_on_diesel_allocate):
			frappe.throw("Please Enter Total TON Value From Which Diesel Will Allocate in Branch")
		if(not diesel_allocation_value_har):
			frappe.throw("Please Enter How Much Diesel Will Allocate (in Liter) in Branch")
		if(not diesel_allocation_per_km):
			frappe.throw("Please Enter Diesel Allocation Per KM (in Liter) in Branch")
		allocated_value=0
		for i in self.get("diseal_sale_item"):
			allocated_value=i.qty
			break
		if(self.transporter):
			doc=frappe.get_doc("H and T Contract",self.contract_id)
			child_table=doc.get("diesel_calculation")
			if(child_table):
				for i in child_table:
					if(len(child_table)>0 and i.customer_type=='Transporter'):
						i.total_sold=i.total_sold+allocated_value
						i.total_lapse=i.total_lapse+(self.total_diesel_allocation_remaining-allocated_value)
						i.remaining=0
				doc.save()
		if(self.harvester):
			doc=frappe.get_doc("H and T Contract",self.contract_id)
			child_table=doc.get("diesel_calculation")
			if(child_table):
				for i in child_table:
					if(len(child_table)>0 and i.customer_type=='Harvester'):
						i.total_sold=i.total_sold+allocated_value
						i.remaining=i.remaining-(allocated_value)
				doc.save()
		

	@frappe.whitelist()
	def update_set_diesel_sale_value(self):
		ton_value_on_diesel_allocate, diesel_allocation_value_har, diesel_allocation_per_km = frappe.get_value("Branch",{"name":self.plant},["total_ton_value_from_which_diesel_will_allocate", "diesel_allocation_amount_per_ton", "diesel_allocation_amount_per_km"])
		if(not ton_value_on_diesel_allocate):
			frappe.throw("Please Enter Total TON Value From Which Diesel Will Allocate in Branch")
		if(not diesel_allocation_value_har):
			frappe.throw("Please Enter How Much Diesel Will Allocate (in Liter) in Branch")
		if(not diesel_allocation_per_km):
			frappe.throw("Please Enter Diesel Allocation Per KM (in Liter) in Branch")
		allocated_value=0
		for i in self.get("diseal_sale_item"):
			allocated_value=i.qty
			break
		if(self.transporter):
			doc=frappe.get_doc("H and T Contract",self.contract_id)
			child_table=doc.get("diesel_calculation")
			if(child_table):
				for i in child_table:
					if(len(child_table)>0 and i.customer_type=='Transporter'):
						i.total_sold=i.total_sold-allocated_value
						i.remaining=i.remaining+self.total_diesel_allocation_remaining
						i.total_lapse=i.total_lapse-(self.total_diesel_allocation_remaining-allocated_value)
				doc.save()
		
	
		if(self.harvester):
			doc=frappe.get_doc("H and T Contract",self.contract_id)
			child_table=doc.get("diesel_calculation")
			if(child_table):
				for i in child_table:
					if(len(child_table)>0 and i.customer_type=='Harvester'):
						i.total_sold=i.total_sold-allocated_value
						i.remaining=i.remaining+(allocated_value)				
				doc.save()


	@frappe.whitelist()
	def get_contract_list(self):
		ton_value_on_diesel_allocate, diesel_allocation_value_har = frappe.get_value("Branch",{"name":self.plant},["total_ton_value_from_which_diesel_will_allocate", "diesel_allocation_amount_per_ton"])
		if(not ton_value_on_diesel_allocate):
			frappe.throw("Please Enter Total TON Value From Which Diesel Will Allocate in Branch")
		if(not diesel_allocation_value_har):
			frappe.throw("Please Enter How Much Diesel Will Allocate (in Liter) in Branch")
		contract_li=[]
		if(self.transporter):
			doc=frappe.get_all("Diesel Sale Calculation",{"customer_type":"Transporter","docstatus":1},["remaining","parent"])
			for i in doc:
				if(i.remaining>0):
					contract_li.append(i.parent)
		if(self.harvester):
			doc=frappe.get_all("Diesel Sale Calculation",{"customer_type":"Harvester","docstatus":1},["total_weight","parent","remaining"])
			for i in doc:
				if(i.total_weight>=100 and i.remaining>0):
					contract_li.append(i.parent)
		return contract_li


	def before_save(self):
		allocated_value=0
		for i in self.get("diseal_sale_item"):
			allocated_value=i.qty
			break
		if(allocated_value>self.total_diesel_allocation_remaining or allocated_value>200):
			frappe.throw("You can not sale the diesel more that total Diesel Allocation or greater than 200 liter")
   
   
	def before_submit(self):
		self.salesinvoice()
		self.set_diesel_sale_value()

  
	def on_cancel(self):
		self.update_set_diesel_sale_value()
  
				
				