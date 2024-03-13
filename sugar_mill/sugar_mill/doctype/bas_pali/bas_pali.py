# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BasPali(Document):
	def before_save(self):
		for i in self.get("transporter_table"):
			frappe.db.set_value("H and T Contract",i.h_and_t_contract_code,"bas_pali",1)

	def on_trash(self):
		for i in self.get("transporter_table"):
			frappe.db.set_value("H and T Contract",i.h_and_t_contract_code,"bas_pali",0)
