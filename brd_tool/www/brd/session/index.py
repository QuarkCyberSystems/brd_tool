import json

import frappe
from frappe import _
from frappe.rate_limiter import rate_limit

no_cache = 1


def get_context(context):
	access_key = frappe.form_dict.get("key")

	if not access_key:
		context.error = "No access key provided."
		context.session = None
		return

	session = frappe.db.get_value(
		"BRD Session",
		{"access_key": access_key},
		[
			"name", "session_title", "project", "template", "status",
			"access_key", "respondent_name", "respondent_email",
			"respondent_role", "progress", "submitted_on",
		],
		as_dict=True,
	)

	if not session:
		context.error = "Invalid or expired access key."
		context.session = None
		return

	# Load project info
	project = frappe.db.get_value(
		"BRD Project", session.project,
		["project_name", "client_name", "client_company"], as_dict=True,
	)

	# Load template info
	template = frappe.db.get_value(
		"BRD Module Template", session.template,
		["template_name", "module_name", "description"], as_dict=True,
	)

	# Load responses
	responses = frappe.get_all(
		"BRD Response",
		filters={"parent": session.name, "parenttype": "BRD Session"},
		fields=[
			"name", "question_id", "section", "section_number", "subsection",
			"question_text", "question_type", "options", "priority",
			"erp_reference", "help_text", "response_text", "response_single",
			"response_multi", "is_answered",
		],
		order_by="idx asc",
	)

	# Build sections list for TOC
	sections = []
	seen = set()
	for r in responses:
		key = f"{r.section_number}-{r.section}"
		if key not in seen:
			seen.add(key)
			sections.append({
				"number": r.section_number,
				"title": r.section,
				"total": 0,
				"answered": 0,
			})
		# Count questions per section
		for s in sections:
			if s["number"] == r.section_number:
				s["total"] += 1
				if r.is_answered:
					s["answered"] += 1
				break

	context.error = None
	context.session = session
	context.project = project
	context.brd_template = template
	context.responses = responses
	context.responses_json = json.dumps(
		[{k: v for k, v in r.items()} for r in responses],
		default=str,
	)
	context.sections = sections
	context.sections_json = json.dumps(sections, default=str)
	context.is_submitted = session.status in ("Submitted", "Reviewed")
	context.title = session.session_title or f"BRD - {template.module_name}"
	context.no_cache = 1


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=30, seconds=60)
def save_responses(access_key, responses, respondent_name=None,
                   respondent_email=None, respondent_role=None):
	"""Save draft responses from the portal."""
	session_name = frappe.db.get_value(
		"BRD Session", {"access_key": access_key}, "name"
	)
	if not session_name:
		frappe.throw(_("Invalid access key"), frappe.AuthenticationError)

	session = frappe.get_doc("BRD Session", session_name)

	if session.status in ("Submitted", "Reviewed"):
		frappe.throw(_("This session has already been submitted."))

	# Update respondent info
	if respondent_name:
		session.respondent_name = respondent_name
	if respondent_email:
		session.respondent_email = respondent_email
	if respondent_role:
		session.respondent_role = respondent_role

	# Parse responses
	if isinstance(responses, str):
		responses = json.loads(responses)

	# Update each response row
	response_map = {r["name"]: r for r in responses if r.get("name")}
	for row in session.responses:
		if row.name in response_map:
			data = response_map[row.name]
			row.response_text = data.get("response_text", "") or ""
			row.response_single = data.get("response_single", "") or ""
			row.response_multi = data.get("response_multi", "") or ""
			# Determine if answered
			row.is_answered = bool(
				row.response_text.strip()
				or row.response_single.strip()
				or (row.response_multi and row.response_multi.strip() not in ("", "[]"))
			)

	# Update progress
	session.update_progress()

	if session.status == "Draft":
		session.status = "In Progress"

	session.save(ignore_permissions=True)
	frappe.db.commit()

	return {"progress": session.progress, "status": session.status}


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=5, seconds=60)
def submit_session(access_key, respondent_name, respondent_email,
                   respondent_role=None):
	"""Submit the BRD session (final)."""
	session_name = frappe.db.get_value(
		"BRD Session", {"access_key": access_key}, "name"
	)
	if not session_name:
		frappe.throw(_("Invalid access key"), frappe.AuthenticationError)

	session = frappe.get_doc("BRD Session", session_name)

	if session.status in ("Submitted", "Reviewed"):
		frappe.throw(_("This session has already been submitted."))

	# Validate required fields
	if not respondent_name:
		frappe.throw(_("Respondent name is required."))
	if not respondent_email:
		frappe.throw(_("Respondent email is required."))

	# Check required questions
	unanswered_required = []
	for row in session.responses:
		if row.priority == "Critical" and not row.is_answered:
			unanswered_required.append(row.question_text)

	if unanswered_required:
		frappe.throw(
			_("Please answer all critical questions before submitting. Missing: {0}").format(
				", ".join(unanswered_required[:5])
				+ ("..." if len(unanswered_required) > 5 else "")
			)
		)

	session.respondent_name = respondent_name
	session.respondent_email = respondent_email
	if respondent_role:
		session.respondent_role = respondent_role
	session.status = "Submitted"
	session.submitted_on = frappe.utils.now()
	session.update_progress()
	session.save(ignore_permissions=True)
	frappe.db.commit()

	return {"status": "Submitted", "submitted_on": str(session.submitted_on)}
