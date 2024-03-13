# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

from datetime import time
import struct
import time
import frappe
from frappe.model.document import Document
import string    
import random
import socket


class CaneInwardSlip(Document):
# Sync Data
	def before_save(self):
		self.set_value_in_h_and_t_contract()
		self.hero()
		self.reset_counter()
		self.set_counter()
		if self.branch == "Nagpur":
			ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))  
			self.uin='CIS-N-'+ran
			self.name=self.uin
#---------------------------------


	@frappe.whitelist()
	def set_counter(self):
		exist_counter_value= frappe.get_value("Branch",self.branch,"cane_slip_no")
		if exist_counter_value:
			self.slip_noday = int(exist_counter_value) + 1
			frappe.set_value("Branch",self.branch,"cane_slip_no",self.slip_noday)
		
	
	@frappe.whitelist()
	def reset_counter(self):
		frappe.msgprint(str(self.time))
		frappe.msgprint(str(self.branch))
		frappe.msgprint(str(self.date))
		if self.time and self.branch and self.date:
			doc = frappe.get_all("Cane Inward Slip", filters= {"time": ["<", self.time], "time" : [">",frappe.get_value("Branch", self.branch, "set_shift_time")] ,"date":self.date}, fields=["slip_noday"])
			frappe.msgprint(str(doc))
			if not doc:
				frappe.db.set_value("Branch", self.branch, "cane_slip_no", "0")


	@frappe.whitelist()
	def set_value_in_h_and_t_contract(self):
		frappe.set_value('H and T Contract',self.transporter_code_ht,'last_cane_slip_entry',self.creation)

	@frappe.whitelist()
	def hdata(self):
		doc = frappe.get_all('Trip Sheet', filters={'name': self.plot_no}, fields={'name','transporter_code','transporter_name','transporter','route_name','route','distance'})
		for s in doc:
			self.transporter_code = s.transporter_code
			self.transporter_name = s.transporter_name
			self.transporter = s.transporter
			self.route_name = s.route_name
			self.route = s.route
			self.distance = s.distance
		
  
	def send_to_data(self, data):
		# Input validation
		if not self.ip_of_indicator or not self.port_no_of_indicator.isdigit():
			frappe.throw("Invalid server IP or port number.")
		
		server_ip = self.ip_of_indicator
		server_port = int(self.port_no_of_indicator)
		timeout = 10  # Set a 10-second timeout for the socket connection (adjust as needed)

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
			client_socket.settimeout(timeout)  # Set the socket timeout
			
			try:
				client_socket.connect((server_ip, server_port))
				num_str = f"{data}\r\n"
				client_socket.send(num_str.encode('utf-8'))
			except ConnectionRefusedError:
				frappe.throw("Connection refused. Make sure the server is running.")
			except TimeoutError:
				frappe.throw("Connection attempt timed out. Check the server and network connection.")
			except Exception as e:
				frappe.throw(f"An error occurred: {e}")
			else:
				print("Data sent successfully.")
		
	@frappe.whitelist()
	def call_indicator(self):
		self.send_to_data(3)

	@frappe.whitelist()
	def vivo(self):
		doc = frappe.get_all('H and T Contract', filters={'name': self.transporter_code}, fields={'name','har_vendor_code','new_h_t_no','vehicle_no','transporter_code','harvester_code','transporter_name','harvester_name','trolly_1','trolly_2','total_vehicle','vehicle_type','gang_type'})
		for s in doc:
			self.transporter_name = s.transporter_name
			self.harvester_code = s.harvester_code
			self.transporter_code_ht = s.name
			self.harvester_code_ht = s.har_vendor_code
			self.harvester_name = s.harvester_name
			self.vehicle_type = s.vehicle_type
			self.vehicle_number = s.vehicle_no
			self.tolly_1 = s.trolly_1
			self.tolly_2 = s.trolly_2
			self.gang_type = s.gang_type

	@frappe.whitelist()
	def after_save(self):
		self.send_to_data(3)
		doc1 = frappe.get_all('Branch',filters={'name':self.branch},fields=["name", "token_number",])
		for n in doc1:
			n.token_number = n.token_number + 1
			frappe.db.set_value("Branch", n.name, "token_number",n.token_number)
			
	# @frappe.whitelist()
	# def get_reading(self):
	# 	user=  frappe.get_all("RFID Master Setting",
    #                         fields=["rfid_machine", "idx", "date"],
    #                         filters={'rfid_operator_id': frappe.session.user},
    #                         order_by="date desc",
    #                         limit=1)
	# 	# =frappe.db.get_list("RFID Master Setting",  filters={'rfid_operator_id': frappe.session.user},fields=['rfid_machine'],)
	# 	rfid_reading=frappe.get_doc("Rfid tag Reading","rfid-tag-reading")
	# 	temp1=rfid_reading.rfid1_status
	# 	temp2=rfid_reading.rfid2_status
	# 	temp3=rfid_reading.rfid3_status
	# 	frappe.msgprint(str(user[0].rfid_machine))
	# 	if temp1=="Connected.":
	# 		self.rfid_tag=rfid_reading.rfid_1
	# 	elif temp2=="Connected.":
	# 		self.rfid_tag=rfid_reading.rfid_2
	# 	elif temp3=="Connected.":
	# 		self.rfid_tag=rfid_reading.rfid_3

	@frappe.whitelist()
	def get_reading(self):
		frappe.msgprint('fkdj')
		if not self.transporter_code_ht:
			# Get the most recent record with 'rfid_machine' as 'RFID 2'
			frappe.msgprint('abc')
			user = frappe.get_all(
				"RFID Master Setting",
				fields=["rfid_machine", "idx", "date"],
				filters={
					'rfid_operator_id': frappe.session.user
				},
				order_by='date desc',
				limit=1
			)
			if not user:
				frappe.throw("No any RFID is found for the current user.")
				return
			frappe.msgprint(str(user))
			# Access the 'rfid_machine' and 'date' fields from the recent record
			rfid_machine = user[0].rfid_machine
			# Get the "Rfid tag Reading" document
			rfid_reading = frappe.get_doc("Rfid tag Reading", "rfid-tag-reading")

			# Get the status of RFID readers
			temp1 = rfid_reading.rfid1_status
			temp2 = rfid_reading.rfid2_status
			temp3 = rfid_reading.rfid3_status

			# Display the 'rfid_machine' value and its status
			# frappe.msgprint(f"RFID Machine: {rfid_machine}")
			frappe.msgprint(str(rfid_reading))
			# Assign the appropriate value to the 'rfid_tag' variable based on the status of RFID readers
			if temp1 == "Connected." and rfid_machine == 'RFID 1':
				self.rfid_tag = rfid_reading.rfid_1
				self.ip_of_indicator=rfid_reading.ip_of_indicator1
				self.port_no_of_indicator=rfid_reading.port_number_of_indicator1
			elif temp2 == "Connected." and rfid_machine == 'RFID 2':
				self.rfid_tag = rfid_reading.rfid_2
				self.ip_of_indicator=rfid_reading.ip_of_indicator2
				self.port_no_of_indicator=rfid_reading.port_number_of_indicator2
				# frappe.msgprint(str(self.port_no_of_indicator))
			elif temp3 == "Connected." and rfid_machine == 'RFID 3':
				self.rfid_tag = rfid_reading.rfid_3
				self.ip_of_indicator=rfid_reading.ip_of_indicator3
				self.port_no_of_indicator=rfid_reading.port_number_of_indicator3

			
			doc1 = frappe.get_all("H and T Contract", fields=["name","new_h_t_no","trolly_1","trolly_2","gang_type","vehicle_no","transporter_name","vehicle_type","harvester_code","harvester_name", "rfid_tag","transporter_name"], filters={"rfid_tag": self.rfid_tag})
			found_rfid_tag = False
			frappe.msgprint(str(doc1))
			for g in doc1:
				if g.rfid_tag == self.rfid_tag:
					self.rfid_tag=g.rfid_tag
					self.transporter_code=g.new_h_t_no
					self.transporter_code_ht=g.name
					self.transporter_name=g.transporter_name
					self.harvester_code_ht = g.harvester_code
					self.harvester_name = g.harvester_name
					self.vehicle_type = g.vehicle_type
					self.vehicle_number = g.vehicle_no
					self.tolly_1 = g.trolly_1
					self.tolly_2 = g.trolly_2
					self.gang_type = g.gang_type
					# frappe.msgprint(f"RFID Tag matches with Transporter {self.transporter_name}")
					found_rfid_tag = True
					self.send_to_data(2)
					break

			if not found_rfid_tag:
				message = "RFID Tag does not match with any Transporter. Assgin token to transportar "
				message += '<br> <a href="/app/list/Tag Reader">Tag Reader</a>'
				frappe.throw(message)
				self.send_to_data(4)
		

    
	@frappe.whitelist()
	def get_infodata(self):
		if not self.transporter_code_ht:
			# Get the most recent record with 'rfid_machine' as 'RFID 2'
			# frappe.msgprint('abc')
			user = frappe.get_all(
				"RFID Master Setting",
				fields=["rfid_machine", "idx", "date"],
				filters={
					'rfid_operator_id': frappe.session.user
				},
				order_by='date desc',
				limit=1)
			# frappe.msgprint(str(user))
			if not user:
				frappe.throw("No any RFID is found for the current user.")

			# Access the 'rfid_machine' and 'date' fields from the recent record
			rfid_machine = user[0].rfid_machine
			# Get the "Rfid tag Reading" document
			rfid_reading = frappe.get_doc("Rfid tag Reading", "rfid-tag-reading")

			# Get the status of RFID readers
			temp1 = rfid_reading.rfid1_status
			temp2 = rfid_reading.rfid2_status
			temp3 = rfid_reading.rfid3_status

			# Display the 'rfid_machine' value and its status
			# frappe.msgprint(f"RFID Machine: {rfid_machine}")
			# frappe.msgprint(str(rfid_reading))
			# # Assign the appropriate value to the 'rfid_tag' variable based on the status of RFID readers
			if temp1 == "Connected." and rfid_machine == 'RFID 1':
				self.rfid_tag = rfid_reading.rfid_1
				self.ip_of_indicator=rfid_reading.ip_of_indicator1
				self.port_no_of_indicator=rfid_reading.port_number_of_indicator1
			elif temp2 == "Connected." and rfid_machine == 'RFID 2':
				self.rfid_tag = rfid_reading.rfid_2
				self.ip_of_indicator=rfid_reading.ip_of_indicator2
				self.port_no_of_indicator=rfid_reading.port_number_of_indicator2
				# frappe.msgprint(str(self.port_no_of_indicator))
			elif temp3 == "Connected." and rfid_machine == 'RFID 3':
				self.rfid_tag = rfid_reading.rfid_3
				self.ip_of_indicator=rfid_reading.ip_of_indicator3
				self.port_no_of_indicator=rfid_reading.port_number_of_indicator3

			doc1 = frappe.get_all("H and T Contract", fields=["name","new_h_t_no","trolly_1","trolly_2","gang_type","vehicle_no","transporter_name","vehicle_type","harvester_code","harvester_name", "rfid_tag","transporter_name"], filters={"rfid_tag": self.rfid_tag,"season":self.season,"plant":self.branch})
			found_rfid_tag = False
			# frappe.msgprint(str(doc1))
			for g in doc1:
				self.rfid_tag=g.rfid_tag
				self.transporter_code=g.new_h_t_no
				self.transporter_code_ht=g.name
				self.transporter_name=g.transporter_name
				self.harvester_code_ht = g.harvester_code
				self.harvester_name = g.harvester_name
				self.vehicle_type = g.vehicle_type
				self.vehicle_number = g.vehicle_no
				self.tolly_1 = g.trolly_1
				self.tolly_2 = g.trolly_2
				self.gang_type = g.gang_type
				# frappe.msgprint(f"RFID Tag matches with Transporter {self.transporter_name}")
				found_rfid_tag = True
				# self.send_to_data(2)
				break

			if not found_rfid_tag:
				message = "RFID Tag does not match with any Transporter. Assgin token to transportar "
				message += '<br> <a href="/app/list/Tag Reader">Tag Reader</a>'
				frappe.throw(message)
				self.send_to_data(4)
		

   
	# def before_save(self):
		# doc=frappe.db.get_list("Branch",filters={"branch" : self.branch},
		# 									fields=["name","cane_inward_slip_no"])
		# if(int(self.cane_inward_no)==int(0)):
		# 	self.cane_inward_no=int(doc[0].get("cane_inward_slip_no"))+1
		# 	frappe.db.set_value("Branch",doc[0].get("name"),"cane_inward_slip_no",self.cane_inward_no)
		

	# def before_save(self):
	# 	doc=frappe.db.get_list("Branch",filters={"branch" : self.branch},
	# 										fields=["name","cane_inward_slip_no"])
	# 	if(int(self.cane_inward_no)==int(0)):
	# 		self.cane_inward_no=int(doc[0].get("cane_inward_slip_no"))+1
	# 		frappe.db.set_value("Branch",doc[0].get("name"),"cane_inward_slip_no",self.cane_inward_no)
	# 	doc1= frappe.get_all("Farmer List",fields=["name","rfid_tag"],filters={"branch":self.branch})
	# 	frappe.msgprint(str(doc1))
	# 	for g in doc1:
	# 		frappe.msgprint(str(g.rfid_tag))
	# 		if g.rfid_tag==self.rfid_tag:
	# 			frappe.msgprint("RFID Tag is  match with vendor")
	# 		else:
	# 			frappe.throw("RFID Tag is dosen't match with vendor")
    
	# @frappe.whitelist()
	# def show_data(self):
	# 	doc1= frappe.get_all("Farmer List",fields=["name","rfid_tag"],filters={"branch":self.branch})
	# 	frappe.msgprint(str(doc1))
	# 	for g in doc1:
	# 		if str(g.rfid_tag) ==str(self.rfid_tag):
	# 			frappe.msgprint("RFID Tag is  match with vendor")
	# 		else:
	# 			frappe.throw("RFID Tag is dosen't match with vendor")
		# count = 0
		# for d in doc1:
		# 	if d.rfid_tag==self.rfid_tag:
		# 		count+=1
		# if count == 0:
		# 	frappe.throw(f"RFID Tag is dosen't match with vendor")

		# doc=frappe.db.get_list("Branch",filters={"branch" : self.branch},
		# 									fields=["name","cane_inward_slip_no"])
		# if(int(self.cane_inward_no)==int(0)):
		# 	self.cane_inward_no=int(doc[0].get("cane_inward_slip_no"))+1
		# 	frappe.db.set_value("Branch",doc[0].get("name"),"cane_inward_slip_no",self.cane_inward_no)
	
        
     
     
	
   
