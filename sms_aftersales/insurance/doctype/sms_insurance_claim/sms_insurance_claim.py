# Copyright (c) 2026, SMS Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SMSInsuranceClaim(Document):
	def validate(self):
		if self.claim_amount and self.policy:
			coverage_limit = frappe.db.get_value("SMS Insurance Policy", self.policy, "coverage_limit")
			if coverage_limit and self.claim_amount > coverage_limit:
				frappe.throw(f"Nominal klaim (Rp {self.claim_amount:,.2f}) melebihi limit pertanggungan polis (Rp {coverage_limit:,.2f}).")
