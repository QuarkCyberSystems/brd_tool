import frappe


@frappe.whitelist()
def create_session(project, template):
	"""Create a new BRD Session from a project and template."""
	session = frappe.new_doc("BRD Session")
	session.project = project
	session.template = template

	# Auto-generate title
	project_doc = frappe.get_doc("BRD Project", project)
	template_doc = frappe.get_doc("BRD Module Template", template)
	existing_count = frappe.db.count(
		"BRD Session", {"project": project, "template": template}
	)
	session.session_title = (
		f"{project_doc.client_name} - {template_doc.module_name} - Session {existing_count + 1}"
	)
	session.session_date = frappe.utils.today()

	session.insert()
	return {"name": session.name, "access_key": session.access_key}


@frappe.whitelist()
def get_share_link(session_name):
	"""Get the shareable URL for a BRD Session."""
	access_key = frappe.db.get_value("BRD Session", session_name, "access_key")
	if not access_key:
		frappe.throw("Session not found or has no access key")

	site_url = frappe.utils.get_url()
	return f"{site_url}/brd/session?key={access_key}"
