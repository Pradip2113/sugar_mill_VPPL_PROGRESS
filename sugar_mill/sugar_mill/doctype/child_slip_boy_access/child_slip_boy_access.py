# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ChildSlipBoyAccess(Document):
	@frappe.whitelist()
	def on_trash(self):
		frappe.msgprint("delete massage")
