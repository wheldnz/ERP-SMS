# Copyright (c) 2026, SMS Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SMSServiceIntake(Document):
	def validate(self):
		if self.serial_no:
			# Auto-check if serial number has active insurance policy
			active_policy = frappe.db.get_value(
				"SMS Insurance Policy",
				{"serial_no": self.serial_no, "status": "Active"},
				"name"
			)
			if active_policy:
				self.is_insurance_covered = 1
				self.insurance_policy = active_policy
