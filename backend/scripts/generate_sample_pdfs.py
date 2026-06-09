"""
Generate 3 realistic vendor quotation PDFs for testing the ProcurePilot AI pipeline.
Uses fpdf2 to create the PDFs.
"""

from fpdf import FPDF
import os

# Ensure the output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class QuotationPDF(FPDF):
    def __init__(self, vendor_name, vendor_address, vendor_contact):
        super().__init__()
        self.vendor_name = vendor_name
        self.vendor_address = vendor_address
        self.vendor_contact = vendor_contact

    def header(self):
        # Arial bold 15
        self.set_font("helvetica", "B", 18)
        # Title
        self.cell(0, 10, self.vendor_name, border=0, ln=1, align="C")
        self.set_font("helvetica", "", 10)
        self.cell(0, 6, self.vendor_address, border=0, ln=1, align="C")
        self.cell(0, 6, self.vendor_contact, border=0, ln=1, align="C")
        self.ln(10)
        
        # Quotation Title
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, "OFFICIAL QUOTATION", border=1, ln=1, align="C")
        self.ln(10)

def create_quotation(filename, data):
    pdf = QuotationPDF(
        vendor_name=data["vendor_name"],
        vendor_address=data["vendor_address"],
        vendor_contact=data["vendor_contact"]
    )
    pdf.add_page()
    
    # Metadata
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(50, 8, "Quotation No:", 0)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(50, 8, data["quotation_no"], 0, ln=1)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(50, 8, "Date:", 0)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(50, 8, data["date"], 0, ln=1)

    pdf.set_font("helvetica", "B", 11)
    pdf.cell(50, 8, "Valid Until:", 0)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(50, 8, data["validity"], 0, ln=1)
    
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(10, 10, "SN", 1, align="C")
    pdf.cell(80, 10, "Description", 1, align="C")
    pdf.cell(20, 10, "Qty", 1, align="C")
    pdf.cell(40, 10, "Unit Price (INR)", 1, align="C")
    pdf.cell(40, 10, "Total (INR)", 1, ln=1, align="C")
    
    # Table Content
    pdf.set_font("helvetica", "", 11)
    subtotal = 0
    for idx, item in enumerate(data["items"], 1):
        total = item["qty"] * item["price"]
        subtotal += total
        
        # Item row
        pdf.cell(10, 10, str(idx), 1, align="C")
        pdf.cell(80, 10, item["name"], 1)
        pdf.cell(20, 10, str(item["qty"]), 1, align="C")
        pdf.cell(40, 10, f"{item['price']:,.2f}", 1, align="R")
        pdf.cell(40, 10, f"{total:,.2f}", 1, ln=1, align="R")
        
        # Specs row (merged)
        pdf.set_font("helvetica", "I", 9)
        pdf.cell(10, 8, "", "LR")
        pdf.cell(180, 8, f"  Specs: {item['specs']}", "LR", ln=1)
        pdf.cell(190, 0, "", "T", ln=1) # Bottom border for specs
        pdf.set_font("helvetica", "", 11)

    pdf.ln(5)
    
    # Totals
    tax_amount = subtotal * (data["tax_pct"] / 100)
    grand_total = subtotal + tax_amount
    
    pdf.set_left_margin(110)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(40, 10, "Subtotal:", 0)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(40, 10, f"{subtotal:,.2f}", 0, ln=1, align="R")
    
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(40, 10, f"GST ({data['tax_pct']}%):", 0)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(40, 10, f"{tax_amount:,.2f}", 0, ln=1, align="R")
    
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(40, 10, "Grand Total:", "T")
    pdf.cell(40, 10, f"{grand_total:,.2f}", "T", ln=1, align="R")
    
    pdf.set_left_margin(10)
    pdf.ln(10)
    
    # Terms and Conditions
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Commercial Terms & Conditions", ln=1)
    pdf.set_font("helvetica", "", 10)
    
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(40, 6, "1. Delivery Time:")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 6, f"{data['delivery_days']} days from PO", ln=1)
    
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(40, 6, "2. Warranty:")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 6, f"{data['warranty_months']} months comprehensive", ln=1)
    
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(40, 6, "3. Payment Terms:")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 6, data["payment_terms"], ln=1)
    
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(40, 6, "4. Notes:")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 6, data["notes"], ln=1)
    
    pdf.ln(20)
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 10, "Authorized Signatory", ln=1)
    pdf.cell(0, 10, data["vendor_name"])
    
    output_path = os.path.join(OUTPUT_DIR, filename)
    pdf.output(output_path)
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    # Vendor A: Premium, expensive, great warranty, fast delivery
    vendor_a = {
        "vendor_name": "Apex Industrial Motors",
        "vendor_address": "Plot 45, Phase 2, Peenya Industrial Area, Bengaluru - 560058",
        "vendor_contact": "sales@apexmotors.in | +91 98765 43210",
        "quotation_no": "APEX/2026/001",
        "date": "2026-06-10",
        "validity": "30 Days",
        "items": [
            {
                "name": "Heavy Duty Induction Motor",
                "specs": "75 kW, 415V, 1440 RPM, IE3 Efficiency",
                "qty": 5,
                "price": 285000
            },
            {
                "name": "VFD Controller",
                "specs": "90 kW, 3-Phase Variable Frequency Drive",
                "qty": 5,
                "price": 65000
            }
        ],
        "tax_pct": 18,
        "delivery_days": 10,
        "warranty_months": 36,
        "payment_terms": "30% Advance, 70% against delivery",
        "notes": "Includes free installation and alignment onsite. Extended warranty covers all parts."
    }

    # Vendor B: Balanced, moderate cost, standard warranty, moderate delivery
    vendor_b = {
        "vendor_name": "Beta Dynamics Engineering",
        "vendor_address": "Block C, MIDC, Andheri East, Mumbai - 400093",
        "vendor_contact": "quotes@betadynamics.com | +91 88776 65544",
        "quotation_no": "BDE-QT-992",
        "date": "2026-06-09",
        "validity": "15 Days",
        "items": [
            {
                "name": "IE3 Induction Motor",
                "specs": "75 kW, 415V, 1500 RPM",
                "qty": 5,
                "price": 255000
            },
            {
                "name": "AC Drive Unit",
                "specs": "90 kW Rating, IP55 Enclosure",
                "qty": 5,
                "price": 55000
            }
        ],
        "tax_pct": 18,
        "delivery_days": 15,
        "warranty_months": 12,
        "payment_terms": "50% Advance, 50% Post-delivery (30 days credit)",
        "notes": "Installation charges extra at actuals."
    }

    # Vendor C: Cheap, standard warranty, high delivery risk
    vendor_c = {
        "vendor_name": "CoreDrive Solutions Ltd",
        "vendor_address": "Sector 14, IMT Manesar, Gurugram - 122050",
        "vendor_contact": "sales@coredrive.co.in | 0124-4567890",
        "quotation_no": "CDS/QT/2026/455",
        "date": "2026-06-08",
        "validity": "60 Days",
        "items": [
            {
                "name": "Standard Squirrel Cage Motor",
                "specs": "75 kW, 415V, 3-phase, 1440 RPM",
                "qty": 5,
                "price": 210000
            },
            {
                "name": "VFD Module",
                "specs": "90 kW compatible VFD",
                "qty": 5,
                "price": 48000
            }
        ],
        "tax_pct": 18,
        "delivery_days": 35,
        "warranty_months": 12,
        "payment_terms": "100% Advance Payment",
        "notes": "Delivery timeline is tentative and subject to supply chain constraints."
    }

    create_quotation("Vendor_A_Apex.pdf", vendor_a)
    create_quotation("Vendor_B_Beta.pdf", vendor_b)
    create_quotation("Vendor_C_CoreDrive.pdf", vendor_c)
