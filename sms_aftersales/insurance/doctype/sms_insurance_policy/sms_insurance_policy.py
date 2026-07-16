# Copyright (c) 2026, SMS Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SMSInsurancePolicy(Document):
	def validate(self):
		if self.valid_start and self.valid_expiry and self.valid_start >= self.valid_expiry:
			frappe.throw("Tanggal Kadaluarsa Polis harus setelah Tanggal Mulai Valid.")
