import os
import json
import glob

SCENARIO_SET_DIR = os.path.join(os.path.dirname(__file__), "..", "scenarios", "set_v1")

# Clean existing scenarios directory
for f in glob.glob(os.path.join(SCENARIO_SET_DIR, "*.json")):
    os.remove(f)

# 32 Canonical Frozen Scenarios (16 Malicious = 50%, 10 Genuine = 31.25%, 6 Ambiguous = 18.75%)
SCENARIOS = [
    # --- FAMILY 1: AUTH+URG Education Email (Malicious) ---
    {
        "scenario_id": "EDU-AUTH-URG-MAL-01",
        "family_id": "FAM-AUTHURG-EDU-01",
        "phase_pool": "baseline",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "truth": "malicious",
        "mechanisms": ["authority", "urgency"],
        "pressure": "high",
        "difficulty": "medium",
        "narrative": "Placement coordinator emails a shortlist notice with an urgent deadline.",
        "message": {
            "sender_display": "Placement Officer <placements@college-career.net>",
            "body": "Urgent: You have been shortlisted for the TechCorp internship. You must fill out the attached registration form within 20 minutes or your nomination will be cancelled.",
            "attachment": "TechCorp_Registration_Form.pdf.exe"
        },
        "evidence": [
            {"id": "e1", "label": "Sender Email Address", "value": "placements@college-career.net", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Attachment Extension", "value": "TechCorp_Registration_Form.pdf.exe", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Greeting Format", "value": "Dear Student,", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Official Placement Portal Notice", "value": "No shortlist notice published on college.edu.in portal.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "Verifying on the official placement portal revealed no such shortlist. You avoided installing malicious executable software.",
            "unsafe": "Opening the executable attachment would have installed malware on your system (simulated)."
        },
        "teaching_point": "Urgent claims from authority figures should increase your verification effort rather than rushing your decision.",
        "transfer_group": "AUTH_URG"
    },
    {
        "scenario_id": "EDU-AUTH-URG-MAL-02",
        "family_id": "FAM-AUTHURG-EDU-01",
        "phase_pool": "retest",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "truth": "malicious",
        "mechanisms": ["authority", "urgency"],
        "pressure": "high",
        "difficulty": "medium",
        "narrative": "Academic Office emails an urgent fee reconciliation alert.",
        "message": {
            "sender_display": "Academic Office <office@academic-services-portal.com>",
            "body": "Final Notice: Your tuition fee receipt is mismatched. Submit the updated verification form within 30 minutes to avoid course deregistration.",
            "attachment": "Fee_Verification_Form.scr"
        },
        "evidence": [
            {"id": "e1", "label": "Sender Address Domain", "value": "office@academic-services-portal.com", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Attachment File Type", "value": "Fee_Verification_Form.scr", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Student ID Mentioned", "value": "Student ID #88421 listed in body", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Official University Registrar Portal", "value": "Fee payment status marked Fully Paid on official portal.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "Checking your official student ledger confirmed your fees were already paid. You avoided opening an untrusted executable.",
            "unsafe": "Executing the script attachment would have compromised your student account credentials (simulated)."
        },
        "teaching_point": "Threats of administrative penalties under tight deadlines are classic high-pressure cues.",
        "transfer_group": "AUTH_URG"
    },
    {
        "scenario_id": "FIN-AUTH-URG-MAL-01",
        "family_id": "FAM-AUTHURG-EDU-01",
        "phase_pool": "transfer",
        "context": "finance",
        "channel": "chat",
        "persona": "bank customer (fictional)",
        "truth": "malicious",
        "mechanisms": ["authority", "urgency"],
        "pressure": "high",
        "difficulty": "medium",
        "narrative": "WhatsApp text claiming to be Bank Security alerting you of a blocked card.",
        "message": {
            "sender_display": "Apex Bank Cyber Support (+91-9876543210)",
            "body": "ALERT: Suspicious transaction of ₹24,500 detected on your Apex Credit Card. Card will be permanently blocked in 15 minutes unless you share the security verification code sent to your phone.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Mobile Number", "value": "Personal 10-digit mobile number (+91-9876543210)", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Request for OTP/Code", "value": "Asks for security verification code via chat", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Bank Logo Profile Picture", "value": "Displays Apex Bank official crest image", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Apex Bank Mobile App Hotline", "value": "App shows card status ACTIVE; security officer states banks never ask for codes over chat.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "Calling Apex Bank using the number on your credit card confirmed your card was active and no transaction occurred.",
            "unsafe": "Sharing the code would have authorized an unauthorized financial transfer (simulated)."
        },
        "teaching_point": "Transfer strategy: Official institutions will never ask for authentication codes or passwords over messaging apps.",
        "transfer_group": "AUTH_URG"
    },

    # --- FAMILY 2: AUTH Genuine Education (Email & Chat) ---
    {
        "scenario_id": "EDU-AUTH-GEN-01",
        "family_id": "FAM-AUTH-EDU-02",
        "phase_pool": "baseline",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "low",
        "narrative": "Central Library sends a routine book return notice.",
        "message": {
            "sender_display": "Library Desk <library@college.edu.in>",
            "body": "Dear Student, your borrowed book 'Computer Networks 5th Ed' is due in 3 days. Please return or renew it online via the library catalog before Friday.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Email Address", "value": "library@college.edu.in", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Due Date", "value": "3 days remaining (Standard notice)", "signal": "neutral", "diagnosticity": "low", "official_channel": False},
            {"id": "e3", "label": "Official Library Catalog Portal", "value": "Log in at library.college.edu.in shows 'Computer Networks 5th Ed' due in 3 days.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You verified the notice on the official library portal and renewed your book on time.",
            "unsafe": "Ignoring or reporting legitimate administrative communications causes missed deadlines and unnecessary friction."
        },
        "teaching_point": "Over-caution check: Legitimate routine notices from official domains should be verified and acted upon.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "EDU-AUTH-GEN-02",
        "family_id": "FAM-AUTH-EDU-02",
        "phase_pool": "retest",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "low",
        "narrative": "Course Coordinator sends an end-semester feedback survey notice.",
        "message": {
            "sender_display": "Academic Evaluation <evaluations@college.edu.in>",
            "body": "The course feedback portal for CS301 is now open until next week. Please complete your evaluation on the student dashboard.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "evaluations@college.edu.in", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Survey Link Destination", "value": "Directs to https://student.college.edu.in/eval", "signal": "trustworthy", "diagnosticity": "medium", "official_channel": False},
            {"id": "e3", "label": "Official Student Dashboard", "value": "Dashboard displays active CS301 feedback banner.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You confirmed the survey on your dashboard and submitted your course feedback safely.",
            "unsafe": "Reporting valid official notifications leads to over-caution and missed administrative tasks."
        },
        "teaching_point": "Verify authentic notices via your official dashboard without suspicion bias.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "SOC-AUTH-GEN-01",
        "family_id": "FAM-AUTH-EDU-02",
        "phase_pool": "transfer",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "community member (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "low",
        "narrative": "Resident Welfare Association Secretary sends a meeting reminder on WhatsApp.",
        "message": {
            "sender_display": "RWA Secretary (Verified Group Admin)",
            "body": "Good evening all. Reminder: Annual General Meeting this Sunday at 10 AM in the Clubhouse. Agenda document is posted on the notice board.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Contact", "value": "Saved contact of elected RWA Secretary", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Message Content", "value": "Informational reminder; asks for no codes or payments", "signal": "neutral", "diagnosticity": "medium", "official_channel": False},
            {"id": "e3", "label": "Official Society Notice Board", "value": "Physical notice board and society app show identical AGM schedule.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You checked the society notice board and confirmed the upcoming meeting details.",
            "unsafe": "Rejecting authentic community reminders creates needless paranoia."
        },
        "teaching_point": "Informational messages from known contacts without sensitive requests are genuine.",
        "transfer_group": "AUTH"
    },

    # --- FAMILY 3: REW+URG Ambiguous (Email / Chat) ---
    {
        "scenario_id": "EDU-REW-URG-AMB-01",
        "family_id": "FAM-REWURG-AMB-03",
        "phase_pool": "baseline",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "truth": "ambiguous",
        "mechanisms": ["reward_scarcity", "urgency"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "An unfamiliar recruiter offers an exclusive research stipend.",
        "message": {
            "sender_display": "Global Ed Foundation <grants@ed-foundation-global.org>",
            "body": "Congratulations! Your profile was nominated for a ₹25,000 summer research micro-grant. Only 3 slots remain. Respond within 24 hours to secure your allocation.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "ed-foundation-global.org", "signal": "neutral", "diagnosticity": "medium", "official_channel": False},
            {"id": "e2", "label": "Stipend Amount", "value": "₹25,000 (Plausible micro-grant amount)", "signal": "neutral", "diagnosticity": "low", "official_channel": False},
            {"id": "e3", "label": "University Research Dean Office", "value": "Dean office notes this foundation is unverified; official confirmation pending.", "signal": "hidden", "diagnosticity": "medium", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "acceptable": ["UNSURE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You reached out to the Research Dean before acting, avoiding sharing details with an unverified foundation.",
            "unsafe": "Proceeding without gathering more evidence on ambiguous offers exposes you to potential scam harvesting."
        },
        "teaching_point": "When encountering unverified offers with missing diagnostic clues, gather more evidence before taking action.",
        "transfer_group": "REW_URG"
    },
    {
        "scenario_id": "EDU-REW-URG-AMB-02",
        "family_id": "FAM-REWURG-AMB-03",
        "phase_pool": "retest",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "truth": "ambiguous",
        "mechanisms": ["reward_scarcity", "urgency"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "An email claims you won an international conference travel pass.",
        "message": {
            "sender_display": "TechSummit Secretariat <passes@techsummit-events.net>",
            "body": "You have been selected for a complimentary student delegate pass to TechSummit 2026. Only 5 passes left. Confirm your registration code today.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "techsummit-events.net", "signal": "neutral", "diagnosticity": "medium", "official_channel": False},
            {"id": "e2", "label": "Conference Name", "value": "TechSummit 2026 (Real annual event)", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e3", "label": "Department Placement Chair", "value": "Placement chair has not received formal sponsor confirmation yet.", "signal": "hidden", "diagnosticity": "medium", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "acceptable": ["UNSURE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You checked with your department chair first to verify whether the sponsor was legitimate.",
            "unsafe": "Rushing to claim unverified passes without checking official channels is unsafe in ambiguous scenarios."
        },
        "teaching_point": "Ambiguous opportunities require out-of-band verification before commitment.",
        "transfer_group": "REW_URG"
    },
    {
        "scenario_id": "SOC-REW-URG-AMB-01",
        "family_id": "FAM-REWURG-AMB-03",
        "phase_pool": "transfer",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "social media user (fictional)",
        "truth": "ambiguous",
        "mechanisms": ["reward_scarcity", "urgency"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "A messaging group post offers early access ticket passes.",
        "message": {
            "sender_display": "Classmate Contact (Forwarded)",
            "body": "Hey everyone! Campus Music Fest early bird passes are live on this portal for 2 hours only. Limited 50 passes left!",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Forwarded Tag", "value": "Forwarded message from unknown original sender", "signal": "suspicious", "diagnosticity": "medium", "official_channel": False},
            {"id": "e2", "label": "Ticket Price", "value": "Standard early bird price (₹500)", "signal": "neutral", "diagnosticity": "low", "official_channel": False},
            {"id": "e3", "label": "Official Student Union Ticketing Portal", "value": "Official portal lists early bird sales starting tomorrow, not today.", "signal": "hidden", "diagnosticity": "medium", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "acceptable": ["UNSURE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "Checking the official union portal revealed the message was an unofficial link.",
            "unsafe": "Clicking unverified ticket links in chat groups can lead to credential phishing."
        },
        "teaching_point": "Forwarded scarcity offers in chat channels should be cross-referenced with official ticket portals.",
        "transfer_group": "REW_URG"
    },

    # --- FAMILY 4: FIN URG Malicious (Chat & Email) ---
    {
        "scenario_id": "FIN-URG-MAL-01",
        "family_id": "FAM-URG-FIN-04",
        "phase_pool": "baseline",
        "context": "finance",
        "channel": "chat",
        "persona": "mobile banking user (fictional)",
        "truth": "malicious",
        "mechanisms": ["urgency"],
        "pressure": "high",
        "difficulty": "high",
        "narrative": "SMS warning about an immediate account suspension.",
        "message": {
            "sender_display": "PAY-ALERT (+91-9123456789)",
            "body": "CRITICAL: Your PayQuick UPI account is flagged for non-compliance. Click http://payquick-verify-kyc.info to update KYC within 10 minutes or your account will be frozen.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Domain URL", "value": "http://payquick-verify-kyc.info", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Protocol Used", "value": "Unencrypted HTTP link (http://)", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "SMS Header", "value": "Uses PAY-ALERT sender ID tag", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "PayQuick Official App", "value": "KYC status shows fully verified; official support notes KYC updates are only done inside the official app.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You checked your KYC status directly inside the official app and confirmed your account was fully compliant.",
            "unsafe": "Following unencrypted external links for KYC update leads to financial credential theft (simulated)."
        },
        "teaching_point": "Financial institutions never require KYC updates over unencrypted external HTTP links.",
        "transfer_group": "URG"
    },
    {
        "scenario_id": "FIN-URG-MAL-02",
        "family_id": "FAM-URG-FIN-04",
        "phase_pool": "retest",
        "context": "finance",
        "channel": "chat",
        "persona": "mobile banking user (fictional)",
        "truth": "malicious",
        "mechanisms": ["urgency"],
        "pressure": "high",
        "difficulty": "high",
        "narrative": "SMS warning about an unauthorized loan debit.",
        "message": {
            "sender_display": "BANK-MSG (+91-9887766554)",
            "body": "URGENT: Auto-debit of ₹49,999 for EMI Loan #9941 is scheduled in 15 mins. If you did NOT authorize this, cancel immediately at http://apex-debit-cancel.com",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Domain Name", "value": "apex-debit-cancel.com", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Sender Number", "value": "Standard 10-digit mobile number", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Loan Reference Number", "value": "Loan #9941 listed", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Apex Bank Customer Service", "value": "Customer care confirms no loan #9941 exists on your account.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You called your bank customer service out-of-band and confirmed no loan debit existed.",
            "unsafe": "Clicking panic-inducing cancellation links delivers your banking login to attackers."
        },
        "teaching_point": "Fake cancellation warnings exploit panic to bypass independent verification.",
        "transfer_group": "URG"
    },
    {
        "scenario_id": "EDU-URG-MAL-01",
        "family_id": "FAM-URG-FIN-04",
        "phase_pool": "transfer",
        "context": "education_career",
        "channel": "email",
        "persona": "student applicant (fictional)",
        "truth": "malicious",
        "mechanisms": ["urgency"],
        "pressure": "high",
        "difficulty": "high",
        "narrative": "Email warning that your exam hall ticket will be revoked.",
        "message": {
            "sender_display": "Exam Cell <halltickets@exam-board-online.org>",
            "body": "URGENT: Discrepancy found in your admit card photo. Upload corrected photo at http://admitcard-fix-portal.org within 20 minutes or hall ticket will be cancelled.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "exam-board-online.org", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "URL Domain", "value": "http://admitcard-fix-portal.org", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Exam Name", "value": "National Entrance Exam 2026", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Official Examination Controller Portal", "value": "Admit card status shows Valid & Verified; no photo correction notice listed.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You verified your hall ticket on the official exam portal and confirmed it was valid.",
            "unsafe": "Submitting details on lookalike portals compromises your personal credentials."
        },
        "teaching_point": "Transfer strategy: Apply verification strategies across academic and exam portals when faced with urgent revocation threats.",
        "transfer_group": "URG"
    },

    # --- FAMILY 5: FIN Genuine (Email & Chat) ---
    {
        "scenario_id": "FIN-GEN-01",
        "family_id": "FAM-GEN-FIN-05",
        "phase_pool": "baseline",
        "context": "finance",
        "channel": "email",
        "persona": "bank customer (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "medium",
        "narrative": "Monthly credit card e-statement notification.",
        "message": {
            "sender_display": "Apex Bank Statements <estatements@apexbank.com>",
            "body": "Dear Customer, your credit card e-statement for September 2026 is now available. Log in to your Apex Bank mobile app or web portal to view your statement.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "apexbank.com (Official domain)", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Instructions", "value": "Asks user to log in via official app/site (no links or attachments)", "signal": "trustworthy", "diagnosticity": "medium", "official_channel": False},
            {"id": "e3", "label": "Apex Bank Mobile App", "value": "Mobile app e-statement section displays matching September statement.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You opened your official bank app and accessed your statement securely.",
            "unsafe": "Reporting legitimate e-statement notifications causes unnecessary alarm."
        },
        "teaching_point": "Routine statement notifications directing users to official apps are safe.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "FIN-GEN-02",
        "family_id": "FAM-GEN-FIN-05",
        "phase_pool": "retest",
        "context": "finance",
        "channel": "email",
        "persona": "bank customer (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "medium",
        "narrative": "Annual interest rate disclosure update notice.",
        "message": {
            "sender_display": "Apex Bank Compliance <compliance@apexbank.com>",
            "body": "Notice of revised savings interest rates effective October 1. View the policy table at https://www.apexbank.com/rates. No action is required.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Address", "value": "compliance@apexbank.com", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "URL Host", "value": "https://www.apexbank.com", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Official Bank Homepage", "value": "Rates page on apexbank.com matches the disclosure table.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You reviewed the rate update on the official bank site.",
            "unsafe": "Ignoring official rate notices keeps you uninformed on bank terms."
        },
        "teaching_point": "Informational announcements pointing to the bank's root domain are genuine.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "SOC-GEN-01",
        "family_id": "FAM-GEN-FIN-05",
        "phase_pool": "transfer",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "chat app user (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "medium",
        "narrative": "Two-factor authentication code sent upon your login request.",
        "message": {
            "sender_display": "AppAuth (Official 2FA Service)",
            "body": "Your 2FA login code is 492-018. If you did not initiate a login, please change your password on the app settings immediately.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Trigger Event", "value": "Sent immediately after you entered your password on your laptop", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Message Text", "value": "Standard 2FA format; does not ask to forward code", "signal": "trustworthy", "diagnosticity": "medium", "official_channel": False},
            {"id": "e3", "label": "Laptop Login Screen", "value": "Login screen is actively waiting for 6-digit 2FA input.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You entered the code into your active login session securely.",
            "unsafe": "Ignoring 2FA codes that you personally requested prevents you from logging in."
        },
        "teaching_point": "2FA codes requested by your own actions are genuine and safe to enter on your login prompt.",
        "transfer_group": "AUTH"
    },

    # --- FAMILY 6: REW Malicious (Email & Chat) ---
    {
        "scenario_id": "SOC-REW-MAL-01",
        "family_id": "FAM-REW-SOC-06",
        "phase_pool": "baseline",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "messaging app user (fictional)",
        "truth": "malicious",
        "mechanisms": ["reward_scarcity"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "A hacked friend contact messages you to vote for them in a contest.",
        "message": {
            "sender_display": "Priya (Classmate)",
            "body": "Hey!! I'm in the top 3 for the National Art Contest win ₹50k prize! Can you please vote for me real quick? Click http://artcontest-vote-verify.com and log in with your account to confirm vote!",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Voting Link Domain", "value": "http://artcontest-vote-verify.com", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Credential Request", "value": "Requires logging in with personal social credentials to vote", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Friend Profile Name", "value": "Matches classmate's real profile name and photo", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Direct Voice Call to Priya", "value": "Priya answers call and says her account was hacked 1 hour ago.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "Calling your friend out-of-band revealed her account was compromised.",
            "unsafe": "Entering credentials on contest voting links hands account control to hijackers."
        },
        "teaching_point": "Contest voting links sent from friend accounts are common social engineering vectors.",
        "transfer_group": "REW"
    },
    {
        "scenario_id": "SOC-REW-MAL-02",
        "family_id": "FAM-REW-SOC-06",
        "phase_pool": "retest",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "messaging app user (fictional)",
        "truth": "malicious",
        "mechanisms": ["reward_scarcity"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "A friend sends a link for a free gift card promotion.",
        "message": {
            "sender_display": "Rohan (College Friend)",
            "body": "Bro check this out! StoreX is giving free ₹2,000 gift vouchers for anniversary! Got mine in 2 mins: http://storex-free-voucher.info",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Voucher Link Domain", "value": "http://storex-free-voucher.info", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Unusual Messaging Tone", "value": "Rohan rarely sends promotional links", "signal": "suspicious", "diagnosticity": "medium", "official_channel": False},
            {"id": "e3", "label": "Sender Contact Name", "value": "Saved contact Rohan", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "StoreX Official Website", "value": "StoreX.com official site states no free voucher promo exists; warns of phishing link.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "Checking StoreX's official website confirmed the voucher link was a scam.",
            "unsafe": "Clicking gift card links spreads malware and steals personal data."
        },
        "teaching_point": "Free voucher claims sent via chat should be verified against official brand websites.",
        "transfer_group": "REW"
    },
    {
        "scenario_id": "FIN-REW-MAL-01",
        "family_id": "FAM-REW-SOC-06",
        "phase_pool": "transfer",
        "context": "finance",
        "channel": "email",
        "persona": "banking customer (fictional)",
        "truth": "malicious",
        "mechanisms": ["reward_scarcity"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "An email claims you received an unexpected cashback reward.",
        "message": {
            "sender_display": "PayQuick Rewards <rewards@payquick-cashback-claim.net>",
            "body": "You have an unclaimed cashback reward of ₹1,450 from your recent UPI transactions. Click below to enter your bank details and claim before link expires.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Address Domain", "value": "payquick-cashback-claim.net", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Request for Banking Details", "value": "Asks for account number and PIN to claim reward", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Brand Logo", "value": "PayQuick corporate logo in header", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "PayQuick Official App Rewards Tab", "value": "App shows ₹0 pending rewards; legitimate cashbacks are credited automatically without requesting details.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You checked your official banking app and confirmed no cashback claim was required.",
            "unsafe": "Entering bank details for fake cashback rewards grants full access to account funds."
        },
        "teaching_point": "Transfer strategy: Real financial rewards do not require entering secret banking details on external sites.",
        "transfer_group": "REW"
    },

    # --- FAMILY 7: AUTH Finance Chat (Malicious) ---
    {
        "scenario_id": "FIN-AUTH-MAL-01",
        "family_id": "FAM-AUTH-FIN-07",
        "phase_pool": "baseline",
        "context": "finance",
        "channel": "chat",
        "persona": "bank customer (fictional)",
        "truth": "malicious",
        "mechanisms": ["authority"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "A chat message claims to be from Income Tax Department regarding refund audit.",
        "message": {
            "sender_display": "IT-TAX-DEPT (+91-9776655443)",
            "body": "Income Tax Refund Notice: Tax refund of ₹12,400 for Assessment Year 2025-26 approved. Verify bank account details at http://incometax-refund-portal.org",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Domain URL", "value": "http://incometax-refund-portal.org", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "SMS Sender Number", "value": "Unregistered 10-digit number", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Assessment Year", "value": "Correct AY 2025-26 format", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Official e-Filing Portal (incometax.gov.in)", "value": "Official portal refund status shows 'No pending refund verification'.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "Checking the official government portal confirmed no tax refund verification was pending.",
            "unsafe": "Submitting bank details on fake tax portals leads to credential theft."
        },
        "teaching_point": "Government tax refunds are processed exclusively on government .gov.in portals.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "FIN-AUTH-MAL-02",
        "family_id": "FAM-AUTH-FIN-07",
        "phase_pool": "retest",
        "context": "finance",
        "channel": "chat",
        "persona": "bank customer (fictional)",
        "truth": "malicious",
        "mechanisms": ["authority"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "Message claiming to be Central Bank Insurance Officer.",
        "message": {
            "sender_display": "RBI-ALERT (+91-9665544332)",
            "body": "Central Bank Safety Regulation: Your deposit insurance compliance needs renewal. Submit account confirmation at http://deposit-safety-verify.net",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Website Link", "value": "http://deposit-safety-verify.net", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Regulatory Claim", "value": "Claims RBI requires individual deposit safety verification", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Regulatory Terms", "value": "Uses official banking terms", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "RBI Official Advisory Site", "value": "RBI advisory explicitly states central bank never contacts individuals for deposit verification.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You checked official RBI advisories and confirmed central banks do not request individual account verification.",
            "unsafe": "Submitting data on fake regulator sites compromises financial credentials."
        },
        "teaching_point": "Central banks and financial regulators do not contact individual customers for account renewals.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "EDU-AUTH-MAL-01",
        "family_id": "FAM-AUTH-FIN-07",
        "phase_pool": "transfer",
        "context": "education_career",
        "channel": "email",
        "persona": "researcher (fictional)",
        "truth": "malicious",
        "mechanisms": ["authority"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "Email claiming to be University Ethics Board requiring protocol audit.",
        "message": {
            "sender_display": "IRB Ethics Board <irb@ethics-compliance-portal.org>",
            "body": "Mandatory IRB Compliance Audit: Your active study protocol requires re-authorization. Upload study data at http://irb-audit-upload.org",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "ethics-compliance-portal.org", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Upload Link", "value": "http://irb-audit-upload.org", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Protocol Reference", "value": "Refers to active research study", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "University Research Ethics Portal", "value": "University IRB site shows all protocol approvals active with no audit required.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You verified protocol status on the university IRB portal and confirmed no audit was pending.",
            "unsafe": "Uploading data to external audit links exposes research data to unauthorized parties."
        },
        "teaching_point": "Transfer strategy: Verify institutional compliance audits via internal university portals.",
        "transfer_group": "AUTH"
    },

    # --- FAMILY 8: FIN Ambiguous (Email & Chat) ---
    {
        "scenario_id": "FIN-AMB-01",
        "family_id": "FAM-AMB-FIN-08",
        "phase_pool": "baseline",
        "context": "finance",
        "channel": "email",
        "persona": "bank customer (fictional)",
        "truth": "ambiguous",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "medium",
        "narrative": "Email regarding an unexpected dividend credit payout.",
        "message": {
            "sender_display": "Registrar Services <disbursements@national-registry-services.net>",
            "body": "Dividend Disbursement Notice: A dividend payment of ₹850 from your mutual fund holdings was processed. Please verify your mandate details on our portal.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "national-registry-services.net", "signal": "neutral", "diagnosticity": "medium", "official_channel": False},
            {"id": "e2", "label": "Payout Amount", "value": "₹850 (Typical quarterly dividend amount)", "signal": "neutral", "diagnosticity": "low", "official_channel": False},
            {"id": "e3", "label": "Mutual Fund Asset Management Company", "value": "Mutual fund portal confirms dividend declared, but list of official registrars is unconfirmed.", "signal": "hidden", "diagnosticity": "medium", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "acceptable": ["UNSURE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You verified dividend payouts directly with your mutual fund manager before clicking links.",
            "unsafe": "Proceeding without verifying dividend registrars can lead to phishing."
        },
        "teaching_point": "Verify financial disbursements with your primary asset manager before taking online action.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "FIN-AMB-02",
        "family_id": "FAM-AMB-FIN-08",
        "phase_pool": "retest",
        "context": "finance",
        "channel": "email",
        "persona": "bank customer (fictional)",
        "truth": "ambiguous",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "medium",
        "narrative": "Email regarding an insurance policy bonus credit.",
        "message": {
            "sender_display": "Policy Admin <bonus@insurance-disbursement.org>",
            "body": "Annual Loyalty Bonus: Your life insurance policy accrued a bonus of ₹4,200. Check your eligibility status on our policy portal.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Address", "value": "bonus@insurance-disbursement.org", "signal": "neutral", "diagnosticity": "medium", "official_channel": False},
            {"id": "e2", "label": "Policy Number Format", "value": "Format matches general policy numbering", "signal": "neutral", "diagnosticity": "low", "official_channel": False},
            {"id": "e3", "label": "Insurance Agent Hotline", "value": "Agent advises checking bonus directly in the insurer's official mobile app.", "signal": "hidden", "diagnosticity": "medium", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "acceptable": ["UNSURE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You checked your bonus status on your insurer's official mobile app.",
            "unsafe": "Rushing into unverified insurance claims carries phishing risks."
        },
        "teaching_point": "Check policy bonuses inside official app portals.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "SOC-AMB-01",
        "family_id": "FAM-AMB-FIN-08",
        "phase_pool": "transfer",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "messaging user (fictional)",
        "truth": "ambiguous",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "medium",
        "narrative": "Chat message from a local delivery agent requesting address confirmation.",
        "message": {
            "sender_display": "Courier Logistics (+91-9554433221)",
            "body": "Hello, we have a parcel for your address but street number is unclear. Confirm address on courier-tracking-portal.com or reply here.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Contact", "value": "Delivery agent number", "signal": "neutral", "diagnosticity": "medium", "official_channel": False},
            {"id": "e2", "label": "Parcel Tracking ID", "value": "Tracking ID #CR-8812 listed", "signal": "neutral", "diagnosticity": "low", "official_channel": False},
            {"id": "e3", "label": "E-Commerce App Orders Page", "value": "App shows an item out for delivery today, but courier partner name is unlisted.", "signal": "hidden", "diagnosticity": "medium", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "acceptable": ["UNSURE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You cross-referenced your e-commerce order page before providing address updates.",
            "unsafe": "Responding blindly to delivery queries can leak home address details to unauthorized entities."
        },
        "teaching_point": "Verify parcel tracking against your main shopping account before sharing details.",
        "transfer_group": "AUTH"
    },

    # --- FAMILY 9: URG Social Chat (Malicious) ---
    {
        "scenario_id": "SOC-URG-MAL-01",
        "family_id": "FAM-URG-SOC-09",
        "phase_pool": "baseline",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "chat user (fictional)",
        "truth": "malicious",
        "mechanisms": ["urgency"],
        "pressure": "high",
        "difficulty": "medium",
        "narrative": "Urgent chat claiming your cloud backup storage will be deleted in 10 minutes.",
        "message": {
            "sender_display": "CloudDrive Alert (+91-9443322110)",
            "body": "CRITICAL: CloudDrive storage quota exceeded. 2.4 GB of personal photos will be PERMANENTLY DELETED in 10 minutes. Upgrade storage immediately at http://clouddrive-upgrade-now.com",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Upgrade Link Domain", "value": "http://clouddrive-upgrade-now.com", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Payment Request", "value": "Requires entering credit card details on unencrypted page", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Service Name", "value": "CloudDrive (Popular service)", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "CloudDrive App Settings", "value": "App settings shows 45 GB available of 100 GB quota.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You opened your CloudDrive app settings and saw plenty of free storage remaining.",
            "unsafe": "Panic-buying storage on suspicious links leads to credit card fraud."
        },
        "teaching_point": "Check cloud storage quotas inside the official app settings when threatened with deletion.",
        "transfer_group": "URG"
    },
    {
        "scenario_id": "SOC-URG-MAL-02",
        "family_id": "FAM-URG-SOC-09",
        "phase_pool": "retest",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "chat user (fictional)",
        "truth": "malicious",
        "mechanisms": ["urgency"],
        "pressure": "high",
        "difficulty": "medium",
        "narrative": "Urgent message claiming your social account will be suspended.",
        "message": {
            "sender_display": "Account Trust Team (+91-9332211009)",
            "body": "URGENT: Copyright violation reported on your post. Your account will be DELETED in 15 minutes unless you appeal at http://social-copyright-appeal.net",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Appeal URL", "value": "http://social-copyright-appeal.net", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Urgency Period", "value": "15-minute deletion threat", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Header Logo", "value": "Displays platform trust badge", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "In-App Support Inbox", "value": "Support inbox shows zero copyright violations or warnings.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "Checking your in-app support inbox revealed no copyright notices.",
            "unsafe": "Entering credentials on fake appeal sites leads to account takeover."
        },
        "teaching_point": "Official copyright warnings appear in your account's in-app support center, never via random text messages.",
        "transfer_group": "URG"
    },
    {
        "scenario_id": "FIN-URG-MAL-03",
        "family_id": "FAM-URG-SOC-09",
        "phase_pool": "transfer",
        "context": "finance",
        "channel": "email",
        "persona": "banking customer (fictional)",
        "truth": "malicious",
        "mechanisms": ["urgency"],
        "pressure": "high",
        "difficulty": "medium",
        "narrative": "Email claiming urgent utility bill payment required to prevent immediate disconnection.",
        "message": {
            "sender_display": "Power Grid Services <billing@power-disconnection-alert.org>",
            "body": "IMMEDIATE DISCONNECTION NOTICE: Electricity connection will be cut at 8:00 PM due to pending bill of ₹1,820. Pay immediately at http://powerbill-quickpay.org",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "power-disconnection-alert.org", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Payment URL", "value": "http://powerbill-quickpay.org", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Consumer Account Number", "value": "Account #7741 listed", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Official Electricity Utility Portal", "value": "Utility portal shows zero outstanding bill; status fully paid.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You checked your utility provider's official portal and confirmed your bill was paid.",
            "unsafe": "Paying bills via suspicious link leads to financial theft."
        },
        "teaching_point": "Verify utility bill alerts on the official provider website before making payments.",
        "transfer_group": "URG"
    },

    # --- FAMILY 10: GENUINE ADDITIONAL SCENARIOS (Pools B, R, T) ---
    {
        "scenario_id": "FIN-GEN-03",
        "family_id": "FAM-GEN-FIN-10",
        "phase_pool": "baseline",
        "context": "finance",
        "channel": "email",
        "persona": "bank customer (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "low",
        "narrative": "Annual bank terms & conditions privacy policy update.",
        "message": {
            "sender_display": "Apex Bank Privacy <privacy@apexbank.com>",
            "body": "Notice of Privacy Policy Update: We updated our privacy policy in accordance with regulations. View the updated terms on www.apexbank.com/privacy",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "apexbank.com", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Policy Link", "value": "https://www.apexbank.com/privacy", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Official Bank Homepage", "value": "Homepage footer links to identical privacy document.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You verified the privacy terms on the bank's official website.",
            "unsafe": "Reporting valid privacy updates creates unnecessary support tickets."
        },
        "teaching_point": "Privacy updates pointing to main corporate domains are authentic.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "SOC-GEN-02",
        "family_id": "FAM-GEN-FIN-10",
        "phase_pool": "retest",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "chat user (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "low",
        "narrative": "Group admin sharing a scheduled study group zoom link.",
        "message": {
            "sender_display": "Study Group Admin (Classmate)",
            "body": "Hey guys! Reminder: Study session starts at 5 PM on our usual Zoom link. Topic: Operating Systems Chapter 4.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Contact", "value": "Classmate phone number in group chat", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Zoom Meeting ID", "value": "Matches regular class recurring meeting ID", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Course Syllabus Calendar", "value": "Syllabus schedules OS Chapter 4 review for today.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You joined the study session using your regular class link.",
            "unsafe": "Ignoring legitimate study group messages leads to missed peer review."
        },
        "teaching_point": "Routine study group reminders matching class schedules are genuine.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "EDU-GEN-03",
        "family_id": "FAM-GEN-FIN-10",
        "phase_pool": "transfer",
        "context": "education_career",
        "channel": "email",
        "persona": "student (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "low",
        "narrative": "Campus IT notice regarding scheduled weekend maintenance.",
        "message": {
            "sender_display": "Campus IT Helpdesk <helpdesk@college.edu.in>",
            "body": "Scheduled Maintenance: Wi-Fi services will undergo maintenance on Saturday from 2 AM to 5 AM. No action is required from users.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Domain", "value": "college.edu.in", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Message Type", "value": "Informational notice; asks for no credentials or clicks", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Campus IT Announcement Portal", "value": "Portal lists scheduled maintenance window for Saturday.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You verified the IT announcement on the college portal.",
            "unsafe": "Reporting routine maintenance notices creates unnecessary helpdesk clutter."
        },
        "teaching_point": "System maintenance notices that require no action are authentic.",
        "transfer_group": "AUTH"
    },

    # --- POOL D (DELAYED RETEST POOL) - 8 SCENARIOS ---
    {
        "scenario_id": "EDU-AUTH-URG-MAL-D1",
        "family_id": "FAM-AUTHURG-EDU-01",
        "phase_pool": "delayed",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "truth": "malicious",
        "mechanisms": ["authority", "urgency"],
        "pressure": "high",
        "difficulty": "high",
        "narrative": "Delayed retest: Thesis submission clearance deadline threat.",
        "message": {
            "sender_display": "Graduate School Office <clearance@grad-school-admin.net>",
            "body": "URGENT: Thesis approval document pending digital signature. Upload signed PDF within 30 minutes at http://grad-thesis-sign.net or graduation will be postponed.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Domain URL", "value": "http://grad-thesis-sign.net", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Sender Address", "value": "clearance@grad-school-admin.net", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Degree Name", "value": "Master of Science in Computer Science", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "Graduate School Portal", "value": "Portal shows thesis status fully approved and signed.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You verified thesis clearance on the official portal.",
            "unsafe": "Submitting files on external links compromises graduate credentials."
        },
        "teaching_point": "Delayed retention: Always verify graduation clearance directly on university portals.",
        "transfer_group": "AUTH_URG"
    },
    {
        "scenario_id": "EDU-AUTH-GEN-D1",
        "family_id": "FAM-AUTH-EDU-02",
        "phase_pool": "delayed",
        "context": "education_career",
        "channel": "email",
        "persona": "college student (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "low",
        "narrative": "Delayed retest: Transcript request completion notice.",
        "message": {
            "sender_display": "Registrar Office <transcripts@college.edu.in>",
            "body": "Your requested official academic transcript is ready. Download it directly from your student portal under My Documents.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Email", "value": "transcripts@college.edu.in", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Instructions", "value": "Directs to internal student portal (no external links)", "signal": "trustworthy", "diagnosticity": "medium", "official_channel": False},
            {"id": "e3", "label": "Student Portal Documents Section", "value": "Portal shows transcript PDF available for download.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You downloaded your transcript safely from the official portal.",
            "unsafe": "Ignoring requested transcript notices causes workflow delays."
        },
        "teaching_point": "Delayed retention: Valid requested administrative notifications directing to internal portals are genuine.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "FIN-GEN-D2",
        "family_id": "FAM-GEN-FIN-05",
        "phase_pool": "delayed",
        "context": "finance",
        "channel": "email",
        "persona": "bank customer (fictional)",
        "truth": "genuine",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "low",
        "narrative": "Delayed retest: Tax deduction certificate notice.",
        "message": {
            "sender_display": "Apex Bank Tax Desk <tax-desk@apexbank.com>",
            "body": "Your Form 16A tax deduction certificate for Q2 is available on your netbanking account.",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Sender Address", "value": "tax-desk@apexbank.com", "signal": "trustworthy", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Channel Direction", "value": "Directs user to netbanking portal", "signal": "trustworthy", "diagnosticity": "medium", "official_channel": False},
            {"id": "e3", "label": "Official Netbanking Tax Section", "value": "Netbanking portal shows Q2 Form 16A ready.", "signal": "trustworthy", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "PROCEED"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["REPORT", "IGNORE"]
        },
        "consequence_text": {
            "safe": "You accessed your tax certificate directly via official netbanking.",
            "unsafe": "Reporting valid tax notices creates administrative confusion."
        },
        "teaching_point": "Delayed retention: Netbanking tax notices pointing to official portals are safe.",
        "transfer_group": "AUTH"
    },
    {
        "scenario_id": "FIN-URG-MAL-D3",
        "family_id": "FAM-URG-FIN-04",
        "phase_pool": "delayed",
        "context": "finance",
        "channel": "chat",
        "persona": "mobile wallet user (fictional)",
        "truth": "malicious",
        "mechanisms": ["urgency"],
        "pressure": "high",
        "difficulty": "high",
        "narrative": "Delayed retest: Mobile wallet compliance suspension threat.",
        "message": {
            "sender_display": "WALLET-ALERT (+91-9001122334)",
            "body": "PayQuick Wallet account access will be TERMINATED at 6 PM due to unverified PAN. Update now at http://payquick-pan-update.com",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Update URL", "value": "http://payquick-pan-update.com", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Sender ID", "value": "Unregistered mobile number", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "PAN Terminology", "value": "PAN compliance text", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "PayQuick App Profile", "value": "Profile settings show PAN status Verified.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You verified PAN compliance inside the official app.",
            "unsafe": "Submitting PAN details on unencrypted external sites leads to identity theft."
        },
        "teaching_point": "Delayed retention: Wallet PAN verification is performed strictly inside the official application.",
        "transfer_group": "URG"
    },
    {
        "scenario_id": "SOC-REW-MAL-D3",
        "family_id": "FAM-REW-SOC-06",
        "phase_pool": "delayed",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "messaging user (fictional)",
        "truth": "malicious",
        "mechanisms": ["reward_scarcity"],
        "pressure": "medium",
        "difficulty": "medium",
        "narrative": "Delayed retest: Hacked contact sending free smartphone giveaway link.",
        "message": {
            "sender_display": "Ananya (Friend)",
            "body": "Hey!! TechBrand is giving free smartphones for trial testing! Claim yours before stock runs out: http://techbrand-trial-giveaway.net",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Giveaway Link", "value": "http://techbrand-trial-giveaway.net", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e2", "label": "Request for Shipping Fee", "value": "Asks for ₹199 processing fee via credit card", "signal": "suspicious", "diagnosticity": "high", "official_channel": False},
            {"id": "e3", "label": "Friend Profile", "value": "Friend contact name", "signal": "trustworthy", "diagnosticity": "low", "official_channel": False},
            {"id": "e4", "label": "TechBrand Official Website", "value": "Official website warns of fake trial giveaway link.", "signal": "suspicious", "diagnosticity": "high", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
            "acceptable": ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You checked the official brand site and confirmed the trial giveaway was a scam.",
            "unsafe": "Paying processing fees for fake smartphone giveaways leads to financial loss."
        },
        "teaching_point": "Delayed retention: Free gadget giveaways requiring processing fees are phishing scams.",
        "transfer_group": "REW"
    },
    {
        "scenario_id": "SOC-AMB-D2",
        "family_id": "FAM-AMB-FIN-08",
        "phase_pool": "delayed",
        "context": "social_messaging",
        "channel": "chat",
        "persona": "messaging user (fictional)",
        "truth": "ambiguous",
        "mechanisms": ["authority"],
        "pressure": "low",
        "difficulty": "medium",
        "narrative": "Delayed retest: Alumni network survey request.",
        "message": {
            "sender_display": "Alumni Network Admin (+91-9223344556)",
            "body": "Hello Alumni! We are compiling the 2026 Placement Benchmark Report. Fill out the career survey at http://alumni-career-survey.org",
            "attachment": ""
        },
        "evidence": [
            {"id": "e1", "label": "Survey Link", "value": "http://alumni-career-survey.org", "signal": "neutral", "diagnosticity": "medium", "official_channel": False},
            {"id": "e2", "label": "Sender Contact", "value": "Number listed as Alumni Admin", "signal": "neutral", "diagnosticity": "low", "official_channel": False},
            {"id": "e3", "label": "Official Alumni Portal", "value": "Official portal has not posted official survey announcement yet.", "signal": "hidden", "diagnosticity": "medium", "official_channel": True}
        ],
        "actions": {
            "safe": ["VERIFY_INDEPENDENTLY", "GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
            "acceptable": ["UNSURE"],
            "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
        },
        "consequence_text": {
            "safe": "You checked the official alumni portal before submitting career details.",
            "unsafe": "Submitting details on unverified survey links carries data privacy risks."
        },
        "teaching_point": "Delayed retention: Verify alumni career surveys on official college portals.",
        "transfer_group": "AUTH"
    }
]

def main():
    print(f"Generating exactly {len(SCENARIOS)} frozen JSON scenarios into {SCENARIO_SET_DIR}...")
    for sc in SCENARIOS:
        filepath = os.path.join(SCENARIO_SET_DIR, f"{sc['scenario_id']}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(sc, f, indent=2)
    print("Scenario library generation complete!")

if __name__ == "__main__":
    main()
