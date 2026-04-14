import frappe


def after_install():
	"""Seed BRD templates after app install. Skips any that already exist."""
	if not frappe.db.exists("BRD Module Template", "Accounting BRD v1.0"):
		seed_accounting_template()

	if not frappe.db.exists("BRD Module Template", "Assets BRD v1.0"):
		seed_assets_template()

	if not frappe.db.exists("BRD Module Template", "Buying BRD v1.0"):
		seed_buying_template()

	if not frappe.db.exists("BRD Module Template", "Selling BRD v1.0"):
		seed_selling_template()

	if not frappe.db.exists("BRD Module Template", "Stock BRD v1.0"):
		seed_stock_template()

	if not frappe.db.exists("BRD Module Template", "CRM BRD v1.0"):
		seed_crm_template()

	if not frappe.db.exists("BRD Module Template", "Projects BRD v1.0"):
		seed_projects_template()

	if not frappe.db.exists("BRD Module Template", "Quality Management BRD v1.0"):
		seed_quality_template()


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


def seed_assets_template():
	"""Create the comprehensive Assets BRD template with all sections and questions."""
	template = frappe.new_doc("BRD Module Template")
	template.template_name = "Assets BRD v1.0"
	template.module_name = "Assets"
	template.version = "1.0"
	template.description = "Comprehensive Business Requirements Document for ERPNext Assets module implementation. Covers 20 sections including asset policy, depreciation, CWIP, capitalization, maintenance, repair, disposal, insurance, and more."
	template.is_active = 1

	questions = get_assets_questions()
	for q in questions:
		template.append("questions", q)

	template.insert(ignore_permissions=True)
	frappe.db.commit()


