import frappe


def after_install():
	"""Seed the Accounting BRD template after app install."""
	if frappe.db.exists("BRD Module Template", "Accounting BRD v1.0"):
		return

	seed_accounting_template()


def seed_accounting_template():
	"""Create the comprehensive Accounting BRD template with all sections and questions."""
	template = frappe.new_doc("BRD Module Template")
	template.template_name = "Accounting BRD v1.0"
	template.module_name = "Accounting"
	template.version = "1.0"
	template.description = "Comprehensive Business Requirements Document for ERPNext Accounting module implementation. Covers 24 sections including company setup, chart of accounts, tax configuration, AP/AR, banking, budgets, and more."
	template.is_active = 1

	questions = get_accounting_questions()
	for q in questions:
		template.append("questions", q)

	template.insert(ignore_permissions=True)
	frappe.db.commit()


def get_accounting_questions():
	"""Return the full list of Accounting BRD questions."""
	questions = []

	# Section 1: Company & Legal Setup
	s = 1
	section = "Company & Legal Setup"
	questions.extend([
		_q(s, section, None, "What is the full legal company name?", "Text", required=1, priority="Critical", erp_ref="Company.company_name"),
		_q(s, section, None, "What is the abbreviated company name for internal use?", "Text", erp_ref="Company.abbr"),
		_q(s, section, None, "What is the default currency?", "Text", required=1, priority="Critical", erp_ref="Company.default_currency"),
		_q(s, section, None, "What is the country of incorporation?", "Text", required=1, erp_ref="Company.country"),
		_q(s, section, None, "What is the company domain?", "Single Select", options="Manufacturing\nRetail\nServices\nDistribution\nEducation\nHealthcare\nNon Profit\nOther", erp_ref="Company.domain"),
		_q(s, section, None, "Is this company a group (parent) or a subsidiary?", "Single Select", options="Group\nSubsidiary\nStandalone", priority="Important"),
		_q(s, section, None, "If subsidiary, what is the parent company name?", "Text", erp_ref="Company.parent_company"),
		_q(s, section, None, "Tax ID / TRN (Tax Registration Number)?", "Text", priority="Critical", erp_ref="Company.tax_id"),
		_q(s, section, None, "Company registration / license number?", "Text"),
		_q(s, section, None, "Registered address (full)?", "Text", erp_ref="Company.address"),
	])

	# Section 2: Chart of Accounts
	s = 2
	section = "Chart of Accounts"
	questions.extend([
		_q(s, section, None, "Will you use a standard chart of accounts template or a custom one?", "Single Select", options="Standard Template\nCustom / Import Existing", required=1, priority="Critical", erp_ref="Company.chart_of_accounts"),
		_q(s, section, None, "If standard, which country template?", "Text", erp_ref="Company.chart_of_accounts"),
		_q(s, section, None, "How many levels of account hierarchy do you need?", "Single Select", options="2\n3\n4\n5+", erp_ref="Account"),
		_q(s, section, None, "Do you need account numbers?", "Single Select", options="Yes\nNo", erp_ref="Account.account_number"),
		_q(s, section, None, "List any custom account groups needed beyond the standard template.", "Text"),
		_q(s, section, "Root Types", "Which root types do you actively use?", "Multi Select", options="Asset\nLiability\nIncome\nExpense\nEquity", priority="Critical", erp_ref="Account.root_type"),
		_q(s, section, "Root Types", "Do you need separate P&L accounts per department or cost centre?", "Single Select", options="Yes\nNo"),
		_q(s, section, "Default Accounts", "What is the default receivable account name?", "Text", priority="Critical", erp_ref="Company.default_receivable_account"),
		_q(s, section, "Default Accounts", "What is the default payable account name?", "Text", priority="Critical", erp_ref="Company.default_payable_account"),
		_q(s, section, "Default Accounts", "What is the default income account?", "Text", erp_ref="Company.default_income_account"),
		_q(s, section, "Default Accounts", "What is the default expense account?", "Text", erp_ref="Company.default_expense_account"),
	])

	# Section 3: Cost Centres & Dimensions
	s = 3
	section = "Cost Centres & Dimensions"
	questions.extend([
		_q(s, section, None, "How do you currently track costs (departments, locations, projects, etc.)?", "Text", priority="Important"),
		_q(s, section, None, "List your cost centres / departments.", "Text", required=1, erp_ref="Cost Center"),
		_q(s, section, None, "Do you need a hierarchical cost centre structure?", "Single Select", options="Yes - Hierarchical\nNo - Flat", erp_ref="Cost Center"),
		_q(s, section, "Accounting Dimensions", "Do you need custom accounting dimensions beyond cost centre?", "Single Select", options="Yes\nNo", erp_ref="Accounting Dimension"),
		_q(s, section, "Accounting Dimensions", "If yes, list the dimensions needed (e.g. Project, Branch, Region).", "Text"),
		_q(s, section, "Accounting Dimensions", "Should any dimension be mandatory on transactions?", "Single Select", options="Yes\nNo"),
	])

	# Section 4: Fiscal Year & Periods
	s = 4
	section = "Fiscal Year & Periods"
	questions.extend([
		_q(s, section, None, "What is your fiscal year start date?", "Text", required=1, priority="Critical", erp_ref="Fiscal Year.year_start_date"),
		_q(s, section, None, "What is your fiscal year end date?", "Text", required=1, priority="Critical", erp_ref="Fiscal Year.year_end_date"),
		_q(s, section, None, "Do you use monthly or custom accounting periods?", "Single Select", options="Monthly (auto)\nCustom periods", erp_ref="Accounting Period"),
		_q(s, section, None, "Do you need to lock (freeze) completed periods?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Accounts Settings.acc_frozen_upto"),
		_q(s, section, None, "If yes, who should be allowed to post in frozen periods?", "Text", erp_ref="Accounts Settings.frozen_accounts_modifier"),
	])

	# Section 5: Multi-Currency & FX
	s = 5
	section = "Multi-Currency & FX"
	questions.extend([
		_q(s, section, None, "Do you transact in multiple currencies?", "Single Select", options="Yes\nNo", required=1, priority="Critical"),
		_q(s, section, None, "If yes, list all transaction currencies.", "Text", erp_ref="Currency"),
		_q(s, section, None, "Source for exchange rates?", "Single Select", options="Manual Entry\nAuto-fetch (exchangerate.host)\nCustom API", erp_ref="Currency Exchange"),
		_q(s, section, None, "How do you handle unrealised exchange gain/loss?", "Single Select", options="At Period End\nAt Payment\nBoth", erp_ref="Company.unrealized_exchange_gain_loss_account"),
		_q(s, section, None, "Do you need a separate exchange gain/loss account?", "Single Select", options="Yes\nNo", erp_ref="Company.exchange_gain_loss_account"),
	])

	# Section 6: UAE VAT & Tax
	s = 6
	section = "UAE VAT & Tax Configuration"
	questions.extend([
		_q(s, section, None, "Are you VAT registered?", "Single Select", options="Yes\nNo", required=1, priority="Critical"),
		_q(s, section, None, "What is your TRN (Tax Registration Number)?", "Text", priority="Critical", erp_ref="Company.tax_id"),
		_q(s, section, None, "Which VAT rates do you use?", "Multi Select", options="5% Standard\n0% Zero-rated\nExempt\nReverse Charge\nOut of Scope", priority="Critical", erp_ref="Item Tax Template"),
		_q(s, section, None, "Do you need separate tax templates per item category?", "Single Select", options="Yes\nNo", erp_ref="Item Tax Template"),
		_q(s, section, None, "Do you file VAT returns monthly or quarterly?", "Single Select", options="Monthly\nQuarterly", erp_ref="UAE VAT Settings"),
		_q(s, section, "Tax Accounts", "What is the VAT output (sales) account?", "Text", erp_ref="Account"),
		_q(s, section, "Tax Accounts", "What is the VAT input (purchase) account?", "Text", erp_ref="Account"),
		_q(s, section, "Tax Accounts", "Do you need designated accounts for reverse charge VAT?", "Single Select", options="Yes\nNo"),
	])

	# Section 7: Accounts Payable
	s = 7
	section = "Accounts Payable"
	questions.extend([
		_q(s, section, None, "How many active suppliers do you have (approx)?", "Text", priority="Important"),
		_q(s, section, None, "Do you use Purchase Orders before Purchase Invoices?", "Single Select", options="Always\nSometimes\nNever", erp_ref="Purchase Order"),
		_q(s, section, None, "Do you need 3-way matching (PO → Receipt → Invoice)?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "Do you use supplier advance payments?", "Single Select", options="Yes\nNo", erp_ref="Payment Entry"),
		_q(s, section, None, "Do you track supplier credit notes / debit notes?", "Single Select", options="Yes\nNo", erp_ref="Purchase Invoice.is_return"),
		_q(s, section, None, "Do you need automatic payment reminders for due invoices?", "Single Select", options="Yes\nNo"),
		_q(s, section, "Approval Workflow", "Do purchase invoices need an approval workflow?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, "Approval Workflow", "If yes, describe the approval levels (e.g. amount thresholds, roles).", "Text"),
	])

	# Section 8: Accounts Receivable
	s = 8
	section = "Accounts Receivable"
	questions.extend([
		_q(s, section, None, "How many active customers do you have (approx)?", "Text", priority="Important"),
		_q(s, section, None, "Do you use Sales Orders before Sales Invoices?", "Single Select", options="Always\nSometimes\nNever", erp_ref="Sales Order"),
		_q(s, section, None, "Do you use Delivery Notes?", "Single Select", options="Yes\nNo", erp_ref="Delivery Note"),
		_q(s, section, None, "Do you issue customer credit notes?", "Single Select", options="Yes\nNo", erp_ref="Sales Invoice.is_return"),
		_q(s, section, None, "Do you track customer advances?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need automatic payment reminders?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Credit limit management needed?", "Single Select", options="Yes\nNo", erp_ref="Customer.credit_limit"),
		_q(s, section, "Revenue Recognition", "Do you have revenue recognition requirements?", "Single Select", options="Yes - at invoice\nYes - deferred\nNo"),
	])

	# Section 9: Payment Terms & Modes
	s = 9
	section = "Payment Terms & Modes"
	questions.extend([
		_q(s, section, None, "What are your standard customer payment terms?", "Text", priority="Important", erp_ref="Payment Terms Template"),
		_q(s, section, None, "What are your standard supplier payment terms?", "Text", erp_ref="Payment Terms Template"),
		_q(s, section, None, "List all payment modes used (Cash, Bank Transfer, Cheque, Credit Card, etc.).", "Text", priority="Important", erp_ref="Mode of Payment"),
		_q(s, section, None, "Do you offer early payment discounts?", "Single Select", options="Yes\nNo", erp_ref="Payment Term.discount"),
		_q(s, section, None, "Do you need split payment terms (e.g. 50% advance, 50% on delivery)?", "Single Select", options="Yes\nNo"),
	])

	# Section 10: Banking & Reconciliation
	s = 10
	section = "Banking & Reconciliation"
	questions.extend([
		_q(s, section, None, "How many bank accounts does the company have?", "Text", priority="Important", erp_ref="Bank Account"),
		_q(s, section, None, "List bank names and account types (current, savings, etc.).", "Text", erp_ref="Bank Account"),
		_q(s, section, None, "Do you currently do bank reconciliation?", "Single Select", options="Yes - Manual\nYes - Using bank feeds\nNo"),
		_q(s, section, None, "Would you like to use automatic bank statement import?", "Single Select", options="Yes\nNo", erp_ref="Bank Statement Import"),
		_q(s, section, None, "What format are your bank statements in?", "Single Select", options="CSV\nOFX/QIF\nPDF (manual)\nAPI integration"),
		_q(s, section, None, "Do you need petty cash tracking?", "Single Select", options="Yes\nNo"),
	])

	# Section 11: Journal Entries
	s = 11
	section = "Journal Entries & Manual Adjustments"
	questions.extend([
		_q(s, section, None, "What types of journal entries do you commonly make?", "Multi Select", options="General\nInter-company\nBank Entry\nCash Entry\nCredit Card Entry\nDebit Note\nCredit Note\nWrite Off\nDepreciation", erp_ref="Journal Entry.voucher_type"),
		_q(s, section, None, "Do journal entries need approval before posting?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need recurring/automatic journal entries?", "Single Select", options="Yes\nNo", erp_ref="Auto Repeat"),
		_q(s, section, None, "Do you need inter-company journal entries?", "Single Select", options="Yes\nNo", erp_ref="Journal Entry.inter_company_journal_entry_reference"),
	])

	# Section 12: Budget Management
	s = 12
	section = "Budget Management"
	questions.extend([
		_q(s, section, None, "Do you use budgets?", "Single Select", options="Yes\nNo", required=1, priority="Important", erp_ref="Budget"),
		_q(s, section, None, "Budget against which dimension?", "Multi Select", options="Cost Center\nProject\nDepartment\nAccounting Dimension", erp_ref="Budget.budget_against"),
		_q(s, section, None, "What action on budget exceeded?", "Single Select", options="Warn\nStop\nIgnore", erp_ref="Budget.action_if_annual_budget_exceeded"),
		_q(s, section, None, "Monthly distribution pattern?", "Single Select", options="Equal monthly\nCustom distribution\nNot needed", erp_ref="Monthly Distribution"),
		_q(s, section, None, "Who should be able to create/modify budgets?", "Text"),
	])

	# Section 13: Deferred Revenue & Expense
	s = 13
	section = "Deferred Revenue & Expense"
	questions.extend([
		_q(s, section, None, "Do you have deferred revenue? (e.g. subscriptions, annual contracts)?", "Single Select", options="Yes\nNo", erp_ref="Company.default_deferred_revenue_account"),
		_q(s, section, None, "Do you have deferred expenses? (e.g. prepaid insurance)?", "Single Select", options="Yes\nNo", erp_ref="Company.default_deferred_expense_account"),
		_q(s, section, None, "Should deferred entries be processed automatically?", "Single Select", options="Yes - automatic monthly\nNo - manual", erp_ref="Accounts Settings.automatically_process_deferred_accounting_entry"),
		_q(s, section, None, "Booking date for deferred entries?", "Single Select", options="Based on actual posting date\nBased on first day of month", erp_ref="Accounts Settings.book_deferred_entries_based_on"),
	])

	# Section 14: Subscriptions
	s = 14
	section = "Subscriptions & Recurring"
	questions.extend([
		_q(s, section, None, "Do you have recurring invoices (subscriptions)?", "Single Select", options="Yes\nNo", erp_ref="Subscription"),
		_q(s, section, None, "If yes, describe the billing patterns (monthly, quarterly, annual).", "Text"),
		_q(s, section, None, "Should subscription invoices be auto-created?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need subscription plans with different tiers?", "Single Select", options="Yes\nNo", erp_ref="Subscription Plan"),
	])

	# Section 15: Period Closing
	s = 15
	section = "Period Closing"
	questions.extend([
		_q(s, section, None, "Do you perform monthly closing procedures?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "What is your closing entry account for P&L balances?", "Text", erp_ref="Period Closing Voucher.closing_account_head"),
		_q(s, section, None, "Do you need a closing checklist or workflow?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "What reports must be generated at period close?", "Text"),
	])

	# Section 16: Payment Reconciliation
	s = 16
	section = "Payment Reconciliation"
	questions.extend([
		_q(s, section, None, "Do you have unallocated payments that need matching to invoices?", "Single Select", options="Yes - frequently\nRarely\nNo", erp_ref="Payment Reconciliation"),
		_q(s, section, None, "Do you need automatic payment matching?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "How do you handle partial payments?", "Single Select", options="Allocate to oldest invoice\nManual allocation\nNot applicable"),
	])

	# Section 17: POS
	s = 17
	section = "Point of Sale (POS)"
	questions.extend([
		_q(s, section, None, "Do you use a Point of Sale system?", "Single Select", options="Yes\nNo", erp_ref="POS Profile"),
		_q(s, section, None, "If yes, how many POS terminals?", "Text"),
		_q(s, section, None, "POS payment methods needed?", "Multi Select", options="Cash\nCard\nBank Transfer\nMobile Payment\nCredit", erp_ref="POS Payment Method"),
		_q(s, section, None, "Do you need POS closing (shift end) reconciliation?", "Single Select", options="Yes\nNo", erp_ref="POS Closing Entry"),
		_q(s, section, None, "Do you need offline POS capability?", "Single Select", options="Yes\nNo"),
	])

	# Section 18: Opening Balances & Migration
	s = 18
	section = "Opening Balances & Migration"
	questions.extend([
		_q(s, section, None, "What is your go-live / cutover date?", "Text", required=1, priority="Critical"),
		_q(s, section, None, "Will you import opening balances from a previous system?", "Single Select", options="Yes\nNo", priority="Critical"),
		_q(s, section, None, "What system are you migrating from?", "Text"),
		_q(s, section, None, "What data needs to be migrated?", "Multi Select", options="Chart of Accounts & Balances\nCustomer Outstanding\nSupplier Outstanding\nBank Balances\nFixed Asset Register\nStock Balances\nOpen Sales Orders\nOpen Purchase Orders"),
		_q(s, section, None, "Is historical transaction data needed (beyond opening balances)?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "If yes, how many years of history?", "Text"),
	])

	# Section 19: Accounts Settings
	s = 19
	section = "Accounts Settings & Preferences"
	questions.extend([
		_q(s, section, None, "Allow over-billing above delivery/order amount?", "Single Select", options="Yes\nNo", erp_ref="Accounts Settings.over_billing_allowance"),
		_q(s, section, None, "Make accounting entry for every stock movement?", "Single Select", options="Yes - Perpetual\nNo - Periodic", priority="Important", erp_ref="Company.enable_perpetual_inventory"),
		_q(s, section, None, "Allow stale exchange rates?", "Single Select", options="Yes\nNo", erp_ref="Accounts Settings.allow_stale"),
		_q(s, section, None, "Stale days limit?", "Text", erp_ref="Accounts Settings.stale_days"),
		_q(s, section, None, "Enable automatic party matching?", "Single Select", options="Yes\nNo", erp_ref="Accounts Settings.enable_party_matching"),
		_q(s, section, None, "Unlink payment on cancel of invoice?", "Single Select", options="Yes\nNo", erp_ref="Accounts Settings.unlink_payment_on_cancellation_of_invoice"),
	])

	# Section 20: Roles & Permissions
	s = 20
	section = "Roles & Permissions"
	questions.extend([
		_q(s, section, None, "How many users will access the accounting module?", "Text", priority="Important"),
		_q(s, section, None, "List the accounting roles needed (e.g. Accounts Manager, Accounts User, Auditor).", "Text", priority="Important"),
		_q(s, section, None, "Should invoice creation be restricted by role?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should journal entry posting be restricted?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do auditors need read-only access?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Any data-level restrictions (e.g. users see only their cost centre)?", "Single Select", options="Yes\nNo", erp_ref="User Permission"),
	])

	# Section 21: Financial Reporting
	s = 21
	section = "Financial Reporting"
	questions.extend([
		_q(s, section, None, "Which standard reports do you need?", "Multi Select", options="Balance Sheet\nProfit & Loss\nCash Flow Statement\nTrial Balance\nGeneral Ledger\nAccounts Receivable\nAccounts Payable\nBudget Variance\nGross Profit", priority="Important"),
		_q(s, section, None, "Do you need custom financial reports?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "If yes, describe the custom reports.", "Text"),
		_q(s, section, None, "Do you need consolidated reports across multiple companies?", "Single Select", options="Yes\nNo", erp_ref="Consolidated Financial Statement"),
		_q(s, section, None, "Preferred report output format?", "Multi Select", options="On-screen\nPDF\nExcel\nEmail scheduled"),
	])

	# Section 22: Print Formats
	s = 22
	section = "Print Formats & Branding"
	questions.extend([
		_q(s, section, None, "Do you need custom print formats for invoices?", "Single Select", options="Yes\nNo", erp_ref="Print Format"),
		_q(s, section, None, "Elements to include on invoice print?", "Multi Select", options="Company Logo\nTRN/Tax ID\nBank Details\nPayment QR Code\nTerms & Conditions\nCustom Footer"),
		_q(s, section, None, "Do you need multi-language invoices?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "If yes, which languages?", "Text"),
		_q(s, section, None, "Paper size preference?", "Single Select", options="A4\nLetter\nCustom"),
	])

	# Section 23: Integrations & Automation
	s = 23
	section = "Integrations & Automation"
	questions.extend([
		_q(s, section, None, "Do you need integration with external payment gateways?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "If yes, which gateways?", "Text"),
		_q(s, section, None, "Do you need e-invoicing integration?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need integration with any external accounting software?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need automated email notifications for invoice/payment events?", "Single Select", options="Yes\nNo", erp_ref="Notification"),
		_q(s, section, None, "Any other integrations needed?", "Text"),
	])

	# Section 24: Parking Lot & Open Items
	s = 24
	section = "Parking Lot & Open Items"
	questions.extend([
		_q(s, section, None, "List any requirements not covered in the sections above.", "Text"),
		_q(s, section, None, "Any known pain points with the current system?", "Text", priority="Important"),
		_q(s, section, None, "Any specific compliance or regulatory requirements?", "Text"),
		_q(s, section, None, "Timeline or deadline constraints for go-live?", "Text", priority="Important"),
		_q(s, section, None, "Any additional notes or comments?", "Text"),
	])

	return questions


def _q(section_number, section, subsection, question_text, question_type,
       options=None, required=0, priority=None, erp_ref=None, help_text=None):
	"""Helper to construct a question dict."""
	return {
		"section_number": section_number,
		"section": section,
		"subsection": subsection or "",
		"question_text": question_text,
		"question_type": question_type,
		"options": options or "",
		"is_required": required,
		"priority": priority or "",
		"erp_reference": erp_ref or "",
		"help_text": help_text or "",
	}
