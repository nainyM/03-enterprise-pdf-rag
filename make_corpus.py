"""Generate the synthetic Kestrel Logistics PDF corpus used by the RAG demo.

Each page is a list of (heading, body) sections. Headings are drawn in bold so the
ingestion step can split chunks on them. Run once: python make_corpus.py
"""
import json
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

ROOT = Path(__file__).parent
PDF_DIR = ROOT / "corpus" / "pdfs"

CONTENT = {
    "HR-001": [
        [("Working Hours", "Standard working hours are 9:00 to 17:30 local time, Monday to Friday. Core collaboration hours are 10:00 to 15:00."),
         ("Paid Leave", "Full-time employees receive 22 days of paid annual leave per calendar year. Unused leave carries over up to 5 days into the next year.")],
        [("Remote Work", "Employees may work remotely up to 3 days per week with manager approval. Remote days must be logged in the attendance tool by Friday noon."),
         ("Parental Leave", "Primary caregivers receive 16 weeks of paid parental leave.")],
    ],
    "HR-002": [
        [("Salary Bands", "Band L3 (Senior Analyst): 95,000 to 115,000 USD. Band L4 (Product Manager): 115,000 to 140,000 USD. Band L5 (Senior Product Manager): 140,000 to 170,000 USD.")],
        [("Bonus and Reviews", "Annual merit increases are reviewed in March. The bonus target for band L5 is 15 percent of base salary.")],
    ],
    "FIN-001": [
        [("Meal Allowance", "Meal allowance for domestic travel is 75 USD per day. Receipts are required for any expense above 25 USD.")],
        [("Submission Deadline", "Expense reports must be submitted within 30 days of the transaction.")],
    ],
    "FIN-002": [
        [("Meal Allowance", "Effective 1 March 2026, the meal allowance for domestic travel is 90 USD per day. Receipts are required for any expense above 30 USD.")],
        [("Submission Deadline", "Expense reports must be submitted within 45 days of the transaction. Policy v2 is superseded and must not be used for claims dated after 1 March 2026.")],
    ],
    "FIN-003": [
        [("Refund Approval Levels", "Customer refunds up to 200 USD may be approved by a Support Lead. Refunds from 200 to 2,000 USD require a Finance Manager. Refunds above 2,000 USD require the CFO.")],
    ],
    "TRV-001": [
        [("Flights and Hotels", "Flights under 6 hours must be booked in economy. Hotels must not exceed 220 USD per night in domestic cities, excluding major events. Bookings are made through the approved travel portal.")],
    ],
    "SEC-001": [
        [("Authentication", "All production systems require multi-factor authentication. Privileged access is granted for a maximum of 90 days and must be re-approved. Shared accounts are prohibited.")],
        [("Access Reviews", "Access reviews are performed quarterly by system owners. Terminated employees must lose access within 24 hours.")],
    ],
    "SEC-002": [
        [("Severity Response", "Severity 1 incidents must be acknowledged within 15 minutes. The incident commander notifies the CISO within 1 hour of a confirmed customer data exposure.")],
        [("Post-Incident Review", "Post-incident reviews are completed within 5 business days and are blameless.")],
    ],
    "ENG-001": [
        [("Retention Periods", "Customer support transcripts are retained for 18 months. Financial records are retained for 7 years. Backups are deleted after 35 days.")],
    ],
    "PRD-001": [
        [("Response Targets", "First response target is 4 business hours for standard tickets and 1 hour for enterprise tickets. Resolution target for standard tickets is 3 business days.")],
        [("Enterprise Support", "Enterprise customers receive a dedicated support channel. Uptime commitment is 99.9 percent per calendar month.")],
    ],
    "PRD-002": [
        [("Release Cadence", "Releases ship every second Tuesday. Each release requires passing automated tests, a security scan, and sign-off from the product owner.")],
        [("Hotfixes", "Hotfixes can ship outside the cycle with approval from the on-call engineering manager. Feature flags must be used for any change touching billing.")],
    ],
    "PRD-003": [
        [("Required Sections", "Each PRD must include a problem statement, target user, success metrics, non-goals, and risks. Launch decisions require a readiness review.")],
    ],
}


def write_pdf(path: Path, title: str, pages: list) -> None:
    pdf = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    margin = 60
    max_width = width - 2 * margin
    for page_no, sections in enumerate(pages, start=1):
        y = height - margin
        pdf.setFont("Helvetica", 8)
        pdf.drawString(margin, height - 35, f"{title} | page {page_no}")
        for heading, body in sections:
            y -= 18
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(margin, y, heading)
            y -= 16
            pdf.setFont("Helvetica", 10)
            for line in simpleSplit(body, "Helvetica", 10, max_width):
                pdf.drawString(margin, y, line)
                y -= 14
            y -= 8
        pdf.showPage()
    pdf.save()


def main() -> None:
    manifest = json.loads((ROOT / "corpus" / "manifest.json").read_text())
    for doc in manifest["documents"]:
        write_pdf(PDF_DIR / doc["file"], doc["title"], CONTENT[doc["doc_id"]])
        print(f"wrote {doc['file']} ({len(CONTENT[doc['doc_id']])} page(s))")


if __name__ == "__main__":
    main()
