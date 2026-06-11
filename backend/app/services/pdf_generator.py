from io import BytesIO
from fpdf import FPDF
from app.schemas.analysis import ProcurementAnalysis

class PDFReportGenerator(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font("Arial", "B", 15)
        # Title
        self.cell(0, 10, "ProcurePilot Executive Summary", 0, 1, "C")
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font("Arial", "I", 8)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        # Arial 12
        self.set_font("Arial", "B", 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 10, title, 0, 1, "L", 1)
        self.ln(4)

    def chapter_body(self, body):
        # Times 12
        self.set_font("Times", "", 12)
        # Output justified text
        self.multi_cell(0, 10, body)
        self.ln()

def generate_report(analysis: ProcurementAnalysis) -> bytes:
    pdf = PDFReportGenerator()
    pdf.add_page()
    
    # Recommendation Section
    pdf.chapter_title("1. Recommendation")
    recommendation_text = f"Recommended Vendor: {analysis.recommended_vendor}\n\nReason: {analysis.recommendation_reason}"
    pdf.chapter_body(recommendation_text)
    
    # Vendor Rankings
    pdf.chapter_title("2. Vendor Rankings")
    pdf.set_font("Times", "B", 12)
    pdf.cell(20, 10, "Rank", border=1, align="C")
    pdf.cell(50, 10, "Vendor Name", border=1, align="C")
    pdf.cell(40, 10, "Cost Score", border=1, align="C")
    pdf.cell(40, 10, "Warranty Score", border=1, align="C")
    pdf.cell(40, 10, "Overall Score", border=1, align="C")
    pdf.ln()
    
    pdf.set_font("Times", "", 12)
    for score in analysis.vendor_scores:
        pdf.cell(20, 10, str(score.rank), border=1, align="C")
        pdf.cell(50, 10, score.vendor_name, border=1, align="C")
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
        pdf.chapter_body("No cost savings available (recommended vendor is most expensive).")
    else:
        savings_text = ""
        for savings in analysis.savings_opportunities:
            savings_text += f"- Save INR {savings.savings_amount:,} ({savings.savings_percentage}%) by choosing {savings.cheaper_vendor} over {savings.expensive_vendor}.\n"
        pdf.chapter_body(savings_text)
        
    return pdf.output(dest="S")
