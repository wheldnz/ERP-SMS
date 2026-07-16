# Copyright (c) 2026, SMS Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SMSServiceOrder(Document):
	def validate(self):
		self.grand_total = (self.spareparts_cost or 0) + (self.labor_cost or 0)
