import secrets

import frappe
from frappe.model.document import Document


class BRDSession(Document):
	def before_insert(self):
		self.generate_access_key()
		self.populate_responses()

	def generate_access_key(self):
		if not self.access_key:
			self.access_key = secrets.token_hex(10)

	def populate_responses(self):
		if self.responses:
			return

		template = frappe.get_doc("BRD Module Template", self.template)
		for q in template.questions:
			self.append(
				"responses",
				{
					"question_id": q.name,
					"section": q.section,
					"section_number": q.section_number,
					"subsection": q.subsection,
					"question_text": q.question_text,
					"question_type": q.question_type,
					"options": q.options,
					"priority": q.priority,
					"erp_reference": q.erp_reference,
					"help_text": q.help_text,
				},
			)

	def update_progress(self):
		total = len(self.responses)
		if total == 0:
			self.progress = 0
			return

		answered = sum(1 for r in self.responses if r.is_answered)
		self.progress = (answered / total) * 100