def get_assets_questions():
	"""Return the full list of Assets BRD questions."""
	questions = []

	# Section 1: Asset Policy & Classification
	s = 1
	section = "Asset Policy & Classification"
	questions.extend([
		_q(s, section, None, "Does your organization have a formal fixed asset capitalization policy?", "Single Select", options="Yes\nNo", required=1, priority="Critical"),
		_q(s, section, None, "What is the minimum capitalization threshold (amount below which items are expensed)?", "Text", priority="Critical"),
		_q(s, section, None, "How do you currently track fixed assets?", "Single Select", options="Spreadsheet\nLegacy System\nManual Register\nNo formal tracking", priority="Important"),
		_q(s, section, None, "Approximately how many fixed assets does the organization own?", "Text", priority="Important"),
		_q(s, section, None, "Do you categorize assets by type (e.g. Furniture, Vehicles, IT Equipment, Plant & Machinery)?", "Single Select", options="Yes\nNo", erp_ref="Asset Category"),
		_q(s, section, None, "List all asset categories you need.", "Text", required=1, erp_ref="Asset Category"),
		_q(s, section, None, "Do you need sub-categories within main asset categories?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you assign unique asset numbers/tags to each asset?", "Single Select", options="Yes\nNo", erp_ref="Asset.naming_series"),
		_q(s, section, None, "Preferred asset naming convention?", "Single Select", options="Manual Entry\nAuto-generated Series\nItem Code Based", erp_ref="Asset.naming_series"),
	])

	# Section 2: Asset Category Accounts
	s = 2
	section = "Asset Category Accounts"
	questions.extend([
		_q(s, section, None, "Do you need separate GL accounts per asset category?", "Single Select", options="Yes\nNo", priority="Critical", erp_ref="Asset Category Account"),
		_q(s, section, None, "For each category, do you maintain separate Fixed Asset, Accumulated Depreciation, and Depreciation Expense accounts?", "Single Select", options="Yes\nNo", priority="Critical", erp_ref="Asset Category Account"),
		_q(s, section, None, "Do any categories require a Capital Work in Progress (CWIP) account?", "Single Select", options="Yes\nNo", erp_ref="Asset Category Account.capital_work_in_progress_account"),
		_q(s, section, None, "Will you use the same account structure across all companies, or different per company?", "Single Select", options="Same for all\nDifferent per company"),
	])

	# Section 3: Asset Locations & Custodians
	s = 3
	section = "Asset Locations & Custodians"
	questions.extend([
		_q(s, section, None, "Do you track where each asset is physically located?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Location"),
		_q(s, section, None, "List your asset locations (buildings, floors, branches, warehouses, etc.).", "Text", erp_ref="Location"),
		_q(s, section, None, "Do you need a hierarchical location structure (e.g. Building > Floor > Room)?", "Single Select", options="Yes\nNo", erp_ref="Location.parent_location"),
		_q(s, section, None, "Do you assign custodians (responsible employees) to assets?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Asset.custodian"),
		_q(s, section, None, "Should custodian changes be tracked and audited?", "Single Select", options="Yes\nNo", erp_ref="Asset Movement"),
		_q(s, section, None, "Do you need geolocation tracking for assets (GPS coordinates)?", "Single Select", options="Yes\nNo", erp_ref="Location.latitude"),
	])

	# Section 4: Asset Acquisition
	s = 4
	section = "Asset Acquisition"
	questions.extend([
		_q(s, section, None, "How are assets typically acquired?", "Multi Select", options="Purchase Order → Receipt\nDirect Purchase Invoice\nSelf-constructed / Capitalized\nDonated / Gifted\nLeased", priority="Critical", erp_ref="Asset"),
		_q(s, section, None, "Do you receive assets through Purchase Receipts or directly via Purchase Invoices?", "Single Select", options="Purchase Receipt\nPurchase Invoice\nBoth", erp_ref="Asset"),
		_q(s, section, None, "Do you need to track the supplier/vendor for each asset?", "Single Select", options="Yes\nNo", erp_ref="Asset.supplier"),
		_q(s, section, None, "Do you need to link assets to the original purchase document?", "Single Select", options="Yes\nNo", erp_ref="Asset.purchase_receipt"),
		_q(s, section, None, "Do you acquire assets in bulk (multiple units of same item)?", "Single Select", options="Yes\nNo", erp_ref="Asset.asset_quantity"),
		_q(s, section, None, "Are there assets owned by third parties but in your possession?", "Single Select", options="Yes\nNo", erp_ref="Asset.asset_owner"),
		_q(s, section, None, "If yes, who owns them?", "Single Select", options="Supplier\nCustomer\nNot applicable", erp_ref="Asset.asset_owner"),
	])

	# Section 5: Depreciation Policy
	s = 5
	section = "Depreciation Policy"
	questions.extend([
		_q(s, section, None, "Do you calculate depreciation on your fixed assets?", "Single Select", options="Yes\nNo", required=1, priority="Critical", erp_ref="Asset.calculate_depreciation"),
		_q(s, section, None, "Which depreciation method(s) do you use?", "Multi Select", options="Straight Line\nWritten Down Value (WDV)\nDouble Declining Balance\nManual", priority="Critical", erp_ref="Asset Finance Book.depreciation_method"),
		_q(s, section, None, "Is the depreciation method consistent across all asset categories, or does it vary?", "Single Select", options="Same for all\nVaries by category"),
		_q(s, section, None, "What is the typical useful life for each asset category (in months)? List per category.", "Text", priority="Important", erp_ref="Asset Finance Book.total_number_of_depreciations"),
		_q(s, section, None, "How frequently do you book depreciation?", "Single Select", options="Monthly\nQuarterly\nAnnually", priority="Important", erp_ref="Asset Finance Book.frequency_of_depreciation"),
		_q(s, section, None, "Do you use daily pro-rata depreciation (based on exact days in month)?", "Single Select", options="Yes\nNo", erp_ref="Asset Finance Book.daily_prorata_based"),
		_q(s, section, None, "Do you assign a salvage/residual value to assets?", "Single Select", options="Yes\nNo", erp_ref="Asset Finance Book.expected_value_after_useful_life"),
		_q(s, section, None, "If yes, is it a fixed amount or percentage of cost?", "Single Select", options="Fixed Amount\nPercentage\nNot applicable", erp_ref="Asset Finance Book.salvage_value_percentage"),
		_q(s, section, None, "Should depreciation journal entries be posted automatically on schedule?", "Single Select", options="Yes - automatic\nNo - manual posting", priority="Important", erp_ref="Accounts Settings.book_asset_depreciation_entry_automatically"),
		_q(s, section, None, "Do you have existing assets with prior accumulated depreciation to import?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Asset.opening_accumulated_depreciation"),
	])

	# Section 6: Multi-Finance Book Depreciation
	s = 6
	section = "Multi-Finance Book Depreciation"
	questions.extend([
		_q(s, section, None, "Do you maintain more than one set of books (e.g. statutory vs. tax vs. management)?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Finance Book"),
		_q(s, section, None, "If yes, list the finance books needed.", "Text", erp_ref="Finance Book"),
		_q(s, section, None, "Do different books use different depreciation methods or useful lives for the same asset?", "Single Select", options="Yes\nNo", erp_ref="Asset Finance Book"),
		_q(s, section, None, "Which finance book should be used for default/primary reporting?", "Text", erp_ref="Company.default_finance_book"),
	])

	# Section 7: Shift-Based Depreciation
	s = 7
	section = "Shift-Based Depreciation"
	questions.extend([
		_q(s, section, None, "Do any of your assets operate in multiple shifts (e.g. manufacturing equipment)?", "Single Select", options="Yes\nNo", erp_ref="Asset Shift Factor"),
		_q(s, section, None, "If yes, do you adjust depreciation based on shift utilization?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "What shift factors do you use? (e.g. Single=1.0, Double=1.5, Triple=2.0)", "Text", erp_ref="Asset Shift Factor.shift_factor"),
		_q(s, section, None, "Do shift allocations change periodically?", "Single Select", options="Yes\nNo", erp_ref="Asset Shift Allocation"),
	])

	# Section 8: Capital Work in Progress (CWIP)
	s = 8
	section = "Capital Work in Progress (CWIP)"
	questions.extend([
		_q(s, section, None, "Do you have assets under construction or assembly before they are ready for use?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Asset Category.enable_cwip_accounting"),
		_q(s, section, None, "Do you need CWIP accounting (accumulate costs until asset is available for use)?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Asset Category.enable_cwip_accounting"),
		_q(s, section, None, "What types of costs are capitalized during construction?", "Multi Select", options="Material\nLabour\nContractor Services\nOverheads\nBorrowing Costs"),
		_q(s, section, None, "When is a CWIP asset transferred to the fixed asset register?", "Single Select", options="On completion certificate\nOn available-for-use date\nOther"),
		_q(s, section, None, "Do you need to track CWIP by project?", "Single Select", options="Yes\nNo"),
	])

	# Section 9: Asset Capitalization (Composite Assets)
	s = 9
	section = "Asset Capitalization (Composite Assets)"
	questions.extend([
		_q(s, section, None, "Do you create composite assets from multiple components (stock items + existing assets + services)?", "Single Select", options="Yes\nNo", erp_ref="Asset Capitalization"),
		_q(s, section, None, "Do you consume stock/inventory items during asset construction?", "Single Select", options="Yes\nNo", erp_ref="Asset Capitalization Stock Item"),
		_q(s, section, None, "Do you merge existing assets into a new composite asset?", "Single Select", options="Yes\nNo", erp_ref="Asset Capitalization Asset Item"),
		_q(s, section, None, "Do you include service/contractor expenses in the capitalized cost?", "Single Select", options="Yes\nNo", erp_ref="Asset Capitalization Service Item"),
		_q(s, section, None, "How do you determine the value of consumed stock items?", "Single Select", options="Warehouse valuation rate\nManual entry\nNot applicable"),
	])

	# Section 10: Asset Maintenance
	s = 10
	section = "Asset Maintenance"
	questions.extend([
		_q(s, section, None, "Do you perform preventive maintenance on assets?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Asset Maintenance"),
		_q(s, section, None, "What types of maintenance do you perform?", "Multi Select", options="Preventive Maintenance\nCalibration\nSafety Inspection\nCleaning\nSoftware Updates", erp_ref="Asset Maintenance Task.maintenance_type"),
		_q(s, section, None, "Do you need scheduled maintenance with recurring periodicities?", "Single Select", options="Yes\nNo", erp_ref="Asset Maintenance Task.periodicity"),
		_q(s, section, None, "What periodicities are needed?", "Multi Select", options="Daily\nWeekly\nMonthly\nQuarterly\nHalf-yearly\nYearly\n2 Yearly\n3 Yearly", erp_ref="Asset Maintenance Task.periodicity"),
		_q(s, section, None, "Do you assign maintenance to specific teams or individuals?", "Single Select", options="Teams\nIndividuals\nBoth", erp_ref="Asset Maintenance Team"),
		_q(s, section, None, "Do you require maintenance completion certificates?", "Single Select", options="Yes\nNo", erp_ref="Asset Maintenance Task.certificate_required"),
		_q(s, section, None, "Do you need overdue maintenance alerts/notifications?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you track maintenance history/logs?", "Single Select", options="Yes\nNo", erp_ref="Asset Maintenance Log"),
	])

	# Section 11: Asset Repair
	s = 11
	section = "Asset Repair"
	questions.extend([
		_q(s, section, None, "Do you track asset repairs separately from maintenance?", "Single Select", options="Yes\nNo", erp_ref="Asset Repair"),
		_q(s, section, None, "Do you consume stock/spare parts during repairs?", "Single Select", options="Yes\nNo", erp_ref="Asset Repair.stock_consumption"),
		_q(s, section, None, "Should repair costs be capitalized (added to asset value)?", "Single Select", options="Always\nSometimes\nNever", erp_ref="Asset Repair.capitalize_repair_cost"),
		_q(s, section, None, "Can repairs extend the useful life of an asset?", "Single Select", options="Yes\nNo", erp_ref="Asset Repair.increase_in_asset_life"),
		_q(s, section, None, "Do you track asset downtime during repairs?", "Single Select", options="Yes\nNo", erp_ref="Asset Repair.downtime"),
		_q(s, section, None, "Do repairs need to be linked to Purchase Invoices for cost tracking?", "Single Select", options="Yes\nNo", erp_ref="Asset Repair.purchase_invoice"),
	])

	# Section 12: Asset Movement & Transfer
	s = 12
	section = "Asset Movement & Transfer"
	questions.extend([
		_q(s, section, None, "Do you transfer assets between locations?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Asset Movement"),
		_q(s, section, None, "Do you transfer asset custody between employees?", "Single Select", options="Yes\nNo", erp_ref="Asset Movement Item.to_employee"),
		_q(s, section, None, "What triggers an asset movement?", "Multi Select", options="Department transfer\nOffice relocation\nProject assignment\nEmployee change\nRepair / maintenance"),
		_q(s, section, None, "Do asset movements need approval before execution?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need a full audit trail of all asset movements?", "Single Select", options="Yes\nNo", erp_ref="Asset Activity"),
	])

	# Section 13: Asset Disposal — Sale & Scrap
	s = 13
	section = "Asset Disposal — Sale & Scrap"
	questions.extend([
		_q(s, section, None, "How do you typically dispose of assets?", "Multi Select", options="Sale to third party\nInternal transfer\nScrapping / write-off\nDonation\nTrade-in", priority="Important"),
		_q(s, section, None, "For asset sales, do you create a Sales Invoice?", "Single Select", options="Yes\nNo", erp_ref="Sales Invoice"),
		_q(s, section, None, "Do you need to track gain/loss on disposal?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "What account should disposal gain/loss be posted to?", "Text"),
		_q(s, section, None, "Do asset disposals need approval?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need to track reason for scrapping?", "Single Select", options="Yes\nNo"),
	])

	# Section 14: Asset Value Adjustment & Impairment
	s = 14
	section = "Asset Value Adjustment & Impairment"
	questions.extend([
		_q(s, section, None, "Do you perform asset revaluations or impairment assessments?", "Single Select", options="Yes\nNo", erp_ref="Asset Value Adjustment"),
		_q(s, section, None, "How often are revaluations done?", "Single Select", options="Annually\nAs needed\nNever"),
		_q(s, section, None, "Do you need to record impairment losses?", "Single Select", options="Yes\nNo", erp_ref="Asset Value Adjustment"),
		_q(s, section, None, "Should value adjustments automatically create journal entries?", "Single Select", options="Yes\nNo"),
	])

	# Section 15: Asset Insurance
	s = 15
	section = "Asset Insurance"
	questions.extend([
		_q(s, section, None, "Do you insure your fixed assets?", "Single Select", options="Yes\nNo", erp_ref="Asset.policy_number"),
		_q(s, section, None, "Do you need to track insurance details per asset (policy number, insurer, insured value)?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need alerts for insurance policy expiry?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Is the insured value the same as the book value or a separate valuation?", "Single Select", options="Same as book value\nSeparate valuation\nReplacement cost"),
	])

	# Section 16: Fixed Asset Register & Reporting
	s = 16
	section = "Fixed Asset Register & Reporting"
	questions.extend([
		_q(s, section, None, "Which asset reports do you need?", "Multi Select", options="Fixed Asset Register\nDepreciation Schedule\nAsset Movement History\nMaintenance Schedule\nAsset Activity Log\nCategory-wise Summary", priority="Important"),
		_q(s, section, None, "Do you need reports filtered by location, department, or custodian?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need asset barcode/QR code labels for physical verification?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you perform periodic physical asset verification?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "If yes, how often?", "Single Select", options="Monthly\nQuarterly\nAnnually\nAd-hoc"),
		_q(s, section, None, "Do you need consolidated asset reports across multiple companies?", "Single Select", options="Yes\nNo"),
	])

	# Section 17: Roles & Permissions
	s = 17
	section = "Roles & Permissions"
	questions.extend([
		_q(s, section, None, "How many users will manage assets?", "Text", priority="Important"),
		_q(s, section, None, "List the asset management roles needed (e.g. Asset Manager, Asset User, Maintenance User, Auditor).", "Text", priority="Important"),
		_q(s, section, None, "Should asset creation be restricted to certain roles?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should depreciation posting be restricted?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should asset disposal be restricted to certain roles?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do auditors need read-only access to the asset register?", "Single Select", options="Yes\nNo"),
	])

	# Section 18: Opening Balances & Migration
	s = 18
	section = "Opening Balances & Migration"
	questions.extend([
		_q(s, section, None, "Do you have existing assets to migrate into the system?", "Single Select", options="Yes\nNo", required=1, priority="Critical"),
		_q(s, section, None, "Approximately how many assets need to be migrated?", "Text"),
		_q(s, section, None, "What data is available for each existing asset?", "Multi Select", options="Purchase date\nPurchase cost\nAccumulated depreciation\nCurrent book value\nLocation\nCustodian\nSerial / tag number\nWarranty info"),
		_q(s, section, None, "What format is the existing asset register in?", "Single Select", options="Excel\nCSV\nLegacy system export\nPaper records"),
		_q(s, section, None, "Do existing assets have remaining useful life to continue depreciating?", "Single Select", options="Yes\nNo", erp_ref="Asset.is_existing_asset"),
		_q(s, section, None, "What is the cutover date for asset migration?", "Text", priority="Critical"),
	])

	# Section 19: Integrations & Automation
	s = 19
	section = "Integrations & Automation"
	questions.extend([
		_q(s, section, None, "Do you need automatic depreciation posting (no manual intervention)?", "Single Select", options="Yes\nNo", erp_ref="Accounts Settings"),
		_q(s, section, None, "Do you need email notifications for maintenance due dates?", "Single Select", options="Yes\nNo", erp_ref="Notification"),
		_q(s, section, None, "Do you need email notifications for insurance expiry?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need integration with a barcode/RFID system for asset tracking?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Any integration with facility management or IoT systems?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Any other asset-related integrations needed?", "Text"),
	])

	# Section 20: Parking Lot & Open Items
	s = 20
	section = "Parking Lot & Open Items"
	questions.extend([
		_q(s, section, None, "List any asset management requirements not covered above.", "Text"),
		_q(s, section, None, "Any known pain points with the current asset tracking process?", "Text", priority="Important"),
		_q(s, section, None, "Any compliance or regulatory requirements for asset management (e.g. IFRS 16, IAS 16)?", "Text"),
		_q(s, section, None, "Timeline constraints for asset module go-live?", "Text", priority="Important"),
		_q(s, section, None, "Any additional notes or comments?", "Text"),
	])

	return questions


def seed_buying_template():
	"""Create the comprehensive Buying BRD template."""
	template = frappe.new_doc("BRD Module Template")
	template.template_name = "Buying BRD v1.0"
	template.module_name = "Buying"
	template.version = "1.0"
	template.description = "Comprehensive Business Requirements Document for ERPNext Buying module implementation. Covers 18 sections including procurement cycle, supplier management, RFQ, purchase orders, subcontracting, supplier scorecards, and more."
	template.is_active = 1

	questions = get_buying_questions()
	for q in questions:
		template.append("questions", q)

	template.insert(ignore_permissions=True)
	frappe.db.commit()


def get_buying_questions():
	"""Return the full list of Buying BRD questions."""
	questions = []

	# Section 1: Procurement Policy & Overview
	s = 1
	section = "Procurement Policy & Overview"
	questions.extend([
		_q(s, section, None, "Does your organization have a formal procurement policy?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "Approximately how many active suppliers do you work with?", "Text", priority="Important"),
		_q(s, section, None, "Approximately how many purchase orders are raised per month?", "Text"),
		_q(s, section, None, "What is the current procurement process (manual, spreadsheet, legacy system)?", "Text", priority="Important"),
		_q(s, section, None, "Do you have a centralized or decentralized purchasing function?", "Single Select", options="Centralized\nDecentralized\nHybrid"),
		_q(s, section, None, "What types of purchases do you make?", "Multi Select", options="Raw Materials\nFinished Goods\nServices\nCapital Equipment\nConsumables\nSubcontracting", priority="Critical"),
	])

	# Section 2: Supplier Management
	s = 2
	section = "Supplier Management"
	questions.extend([
		_q(s, section, None, "How do you classify suppliers?", "Text", erp_ref="Supplier Group"),
		_q(s, section, None, "List your supplier groups/categories.", "Text", required=1, erp_ref="Supplier Group"),
		_q(s, section, None, "Do you track supplier type (Company, Individual, Partnership)?", "Single Select", options="Yes\nNo", erp_ref="Supplier.supplier_type"),
		_q(s, section, None, "Do you maintain preferred/approved supplier lists per item?", "Single Select", options="Yes\nNo", erp_ref="Item Supplier"),
		_q(s, section, None, "Do you need to block/hold suppliers (e.g. for non-compliance)?", "Single Select", options="Yes\nNo", erp_ref="Supplier.on_hold"),
		_q(s, section, None, "If yes, what hold types are needed?", "Multi Select", options="Block all transactions\nBlock invoices only\nBlock payments only", erp_ref="Supplier.hold_type"),
		_q(s, section, None, "Do you track supplier lead times per item?", "Single Select", options="Yes\nNo", erp_ref="Item Supplier.lead_time_days"),
		_q(s, section, None, "Do you need a supplier self-service portal?", "Single Select", options="Yes\nNo", erp_ref="Supplier.portal_users"),
		_q(s, section, None, "Do you have internal suppliers (inter-company procurement)?", "Single Select", options="Yes\nNo", erp_ref="Supplier.is_internal_supplier"),
	])

	# Section 3: Supplier Scorecards
	s = 3
	section = "Supplier Scorecards & Evaluation"
	questions.extend([
		_q(s, section, None, "Do you evaluate supplier performance?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Supplier Scorecard"),
		_q(s, section, None, "What KPIs do you use for supplier evaluation?", "Multi Select", options="On-time Delivery\nQuality / Defect Rate\nPricing Competitiveness\nResponsiveness\nCompliance\nCustom Criteria"),
		_q(s, section, None, "How often are supplier evaluations performed?", "Single Select", options="Weekly\nMonthly\nQuarterly\nAnnually", erp_ref="Supplier Scorecard.period"),
		_q(s, section, None, "Should poor-performing suppliers be automatically blocked from new POs/RFQs?", "Single Select", options="Yes - block\nYes - warn only\nNo", erp_ref="Supplier.prevent_pos"),
		_q(s, section, None, "Do you need supplier scorecard reports for management review?", "Single Select", options="Yes\nNo"),
	])

	# Section 4: Material Requests
	s = 4
	section = "Material Requests & Requisitions"
	questions.extend([
		_q(s, section, None, "Do you use formal material/purchase requisitions?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Material Request"),
		_q(s, section, None, "What types of material requests do you raise?", "Multi Select", options="Purchase\nMaterial Transfer\nMaterial Issue\nManufacture\nCustomer Provided", erp_ref="Material Request.material_request_type"),
		_q(s, section, None, "Do material requests need approval before conversion to PO?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "If yes, describe the approval levels (e.g. amount thresholds, roles).", "Text"),
		_q(s, section, None, "Should material requests be auto-created when stock falls below reorder level?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.auto_indent"),
		_q(s, section, None, "Do you need to consolidate multiple material requests into a single PO?", "Single Select", options="Yes\nNo"),
	])

	# Section 5: Request for Quotation (RFQ)
	s = 5
	section = "Request for Quotation (RFQ)"
	questions.extend([
		_q(s, section, None, "Do you send RFQs to suppliers before placing orders?", "Single Select", options="Always\nSometimes\nNever", erp_ref="Request for Quotation"),
		_q(s, section, None, "How many suppliers do you typically invite per RFQ?", "Text"),
		_q(s, section, None, "Do you need to email RFQs directly from the system?", "Single Select", options="Yes\nNo", erp_ref="Request for Quotation.send_email"),
		_q(s, section, None, "Do you need to attach documents (specs, drawings) to RFQs?", "Single Select", options="Yes\nNo", erp_ref="Request for Quotation.send_attached_files"),
		_q(s, section, None, "Do you need side-by-side supplier quotation comparison?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should suppliers respond via a portal or email?", "Single Select", options="Portal\nEmail\nBoth"),
	])

	# Section 6: Supplier Quotations
	s = 6
	section = "Supplier Quotations"
	questions.extend([
		_q(s, section, None, "Do you track supplier quotations in a system?", "Single Select", options="Yes\nNo", erp_ref="Supplier Quotation"),
		_q(s, section, None, "Do you need to track quotation validity/expiry dates?", "Single Select", options="Yes\nNo", erp_ref="Supplier Quotation.valid_till"),
		_q(s, section, None, "Do you track supplier-specific part numbers?", "Single Select", options="Yes\nNo", erp_ref="Supplier Quotation Item.supplier_part_no"),
		_q(s, section, None, "Do you need to track lead times per quotation item?", "Single Select", options="Yes\nNo", erp_ref="Supplier Quotation Item.lead_time_days"),
	])

	# Section 7: Purchase Orders
	s = 7
	section = "Purchase Orders"
	questions.extend([
		_q(s, section, None, "Is a Purchase Order mandatory before receiving goods?", "Single Select", options="Yes\nNo", required=1, priority="Critical", erp_ref="Buying Settings.po_required"),
		_q(s, section, None, "Is a Purchase Order mandatory before creating a Purchase Invoice?", "Single Select", options="Yes\nNo", erp_ref="Buying Settings.po_required"),
		_q(s, section, None, "Do purchase orders need approval workflows?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "If yes, describe the approval levels (e.g. amount thresholds, roles).", "Text"),
		_q(s, section, None, "Do you track the customer PO/order confirmation number on purchase orders?", "Single Select", options="Yes\nNo", erp_ref="Purchase Order.order_confirmation_no"),
		_q(s, section, None, "Do you need to set expected delivery dates per line item?", "Single Select", options="Yes\nNo", erp_ref="Purchase Order Item.expected_delivery_date"),
		_q(s, section, None, "Should the system enforce rate consistency from quotation through to invoice?", "Single Select", options="Yes - Stop\nYes - Warn only\nNo", erp_ref="Buying Settings.maintain_same_rate"),
		_q(s, section, None, "Do you use drop shipping (supplier ships directly to customer)?", "Single Select", options="Yes\nNo", erp_ref="Purchase Order.drop_ship"),
		_q(s, section, None, "Do you need to place POs on hold?", "Single Select", options="Yes\nNo"),
	])

	# Section 8: Purchase Receipt & Goods Receipt
	s = 8
	section = "Purchase Receipt & Goods Receipt"
	questions.extend([
		_q(s, section, None, "Is a Purchase Receipt mandatory before creating a Purchase Invoice?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Buying Settings.pr_required"),
		_q(s, section, None, "Do you need 3-way matching (PO → Receipt → Invoice)?", "Single Select", options="Yes\nNo", priority="Critical"),
		_q(s, section, None, "Do you have a separate goods receiving / warehouse team?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you inspect goods on receipt (quality inspection)?", "Single Select", options="Always\nSometimes\nNever"),
		_q(s, section, None, "Do you need to handle partial receipts against a PO?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you accept over-delivery above PO quantity?", "Single Select", options="Yes - with tolerance %\nNo - strict", erp_ref="Stock Settings.over_delivery_receipt_allowance"),
		_q(s, section, None, "Do you have a rejected goods warehouse?", "Single Select", options="Yes\nNo", erp_ref="Purchase Receipt.rejected_warehouse"),
		_q(s, section, None, "Should rejected quantity be billed?", "Single Select", options="Yes\nNo", erp_ref="Buying Settings.bill_for_rejected_quantity_in_purchase_invoice"),
	])

	# Section 9: Blanket Orders & Contracts
	s = 9
	section = "Blanket Orders & Contracts"
	questions.extend([
		_q(s, section, None, "Do you use blanket orders / framework agreements with suppliers?", "Single Select", options="Yes\nNo", erp_ref="Blanket Order"),
		_q(s, section, None, "If yes, are they based on quantity, value, or time period?", "Multi Select", options="Quantity-based\nValue-based\nTime-period based"),
		_q(s, section, None, "What overage allowance (%) should be permitted against blanket orders?", "Text", erp_ref="Buying Settings.blanket_order_allowance"),
		_q(s, section, None, "Do you need to track contract expiry and renewal dates?", "Single Select", options="Yes\nNo"),
	])

	# Section 10: Subcontracting
	s = 10
	section = "Subcontracting"
	questions.extend([
		_q(s, section, None, "Do you subcontract any manufacturing/processing work to suppliers?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Purchase Order.is_subcontracted"),
		_q(s, section, None, "If yes, describe the subcontracting process.", "Text"),
		_q(s, section, None, "Do you supply raw materials to the subcontractor?", "Single Select", options="Yes\nNo", erp_ref="Purchase Order Item Supplied"),
		_q(s, section, None, "How should raw material consumption be calculated?", "Single Select", options="Based on BOM\nBased on Material Transferred\nManual", erp_ref="Buying Settings.backflush_raw_materials_of_subcontract_based_on"),
		_q(s, section, None, "Do you need to track raw materials at the supplier's warehouse?", "Single Select", options="Yes\nNo", erp_ref="Purchase Order.supplier_warehouse"),
		_q(s, section, None, "What over-transfer allowance (%) for raw materials to subcontractors?", "Text", erp_ref="Buying Settings.over_transfer_allowance"),
		_q(s, section, None, "Should subcontracting orders be auto-created from Purchase Orders?", "Single Select", options="Yes\nNo", erp_ref="Buying Settings.auto_create_subcontracting_order"),
	])

	# Section 11: Purchase Pricing & Taxes
	s = 11
	section = "Purchase Pricing & Taxes"
	questions.extend([
		_q(s, section, None, "Do you maintain a buying price list?", "Single Select", options="Yes\nNo", erp_ref="Buying Settings.buying_price_list"),
		_q(s, section, None, "Do you need supplier-specific pricing?", "Single Select", options="Yes\nNo", erp_ref="Item Price"),
		_q(s, section, None, "Do you track the last purchase rate per item?", "Single Select", options="Yes\nNo", erp_ref="Buying Settings.disable_last_purchase_rate"),
		_q(s, section, None, "Do you need dynamic pricing rules (volume discounts, date-based pricing)?", "Single Select", options="Yes\nNo", erp_ref="Pricing Rule"),
		_q(s, section, None, "Do you use purchase tax templates?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Purchase Taxes and Charges Template"),
		_q(s, section, None, "List the tax types applied on purchases (e.g. VAT 5%, Import Duty, Withholding Tax).", "Text", priority="Critical"),
		_q(s, section, None, "Do you need Tax Deducted at Source (TDS / withholding tax)?", "Single Select", options="Yes\nNo", erp_ref="Tax Withholding Category"),
		_q(s, section, None, "Do you use Incoterms for international purchases?", "Single Select", options="Yes\nNo", erp_ref="Purchase Order.incoterm"),
	])

	# Section 12: Landed Cost
	s = 12
	section = "Landed Cost"
	questions.extend([
		_q(s, section, None, "Do you need to allocate freight, customs duty, or other charges to purchase cost?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Landed Cost Voucher"),
		_q(s, section, None, "What types of additional costs are allocated?", "Multi Select", options="Freight / Shipping\nCustoms Duty\nInsurance\nHandling Charges\nInspection Fees\nOther"),
		_q(s, section, None, "How should charges be distributed across items?", "Single Select", options="By Quantity\nBy Amount\nManual allocation", erp_ref="Landed Cost Voucher.distribute_charges_based_on"),
		_q(s, section, None, "Should landed cost be automatically set based on Purchase Invoice rate?", "Single Select", options="Yes\nNo", erp_ref="Buying Settings.set_landed_cost_based_on_purchase_invoice_rate"),
	])

	# Section 13: Multi-Currency Purchasing
	s = 13
	section = "Multi-Currency Purchasing"
	questions.extend([
		_q(s, section, None, "Do you purchase in multiple currencies?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "If yes, list all purchase currencies.", "Text"),
		_q(s, section, None, "Should exchange rates be based on transaction date or posting date?", "Single Select", options="Transaction Date\nPosting Date", erp_ref="Buying Settings.use_transaction_date_exchange_rate"),
		_q(s, section, None, "Do you use a separate price list currency vs. transaction currency?", "Single Select", options="Yes\nNo"),
	])

	# Section 14: Purchase Returns
	s = 14
	section = "Purchase Returns"
	questions.extend([
		_q(s, section, None, "Do you return goods to suppliers?", "Single Select", options="Yes\nNo", erp_ref="Purchase Receipt.is_return"),
		_q(s, section, None, "How are returns processed (debit note, credit note, replacement)?", "Multi Select", options="Debit Note to Supplier\nCredit Note\nReplacement\nReturn to stock"),
		_q(s, section, None, "Do returns need approval?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need to track reasons for returns?", "Single Select", options="Yes\nNo"),
	])

	# Section 15: Procurement Reporting
	s = 15
	section = "Procurement Reporting"
	questions.extend([
		_q(s, section, None, "Which procurement reports do you need?", "Multi Select", options="Purchase Analytics\nPurchase Order Trends\nProcurement Tracker\nSupplier Quotation Comparison\nItem-wise Purchase History\nPending Items to Order\nSubcontracted Items to Receive\nSupplier Scorecard Summary", priority="Important"),
		_q(s, section, None, "Do you need reports on delayed deliveries from suppliers?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need spend analysis by supplier, item group, or cost centre?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need purchase budget vs. actual reports?", "Single Select", options="Yes\nNo"),
	])

	# Section 16: Roles & Permissions
	s = 16
	section = "Roles & Permissions"
	questions.extend([
		_q(s, section, None, "How many users will use the buying module?", "Text", priority="Important"),
		_q(s, section, None, "List the procurement roles needed (e.g. Purchase Manager, Purchase User, Store Keeper).", "Text", priority="Important"),
		_q(s, section, None, "Should PO creation be restricted to certain roles?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should only certain roles be able to approve purchase orders?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need amount-based approval limits per role?", "Single Select", options="Yes\nNo"),
	])

	# Section 17: Integrations & Automation
	s = 17
	section = "Integrations & Automation"
	questions.extend([
		_q(s, section, None, "Do you need email notifications for PO approval, receipt, or overdue deliveries?", "Single Select", options="Yes\nNo", erp_ref="Notification"),
		_q(s, section, None, "Do you need recurring/standing purchase orders?", "Single Select", options="Yes\nNo", erp_ref="Auto Repeat"),
		_q(s, section, None, "Do you need integration with any e-procurement or supplier portal?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need barcode scanning for goods receipt?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Any other procurement-related integrations needed?", "Text"),
	])

	# Section 18: Parking Lot & Open Items
	s = 18
	section = "Parking Lot & Open Items"
	questions.extend([
		_q(s, section, None, "List any procurement requirements not covered above.", "Text"),
		_q(s, section, None, "Any known pain points with the current procurement process?", "Text", priority="Important"),
		_q(s, section, None, "Any compliance or regulatory requirements for procurement?", "Text"),
		_q(s, section, None, "Timeline constraints for buying module go-live?", "Text", priority="Important"),
		_q(s, section, None, "Any additional notes or comments?", "Text"),
	])

	return questions


def seed_selling_template():
	"""Create the comprehensive Selling BRD template."""
	template = frappe.new_doc("BRD Module Template")
	template.template_name = "Selling BRD v1.0"
	template.module_name = "Selling"
	template.version = "1.0"
	template.description = "Comprehensive Business Requirements Document for ERPNext Selling module implementation. Covers 20 sections including sales cycle, customer management, quotations, sales orders, pricing, commissions, territories, and more."
	template.is_active = 1

	questions = get_selling_questions()
	for q in questions:
		template.append("questions", q)

	template.insert(ignore_permissions=True)
	frappe.db.commit()


def get_selling_questions():
	"""Return the full list of Selling BRD questions."""
	questions = []

	# Section 1: Sales Process Overview
	s = 1
	section = "Sales Process Overview"
	questions.extend([
		_q(s, section, None, "Describe your current sales process from lead to cash collection.", "Text", priority="Critical"),
		_q(s, section, None, "What types of sales does your company make?", "Multi Select", options="Product Sales\nService Sales\nProject-based Sales\nSubscription / Recurring\nE-commerce", priority="Important"),
		_q(s, section, None, "Approximately how many sales orders are processed per month?", "Text"),
		_q(s, section, None, "What is the current system used for sales management?", "Text"),
		_q(s, section, None, "Do you need different order types?", "Multi Select", options="Sales\nMaintenance\nShopping Cart (E-commerce)", erp_ref="Sales Order.order_type"),
	])

	# Section 2: Customer Management
	s = 2
	section = "Customer Management"
	questions.extend([
		_q(s, section, None, "Approximately how many active customers do you have?", "Text", priority="Important"),
		_q(s, section, None, "How do you classify customers?", "Text", erp_ref="Customer Group"),
		_q(s, section, None, "List your customer groups/categories.", "Text", required=1, erp_ref="Customer Group"),
		_q(s, section, None, "Do you need hierarchical customer groups?", "Single Select", options="Yes\nNo", erp_ref="Customer Group.is_group"),
		_q(s, section, None, "Do you track customer type (Company, Individual, Partnership)?", "Single Select", options="Yes\nNo", erp_ref="Customer.customer_type"),
		_q(s, section, None, "Do you need customer credit limits?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Customer Credit Limit"),
		_q(s, section, None, "If yes, are credit limits per company or global?", "Single Select", options="Per Company\nGlobal\nNot applicable"),
		_q(s, section, None, "Do you have internal customers (inter-company sales)?", "Single Select", options="Yes\nNo", erp_ref="Customer.is_internal_customer"),
		_q(s, section, None, "Do you need a customer self-service portal?", "Single Select", options="Yes\nNo", erp_ref="Customer.portal_users"),
		_q(s, section, None, "Do you need to restrict specific items per customer?", "Single Select", options="Yes\nNo", erp_ref="Party Specific Item"),
	])

	# Section 3: Territory Management
	s = 3
	section = "Territory Management"
	questions.extend([
		_q(s, section, None, "Do you organize customers by territory/region?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Territory"),
		_q(s, section, None, "List your territories/regions.", "Text", erp_ref="Territory"),
		_q(s, section, None, "Do you need a hierarchical territory structure?", "Single Select", options="Yes\nNo", erp_ref="Territory.parent_territory"),
		_q(s, section, None, "Do you assign territory managers?", "Single Select", options="Yes\nNo", erp_ref="Territory.territory_manager"),
		_q(s, section, None, "Do you set sales targets by territory?", "Single Select", options="Yes\nNo"),
	])

	# Section 4: Quotations
	s = 4
	section = "Quotations"
	questions.extend([
		_q(s, section, None, "Do you issue formal quotations to customers?", "Single Select", options="Always\nSometimes\nNever", priority="Important", erp_ref="Quotation"),
		_q(s, section, None, "Can quotations be sent to leads (not yet customers)?", "Single Select", options="Yes\nNo", erp_ref="Quotation.quotation_to"),
		_q(s, section, None, "Do you track quotation validity/expiry dates?", "Single Select", options="Yes\nNo", erp_ref="Quotation.valid_till"),
		_q(s, section, None, "Do you need to track lost quotations with reasons?", "Single Select", options="Yes\nNo", erp_ref="Quotation.lost_reasons"),
		_q(s, section, None, "Do you track competitors on quotations?", "Single Select", options="Yes\nNo", erp_ref="Quotation.competitors"),
		_q(s, section, None, "Do quotations need approval before sending to customer?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should expired quotations be allowed to convert to Sales Orders?", "Single Select", options="Yes\nNo", erp_ref="Selling Settings.allow_sales_order_creation_for_expired_quotation"),
	])

	# Section 5: Sales Orders
	s = 5
	section = "Sales Orders"
	questions.extend([
		_q(s, section, None, "Is a Sales Order mandatory before creating a Delivery Note?", "Single Select", options="Yes\nNo", priority="Critical", erp_ref="Selling Settings.so_required"),
		_q(s, section, None, "Is a Delivery Note mandatory before creating a Sales Invoice?", "Single Select", options="Yes\nNo", priority="Critical", erp_ref="Selling Settings.dn_required"),
		_q(s, section, None, "Do Sales Orders need approval workflows?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "If yes, describe the approval levels (e.g. amount thresholds, roles).", "Text"),
		_q(s, section, None, "Do you track customer PO numbers on Sales Orders?", "Single Select", options="Yes\nNo", erp_ref="Sales Order.po_no"),
		_q(s, section, None, "Do you need to allow multiple Sales Orders against a single customer PO?", "Single Select", options="Yes\nNo", erp_ref="Selling Settings.allow_against_multiple_purchase_orders"),
		_q(s, section, None, "Do you need delivery date tracking per line item?", "Single Select", options="Yes\nNo", erp_ref="Sales Order Item.delivery_date"),
		_q(s, section, None, "Do you skip delivery notes for any order types (direct invoice)?", "Single Select", options="Yes\nNo", erp_ref="Sales Order.skip_delivery_note"),
		_q(s, section, None, "Do you need to close/re-open Sales Orders?", "Single Select", options="Yes\nNo"),
	])

	# Section 6: Pricing & Discounts
	s = 6
	section = "Pricing & Discounts"
	questions.extend([
		_q(s, section, None, "Do you maintain a selling price list?", "Single Select", options="Yes\nNo", required=1, erp_ref="Selling Settings.selling_price_list"),
		_q(s, section, None, "Do you need multiple selling price lists (e.g. Retail, Wholesale, Export)?", "Single Select", options="Yes\nNo", erp_ref="Price List"),
		_q(s, section, None, "Do you need customer-specific pricing?", "Single Select", options="Yes\nNo", erp_ref="Item Price"),
		_q(s, section, None, "Do you need customer group-level pricing?", "Single Select", options="Yes\nNo", erp_ref="Pricing Rule"),
		_q(s, section, None, "Do you use dynamic pricing rules (volume discounts, date-based, coupon codes)?", "Single Select", options="Yes\nNo", erp_ref="Pricing Rule"),
		_q(s, section, None, "If yes, describe your discount/pricing rule structure.", "Text"),
		_q(s, section, None, "Do you offer free items (buy X get Y free)?", "Single Select", options="Yes\nNo", erp_ref="Pricing Rule"),
		_q(s, section, None, "Do you use margin-based pricing (cost + margin)?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should the system validate that selling price is above purchase/valuation rate?", "Single Select", options="Yes\nNo", erp_ref="Selling Settings.validate_selling_price"),
		_q(s, section, None, "Should price list rates be editable on transactions?", "Single Select", options="Yes\nNo", erp_ref="Selling Settings.editable_price_list_rate"),
		_q(s, section, None, "Should the system enforce rate consistency from quotation through to invoice?", "Single Select", options="Yes - Stop\nYes - Warn only\nNo", erp_ref="Selling Settings.maintain_same_rate"),
	])

	# Section 7: Product Bundles
	s = 7
	section = "Product Bundles"
	questions.extend([
		_q(s, section, None, "Do you sell product bundles/kits (a set of items sold as one)?", "Single Select", options="Yes\nNo", erp_ref="Product Bundle"),
		_q(s, section, None, "If yes, should bundle component rates be editable?", "Single Select", options="Yes\nNo", erp_ref="Selling Settings.editable_bundle_item_rates"),
		_q(s, section, None, "List your product bundles if known.", "Text"),
	])

	# Section 8: Blanket Orders
	s = 8
	section = "Blanket Orders & Contracts"
	questions.extend([
		_q(s, section, None, "Do you use blanket orders / framework agreements with customers?", "Single Select", options="Yes\nNo", erp_ref="Blanket Order"),
		_q(s, section, None, "If yes, are they based on quantity, value, or time period?", "Multi Select", options="Quantity-based\nValue-based\nTime-period based"),
		_q(s, section, None, "What overage allowance (%) should be permitted?", "Text", erp_ref="Selling Settings.blanket_order_allowance"),
	])

	# Section 9: Sales Taxes & Charges
	s = 9
	section = "Sales Taxes & Charges"
	questions.extend([
		_q(s, section, None, "List the tax types applied on sales (e.g. VAT 5%, Zero-rated, Exempt).", "Text", required=1, priority="Critical", erp_ref="Sales Taxes and Charges Template"),
		_q(s, section, None, "Do you need separate tax templates per customer or item category?", "Single Select", options="Yes\nNo", erp_ref="Tax Category"),
		_q(s, section, None, "Do you use shipping rules to auto-calculate freight?", "Single Select", options="Yes\nNo", erp_ref="Shipping Rule"),
		_q(s, section, None, "Do you use Incoterms for international sales?", "Single Select", options="Yes\nNo", erp_ref="Sales Order.incoterm"),
		_q(s, section, None, "Do you need Tax Deducted at Source (TDS / withholding tax) on sales?", "Single Select", options="Yes\nNo", erp_ref="Tax Withholding Category"),
	])

	# Section 10: Sales Commission & Partners
	s = 10
	section = "Sales Commission & Partners"
	questions.extend([
		_q(s, section, None, "Do you have internal sales personnel who earn commissions?", "Single Select", options="Yes\nNo", erp_ref="Sales Person"),
		_q(s, section, None, "Do you have external sales partners (agents, dealers, resellers)?", "Single Select", options="Yes\nNo", erp_ref="Sales Partner"),
		_q(s, section, None, "How is commission calculated?", "Single Select", options="Fixed %\nVariable by item\nTiered / slab-based\nNot applicable"),
		_q(s, section, None, "Can multiple salespeople share commission on a single order?", "Single Select", options="Yes\nNo", erp_ref="Sales Team"),
		_q(s, section, None, "Do you set sales targets for salespeople or territories?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "List your sales partner types if applicable (Distributor, Agent, Dealer, etc.).", "Text", erp_ref="Sales Partner Type"),
	])

	# Section 11: Delivery & Fulfillment
	s = 11
	section = "Delivery & Fulfillment"
	questions.extend([
		_q(s, section, None, "Do you use Delivery Notes to track goods dispatch?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Delivery Note"),
		_q(s, section, None, "Do you need partial deliveries against a Sales Order?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you use drop shipping (supplier ships directly to customer)?", "Single Select", options="Yes\nNo", erp_ref="Sales Order Item.delivered_by_supplier"),
		_q(s, section, None, "Do you need stock reservation for confirmed orders?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Sales Order.reserve_stock"),
		_q(s, section, None, "Do you track installation after delivery?", "Single Select", options="Yes\nNo", erp_ref="Installation Note"),
		_q(s, section, None, "Do you need packing slips for shipments?", "Single Select", options="Yes\nNo", erp_ref="Packing Slip"),
		_q(s, section, None, "Do you need to manage shipping / delivery trips?", "Single Select", options="Yes\nNo", erp_ref="Delivery Trip"),
	])

	# Section 12: Sales Returns
	s = 12
	section = "Sales Returns"
	questions.extend([
		_q(s, section, None, "Do customers return goods?", "Single Select", options="Yes\nNo", erp_ref="Delivery Note.is_return"),
		_q(s, section, None, "How are returns processed?", "Multi Select", options="Credit Note\nReplacement\nReturn to stock\nRefund"),
		_q(s, section, None, "Should a credit note be auto-created on return?", "Single Select", options="Yes\nNo", erp_ref="Delivery Note.issue_credit_note"),
		_q(s, section, None, "Do returns need approval?", "Single Select", options="Yes\nNo"),
	])

	# Section 13: Multi-Currency Sales
	s = 13
	section = "Multi-Currency Sales"
	questions.extend([
		_q(s, section, None, "Do you sell in multiple currencies?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "If yes, list all selling currencies.", "Text"),
		_q(s, section, None, "Do customers have a default currency?", "Single Select", options="Yes\nNo", erp_ref="Customer.default_currency"),
	])

	# Section 14: Loyalty Programs
	s = 14
	section = "Loyalty Programs"
	questions.extend([
		_q(s, section, None, "Do you have a customer loyalty program?", "Single Select", options="Yes\nNo", erp_ref="Loyalty Program"),
		_q(s, section, None, "If yes, describe the loyalty structure (points, tiers, redemption).", "Text"),
		_q(s, section, None, "Do customers redeem loyalty points on orders?", "Single Select", options="Yes\nNo"),
	])

	# Section 15: Subscriptions & Recurring Sales
	s = 15
	section = "Subscriptions & Recurring Sales"
	questions.extend([
		_q(s, section, None, "Do you have recurring/subscription-based sales?", "Single Select", options="Yes\nNo", erp_ref="Subscription"),
		_q(s, section, None, "If yes, describe the billing patterns (monthly, quarterly, annual).", "Text"),
		_q(s, section, None, "Should recurring invoices/orders be auto-created?", "Single Select", options="Yes\nNo", erp_ref="Auto Repeat"),
	])

	# Section 16: CRM Integration
	s = 16
	section = "CRM Integration"
	questions.extend([
		_q(s, section, None, "Do you need CRM integration (Lead → Opportunity → Quotation)?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "Do you track marketing campaigns on sales transactions?", "Single Select", options="Yes\nNo", erp_ref="Quotation.campaign"),
		_q(s, section, None, "Do you need win/loss analysis on quotations?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you track the source of leads/sales?", "Single Select", options="Yes\nNo", erp_ref="Quotation.source"),
	])

	# Section 17: Sales Reporting
	s = 17
	section = "Sales Reporting"
	questions.extend([
		_q(s, section, None, "Which sales reports do you need?", "Multi Select", options="Sales Analytics\nSales Order Trends\nQuotation Trends\nTerritory-wise Sales\nSales Person Summary\nCustomer Acquisition & Loyalty\nInactive Customers\nSales Partner Commission\nPayment Terms Status\nCustomer Credit Balance\nLost Quotations", priority="Important"),
		_q(s, section, None, "Do you need sales target vs. actual reports?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need reports by sales person, territory, and customer group?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need custom sales dashboards?", "Single Select", options="Yes\nNo"),
	])

	# Section 18: Roles & Permissions
	s = 18
	section = "Roles & Permissions"
	questions.extend([
		_q(s, section, None, "How many users will use the selling module?", "Text", priority="Important"),
		_q(s, section, None, "List the sales roles needed (e.g. Sales Manager, Sales User, Sales Master Manager).", "Text", priority="Important"),
		_q(s, section, None, "Should quotation/SO creation be restricted by role?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should discount limits vary by role?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need data-level restrictions (e.g. salespeople see only their territory)?", "Single Select", options="Yes\nNo", erp_ref="User Permission"),
	])

	# Section 19: Integrations & Automation
	s = 19
	section = "Integrations & Automation"
	questions.extend([
		_q(s, section, None, "Do you need email notifications for quotation/SO events?", "Single Select", options="Yes\nNo", erp_ref="Notification"),
		_q(s, section, None, "Do you need e-commerce / shopping cart integration?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need SMS notifications for sales events?", "Single Select", options="Yes\nNo", erp_ref="SMS Center"),
		_q(s, section, None, "Any other sales-related integrations needed?", "Text"),
	])

	# Section 20: Parking Lot & Open Items
	s = 20
	section = "Parking Lot & Open Items"
	questions.extend([
		_q(s, section, None, "List any sales requirements not covered above.", "Text"),
		_q(s, section, None, "Any known pain points with the current sales process?", "Text", priority="Important"),
		_q(s, section, None, "Any compliance or regulatory requirements for sales?", "Text"),
		_q(s, section, None, "Timeline constraints for selling module go-live?", "Text", priority="Important"),
		_q(s, section, None, "Any additional notes or comments?", "Text"),
	])

	return questions


def seed_stock_template():
	"""Create the comprehensive Stock/Inventory BRD template."""
	template = frappe.new_doc("BRD Module Template")
	template.template_name = "Stock BRD v1.0"
	template.module_name = "Stock"
	template.version = "1.0"
	template.description = "Comprehensive Business Requirements Document for ERPNext Stock/Inventory module implementation. Covers 22 sections including item management, warehousing, valuation, serial/batch tracking, quality inspection, stock reconciliation, and more."
	template.is_active = 1

	questions = get_stock_questions()
	for q in questions:
		template.append("questions", q)

	template.insert(ignore_permissions=True)
	frappe.db.commit()


def get_stock_questions():
	"""Return the full list of Stock/Inventory BRD questions."""
	questions = []

	# Section 1: Inventory Overview
	s = 1
	section = "Inventory Overview"
	questions.extend([
		_q(s, section, None, "Describe your current inventory management process.", "Text", priority="Critical"),
		_q(s, section, None, "Approximately how many stock items (SKUs) do you manage?", "Text", priority="Important"),
		_q(s, section, None, "What types of items do you stock?", "Multi Select", options="Raw Materials\nFinished Goods\nWork in Progress\nConsumables\nSpare Parts\nPacking Materials\nServices (non-stock)", priority="Important"),
		_q(s, section, None, "What is the current system used for inventory management?", "Text"),
		_q(s, section, None, "Do you carry any non-stock items (services, digital products)?", "Single Select", options="Yes\nNo"),
	])

	# Section 2: Item Master & Classification
	s = 2
	section = "Item Master & Classification"
	questions.extend([
		_q(s, section, None, "How are items named/coded?", "Single Select", options="Item Code (manual)\nItem Name\nNaming Series (auto)\nBarcode-based", erp_ref="Stock Settings.item_naming_by"),
		_q(s, section, None, "What is your item naming convention? Describe the pattern.", "Text"),
		_q(s, section, None, "List your item groups/categories.", "Text", required=1, erp_ref="Item Group"),
		_q(s, section, None, "Do you need hierarchical item groups?", "Single Select", options="Yes\nNo", erp_ref="Item Group.is_group"),
		_q(s, section, None, "Do you classify items by brand?", "Single Select", options="Yes\nNo", erp_ref="Item.brand"),
		_q(s, section, None, "Do you need item-level images/photos?", "Single Select", options="Yes\nNo", erp_ref="Item.image"),
		_q(s, section, None, "Do you track manufacturer and manufacturer part number?", "Single Select", options="Yes\nNo", erp_ref="Item Manufacturer"),
		_q(s, section, None, "Do you need to set end-of-life dates for items?", "Single Select", options="Yes\nNo", erp_ref="Item.end_of_life"),
		_q(s, section, None, "Do you track HSN/SAC codes for tax purposes?", "Single Select", options="Yes\nNo", erp_ref="Item.gst_hsn_code"),
	])

	# Section 3: Item Variants
	s = 3
	section = "Item Variants"
	questions.extend([
		_q(s, section, None, "Do you have items with variants (e.g. same product in different sizes, colours)?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Item.has_variants"),
		_q(s, section, None, "If yes, what attributes define your variants?", "Text", erp_ref="Item Attribute"),
		_q(s, section, None, "Are variant attributes text-based (e.g. Red, Blue) or numeric ranges (e.g. 10mm-50mm)?", "Single Select", options="Text-based\nNumeric ranges\nBoth\nNot applicable", erp_ref="Item Attribute.numeric_values"),
		_q(s, section, None, "Do you need to allow alternative items when primary is out of stock?", "Single Select", options="Yes\nNo", erp_ref="Item.allow_alternative_item"),
	])

	# Section 4: Units of Measure (UOM)
	s = 4
	section = "Units of Measure (UOM)"
	questions.extend([
		_q(s, section, None, "What is your primary stock UOM for most items (e.g. Nos, Kg, Metre)?", "Text", required=1, erp_ref="Stock Settings.stock_uom"),
		_q(s, section, None, "Do you buy and sell in different UOMs than you store?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Item.purchase_uom"),
		_q(s, section, None, "If yes, list the UOM conversions needed (e.g. 1 Box = 12 Pcs, 1 Pallet = 48 Boxes).", "Text", erp_ref="UOM Conversion Detail"),
		_q(s, section, None, "Do you need weight tracking per item (weight per unit)?", "Single Select", options="Yes\nNo", erp_ref="Item.weight_per_unit"),
	])

	# Section 5: Warehouses & Storage
	s = 5
	section = "Warehouses & Storage"
	questions.extend([
		_q(s, section, None, "How many warehouses/storage locations do you have?", "Text", required=1, priority="Critical", erp_ref="Warehouse"),
		_q(s, section, None, "List your warehouses (name, type, location).", "Text", erp_ref="Warehouse"),
		_q(s, section, None, "Do you need a hierarchical warehouse structure (e.g. Site > Building > Zone)?", "Single Select", options="Yes\nNo", erp_ref="Warehouse.parent_warehouse"),
		_q(s, section, None, "Do you need different warehouse types (Raw Material, Finished Goods, Reject, Transit)?", "Single Select", options="Yes\nNo", erp_ref="Warehouse Type"),
		_q(s, section, None, "Do you need a separate rejected goods warehouse?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need in-transit warehouses for inter-location transfers?", "Single Select", options="Yes\nNo", erp_ref="Warehouse.default_in_transit_warehouse"),
		_q(s, section, None, "Do you need bin/location level tracking within a warehouse?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do warehouses map to specific GL accounts?", "Single Select", options="Yes\nNo", erp_ref="Warehouse.account"),
	])

	# Section 6: Stock Valuation
	s = 6
	section = "Stock Valuation"
	questions.extend([
		_q(s, section, None, "Which stock valuation method do you use?", "Single Select", options="FIFO (First In First Out)\nMoving Average\nLIFO (Last In First Out)", required=1, priority="Critical", erp_ref="Stock Settings.default_valuation_method"),
		_q(s, section, None, "Is the valuation method the same for all items, or does it vary?", "Single Select", options="Same for all\nVaries by item", erp_ref="Item.valuation_method"),
		_q(s, section, None, "Do you use perpetual inventory (every stock movement creates a GL entry)?", "Single Select", options="Yes - Perpetual\nNo - Periodic", priority="Critical", erp_ref="Company.enable_perpetual_inventory"),
		_q(s, section, None, "Do you need batch-wise valuation (different rates per batch)?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.do_not_use_batchwise_valuation"),
	])

	# Section 7: Serial Number Tracking
	s = 7
	section = "Serial Number Tracking"
	questions.extend([
		_q(s, section, None, "Do you track items by serial number?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Item.has_serial_no"),
		_q(s, section, None, "If yes, which item categories require serial tracking?", "Text"),
		_q(s, section, None, "Should serial numbers be auto-generated or manually entered?", "Single Select", options="Auto-generated\nManual\nBoth\nNot applicable", erp_ref="Item.serial_no_series"),
		_q(s, section, None, "Do you need to track warranty expiry per serial number?", "Single Select", options="Yes\nNo", erp_ref="Serial No.warranty_expiry_date"),
		_q(s, section, None, "Do you need to track AMC (Annual Maintenance Contract) per serial?", "Single Select", options="Yes\nNo", erp_ref="Serial No.amc_expiry_date"),
		_q(s, section, None, "Do you need to track which customer received which serial number?", "Single Select", options="Yes\nNo"),
	])

	# Section 8: Batch / Lot Tracking
	s = 8
	section = "Batch / Lot Tracking"
	questions.extend([
		_q(s, section, None, "Do you track items by batch/lot number?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Item.has_batch_no"),
		_q(s, section, None, "If yes, which item categories require batch tracking?", "Text"),
		_q(s, section, None, "Should batch numbers be auto-generated or manually entered?", "Single Select", options="Auto-generated\nManual\nBoth\nNot applicable", erp_ref="Item.batch_number_series"),
		_q(s, section, None, "Do your batches have expiry dates?", "Single Select", options="Yes\nNo", erp_ref="Item.has_expiry_date"),
		_q(s, section, None, "If yes, what is the typical shelf life?", "Text", erp_ref="Item.shelf_life_in_days"),
		_q(s, section, None, "Do you need to retain samples from batches for quality purposes?", "Single Select", options="Yes\nNo", erp_ref="Item.retain_sample"),
		_q(s, section, None, "What strategy for picking batches during dispatch?", "Single Select", options="FIFO (First Expiry First Out)\nLIFO\nManual selection\nNot applicable", erp_ref="Stock Settings.pick_serial_and_batch_based_on"),
	])

	# Section 9: Barcode Management
	s = 9
	section = "Barcode Management"
	questions.extend([
		_q(s, section, None, "Do you use barcodes on items?", "Single Select", options="Yes\nNo", erp_ref="Item Barcode"),
		_q(s, section, None, "If yes, what barcode format?", "Multi Select", options="EAN-13\nUPC-A\nCODE-39\nCODE-128\nGS1\nQR Code\nOther", erp_ref="Item Barcode.barcode_type"),
		_q(s, section, None, "Do you use barcode scanning for goods receipt, dispatch, or stock counting?", "Multi Select", options="Goods Receipt\nDispatch\nStock Counting\nPick List\nNone"),
		_q(s, section, None, "Do you need to print barcode labels from the system?", "Single Select", options="Yes\nNo"),
	])

	# Section 10: Stock Transactions
	s = 10
	section = "Stock Transactions"
	questions.extend([
		_q(s, section, None, "What types of stock movements do you need?", "Multi Select", options="Material Receipt\nMaterial Issue\nMaterial Transfer\nManufacture\nRepack\nSubcontracting\nDisassembly", required=1, priority="Critical", erp_ref="Stock Entry.stock_entry_type"),
		_q(s, section, None, "Do you need inter-warehouse transfers?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "If yes, do you need two-step transfers (via transit warehouse)?", "Single Select", options="Yes\nNo", erp_ref="Stock Entry.add_to_transit"),
		_q(s, section, None, "Do you need stock entry approval workflows?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you transfer stock at cost price or arm's length price (for inter-company)?", "Single Select", options="Cost Price\nArm's Length Price\nNot applicable", erp_ref="Stock Settings.allow_from_dn"),
	])

	# Section 11: Material Requests
	s = 11
	section = "Material Requests"
	questions.extend([
		_q(s, section, None, "Do you use formal material/purchase requisitions?", "Single Select", options="Yes\nNo", erp_ref="Material Request"),
		_q(s, section, None, "What types of material requests do you raise?", "Multi Select", options="Purchase\nMaterial Transfer\nMaterial Issue\nManufacture\nCustomer Provided", erp_ref="Material Request.material_request_type"),
		_q(s, section, None, "Do material requests need approval workflows?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should material requests be auto-created from reorder levels?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.auto_indent"),
	])

	# Section 12: Quality Inspection
	s = 12
	section = "Quality Inspection"
	questions.extend([
		_q(s, section, None, "Do you perform quality inspections on incoming goods?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Item.inspection_required_before_purchase"),
		_q(s, section, None, "Do you perform quality inspections on outgoing goods?", "Single Select", options="Yes\nNo", erp_ref="Item.inspection_required_before_delivery"),
		_q(s, section, None, "Do you have inspection templates with standard parameters?", "Single Select", options="Yes\nNo", erp_ref="Quality Inspection Template"),
		_q(s, section, None, "What action should be taken if quality inspection fails?", "Single Select", options="Stop transaction\nWarn only\nNo action", erp_ref="Stock Settings.action_if_quality_inspection_is_rejected"),
		_q(s, section, None, "What action if quality inspection is not submitted?", "Single Select", options="Stop transaction\nWarn only\nNo action", erp_ref="Stock Settings.action_if_quality_inspection_is_not_submitted"),
		_q(s, section, None, "Do you need to track inspector name and verification?", "Single Select", options="Yes\nNo", erp_ref="Quality Inspection.inspected_by"),
	])

	# Section 13: Reorder Levels & Auto-Replenishment
	s = 13
	section = "Reorder Levels & Auto-Replenishment"
	questions.extend([
		_q(s, section, None, "Do you set minimum stock levels (reorder points) for items?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Item Reorder"),
		_q(s, section, None, "Are reorder levels set per warehouse or globally?", "Single Select", options="Per Warehouse\nGlobal\nNot applicable", erp_ref="Item Reorder.warehouse"),
		_q(s, section, None, "Should the system auto-create purchase requests when stock falls below reorder level?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.auto_indent"),
		_q(s, section, None, "Do you need email notifications for reorder alerts?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.reorder_email_notify"),
		_q(s, section, None, "Do you track safety stock levels?", "Single Select", options="Yes\nNo", erp_ref="Item.safety_stock"),
		_q(s, section, None, "Do you track lead times for replenishment planning?", "Single Select", options="Yes\nNo", erp_ref="Item.lead_time_days"),
	])

	# Section 14: Pick List & Packing
	s = 14
	section = "Pick List & Packing"
	questions.extend([
		_q(s, section, None, "Do you use pick lists for warehouse picking?", "Single Select", options="Yes\nNo", erp_ref="Pick List"),
		_q(s, section, None, "What purposes do pick lists serve?", "Multi Select", options="Delivery / Sales Orders\nMaterial Transfer\nManufacture\nNot applicable", erp_ref="Pick List.purpose"),
		_q(s, section, None, "Do you use barcode scanning for pick confirmation?", "Single Select", options="Yes\nNo", erp_ref="Pick List.scan_barcode"),
		_q(s, section, None, "Do you create packing slips for shipments?", "Single Select", options="Yes\nNo", erp_ref="Packing Slip"),
		_q(s, section, None, "Do you track package weight (net and gross)?", "Single Select", options="Yes\nNo", erp_ref="Packing Slip.net_weight_pkg"),
	])

	# Section 15: Putaway Rules
	s = 15
	section = "Putaway Rules"
	questions.extend([
		_q(s, section, None, "Do you need automated warehouse bin/location assignment on receipt?", "Single Select", options="Yes\nNo", erp_ref="Putaway Rule"),
		_q(s, section, None, "Do you track bin capacity per item per warehouse?", "Single Select", options="Yes\nNo", erp_ref="Putaway Rule.capacity"),
		_q(s, section, None, "Do you prioritize certain warehouse locations over others?", "Single Select", options="Yes\nNo", erp_ref="Putaway Rule.priority"),
	])

	# Section 16: Stock Reconciliation
	s = 16
	section = "Stock Reconciliation & Physical Count"
	questions.extend([
		_q(s, section, None, "Do you perform physical stock counts?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Stock Reconciliation"),
		_q(s, section, None, "How often are physical counts done?", "Single Select", options="Monthly\nQuarterly\nAnnually\nCyclic counting\nAd-hoc"),
		_q(s, section, None, "Do you need cycle counting (count subset of items on rotation)?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "What difference account should stock variances be posted to?", "Text", erp_ref="Stock Reconciliation.expense_account"),
		_q(s, section, None, "Do you need barcode scanning for stock counts?", "Single Select", options="Yes\nNo"),
	])

	# Section 17: Landed Cost
	s = 17
	section = "Landed Cost"
	questions.extend([
		_q(s, section, None, "Do you need to allocate freight, customs, or other charges to inventory cost?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Landed Cost Voucher"),
		_q(s, section, None, "What types of landed costs do you incur?", "Multi Select", options="Freight / Shipping\nCustoms Duty\nInsurance\nHandling\nInspection Fees\nOther"),
		_q(s, section, None, "How should landed costs be distributed?", "Single Select", options="By Quantity\nBy Amount\nManual\nNot applicable", erp_ref="Landed Cost Voucher.distribute_charges_based_on"),
	])

	# Section 18: Stock Reservation
	s = 18
	section = "Stock Reservation"
	questions.extend([
		_q(s, section, None, "Do you need to reserve stock for confirmed orders?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Stock Settings.enable_stock_reservation"),
		_q(s, section, None, "Should partial stock reservation be allowed?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.allow_partial_reservation"),
		_q(s, section, None, "Should serial/batch numbers be auto-reserved?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.auto_reserve_serial_and_batch"),
		_q(s, section, None, "When should reserved stock be released?", "Single Select", options="On delivery\nOn invoice\nManual release\nNot applicable"),
	])

	# Section 19: Stock Freezing & Controls
	s = 19
	section = "Stock Freezing & Controls"
	questions.extend([
		_q(s, section, None, "Do you need to freeze stock transactions before a certain date?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.stock_frozen_upto"),
		_q(s, section, None, "If yes, which role should be allowed to post in frozen periods?", "Text", erp_ref="Stock Settings.role_allowed_to_edit"),
		_q(s, section, None, "Should the system allow negative stock?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Stock Settings.allow_negative_stock"),
		_q(s, section, None, "Do you need to restrict back-dated stock transactions?", "Single Select", options="Yes\nNo", erp_ref="Stock Settings.role_allowed_to_create_edit_back_dated_transactions"),
		_q(s, section, None, "What over-delivery/receipt tolerance (%) do you allow?", "Text", erp_ref="Stock Settings.over_delivery_receipt_allowance"),
	])

	# Section 20: Inventory Reporting
	s = 20
	section = "Inventory Reporting"
	questions.extend([
		_q(s, section, None, "Which inventory reports do you need?", "Multi Select", options="Stock Balance\nStock Ledger\nStock Projected Qty\nStock Ageing\nStock Analytics\nWarehouse-wise Balance\nSerial No Ledger\nBatch-wise Balance\nItem Price List\nStock vs Account Value\nReorder Level Report\nBOM Search", priority="Important"),
		_q(s, section, None, "Do you need stock reports filtered by warehouse, item group, or brand?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need stock aging analysis (how long items have been in stock)?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need delayed delivery/receipt reports?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need stock and account value reconciliation reports?", "Single Select", options="Yes\nNo"),
	])

	# Section 21: Roles & Permissions
	s = 21
	section = "Roles & Permissions"
	questions.extend([
		_q(s, section, None, "How many users will use the stock module?", "Text", priority="Important"),
		_q(s, section, None, "List the inventory roles needed (e.g. Stock Manager, Stock User, Item Manager, Quality Manager).", "Text", priority="Important"),
		_q(s, section, None, "Should item creation be restricted to certain roles?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should stock entries need approval?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need warehouse-level access restrictions?", "Single Select", options="Yes\nNo", erp_ref="User Permission"),
	])

	# Section 22: Parking Lot & Open Items
	s = 22
	section = "Parking Lot & Open Items"
	questions.extend([
		_q(s, section, None, "List any inventory requirements not covered above.", "Text"),
		_q(s, section, None, "Any known pain points with the current inventory process?", "Text", priority="Important"),
		_q(s, section, None, "Any compliance or regulatory requirements for inventory (e.g. pharma, food safety)?", "Text"),
		_q(s, section, None, "Do you need opening stock balances imported? If yes, approximately how many item-warehouse combinations?", "Text", priority="Critical"),
		_q(s, section, None, "Timeline constraints for stock module go-live?", "Text", priority="Important"),
		_q(s, section, None, "Any additional notes or comments?", "Text"),
	])

	return questions


def seed_crm_template():
	"""Create the comprehensive CRM BRD template."""
	template = frappe.new_doc("BRD Module Template")
	template.template_name = "CRM BRD v1.0"
	template.module_name = "CRM"
	template.version = "1.0"
	template.description = "Comprehensive Business Requirements Document for CRM implementation. Covers lead management, deal pipeline, organizations, campaigns, email marketing, telephony, SLAs, appointments, contracts, territories, and reporting."
	template.is_active = 1

	questions = get_crm_questions()
	for q in questions:
		template.append("questions", q)

	template.insert(ignore_permissions=True)
	frappe.db.commit()


def get_crm_questions():
	"""Return the full list of CRM BRD questions."""
	questions = []

	# Section 1: CRM Strategy & Current State
	s = 1
	section = "CRM Strategy & Current State"
	questions.extend([
		_q(s, section, None, "How do you currently manage customer relationships (spreadsheet, legacy CRM, manual)?", "Text", priority="Important"),
		_q(s, section, None, "What are the primary goals for your CRM implementation?", "Multi Select", options="Lead Tracking\nSales Pipeline Management\nCustomer Retention\nMarketing Automation\nCustomer Support\nReporting & Analytics", required=1, priority="Critical"),
		_q(s, section, None, "How many salespeople / CRM users will there be?", "Text", priority="Important"),
		_q(s, section, None, "Do you need separate CRM views for different teams?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "What is your average sales cycle length?", "Single Select", options="Less than 1 week\n1-4 weeks\n1-3 months\n3-6 months\n6+ months"),
	])

	# Section 2: Lead Management
	s = 2
	section = "Lead Management"
	questions.extend([
		_q(s, section, None, "What are your primary lead sources?", "Multi Select", options="Website\nPhone/Walk-in\nReferral\nSocial Media\nEmail Campaign\nTrade Show/Event\nPaid Advertising\nPartner/Channel\nCold Outreach", required=1, priority="Critical", erp_ref="CRM Lead.source"),
		_q(s, section, None, "Approximately how many new leads per month?", "Text", priority="Important"),
		_q(s, section, None, "Do you need automatic lead capture from web forms?", "Single Select", options="Yes\nNo", erp_ref="CRM Lead"),
		_q(s, section, None, "What information do you capture for each lead?", "Multi Select", options="Name\nEmail\nPhone\nCompany\nJob Title\nIndustry\nRevenue\nEmployee Count\nLocation", erp_ref="CRM Lead"),
		_q(s, section, None, "Do you need lead auto-assignment to sales reps?", "Single Select", options="Yes - Round robin\nYes - By territory\nYes - By lead source\nNo - Manual assignment", erp_ref="CRM Lead.lead_owner"),
		_q(s, section, "Lead Statuses", "What lead statuses do you need?", "Text", help_text="e.g. New, Contacted, Qualified, Unqualified, Converted, Junk", priority="Important", erp_ref="CRM Lead Status"),
		_q(s, section, "Lead Statuses", "Do you need lead qualification criteria or scoring?", "Single Select", options="Yes\nNo"),
		_q(s, section, "Lead Statuses", "If yes, describe your qualification criteria.", "Text"),
		_q(s, section, "Duplicates", "How should duplicate leads be handled?", "Single Select", options="Prevent duplicates by email\nAllow duplicates\nMerge duplicates manually", erp_ref="CRM Settings"),
	])

	# Section 3: Deal / Opportunity Pipeline
	s = 3
	section = "Deal / Opportunity Pipeline"
	questions.extend([
		_q(s, section, None, "What are your deal/opportunity stages?", "Text", help_text="e.g. Qualification, Proposal, Negotiation, Closed Won, Closed Lost", required=1, priority="Critical", erp_ref="CRM Deal Status"),
		_q(s, section, None, "Do you assign probability percentages to each stage?", "Single Select", options="Yes\nNo", erp_ref="CRM Deal Status.probability"),
		_q(s, section, None, "Do you need to track deal value / opportunity amount?", "Single Select", options="Yes\nNo", erp_ref="CRM Deal / Opportunity.opportunity_amount"),
		_q(s, section, None, "Do you track products/items within each deal?", "Single Select", options="Yes\nNo", erp_ref="Opportunity Item / CRM Product"),
		_q(s, section, None, "Do you need a Kanban board view for the sales pipeline?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you track competitors on deals?", "Single Select", options="Yes\nNo", erp_ref="Competitor"),
		_q(s, section, "Lost Deals", "Do you track reasons for lost deals?", "Single Select", options="Yes\nNo", erp_ref="CRM Lost Reason / Opportunity Lost Reason"),
		_q(s, section, "Lost Deals", "If yes, list the standard lost reasons.", "Text"),
		_q(s, section, None, "Do you need multiple deal pipelines (e.g. by product line)?", "Single Select", options="Yes\nNo"),
	])

	# Section 4: Organizations & Contacts
	s = 4
	section = "Organizations & Contacts"
	questions.extend([
		_q(s, section, None, "Do you track organizations/companies separately from individual contacts?", "Single Select", options="Yes\nNo", erp_ref="CRM Organization"),
		_q(s, section, None, "What organization information do you need?", "Multi Select", options="Company Name\nIndustry\nWebsite\nEmployee Count\nAnnual Revenue\nAddress\nTerritory\nLogo", erp_ref="CRM Organization"),
		_q(s, section, None, "Can multiple contacts belong to the same organization?", "Single Select", options="Yes\nNo", erp_ref="CRM Deal.contacts"),
		_q(s, section, None, "Do you need to link contacts to deals?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need to auto-create ERPNext Customers from CRM deals?", "Single Select", options="Yes - on deal won\nYes - at specific stage\nNo - manual", erp_ref="ERPNext CRM Settings"),
	])

	# Section 5: Territory & Sales Team
	s = 5
	section = "Territory & Sales Team"
	questions.extend([
		_q(s, section, None, "Do you manage sales territories?", "Single Select", options="Yes\nNo", erp_ref="CRM Territory"),
		_q(s, section, None, "If yes, list your territories or regions.", "Text"),
		_q(s, section, None, "Do you need territory-based lead/deal assignment?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you have sales teams or individual sales reps?", "Single Select", options="Individual reps\nTeams\nBoth"),
		_q(s, section, None, "Do sales managers need visibility into their team's pipeline?", "Single Select", options="Yes\nNo"),
	])

	# Section 6: Campaigns & Email Marketing
	s = 6
	section = "Campaigns & Email Marketing"
	questions.extend([
		_q(s, section, None, "Do you run marketing campaigns?", "Single Select", options="Yes\nNo", erp_ref="Campaign"),
		_q(s, section, None, "What types of campaigns?", "Multi Select", options="Email Drip/Nurture\nEvent/Webinar\nProduct Launch\nSeasonal Promotion\nReferral Program\nSocial Media"),
		_q(s, section, None, "Do you need automated email sequences (drip campaigns)?", "Single Select", options="Yes\nNo", erp_ref="Email Campaign"),
		_q(s, section, None, "Do you need to track campaign effectiveness (leads generated, conversion rate)?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need email open/click tracking?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need an unsubscribe mechanism?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you use any external marketing tools that need integration?", "Text"),
	])

	# Section 7: Communication & Activity Tracking
	s = 7
	section = "Communication & Activity Tracking"
	questions.extend([
		_q(s, section, None, "What communication channels do you use with leads/customers?", "Multi Select", options="Email\nPhone\nWhatsApp\nSMS\nIn-person meetings\nVideo calls\nSocial media", priority="Important"),
		_q(s, section, None, "Do you need email integration (send/receive from CRM)?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need call logging?", "Single Select", options="Yes\nNo", erp_ref="CRM Call Log"),
		_q(s, section, None, "Do you need telephony integration (Twilio, Exotel)?", "Single Select", options="Yes - Twilio\nYes - Exotel\nYes - Other\nNo", erp_ref="CRM Twilio Settings / CRM Exotel Settings"),
		_q(s, section, None, "Do you need task management within CRM?", "Single Select", options="Yes\nNo", erp_ref="CRM Task"),
		_q(s, section, None, "Do you need notes/activity timeline on leads and deals?", "Single Select", options="Yes\nNo", erp_ref="FCRM Note"),
	])

	# Section 8: Service Level Agreements (SLA)
	s = 8
	section = "Service Level Agreements"
	questions.extend([
		_q(s, section, None, "Do you need SLAs for lead response time?", "Single Select", options="Yes\nNo", erp_ref="CRM Service Level Agreement"),
		_q(s, section, None, "If yes, what is the target first response time?", "Text", erp_ref="CRM Service Level Priority"),
		_q(s, section, None, "Do SLA targets vary by priority or lead source?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need SLA tracking on deals as well?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need SLA breach notifications?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you have working hours / holiday lists that affect SLA calculation?", "Single Select", options="Yes\nNo", erp_ref="CRM Holiday List"),
	])

	# Section 9: Appointments & Scheduling
	s = 9
	section = "Appointments & Scheduling"
	questions.extend([
		_q(s, section, None, "Do you need online appointment booking for prospects/customers?", "Single Select", options="Yes\nNo", erp_ref="Appointment Booking Settings"),
		_q(s, section, None, "Should appointments be bookable from your website?", "Single Select", options="Yes\nNo", erp_ref="Appointment"),
		_q(s, section, None, "What is the default appointment duration?", "Single Select", options="15 minutes\n30 minutes\n1 hour\nCustom", erp_ref="Appointment Booking Settings.appointment_duration"),
		_q(s, section, None, "How many days in advance can appointments be booked?", "Text", erp_ref="Appointment Booking Settings.advance_booking_days"),
		_q(s, section, None, "Do you need automated email reminders for appointments?", "Single Select", options="Yes\nNo", erp_ref="Appointment Booking Settings.email_reminders"),
	])

	# Section 10: Contracts
	s = 10
	section = "Contracts"
	questions.extend([
		_q(s, section, None, "Do you manage contracts with customers?", "Single Select", options="Yes\nNo", erp_ref="Contract"),
		_q(s, section, None, "Do you use contract templates?", "Single Select", options="Yes\nNo", erp_ref="Contract Template"),
		_q(s, section, None, "Do contracts need digital signatures?", "Single Select", options="Yes\nNo", erp_ref="Contract.is_signed"),
		_q(s, section, None, "Do you track contract fulfilment milestones?", "Single Select", options="Yes\nNo", erp_ref="Contract.requires_fulfilment"),
		_q(s, section, None, "Do you need contract expiry alerts?", "Single Select", options="Yes\nNo"),
	])

	# Section 11: ERPNext Integration
	s = 11
	section = "ERPNext Integration"
	questions.extend([
		_q(s, section, None, "Do you use ERPNext for accounting/inventory alongside CRM?", "Single Select", options="Yes\nNo", erp_ref="ERPNext CRM Settings"),
		_q(s, section, None, "Should won deals automatically create Customers in ERPNext?", "Single Select", options="Yes\nNo", erp_ref="ERPNext CRM Settings.create_customer_on_status_change"),
		_q(s, section, None, "At which deal stage should the Customer be created?", "Text", erp_ref="ERPNext CRM Settings.deal_status"),
		_q(s, section, None, "Do you need Quotations created from CRM deals?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need Sales Orders created from CRM?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Which ERPNext company should CRM data sync with?", "Text", erp_ref="ERPNext CRM Settings.erpnext_company"),
	])

	# Section 12: CRM Reporting & Dashboards
	s = 12
	section = "Reporting & Dashboards"
	questions.extend([
		_q(s, section, None, "Which CRM reports do you need?", "Multi Select", options="Sales Pipeline\nLead Conversion Rate\nLead Source Analysis\nCampaign Efficiency\nSales Rep Performance\nTerritory-wise Analysis\nLost Opportunity Analysis\nFirst Response Time\nForecast / Revenue Projection", priority="Important"),
		_q(s, section, None, "Do you need custom CRM dashboards?", "Single Select", options="Yes\nNo", erp_ref="CRM Dashboard"),
		_q(s, section, None, "Do you need scheduled email reports?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Who needs access to CRM reports?", "Multi Select", options="Sales Reps\nSales Managers\nMarketing Team\nExecutive Management"),
	])

	# Section 13: Roles & Permissions
	s = 13
	section = "Roles & Permissions"
	questions.extend([
		_q(s, section, None, "What CRM roles do you need?", "Multi Select", options="Sales Manager\nSales User\nMarketing User\nCRM Admin\nRead-only Viewer", priority="Important"),
		_q(s, section, None, "Should sales reps only see their own leads/deals?", "Single Select", options="Yes - own only\nNo - see all\nBy territory", erp_ref="CRM Lead.lead_owner"),
		_q(s, section, None, "Should managers see all team data?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should lead deletion be restricted?", "Single Select", options="Yes\nNo"),
	])

	# Section 14: Data Migration
	s = 14
	section = "Data Migration"
	questions.extend([
		_q(s, section, None, "Do you have existing CRM data to migrate?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "What data needs to be migrated?", "Multi Select", options="Leads\nContacts\nOrganizations/Companies\nDeals/Opportunities\nCommunication History\nTasks/Activities\nCampaign Data"),
		_q(s, section, None, "What is the source system?", "Text"),
		_q(s, section, None, "What format is the data in?", "Single Select", options="Excel/CSV\nAPI export\nDatabase dump\nManual records"),
		_q(s, section, None, "Approximately how many records to migrate?", "Text"),
	])

	# Section 15: Parking Lot & Open Items
	s = 15
	section = "Parking Lot & Open Items"
	questions.extend([
		_q(s, section, None, "List any CRM requirements not covered above.", "Text"),
		_q(s, section, None, "Any known pain points with the current sales process?", "Text", priority="Important"),
		_q(s, section, None, "Any third-party integrations needed (Mailchimp, HubSpot, Zapier, etc.)?", "Text"),
		_q(s, section, None, "Timeline constraints for CRM go-live?", "Text", priority="Important"),
		_q(s, section, None, "Any additional notes or comments?", "Text"),
	])

	return questions


def seed_projects_template():
	"""Create the comprehensive Projects BRD template."""
	template = frappe.new_doc("BRD Module Template")
	template.template_name = "Projects BRD v1.0"
	template.module_name = "Projects"
	template.version = "1.0"
	template.description = "Comprehensive Business Requirements Document for ERPNext Projects module implementation. Covers project types, task management, time tracking, costing, billing, templates, and reporting."
	template.is_active = 1

	questions = get_projects_questions()
	for q in questions:
		template.append("questions", q)

	template.insert(ignore_permissions=True)
	frappe.db.commit()


def get_projects_questions():
	"""Return the full list of Projects BRD questions."""
	questions = []

	# Section 1: Project Management Overview
	s = 1
	section = "Project Management Overview"
	questions.extend([
		_q(s, section, None, "How do you currently manage projects (spreadsheet, MS Project, other tool)?", "Text", priority="Important"),
		_q(s, section, None, "What is the primary purpose of projects in your organization?", "Multi Select", options="Client delivery\nInternal initiatives\nProduct development\nConstruction/Engineering\nConsulting/Services\nIT/Software\nEvent management\nOther", required=1, priority="Critical"),
		_q(s, section, None, "Approximately how many concurrent projects do you typically have?", "Text"),
		_q(s, section, None, "What is the typical project duration?", "Single Select", options="Less than 1 week\n1-4 weeks\n1-3 months\n3-6 months\n6-12 months\n12+ months"),
		_q(s, section, None, "Do you need project portfolio management (multiple related projects)?", "Single Select", options="Yes\nNo"),
	])

	# Section 2: Project Types & Categories
	s = 2
	section = "Project Types & Categories"
	questions.extend([
		_q(s, section, None, "What types of projects do you run?", "Text", required=1, priority="Important", erp_ref="Project Type"),
		_q(s, section, None, "Do you need to categorize projects by type?", "Single Select", options="Yes\nNo", erp_ref="Project.project_type"),
		_q(s, section, None, "Do you link projects to specific customers?", "Single Select", options="Yes\nNo", erp_ref="Project.customer"),
		_q(s, section, None, "Do you link projects to Sales Orders?", "Single Select", options="Yes\nNo", erp_ref="Project.sales_order"),
		_q(s, section, None, "Do you need project priority levels?", "Single Select", options="Yes\nNo", erp_ref="Project.priority"),
	])

	# Section 3: Project Templates
	s = 3
	section = "Project Templates"
	questions.extend([
		_q(s, section, None, "Do you have repeatable project structures that could use templates?", "Single Select", options="Yes\nNo", erp_ref="Project Template"),
		_q(s, section, None, "If yes, describe your standard project structures.", "Text"),
		_q(s, section, None, "Do templates include predefined tasks with durations and dependencies?", "Single Select", options="Yes\nNo", erp_ref="Project Template Task"),
		_q(s, section, None, "How many project templates do you anticipate needing?", "Text"),
	])

	# Section 4: Task Management
	s = 4
	section = "Task Management"
	questions.extend([
		_q(s, section, None, "How granular are your project tasks?", "Single Select", options="High level milestones only\nDetailed task breakdown\nMulti-level hierarchy (task groups + sub-tasks)", erp_ref="Task"),
		_q(s, section, None, "Do you need task dependencies (Task B starts after Task A)?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Task Depends On"),
		_q(s, section, None, "Do you need Gantt chart visualization?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "What task statuses do you use?", "Text", help_text="Default: Open, Working, Pending Review, Overdue, Template, Completed, Cancelled", erp_ref="Task.status"),
		_q(s, section, None, "Do you need task priority levels?", "Single Select", options="Yes\nNo", erp_ref="Task.priority"),
		_q(s, section, None, "Do you need milestones within projects?", "Single Select", options="Yes\nNo", erp_ref="Task.is_milestone"),
		_q(s, section, None, "Do you track task progress percentage?", "Single Select", options="Yes\nNo", erp_ref="Task.progress"),
		_q(s, section, None, "Do you need task types/categories?", "Single Select", options="Yes\nNo", erp_ref="Task Type"),
		_q(s, section, None, "Do you assign tasks to specific users?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need task weight for weighted progress calculation?", "Single Select", options="Yes\nNo", erp_ref="Task.task_weight"),
	])

	# Section 5: Project Progress Tracking
	s = 5
	section = "Project Progress Tracking"
	questions.extend([
		_q(s, section, None, "How should project completion percentage be calculated?", "Single Select", options="Task Completion\nTask Progress\nTask Weight\nManual", required=1, priority="Important", erp_ref="Project.percent_complete_method"),
		_q(s, section, None, "Do you need periodic project status updates?", "Single Select", options="Yes\nNo", erp_ref="Project Update"),
		_q(s, section, None, "If yes, how often?", "Single Select", options="Daily\nWeekly\nBi-weekly\nMonthly", erp_ref="Project.frequency"),
		_q(s, section, None, "Do you track project start and end dates (expected vs actual)?", "Single Select", options="Yes\nNo", erp_ref="Project.expected_start_date"),
		_q(s, section, None, "Do you need project status workflow (e.g. Open → In Progress → Completed)?", "Single Select", options="Yes\nNo", erp_ref="Project.status"),
	])

	# Section 6: Time Tracking & Timesheets
	s = 6
	section = "Time Tracking & Timesheets"
	questions.extend([
		_q(s, section, None, "Do you need to track time spent on projects/tasks?", "Single Select", options="Yes\nNo", required=1, priority="Critical", erp_ref="Timesheet"),
		_q(s, section, None, "Who fills in timesheets?", "Multi Select", options="All employees\nProject team members only\nConsultants/contractors\nSpecific roles"),
		_q(s, section, None, "What is the time logging granularity?", "Single Select", options="Minutes\nHalf-hours\n Hours\nDays"),
		_q(s, section, None, "Do you need activity types for categorizing time entries?", "Single Select", options="Yes\nNo", erp_ref="Activity Type"),
		_q(s, section, None, "If yes, list your activity types.", "Text", help_text="e.g. Development, Design, Meeting, Travel, Support", erp_ref="Activity Type"),
		_q(s, section, None, "Do timesheets need approval before submission?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need to prevent overlapping time entries?", "Single Select", options="Yes\nNo", erp_ref="Projects Settings.ignore_employee_time_overlap"),
	])

	# Section 7: Project Costing
	s = 7
	section = "Project Costing"
	questions.extend([
		_q(s, section, None, "Do you track project costs?", "Single Select", options="Yes\nNo", priority="Critical", erp_ref="Project.total_costing_amount"),
		_q(s, section, None, "What cost components do you track?", "Multi Select", options="Labour (timesheets)\nMaterial / Stock\nPurchases\nExpenses\nSubcontractor costs\nOverheads"),
		_q(s, section, None, "Do you set estimated budgets per project?", "Single Select", options="Yes\nNo", erp_ref="Project.estimated_costing"),
		_q(s, section, None, "Do you need costing rates per activity type?", "Single Select", options="Yes\nNo", erp_ref="Activity Type.costing_rate"),
		_q(s, section, None, "Do you need per-employee costing rates (Activity Cost)?", "Single Select", options="Yes\nNo", erp_ref="Activity Cost"),
		_q(s, section, None, "Do you need to track material consumption against projects?", "Single Select", options="Yes\nNo", erp_ref="Project.total_consumed_material_cost"),
		_q(s, section, None, "Do you link Purchase Orders/Invoices to projects for cost tracking?", "Single Select", options="Yes\nNo", erp_ref="Project.total_purchase_cost"),
		_q(s, section, None, "Do you need project profitability analysis (revenue vs cost)?", "Single Select", options="Yes\nNo", erp_ref="Project.gross_margin"),
	])

	# Section 8: Project Billing
	s = 8
	section = "Project Billing"
	questions.extend([
		_q(s, section, None, "Do you bill clients for project work?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "What is your billing model?", "Multi Select", options="Time & Material (hourly)\nFixed Price\nMilestone-based\nRetainer/Subscription\nMixed"),
		_q(s, section, None, "Do you need billing rates per activity type?", "Single Select", options="Yes\nNo", erp_ref="Activity Type.billing_rate"),
		_q(s, section, None, "Do you generate Sales Invoices from timesheets?", "Single Select", options="Yes\nNo", erp_ref="Timesheet.sales_invoice"),
		_q(s, section, None, "Do you track billable vs non-billable hours?", "Single Select", options="Yes\nNo", erp_ref="Timesheet.total_billable_hours"),
		_q(s, section, None, "Do you need to track billed percentage per project?", "Single Select", options="Yes\nNo", erp_ref="Project.total_billed_amount"),
	])

	# Section 9: Project Team & Resources
	s = 9
	section = "Project Team & Resources"
	questions.extend([
		_q(s, section, None, "Do you assign team members to projects?", "Single Select", options="Yes\nNo", erp_ref="Project User"),
		_q(s, section, None, "Do you need to track resource allocation across projects?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you link projects to departments?", "Single Select", options="Yes\nNo", erp_ref="Project.department"),
		_q(s, section, None, "Do you need a project cost centre for accounting?", "Single Select", options="Yes\nNo", erp_ref="Project.cost_center"),
		_q(s, section, None, "Do project team members need a portal/external view?", "Single Select", options="Yes\nNo"),
	])

	# Section 10: Holiday & Working Hours
	s = 10
	section = "Holiday & Working Hours"
	questions.extend([
		_q(s, section, None, "Do projects follow a specific holiday calendar?", "Single Select", options="Yes - company calendar\nYes - project-specific\nNo", erp_ref="Project.holiday_list"),
		_q(s, section, None, "Do you define working hours for time-based calculations?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need to account for holidays when calculating task durations?", "Single Select", options="Yes\nNo"),
	])

	# Section 11: Reporting
	s = 11
	section = "Reporting"
	questions.extend([
		_q(s, section, None, "Which project reports do you need?", "Multi Select", options="Project Summary\nProject Billing Summary\nEmployee Billing Summary\nDaily Timesheet Summary\nDelayed Tasks Summary\nProject-wise Stock Tracking\nProject Profitability\nResource Utilization", priority="Important"),
		_q(s, section, None, "Do you need project dashboards?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need scheduled project status email reports?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need consolidated reporting across all projects?", "Single Select", options="Yes\nNo"),
	])

	# Section 12: Roles & Permissions
	s = 12
	section = "Roles & Permissions"
	questions.extend([
		_q(s, section, None, "What project roles do you need?", "Multi Select", options="Projects Manager\nProjects User\nTimesheet User\nRead-only Viewer", priority="Important"),
		_q(s, section, None, "Should project creation be restricted to managers?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should users only see projects they are assigned to?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should timesheet submission require approval?", "Single Select", options="Yes\nNo"),
	])

	# Section 13: Parking Lot & Open Items
	s = 13
	section = "Parking Lot & Open Items"
	questions.extend([
		_q(s, section, None, "List any project management requirements not covered above.", "Text"),
		_q(s, section, None, "Any known pain points with current project tracking?", "Text", priority="Important"),
		_q(s, section, None, "Any third-party integrations needed (Jira, Asana, MS Project, etc.)?", "Text"),
		_q(s, section, None, "Timeline constraints for projects module go-live?", "Text", priority="Important"),
		_q(s, section, None, "Any additional notes or comments?", "Text"),
	])

	return questions


def seed_quality_template():
	"""Create the comprehensive Quality Management BRD template."""
	template = frappe.new_doc("BRD Module Template")
	template.template_name = "Quality Management BRD v1.0"
	template.module_name = "Quality Management"
	template.version = "1.0"
	template.description = "Comprehensive Business Requirements Document for ERPNext Quality Management module implementation. Covers quality inspections, goals, procedures, reviews, non-conformance, CAPA, feedback, meetings, and reporting."
	template.is_active = 1

	questions = get_quality_questions()
	for q in questions:
		template.append("questions", q)

	template.insert(ignore_permissions=True)
	frappe.db.commit()


def get_quality_questions():
	"""Return the full list of Quality Management BRD questions."""
	questions = []

	# Section 1: Quality Management Overview
	s = 1
	section = "Quality Management Overview"
	questions.extend([
		_q(s, section, None, "Does your organization have a formal Quality Management System (QMS)?", "Single Select", options="Yes - ISO 9001 certified\nYes - Other standard\nYes - Internal QMS\nNo - planning to implement", priority="Critical"),
		_q(s, section, None, "What quality standards or certifications do you need to comply with?", "Multi Select", options="ISO 9001\nISO 14001\nISO 45001\nISO 22000\nIATF 16949\nAS9100\nGMP\nFDA\nNone specific", priority="Important"),
		_q(s, section, None, "Who is responsible for quality management?", "Text"),
		_q(s, section, None, "How do you currently manage quality processes (manual, spreadsheet, software)?", "Text"),
		_q(s, section, None, "What are the primary goals of quality management?", "Multi Select", options="Product quality assurance\nProcess improvement\nRegulatory compliance\nCustomer satisfaction\nDefect reduction\nSupplier quality\nAudit readiness", required=1, priority="Critical"),
	])

	# Section 2: Quality Inspection
	s = 2
	section = "Quality Inspection"
	questions.extend([
		_q(s, section, None, "Do you perform quality inspections on incoming materials?", "Single Select", options="Yes - all items\nYes - selected items\nNo", priority="Critical", erp_ref="Quality Inspection.inspection_type = Incoming"),
		_q(s, section, None, "Do you perform in-process quality inspections?", "Single Select", options="Yes\nNo", erp_ref="Quality Inspection.inspection_type = In Process"),
		_q(s, section, None, "Do you perform outgoing/final quality inspections?", "Single Select", options="Yes\nNo", erp_ref="Quality Inspection.inspection_type = Outgoing"),
		_q(s, section, None, "What triggers an inspection?", "Multi Select", options="Purchase Receipt\nStock Entry (Manufacture)\nDelivery Note\nManual/Ad-hoc\nSubcontracting Receipt", erp_ref="Quality Inspection.reference_type"),
		_q(s, section, None, "Do you use inspection templates with predefined parameters?", "Single Select", options="Yes\nNo", erp_ref="Quality Inspection Template"),
		_q(s, section, None, "List the inspection parameters you typically measure.", "Text", help_text="e.g. Dimensions, Weight, Color, Hardness, pH, Temperature", erp_ref="Quality Inspection Reading"),
		_q(s, section, None, "Do you need acceptance criteria (min/max values, formula-based)?", "Single Select", options="Yes - numeric ranges\nYes - pass/fail\nBoth", erp_ref="Quality Inspection Reading"),
		_q(s, section, None, "Do you inspect every item or use sample-based inspection?", "Single Select", options="100% inspection\nSample-based\nBoth depending on item", erp_ref="Quality Inspection.sample_size"),
		_q(s, section, None, "Should inspection be mandatory before stock acceptance?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "Do you need serial number or batch-level inspections?", "Single Select", options="Yes - Serial number\nYes - Batch\nBoth\nNo", erp_ref="Quality Inspection.item_serial_no / batch_no"),
	])

	# Section 3: Quality Goals
	s = 3
	section = "Quality Goals"
	questions.extend([
		_q(s, section, None, "Do you set measurable quality goals/KPIs?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Quality Goal"),
		_q(s, section, None, "How often are quality goals reviewed?", "Single Select", options="Daily\nWeekly\nMonthly\nQuarterly\nAnnually", erp_ref="Quality Goal.frequency"),
		_q(s, section, None, "What types of quality objectives do you track?", "Multi Select", options="Defect rate\nFirst pass yield\nCustomer complaints\nReturn rate\nInspection pass rate\nOn-time delivery\nSupplier quality score\nProcess capability (Cpk)\nAudit findings closure", erp_ref="Quality Goal Objective"),
		_q(s, section, None, "Do you link quality goals to specific procedures?", "Single Select", options="Yes\nNo", erp_ref="Quality Goal.procedure"),
		_q(s, section, None, "Do you need target vs actual tracking for quality objectives?", "Single Select", options="Yes\nNo", erp_ref="Quality Goal Objective"),
	])

	# Section 4: Quality Procedures
	s = 4
	section = "Quality Procedures"
	questions.extend([
		_q(s, section, None, "Do you have documented quality procedures / SOPs?", "Single Select", options="Yes\nNo", priority="Important", erp_ref="Quality Procedure"),
		_q(s, section, None, "Do procedures have a hierarchical structure (parent-child)?", "Single Select", options="Yes\nNo", erp_ref="Quality Procedure.parent_quality_procedure"),
		_q(s, section, None, "Do procedures define step-by-step processes?", "Single Select", options="Yes\nNo", erp_ref="Quality Procedure Process"),
		_q(s, section, None, "Do you assign process owners to procedures?", "Single Select", options="Yes\nNo", erp_ref="Quality Procedure.process_owner"),
		_q(s, section, None, "Approximately how many quality procedures do you have?", "Text"),
		_q(s, section, None, "Do procedures need version control / revision tracking?", "Single Select", options="Yes\nNo"),
	])

	# Section 5: Quality Reviews
	s = 5
	section = "Quality Reviews"
	questions.extend([
		_q(s, section, None, "Do you conduct periodic quality reviews?", "Single Select", options="Yes\nNo", erp_ref="Quality Review"),
		_q(s, section, None, "How often are reviews conducted?", "Single Select", options="Weekly\nMonthly\nQuarterly\nAnnually\nAs needed"),
		_q(s, section, None, "Are reviews linked to specific quality goals?", "Single Select", options="Yes\nNo", erp_ref="Quality Review.goal"),
		_q(s, section, None, "Do reviews measure performance against objectives?", "Single Select", options="Yes\nNo", erp_ref="Quality Review Objective"),
		_q(s, section, None, "Do you track review status (Open, Pending, Closed)?", "Single Select", options="Yes\nNo", erp_ref="Quality Review.status"),
	])

	# Section 6: Non-Conformance & CAPA
	s = 6
	section = "Non-Conformance & CAPA"
	questions.extend([
		_q(s, section, None, "Do you track non-conformances (NCRs)?", "Single Select", options="Yes\nNo", priority="Critical", erp_ref="Non Conformance"),
		_q(s, section, None, "What triggers a non-conformance report?", "Multi Select", options="Failed inspection\nCustomer complaint\nProcess deviation\nAudit finding\nSupplier issue\nInternal observation", erp_ref="Non Conformance"),
		_q(s, section, None, "Do you link non-conformances to quality procedures?", "Single Select", options="Yes\nNo", erp_ref="Non Conformance.procedure"),
		_q(s, section, None, "Do you implement Corrective and Preventive Actions (CAPA)?", "Single Select", options="Yes\nNo", priority="Critical", erp_ref="Quality Action"),
		_q(s, section, None, "Do you need to track action resolutions with deadlines?", "Single Select", options="Yes\nNo", erp_ref="Quality Action Resolution"),
		_q(s, section, None, "Do quality actions need status tracking (Open, In Progress, Completed)?", "Single Select", options="Yes\nNo", erp_ref="Quality Action.status"),
		_q(s, section, None, "Do you link CAPA to quality reviews or feedback?", "Single Select", options="Yes\nNo", erp_ref="Quality Action.review / Quality Action.feedback"),
	])

	# Section 7: Quality Feedback
	s = 7
	section = "Quality Feedback"
	questions.extend([
		_q(s, section, None, "Do you collect quality feedback from internal or external sources?", "Single Select", options="Internal only\nExternal (customers/suppliers)\nBoth\nNo", erp_ref="Quality Feedback"),
		_q(s, section, None, "Do you use standardized feedback templates?", "Single Select", options="Yes\nNo", erp_ref="Quality Feedback Template"),
		_q(s, section, None, "What feedback parameters do you capture?", "Text", help_text="e.g. Product Quality, Delivery Time, Packaging, Service, Communication", erp_ref="Quality Feedback Parameter"),
		_q(s, section, None, "Do you link feedback to specific transactions (PO, SO, DN)?", "Single Select", options="Yes\nNo", erp_ref="Quality Feedback.document_type"),
		_q(s, section, None, "Should negative feedback trigger a quality action?", "Single Select", options="Yes\nNo"),
	])

	# Section 8: Quality Meetings
	s = 8
	section = "Quality Meetings"
	questions.extend([
		_q(s, section, None, "Do you hold regular quality meetings (e.g. MRM - Management Review Meeting)?", "Single Select", options="Yes\nNo", erp_ref="Quality Meeting"),
		_q(s, section, None, "Do you need to track meeting agendas and minutes?", "Single Select", options="Yes\nNo", erp_ref="Quality Meeting Agenda / Quality Meeting Minutes"),
		_q(s, section, None, "Do meetings generate action items that need follow-up?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "What is the typical frequency of quality meetings?", "Single Select", options="Weekly\nMonthly\nQuarterly\nAs needed"),
	])

	# Section 9: Supplier Quality
	s = 9
	section = "Supplier Quality"
	questions.extend([
		_q(s, section, None, "Do you evaluate supplier quality?", "Single Select", options="Yes\nNo", priority="Important"),
		_q(s, section, None, "Do you maintain an approved supplier list?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you require incoming inspection for all supplier deliveries?", "Single Select", options="Yes - all\nYes - new suppliers only\nYes - critical items only\nNo"),
		_q(s, section, None, "Do you track supplier quality scores/ratings?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you issue corrective action requests to suppliers?", "Single Select", options="Yes\nNo"),
	])

	# Section 10: Reporting & Analytics
	s = 10
	section = "Reporting & Analytics"
	questions.extend([
		_q(s, section, None, "Which quality reports do you need?", "Multi Select", options="Inspection Summary\nDefect Analysis\nNon-Conformance Log\nCAPA Status\nQuality Goal vs Actual\nSupplier Quality Scorecard\nCustomer Complaint Trend\nAudit Findings Summary", priority="Important"),
		_q(s, section, None, "Do you need quality dashboards?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need trend analysis (defect trends over time)?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Do you need quality data for management review presentations?", "Single Select", options="Yes\nNo"),
	])

	# Section 11: Roles & Permissions
	s = 11
	section = "Roles & Permissions"
	questions.extend([
		_q(s, section, None, "What quality roles do you need?", "Multi Select", options="Quality Manager\nQuality Inspector\nQuality Auditor\nProcess Owner\nRead-only Viewer", priority="Important"),
		_q(s, section, None, "Should only Quality Inspectors create inspection reports?", "Single Select", options="Yes\nNo"),
		_q(s, section, None, "Should non-conformance reports be visible to all or restricted?", "Single Select", options="All users\nQuality team only\nManagement + Quality team"),
		_q(s, section, None, "Do auditors need read-only access?", "Single Select", options="Yes\nNo"),
	])

	# Section 12: Parking Lot & Open Items
	s = 12
	section = "Parking Lot & Open Items"
	questions.extend([
		_q(s, section, None, "List any quality management requirements not covered above.", "Text"),
		_q(s, section, None, "Any known pain points with current quality processes?", "Text", priority="Important"),
		_q(s, section, None, "Any upcoming audits or certifications with deadlines?", "Text", priority="Important"),
		_q(s, section, None, "Any third-party integrations needed (LIMS, SPC tools, etc.)?", "Text"),
		_q(s, section, None, "Timeline constraints for quality module go-live?", "Text", priority="Important"),
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
