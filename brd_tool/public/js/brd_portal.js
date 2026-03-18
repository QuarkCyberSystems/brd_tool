document.addEventListener("DOMContentLoaded", function () {
	const app = document.getElementById("brd-app");
	if (!app) return;

	const accessKey = app.dataset.accessKey;
	const isSubmitted = app.dataset.isSubmitted === "true";

	// State
	let saveTimer = null;
	let isDirty = false;

	// DOM refs
	const statusDot = document.getElementById("brd-status-dot");
	const statusText = document.getElementById("brd-status-text");
	const progressPct = document.getElementById("brd-progress-pct");
	const progressFill = document.getElementById("brd-progress-fill");
	const saveBtn = document.getElementById("brd-save-btn");
	const submitBtn = document.getElementById("brd-submit-btn");

	// --- Status helpers ---
	function setStatus(state, msg) {
		if (!statusDot) return;
		statusDot.className = "brd-status-dot brd-status-" + state;
		if (statusText) statusText.textContent = msg || "";
	}

	function updateProgress() {
		const blocks = document.querySelectorAll(".brd-q-block");
		let total = blocks.length;
		let answered = 0;
		blocks.forEach(function (b) {
			if (isBlockAnswered(b)) answered++;
		});
		let pct = total > 0 ? Math.round((answered / total) * 100) : 0;
		if (progressPct) progressPct.textContent = pct + "%";
		if (progressFill) progressFill.style.width = pct + "%";

		// Update section dots
		updateSectionDots();
	}

	function isBlockAnswered(block) {
		// Text
		let ta = block.querySelector("textarea[data-field='response_text']");
		if (ta && ta.value.trim()) return true;
		// Single select
		let radio = block.querySelector(
			"input[data-field='response_single']:checked"
		);
		if (radio) return true;
		// Multi select
		let checks = block.querySelectorAll(
			"input[data-field='response_multi']:checked"
		);
		if (checks.length > 0) return true;
		return false;
	}

	function updateSectionDots() {
		const sectionEls = document.querySelectorAll(".brd-section");
		sectionEls.forEach(function (sec) {
			const num = sec.id.replace("section-", "");
			const blocks = sec.querySelectorAll(".brd-q-block");
			let total = blocks.length;
			let answered = 0;
			blocks.forEach(function (b) {
				if (isBlockAnswered(b)) answered++;
			});
			const dot = document.querySelector(
				'[data-section-dot="' + num + '"]'
			);
			if (dot) {
				if (answered === total && total > 0) {
					dot.classList.add("brd-toc-done");
				} else {
					dot.classList.remove("brd-toc-done");
				}
			}
		});
	}

	// --- Collect responses ---
	function collectResponses() {
		const result = [];
		document.querySelectorAll(".brd-q-block").forEach(function (block) {
			const name = block.dataset.responseName;
			const entry = { name: name };

			// Text
			const ta = block.querySelector(
				"textarea[data-field='response_text']"
			);
			if (ta) entry.response_text = ta.value;

			// Single select
			const radio = block.querySelector(
				"input[data-field='response_single']:checked"
			);
			entry.response_single = radio ? radio.value : "";

			// Multi select
			const checks = block.querySelectorAll(
				"input[data-field='response_multi']:checked"
			);
			const vals = [];
			checks.forEach(function (c) {
				vals.push(c.value);
			});
			entry.response_multi = JSON.stringify(vals);

			result.push(entry);
		});
		return result;
	}

	// --- Save ---
	function save(callback) {
		setStatus("saving", "Saving...");
		const responses = collectResponses();

		const respName = document.getElementById("brd-resp-name");
		const respEmail = document.getElementById("brd-resp-email");
		const respRole = document.getElementById("brd-resp-role");

		frappe.call({
			method: "brd_tool.www.brd.session.index.save_responses",
			args: {
				access_key: accessKey,
				responses: JSON.stringify(responses),
				respondent_name: respName ? respName.value : "",
				respondent_email: respEmail ? respEmail.value : "",
				respondent_role: respRole ? respRole.value : "",
			},
			callback: function (r) {
				isDirty = false;
				setStatus("saved", "Saved");
				if (r.message && r.message.progress !== undefined) {
					let pct = Math.round(r.message.progress);
					if (progressPct) progressPct.textContent = pct + "%";
					if (progressFill) progressFill.style.width = pct + "%";
				}
				if (callback) callback();
			},
			error: function () {
				setStatus("error", "Save failed");
			},
		});
	}

	function scheduleSave() {
		isDirty = true;
		setStatus("unsaved", "Unsaved changes");
		if (saveTimer) clearTimeout(saveTimer);
		saveTimer = setTimeout(function () {
			save();
		}, 2000);
	}

	// --- Submit ---
	function submitSession() {
		const respName = document.getElementById("brd-resp-name");
		const respEmail = document.getElementById("brd-resp-email");
		const respRole = document.getElementById("brd-resp-role");

		if (!respName || !respName.value.trim()) {
			frappe.msgprint("Please enter your name before submitting.");
			respName && respName.focus();
			return;
		}
		if (!respEmail || !respEmail.value.trim()) {
			frappe.msgprint("Please enter your email before submitting.");
			respEmail && respEmail.focus();
			return;
		}

		// Save first, then submit
		save(function () {
			frappe.confirm(
				"Are you sure you want to submit this BRD? You will not be able to make changes after submission.",
				function () {
					frappe.call({
						method: "brd_tool.www.brd.session.index.submit_session",
						args: {
							access_key: accessKey,
							respondent_name: respName.value.trim(),
							respondent_email: respEmail.value.trim(),
							respondent_role: respRole
								? respRole.value.trim()
								: "",
						},
						callback: function () {
							frappe.msgprint({
								title: "Thank You!",
								message:
									"Your BRD has been submitted successfully. Your consultant will review it shortly.",
								indicator: "green",
								primary_action: {
									label: "OK",
									action: function () {
										window.location.reload();
									},
								},
							});
						},
						error: function (r) {
							frappe.msgprint(
								r.message || "Submission failed. Please try again."
							);
						},
					});
				}
			);
		});
	}

	// --- Event Listeners ---
	if (!isSubmitted) {
		// Textareas
		document.querySelectorAll(".brd-textarea").forEach(function (el) {
			el.addEventListener("input", function () {
				updateProgress();
				scheduleSave();
			});
		});

		// Radios
		document
			.querySelectorAll("input[data-field='response_single']")
			.forEach(function (el) {
				el.addEventListener("change", function () {
					updateProgress();
					scheduleSave();
				});
			});

		// Checkboxes
		document
			.querySelectorAll("input[data-field='response_multi']")
			.forEach(function (el) {
				el.addEventListener("change", function () {
					updateProgress();
					scheduleSave();
				});
			});

		// Save button
		if (saveBtn) {
			saveBtn.addEventListener("click", function () {
				save();
			});
		}

		// Submit button
		if (submitBtn) {
			submitBtn.addEventListener("click", submitSession);
		}

		// Initial status
		setStatus("saved", "Ready");
	} else {
		setStatus("saved", "Submitted");
	}

	// --- TOC smooth scroll ---
	document.querySelectorAll(".brd-toc-item").forEach(function (a) {
		a.addEventListener("click", function (e) {
			e.preventDefault();
			const target = document.querySelector(a.getAttribute("href"));
			if (target) {
				target.scrollIntoView({ behavior: "smooth", block: "start" });
			}
		});
	});

	// Nav buttons smooth scroll
	document.querySelectorAll(".brd-btn-nav").forEach(function (a) {
		a.addEventListener("click", function (e) {
			e.preventDefault();
			const target = document.querySelector(a.getAttribute("href"));
			if (target) {
				target.scrollIntoView({ behavior: "smooth", block: "start" });
			}
		});
	});

	// Initial progress
	updateProgress();
});
