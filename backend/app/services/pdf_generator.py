from io import BytesIO
from fpdf import FPDF
from app.schemas.analysis import ProcurementAnalysis

def safe_text(text: str) -> str:
    if not text:
        return ""
    return str(text).encode('latin-1', 'replace').decode('latin-1')


class PDFReportGenerator(FPDF):
    def header(self):
        # Header background
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 30, 'F')
        
        # ProcurePilot Text
        self.set_y(10)
        self.set_font("Arial", "B", 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "ProcurePilot", 0, 0, "L")
        
        # Subtitle
        self.set_font("Arial", "", 12)
        self.set_text_color(6, 182, 212)
        self.cell(0, 10, "Deterministic Procurement Analysis Report", 0, 1, "R")
        self.ln(15)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_fill_color(241, 245, 249)
        self.set_text_color(15, 23, 42)
        self.cell(0, 12, f"  {safe_text(title)}", 0, 1, "L", 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 8, safe_text(body))
        self.ln(4)

def generate_report(analysis: ProcurementAnalysis) -> bytes:
    pdf = PDFReportGenerator()
    pdf.add_page()
    
    # Recommendation Section
    pdf.chapter_title("1. Recommendation")
    recommendation_text = f"Recommended Vendor: {analysis.recommended_vendor}\n\nReason: {analysis.recommendation_reason}"
    pdf.chapter_body(recommendation_text)
    
    # Vendor Rankings
    pdf.chapter_title("2. Vendor Rankings")
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(226, 232, 240)
    pdf.cell(15, 10, "Rank", border=1, align="C", fill=1)
    pdf.cell(55, 10, "Vendor Name", border=1, align="C", fill=1)
    pdf.cell(40, 10, "Cost Score", border=1, align="C", fill=1)
    pdf.cell(40, 10, "Warranty Score", border=1, align="C", fill=1)
    pdf.cell(40, 10, "Overall Score", border=1, align="C", fill=1)
    pdf.ln()
    
    pdf.set_font("Arial", "", 10)
    for score in analysis.vendor_scores:
        pdf.cell(15, 10, str(score.rank), border=1, align="C")
        pdf.cell(55, 10, safe_text(score.vendor_name), border=1, align="C")
        pdf.cell(40, 10, str(score.cost_score), border=1, align="C")
        pdf.cell(40, 10, str(score.warranty_score), border=1, align="C")
        pdf.cell(40, 10, str(round(score.overall_score, 1)), border=1, align="C")
        pdf.ln()
    pdf.ln()
    
    # Risk Flags
    pdf.chapter_title("3. Identified Risks")
    if not analysis.risk_flags:
        pdf.chapter_body("No major risks identified.")
    else:
        risk_text = ""
        for risk in analysis.risk_flags:
            risk_text += f"- {risk.vendor_name} ({risk.level.split('.')[-1]}): {risk.description}\n"
        pdf.chapter_body(risk_text)
        
    # Savings Opportunities
    pdf.chapter_title("4. Savings Opportunities")
    if not analysis.savings_opportunities:
        pdf.chapter_body("The recommended vendor optimizes for warranty and delivery speed over unit cost.")
    else:
        savings_text = ""
        for savings in analysis.savings_opportunities:
            savings_text += f"- Save INR {savings.savings_amount:,} ({savings.savings_percentage}%) by choosing {savings.cheaper_vendor} over {savings.expensive_vendor}.\n"
        pdf.chapter_body(savings_text)
        
    return pdf.output(dest="S")