#   for i in user:
			# frappe.msgprint(str(i.rfid_machine))
		# doc=frappe.get_doc("Rfid tag Reading","rfid-tag-reading")
		# frappe.msgprint(str(doc))


	# @frappe.whitelist()
	# def vivo(self):
	# 	doc = frappe.get_all('H and T Contract', filters={'name': self.transporter_code}, fields={'name','vehicle_no','transporter_code','harvester_code','transporter_name','harvester_name','trolly_1','trolly_2','total_vehicle','vehicle_type'})
	# 	for s in doc:
	# 		self.transporter_name = s.transporter_name
	# 		self.harvester_code = s.harvester_code
	# 		self.harvester_name = s.harvester_name
	# 		self.vehicle_type = s.vehicle_type
	# 		self.vehicle_number = s.vehicle_no
	# 		self.tolly_1 = s.trolly_1
	# 		self.tolly_2 = s.trolly_2
   
	# @frappe.whitelist()
	# def slip_number(self):
	# 	self.slip_no = self.get_new_slip_number()
	# @frappe.whitelist()
	# def get_new_slip_number(self):
	# 	last_slip = frappe.db.get_value('Cane Inward Slip', filters={}, fieldname='slip_no', order_by='creation desc')
	# 	if last_slip:
	# 		new_slip = int(last_slip) + 1
	# 	else:
	# 		new_slip = 1
	# 	return str(new_slip)


	#To get data on tripsheet 
	@frappe.whitelist()
	def get_tripsheet_info(self):
		doc = frappe.get_all('Trip Sheet', filters={'can_slip_flag':0,'transporter_code': self.transporter_code,'branch':self.branch,'season':self.season }, fields={'name','farmer_code','farmer_name','area_acre','cane_variety','burn_cane','slip_no'})
		for d in doc:
					self.append(
						"pending_slip",
								{
									'plot_no':str(d.name),
									'farmer_code':d.farmer_code,
									'farmer_name':d.farmer_name,
									'area_acre':d.area_acre,
									'cane_variety':d.cane_variety,
									'burn_cane':d.burn_cane,
									'slip_no':d.slip_no
								}
					)
	@frappe.whitelist()
	def hero(self):
		for i in self.get("pending_slip"):
			frappe.db.set_value("Trip Sheet",i.plot_no,"can_slip_flag",1)
		# self.send_to_data(4)
	@frappe.whitelist()
	def on_trash(self):
		for i in self.get("pending_slip"):
			frappe.db.set_value("Trip Sheet",i.plot_no,"can_slip_flag",0)
		
# @frappe.whitelist()
# def reset_counter():
# 	doc=frappe.get_doc("Cane Sampling Formula", "Cane Sampling Formula", fields=["minimum_brix", "maximum_brix", "minimum_pairs", "maximum_pairs","cane_slip_counter"])
# 	doc.cane_slip_counter = 0