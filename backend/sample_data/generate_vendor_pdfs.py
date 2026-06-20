"""
Generate complex, realistic vendor quotation PDFs for ProcurePilot demo.
Each PDF contains dense legal clauses buried in Terms & Conditions to
challenge the AI extraction model.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# STYLE HELPERS
# ─────────────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def style(name, parent='Normal', **kwargs):
    return ParagraphStyle(name, parent=styles[parent], **kwargs)

H1     = style('H1',     'Heading1', fontSize=16, textColor=colors.HexColor('#1a1a2e'), spaceAfter=6)
H2     = style('H2',     'Heading2', fontSize=12, textColor=colors.HexColor('#16213e'), spaceAfter=4)
H3     = style('H3',     'Heading2', fontSize=10, textColor=colors.HexColor('#0f3460'), spaceAfter=3)
NORMAL = style('NORM',   'Normal',   fontSize=9,  leading=13, spaceAfter=4)
LEGAL  = style('LEGAL',  'Normal',   fontSize=7.5, leading=11, spaceAfter=3, alignment=TA_JUSTIFY,
               textColor=colors.HexColor('#2c2c2c'))
SMALL  = style('SMALL',  'Normal',   fontSize=8,  leading=11, textColor=colors.grey)
BOLD   = style('BOLD',   'Normal',   fontSize=9,  leading=13, fontName='Helvetica-Bold')
CENTER = style('CENTER', 'Normal',   fontSize=9,  leading=13, alignment=TA_CENTER)
RIGHT  = style('RIGHT',  'Normal',   fontSize=9,  leading=13, alignment=TA_RIGHT)

TABLE_HEADER = [colors.HexColor('#1a1a2e'), colors.white]
TABLE_ALT    = colors.HexColor('#f5f5f5')


def make_table(data, col_widths, header_rows=1):
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style_cmds = [
        ('BACKGROUND',  (0, 0), (-1, header_rows - 1), TABLE_HEADER[0]),
        ('TEXTCOLOR',   (0, 0), (-1, header_rows - 1), TABLE_HEADER[1]),
        ('FONTNAME',    (0, 0), (-1, header_rows - 1), 'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, header_rows), (-1, -1), [colors.white, TABLE_ALT]),
        ('GRID',        (0, 0), (-1, -1), 0.4, colors.HexColor('#cccccc')),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',  (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def sp(n=1):
    return Spacer(1, n * 0.35 * cm)


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=6)


# ─────────────────────────────────────────────────────────────────────────────
# VENDOR A — APEX INDUSTRIAL SYSTEMS PVT. LTD.
# Profile: Cheapest price, but genuinely HIGH-RISK contractual terms.
# AI Challenge: Penalty is written in tranche-based formula that must be computed.
#               Liability cap is buried inside a force majeure exclusion clause.
#               Payment advance buried inside milestone table.
# ─────────────────────────────────────────────────────────────────────────────
def generate_vendor_a():
    path = os.path.join(OUTPUT_DIR, "Vendor_A_Apex.pdf")
    doc  = SimpleDocTemplate(path, pagesize=A4,
                             topMargin=1.8*cm, bottomMargin=1.8*cm,
                             leftMargin=2*cm, rightMargin=2*cm)
    story = []

    # ── Header ──────────────────────────────────────────────────────────────
    story.append(Paragraph("APEX INDUSTRIAL SYSTEMS PVT. LTD.", H1))
    story.append(Paragraph("Plot 47, Phase-II, Manesar Industrial Area, Gurugram – 122051, Haryana", SMALL))
    story.append(Paragraph("GSTIN: 06AABCA3456M1ZP | CIN: U28991HR2014PTC056789 | ISO 9001:2015 Certified", SMALL))
    story.append(sp())
    story.append(hr())

    # ── Quotation Meta ───────────────────────────────────────────────────────
    meta = [
        ["Quotation Reference:", "APEX/QTN/2026/0047",   "Date of Issue:", "14 June 2026"],
        ["Valid Until:",         "13 August 2026",        "Incoterms:",     "DDP – Buyer's Premises"],
        ["Currency:",            "Indian Rupee (INR)",    "RFQ Reference:", "BUYER/RFQ/2026/MTP-09"],
    ]
    story.append(make_table(meta, [4.5*cm, 5.5*cm, 4*cm, 4.5*cm], header_rows=0))
    story.append(sp())

    story.append(Paragraph("Subject: Formal Quotation for Supply of Industrial Servo Motor Drive Units — Model AIS-SDU 2200", H2))
    story.append(Paragraph(
        "Dear Procurement Committee, we at Apex Industrial Systems are pleased to submit our competitive commercial "
        "and technical offer for the above-referenced requirement. Our proposal represents the most cost-optimised "
        "solution within the specified technical envelope, supported by our ISO-certified manufacturing processes.",
        NORMAL))
    story.append(sp())

    # ── Section 1: Items ─────────────────────────────────────────────────────
    story.append(Paragraph("SECTION 1 — ITEMISED BILL OF MATERIALS & PRICING", H2))
    items = [
        ["S.No.", "Part Code", "Description", "Qty", "Unit Price (₹)", "Amount (₹)"],
        ["1", "AIS-SDU-2200-AC",
         "Servo Motor Drive Unit, 3-Phase AC, 22kW, IP55, Class-F Insulation,\n"
         "Ambient Temp: 0–55°C, Input: 415V ± 10%, Output: 0–440V Variable",
         "10", "1,12,500.00", "11,25,000.00"],
        ["2", "AIS-CTRL-MOD-485",
         "RS-485 Modbus Communication Module, DIN Rail Mount, galvanic\n"
         "isolation, baud rate 9600–115200, SCADA-compatible",
         "10", "4,800.00", "48,000.00"],
        ["3", "AIS-PNL-MNTKIT-HV",
         "HV Panel Mounting Hardware Kit — M10 stainless steel fasteners,\n"
         "anti-vibration grommets, earthing lugs (per drive unit)",
         "10", "1,200.00", "12,000.00"],
        ["4", "AIS-CAB-SHD-20M",
         "20-metre Shielded Encoder Cable, 8-core, 0.5mm², 300V rating,\n"
         "temperature range –20°C to +80°C",
         "10", "3,400.00", "34,000.00"],
        ["5", "AIS-SVC-COMM",
         "Pre-Commissioning, FAT (Factory Acceptance Test), Parameterisation,\n"
         "Site Installation Supervision (3 engineer-days) per lot",
         "1", "28,500.00", "28,500.00"],
    ]
    story.append(make_table(items, [0.8*cm, 3.2*cm, 7.2*cm, 0.8*cm, 2.8*cm, 2.7*cm]))
    story.append(sp(0.5))

    # Pricing summary
    summary = [
        ["", "Sub-Total (Ex-Tax)", "₹ 12,47,500.00"],
        ["", "CGST @ 9%", "₹ 1,12,275.00"],
        ["", "SGST @ 9%", "₹ 1,12,275.00"],
        ["", "GRAND TOTAL (Inclusive of all taxes)", "₹ 14,72,050.00"],
    ]
    t = Table(summary, colWidths=[9*cm, 5.5*cm, 4*cm])
    t.setStyle(TableStyle([
        ('FONTNAME',  (1, 3), (2, 3), 'Helvetica-Bold'),
        ('FONTSIZE',  (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#fff3cd')),
        ('LINEABOVE', (1, 3), (2, 3), 1.0, colors.black),
        ('ALIGN',     (2, 0), (2, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(sp())

    # ── Section 2: Technical Compliance ─────────────────────────────────────
    story.append(Paragraph("SECTION 2 — TECHNICAL COMPLIANCE MATRIX", H2))
    tech = [
        ["Parameter", "Required", "Apex Offered", "Compliance"],
        ["Drive Rating", "22 kW", "22 kW", "✓ FULL"],
        ["Protection Class", "IP55 minimum", "IP55", "✓ FULL"],
        ["Input Voltage Tolerance", "±10%", "±10%", "✓ FULL"],
        ["Insulation Class", "Class-F", "Class-F", "✓ FULL"],
        ["Communication Protocol", "RS-485 Modbus", "RS-485 Modbus RTU", "✓ FULL"],
        ["Ambient Operating Temp", "0–50°C", "0–55°C", "✓ ENHANCED"],
        ["MTBF", "≥ 80,000 hours", "95,000 hours", "✓ ENHANCED"],
        ["CE / BIS Certification", "Required", "CE Marked, BIS Reg. R-41089123", "✓ FULL"],
    ]
    story.append(make_table(tech, [4.5*cm, 3.5*cm, 4.5*cm, 3*cm]))
    story.append(sp())

    # ── Section 3: Delivery ──────────────────────────────────────────────────
    story.append(Paragraph("SECTION 3 — DELIVERY SCHEDULE", H2))
    story.append(Paragraph(
        "Delivery shall be completed within <b>21 calendar days</b> from the date of receipt of confirmed Purchase Order "
        "and receipt of advance payment tranche as specified in Section 5. Delivery is ex-warehouse Manesar facility "
        "on DDP basis to the buyer's designated site in Pune, Maharashtra. Partial deliveries of minimum 5 units "
        "may be accepted by mutual written agreement.",
        NORMAL))
    story.append(sp())

    # ── Section 4: Warranty ──────────────────────────────────────────────────
    story.append(Paragraph("SECTION 4 — WARRANTY & AFTER-SALES SUPPORT", H2))
    story.append(Paragraph(
        "Apex Industrial Systems warrants all supplied equipment against defects in materials and workmanship "
        "for a period of <b>18 months</b> from the date of commissioning or <b>24 months</b> from the date of dispatch, "
        "whichever is earlier. Warranty covers all parts and on-site labour within a radius of 300 km from "
        "Manesar; travel and lodging costs for sites beyond this radius shall be borne by the buyer. "
        "Consumable components (encoder belts, cooling fans, display modules) are explicitly excluded from "
        "warranty coverage after the first 6 months of commissioning. The warranty shall be voided if the "
        "equipment is operated outside the rated parameters or modified without Apex's written consent.",
        NORMAL))
    story.append(sp())

    # ── Section 5: Payment Terms (COMPLEX) ──────────────────────────────────
    story.append(Paragraph("SECTION 5 — PAYMENT MILESTONES & COMMERCIAL TERMS", H2))
    story.append(Paragraph(
        "Payment shall be structured across the following tranches, each of which is a condition precedent "
        "to the corresponding stage of supply and services. Failure to remit any tranche within the stipulated "
        "window shall entitle Apex to suspend manufacturing activities without liability and shall toll all "
        "delivery timelines accordingly:",
        NORMAL))
    pay = [
        ["Milestone", "Trigger Event", "% of Contract Value", "Amount (₹)", "Due Within"],
        ["Tranche I — Mobilisation",
         "Within 3 working days of Purchase Order issuance; prior to commencement of manufacturing",
         "50%", "₹ 7,36,025.00", "3 working days of PO"],
        ["Tranche II — Pre-Dispatch Inspection",
         "Upon successful FAT/PDI sign-off by buyer's QA representative at Apex factory (or waiver thereof)",
         "40%", "₹ 5,88,820.00", "48 hours of PDI clearance"],
        ["Tranche III — Final Acceptance",
         "Upon successful site commissioning, punch-list closure, and counter-signature of Completion Certificate",
         "10%", "₹ 1,47,205.00", "7 days of commissioning"],
    ]
    story.append(make_table(pay, [3.5*cm, 5.5*cm, 2.5*cm, 3*cm, 3*cm]))
    story.append(sp(0.5))
    story.append(Paragraph(
        "<b>Late Payment:</b> In the event Tranche II or Tranche III is not received by the buyer within the "
        "stipulated window, interest shall accrue at the prevailing SBI MCLR (1-year) rate plus a spread of "
        "250 basis points per annum, compounded monthly, on the outstanding amount.",
        LEGAL))
    story.append(sp())

    # ── Section 6: Liquidated Damages (COMPLEX FORMULA) ─────────────────────
    story.append(Paragraph("SECTION 6 — PENALTY & LIQUIDATED DAMAGES", H2))
    story.append(Paragraph(
        "Subject always to Section 7 (Force Majeure) and Section 8 (Limitation of Liability), "
        "and without prejudice to any other remedies available to the buyer at law or equity, "
        "the following Liquidated Damages (LD) regime shall apply to delays attributable solely "
        "to Apex's failure to deliver within the confirmed schedule:",
        LEGAL))
    story.append(sp(0.3))
    ld = [
        ["Delay Period", "LD Rate", "Calculation Basis", "Illustration"],
        ["Day 1 – Day 7\n(Grace Band)",
         "Nil",
         "No damages accrue within the first 7 calendar days of confirmed delivery date",
         "No charge"],
        ["Day 8 – Day 14",
         "0.25% per commenced period of 3 calendar days",
         "Applied on the contract value of the delayed line items only (not the full PO value)",
         "If 10 drives delayed 10 days beyond grace: 0.25% × ₹12,47,500 × 2 tranches = ₹6,237.50"],
        ["Day 15 – Day 30",
         "0.50% per commenced period of 3 calendar days",
         "Applied on the contract value of the delayed line items only",
         "If 10 drives delayed 20 days beyond grace: 0.50% × ₹12,47,500 × 5 tranches = ₹31,187.50"],
        ["Day 31 and beyond",
         "0.75% per commenced period of 3 calendar days",
         "Applied on full PO value (all items irrespective of what is delayed)",
         "Escalating beyond Day 30; buyer may also invoke termination"],
        ["Aggregate Cap on LD",
         "7.5% of Total Contract Value",
         "Maximum LD payable by Apex under all circumstances",
         "Cap = ₹ 1,10,403.75 (excl. taxes)"],
    ]
    story.append(make_table(ld, [2.5*cm, 3.5*cm, 5.5*cm, 5*cm]))
    story.append(sp(0.5))
    story.append(Paragraph(
        "The buyer acknowledges that the LD rates set forth above constitute a genuine pre-estimate of "
        "damages and are not a penalty. Acceptance of LD payment by the buyer shall not constitute a waiver "
        "of any further rights including termination in the event of delay exceeding 45 days from the "
        "confirmed schedule.",
        LEGAL))
    story.append(sp())

    # ── Section 7: Force Majeure ─────────────────────────────────────────────
    story.append(Paragraph("SECTION 7 — FORCE MAJEURE", H2))
    story.append(Paragraph(
        "Apex shall not be held liable for any delay or failure in performance resulting from circumstances "
        "beyond its reasonable control, including but not limited to: acts of God, floods, earthquakes, "
        "epidemic or pandemic declared by a competent government authority, war, civil commotion, strikes "
        "or lockouts of Apex's workforce (but <b>not</b> sub-contractor workforces), government-imposed export "
        "or import restrictions on critical semiconductor components, or grid power failures exceeding "
        "72 continuous hours. <b>Notably, general supply chain disruptions, sub-contractor delays, or "
        "raw material price increases shall not constitute force majeure events.</b> Apex shall notify the "
        "buyer within 48 hours of the occurrence of a force majeure event, failing which this clause shall "
        "not be available as a defence.",
        LEGAL))
    story.append(sp())

    # ── Section 8: Limitation of Liability (BURIED, COMPLEX) ────────────────
    story.append(Paragraph("SECTION 8 — LIMITATION OF LIABILITY & INDEMNIFICATION", H2))
    story.append(Paragraph(
        "8.1 <b>Mutual Limitation:</b> Notwithstanding any other provision of this agreement, and to the fullest "
        "extent permissible under applicable Indian law, the aggregate liability of Apex Industrial Systems "
        "Pvt. Ltd. to the buyer, whether in contract, tort (including negligence), misrepresentation, "
        "breach of statutory duty, or otherwise, arising out of or in connection with this purchase order, "
        "shall be strictly limited to and shall not exceed an amount equal to <b>one hundred percent (100%) "
        "of the total consideration actually received by Apex</b> under the relevant purchase order giving "
        "rise to the claim, in the twelve (12) calendar months immediately preceding the event that gave "
        "rise to the claim.",
        LEGAL))
    story.append(sp(0.3))
    story.append(Paragraph(
        "8.2 <b>Consequential Loss Exclusion:</b> Under no circumstances shall either party be liable to the "
        "other for any indirect, incidental, special, punitive, or consequential loss or damage, including "
        "but not limited to: loss of profit, loss of revenue, loss of business opportunity, loss of "
        "production, loss of anticipated savings, or any damage to reputation, even if such party has been "
        "advised of the possibility of such loss.",
        LEGAL))
    story.append(sp(0.3))
    story.append(Paragraph(
        "8.3 <b>Carve-Out:</b> The limitations in 8.1 and 8.2 shall not apply to: (i) death or personal injury "
        "caused by Apex's negligence; (ii) fraud or fraudulent misrepresentation; (iii) wilful misconduct; "
        "or (iv) any statutory liability that cannot be excluded by contract under the laws of India.",
        LEGAL))
    story.append(sp())

    story.append(Paragraph("SECTION 9 — GOVERNING LAW & DISPUTE RESOLUTION", H2))
    story.append(Paragraph(
        "This agreement shall be governed by and construed in accordance with the laws of India. Any dispute "
        "arising out of or in connection herewith shall be first subjected to a 30-day structured negotiation "
        "period. Failing resolution, disputes shall be referred to arbitration under the Arbitration and "
        "Conciliation Act, 1996, with a sole arbitrator appointed by mutual consent, seated at New Delhi, "
        "conducted in English.",
        LEGAL))
    story.append(sp(2))
    story.append(Paragraph("For APEX INDUSTRIAL SYSTEMS PVT. LTD.", BOLD))
    story.append(sp(0.5))
    story.append(Paragraph("Authorised Signatory: __________________ | Designation: VP — Commercial", SMALL))

    doc.build(story)
    print(f"✓ Generated: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# VENDOR B — BETA PRECISION DRIVES LLP
# Profile: Mid-range price, balanced risk — good warranty, moderate payment,
#          penalty clause that requires currency conversion math.
# AI Challenge: Force majeure clause has a notice period trap.
#               Warranty has an ambiguous milestone tied to BOTH installation
#               AND a 500-hour run-in test, whichever triggers later.
# ─────────────────────────────────────────────────────────────────────────────
def generate_vendor_b():
    path = os.path.join(OUTPUT_DIR, "Vendor_B_Beta.pdf")
    doc  = SimpleDocTemplate(path, pagesize=A4,
                             topMargin=1.8*cm, bottomMargin=1.8*cm,
                             leftMargin=2*cm, rightMargin=2*cm)
    story = []

    story.append(Paragraph("BETA PRECISION DRIVES LLP", H1))
    story.append(Paragraph("Survey No. 112/B, Rajiv Gandhi IT Park, Hinjawadi Phase-III, Pune – 411057, Maharashtra", SMALL))
    story.append(Paragraph("GSTIN: 27AAGFB5543R1Z8 | UDYAM: MH-28-0058841 | ISO 9001:2015 | ISO 14001:2015", SMALL))
    story.append(sp())
    story.append(hr())

    meta = [
        ["Quotation Number:", "BPDL/COM/2026/Q-1139",  "Issue Date:", "15 June 2026"],
        ["Offer Validity:",   "90 days from issue date", "Incoterms:", "CIP – Buyer's Warehouse"],
        ["Quotation Type:",   "Binding Commercial Offer", "RFQ Ref.:",  "BUYER/RFQ/2026/MTP-09"],
    ]
    story.append(make_table(meta, [4.5*cm, 5.5*cm, 3.5*cm, 5*cm], header_rows=0))
    story.append(sp())
    story.append(Paragraph("Re: Binding Commercial Proposal — High-Efficiency Variable Frequency Drive Systems (BPD-HVFD-2200 Series)", H2))
    story.append(Paragraph(
        "Beta Precision Drives LLP is pleased to present this binding commercial and technical proposal for "
        "the supply, commissioning, and post-commissioning support of Variable Frequency Drive systems meeting "
        "or exceeding the technical requirements outlined in your RFQ. Our BPD-HVFD-2200 series is indigenously "
        "manufactured with critical IGBT modules sourced from Infineon Technologies AG (Germany) and tested "
        "against IEC 61800-5-1 Safety of Power Drive Systems.",
        NORMAL))
    story.append(sp())

    story.append(Paragraph("SECTION 1 — BILL OF MATERIALS & COMMERCIAL PRICING", H2))
    items = [
        ["#", "SKU", "Item Description", "Qty", "Rate (₹)", "Ext. (₹)"],
        ["1", "BPD-HVFD-2200-IP55",
         "Variable Frequency Drive, 22kW, 3-Phase, 415V AC, IP55 Enclosure,\n"
         "Integrated EMC Filter Class C3, Brake Chopper, Keypad+USB port,\n"
         "STO (Safe Torque Off) — SIL-2 Certified",
         "10", "1,24,000.00", "12,40,000.00"],
        ["2", "BPD-COMM-PROFINET",
         "PROFINET IO Communication Adapter Card — plug-in to VFD slot;\n"
         "cyclic process data, acyclic records, alarm handling, IRT supported",
         "10", "8,500.00", "85,000.00"],
        ["3", "BPD-ACC-CABLING",
         "Power & Control Cabling Accessories Kit — cable glands PG21/PG16,\n"
         "ferrite cores, DIN terminal blocks, labelling strips",
         "10", "2,250.00", "22,500.00"],
        ["4", "BPD-SVC-COMM-FULL",
         "Full Commissioning Package — includes FAT at Pune factory, "
         "site installation, parameter commissioning, 2-day site acceptance\n"
         "test, training (half-day) for buyer's maintenance team",
         "1", "55,000.00", "55,000.00"],
        ["5", "BPD-AMC-YR1",
         "Annual Maintenance Contract — Year 1; covers 2 preventive maintenance\n"
         "visits, unlimited telephone support, firmware updates, emergency\n"
         "callout within 48 hours (parts cost additional)",
         "1", "42,000.00", "42,000.00"],
    ]
    story.append(make_table(items, [0.6*cm, 3*cm, 7.5*cm, 0.7*cm, 2.8*cm, 2.7*cm]))
    story.append(sp(0.5))

    summary = [
        ["", "Sub-Total (Before Tax)", "₹ 14,44,500.00"],
        ["", "GST @ 18% (CGST 9% + SGST 9%)", "₹ 2,60,010.00"],
        ["", "GRAND TOTAL (All-Inclusive)", "₹ 17,04,510.00"],
    ]
    t = Table(summary, colWidths=[9*cm, 5.5*cm, 4*cm])
    t.setStyle(TableStyle([
        ('FONTNAME',  (1, 2), (2, 2), 'Helvetica-Bold'),
        ('FONTSIZE',  (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#d4edda')),
        ('LINEABOVE', (1, 2), (2, 2), 1.0, colors.black),
        ('ALIGN',     (2, 0), (2, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(sp())

    story.append(Paragraph("SECTION 2 — DELIVERY PROGRAMME", H2))
    story.append(Paragraph(
        "Beta Precision Drives commits to a delivery timeline of <b>28 calendar days</b> from the date of "
        "Purchase Order acknowledgement and clearance of Tranche I advance payment. The delivery shall "
        "be to buyer's Pune warehouse on CIP (Carriage and Insurance Paid) basis. Transit insurance "
        "covering 110% of invoice value is included. Factory Acceptance Test shall be conducted at "
        "BPDL's Hinjawadi facility during days 20–23 of the schedule, and buyer is requested to depute "
        "a QA representative for the same. Site commissioning shall be completed within 5 working days "
        "from delivery date.",
        NORMAL))
    story.append(sp())

    story.append(Paragraph("SECTION 3 — WARRANTY POLICY", H2))
    story.append(Paragraph(
        "3.1 <b>Comprehensive Warranty Duration:</b> Beta Precision Drives extends a comprehensive product "
        "warranty of <b>24 calendar months</b> against all defects in design, material, and workmanship. "
        "The warranty period shall commence from whichever is <b>later</b> of: (a) the date of successful "
        "site commissioning as evidenced by a signed Commissioning Certificate, or (b) the completion "
        "of an uninterrupted 500-hour operational run-in period at the buyer's facility under rated load "
        "conditions, as verified by BPDL's field application engineer. In no case shall the warranty period "
        "extend beyond 30 months from the date of dispatch.",
        NORMAL))
    story.append(sp(0.3))
    story.append(Paragraph(
        "3.2 <b>Warranty Coverage:</b> Covers all parts, labour, travel within India, and firmware "
        "replacements. Excludes damage from: incorrect installation not performed by certified personnel, "
        "input supply voltage fluctuations beyond ±15% of rated, water ingress beyond IP rating, "
        "and acts of God. BPDL shall respond to warranty calls within 24 hours; on-site attendance "
        "within 72 hours; replacement unit dispatched within 5 working days for DOA scenarios.",
        LEGAL))
    story.append(sp())

    story.append(Paragraph("SECTION 4 — PAYMENT TERMS", H2))
    pay = [
        ["Payment Stage", "Description", "% of PO Value", "Amount (₹)"],
        ["Advance (Tranche I)",
         "30% advance payable within 5 working days of Purchase Order issue. "
         "Manufacturing commences upon receipt of this tranche.",
         "30%", "₹ 5,11,353.00"],
        ["Pre-Dispatch (Tranche II)",
         "50% payable against Pro-Forma Invoice issued on successful FAT completion; "
         "due within 3 working days of FAT sign-off.",
         "50%", "₹ 8,52,255.00"],
        ["Commissioning (Tranche III)",
         "Balance 20% payable within 30 days of site commissioning completion "
         "and submission of all O&M manuals and test certificates.",
         "20%", "₹ 3,40,902.00"],
    ]
    story.append(make_table(pay, [3*cm, 6.5*cm, 2.5*cm, 3*cm]))
    story.append(sp(0.3))
    story.append(Paragraph(
        "<b>Late Payment Charge:</b> Amounts outstanding beyond the stipulated due date shall attract a carrying "
        "charge of 1.5% per month (simple interest, non-compounding) on the net overdue principal, "
        "calculated pro-rata for each calendar day of delay. This charge shall be invoiced separately "
        "and is payable within 7 days of the supplementary invoice.",
        LEGAL))
    story.append(sp())

    story.append(Paragraph("SECTION 5 — LIQUIDATED DAMAGES FOR DELAY", H2))
    story.append(Paragraph(
        "In the event of delay in delivery of the equipment by BPDL beyond the contracted delivery date "
        "(subject to permitted extensions under Force Majeure), the following Liquidated Damages shall apply "
        "as the buyer's sole financial remedy for delay (excluding termination rights):",
        LEGAL))
    story.append(sp(0.3))
    ld = [
        ["Period of Delay", "LD Rate", "Basis", "Notes"],
        ["First 14 calendar days", "0.4% per week (or part thereof)",
         "On the value of the delayed equipment portion only",
         "Fractional weeks rounded up to the next full week"],
        ["Day 15 to Day 45", "0.6% per week (or part thereof)",
         "On the total PO value",
         "Escalation clause; applies if root cause remains unresolved"],
        ["Beyond 45 days", "1.0% per week",
         "On total PO value; buyer may issue Notice to Cure",
         "Buyer may terminate if 15-day Cure Notice is not resolved"],
        ["Maximum LD (aggregate cap)", "8% of total PO value",
         "₹ 1,36,360.80 (approx.)",
         "Amounts beyond cap require negotiated settlement or arbitration"],
    ]
    story.append(make_table(ld, [3*cm, 3.5*cm, 5*cm, 4.5*cm]))
    story.append(sp())

    story.append(Paragraph("SECTION 6 — FORCE MAJEURE", H2))
    story.append(Paragraph(
        "Neither party shall be liable for delays in performance caused by circumstances beyond their "
        "reasonable control. However, BPDL explicitly accepts that the following do NOT constitute "
        "force majeure events under this contract: (i) sub-vendor or third-party logistics delays, "
        "(ii) import duty changes or customs delays for components, (iii) labour disputes internal to "
        "BPDL. Force majeure events must be notified to the buyer <b>within 24 hours</b> of occurrence, "
        "failing which the right to claim force majeure is waived. Relief shall be limited to extension "
        "of time only; no additional cost relief is permissible.",
        LEGAL))
    story.append(sp())

    story.append(Paragraph("SECTION 7 — LIMITATION OF LIABILITY", H2))
    story.append(Paragraph(
        "7.1 BPDL's total aggregate liability under this contract shall not exceed <b>150% of the total "
        "PO value</b> (i.e., ₹ 25,56,765.00 approximately). This cap reflects BPDL's enhanced liability "
        "commitment compared to industry standard, in recognition of the safety-critical nature of "
        "the application.",
        LEGAL))
    story.append(sp(0.3))
    story.append(Paragraph(
        "7.2 Neither party shall be liable for consequential, indirect, incidental, special or punitive "
        "damages, whether foreseeable or not, even if the other party has been advised of the possibility "
        "of such damages. The AMC (Section 1, Item 5) carries its own independent liability sub-cap "
        "of 100% of AMC value paid.",
        LEGAL))
    story.append(sp(2))
    story.append(Paragraph("For BETA PRECISION DRIVES LLP", BOLD))
    story.append(Paragraph("Partner / Authorised Signatory: __________________ | DPIN: 08832941", SMALL))

    doc.build(story)
    print(f"✓ Generated: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# VENDOR C — COREDRIVE TECHNOLOGIES LTD.
# Profile: Most expensive, but genuinely LOW-RISK — best-in-class warranty,
#          buyer-friendly payment (Net 60 from delivery), strict penalty for
#          their own delays.
# AI Challenge: Penalty is denominated partially in EUR, requiring AI to
#               flag the currency ambiguity. Liability has a carve-out that
#               conditionally expands coverage if a safety incident occurs.
# ─────────────────────────────────────────────────────────────────────────────
def generate_vendor_c():
    path = os.path.join(OUTPUT_DIR, "Vendor_C_CoreDrive.pdf")
    doc  = SimpleDocTemplate(path, pagesize=A4,
                             topMargin=1.8*cm, bottomMargin=1.8*cm,
                             leftMargin=2*cm, rightMargin=2*cm)
    story = []

    story.append(Paragraph("COREDRIVE TECHNOLOGIES LTD.", H1))
    story.append(Paragraph("Unit 3, MIDC Taloja Phase-II, Navi Mumbai – 410208, Maharashtra | Branch: DLF Cyber City, Gurugram", SMALL))
    story.append(Paragraph("GSTIN: 27AADCC8821P1ZW | CIN: L31909MH2009PLC195647 | ISO 9001:2015 | IEC 62061 Functional Safety", SMALL))
    story.append(sp())
    story.append(hr())

    meta = [
        ["Document No.:",    "CTL/QTN/FY26-27/00312",  "Date:",        "15 June 2026"],
        ["Revision:",        "Rev 0 — Initial Issue",  "Valid Until:", "13 September 2026 (90 days)"],
        ["Classification:",  "Commercially Sensitive — Recipient Confidential", "RFQ:", "BUYER/RFQ/2026/MTP-09"],
    ]
    story.append(make_table(meta, [3.5*cm, 6*cm, 3.5*cm, 5.5*cm], header_rows=0))
    story.append(sp())
    story.append(Paragraph("Subject: Formal Commercial & Technical Proposal — CoreDrive CDX-22 Series Intelligent Motion Control Systems", H2))
    story.append(Paragraph(
        "CoreDrive Technologies is pleased to present this comprehensive proposal for the supply and lifecycle "
        "support of our CDX-22 Series Intelligent VFD Systems. The CDX-22 is the only drive in its class to "
        "achieve both IEC 62061 SIL-2 and PLd (EN ISO 13849-1) dual functional safety certification. "
        "It incorporates an integrated condition monitoring module with predictive health analytics accessible "
        "via CoreDrive's cloud portal, CoreSight™, enabling proactive maintenance scheduling.",
        NORMAL))
    story.append(sp())

    story.append(Paragraph("SECTION 1 — SCOPE OF SUPPLY & PRICING SCHEDULE", H2))
    items = [
        ["#", "Part No.", "Description", "Qty", "Unit Price (₹)", "Total (₹)"],
        ["1", "CDX-22-SIL2-IP66",
         "CoreDrive CDX-22 VFD, 22kW, 415V 3-Ph AC, IP66 Enclosure (enhanced\n"
         "over spec), Dual SIL-2 certified STO+SS1, Integrated EMC Filter Class C2,\n"
         "4-line LCD display, USB + Ethernet + RS-485 multi-port, onboard PLC "
         "with 8DI/4DO, CoreSight™ IoT module pre-installed",
         "10", "1,58,000.00", "15,80,000.00"],
        ["2", "CDX-ACC-BYPASS-MAN",
         "Manual Bypass Module — allows maintenance without shutting process;\n"
         "integrated in the drive enclosure; MCCB rated at 1.25× drive capacity",
         "10", "14,200.00", "1,42,000.00"],
        ["3", "CDX-COMM-EIP",
         "EtherNet/IP + PROFINET Dual-Protocol Comm Card (simultaneous support);\n"
         "enables integration with both Rockwell and Siemens PLCs without gateway",
         "10", "9,800.00", "98,000.00"],
        ["4", "CDX-SVC-PLAT-PLUS",
         "Platinum Commissioning & Validation Package — includes FAT at Navi Mumbai\n"
         "facility with NABL-accredited test reports, site installation, 48-hour\n"
         "continuous load test, IQ/OQ/PQ validation documentation, and 5-day\n"
         "operator + maintenance training programme",
         "1", "1,20,000.00", "1,20,000.00"],
        ["5", "CDX-CORESIGHT-3YR",
         "CoreSight™ Predictive Analytics Subscription — 3 years; cloud dashboard,\n"
         "AI-based bearing wear and capacitor health alerts, monthly automated\n"
         "health reports, SLA: alert-to-acknowledgement ≤ 15 minutes",
         "1", "95,000.00", "95,000.00"],
    ]
    story.append(make_table(items, [0.6*cm, 2.8*cm, 7.7*cm, 0.7*cm, 2.8*cm, 2.6*cm]))
    story.append(sp(0.5))

    summary = [
        ["", "Sub-Total (Ex-Tax)", "₹ 20,35,000.00"],
        ["", "GST @ 18% (CGST 9% + SGST 9%)", "₹ 3,66,300.00"],
        ["", "GRAND TOTAL (All Inclusive)", "₹ 23,01,300.00"],
    ]
    t = Table(summary, colWidths=[9*cm, 5.5*cm, 4*cm])
    t.setStyle(TableStyle([
        ('FONTNAME',  (1, 2), (2, 2), 'Helvetica-Bold'),
        ('FONTSIZE',  (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#cce5ff')),
        ('LINEABOVE', (1, 2), (2, 2), 1.0, colors.black),
        ('ALIGN',     (2, 0), (2, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(sp())

    story.append(Paragraph("SECTION 2 — DELIVERY COMMITMENT", H2))
    story.append(Paragraph(
        "CoreDrive commits to complete delivery and site commissioning of all 10 CDX-22 drive systems within "
        "<b>35 calendar days</b> from the date of Purchase Order. This timeline includes: manufacturing (Days 1–20), "
        "FAT and pre-dispatch activities (Days 21–27), logistics and delivery (Days 28–32), and site commissioning "
        "including 48-hour load test (Days 33–35). This timeline is guaranteed and backed by the LD provisions "
        "in Section 5. CoreDrive maintains a finished-goods buffer stock of up to 4 CDX-22 units at its "
        "Navi Mumbai facility to mitigate supply chain risks. <b>No advance payment is required to commence "
        "manufacturing.</b>",
        NORMAL))
    story.append(sp())

    story.append(Paragraph("SECTION 3 — COMPREHENSIVE WARRANTY PROGRAMME", H2))
    story.append(Paragraph(
        "3.1 <b>Warranty Duration:</b> CoreDrive warrants the CDX-22 series equipment for a period of "
        "<b>36 months (3 years)</b> from the date of successful commissioning as evidenced by the signed "
        "Site Acceptance Test (SAT) report. In the event that commissioning is delayed for reasons "
        "attributable to the buyer, the warranty period shall nonetheless commence no later than "
        "6 months from the date of delivery. The CoreSight™ subscription (Item 5) carries its own "
        "independent 36-month SLA.",
        NORMAL))
    story.append(sp(0.3))
    story.append(Paragraph(
        "3.2 <b>Coverage:</b> Comprehensive parts, labour, firmware, and travel (within India). "
        "Includes annual calibration of integrated measurement sensors. Excludes damage resulting from: "
        "third-party modifications, external overvoltage events (lightning strike with documented evidence), "
        "and intentional misuse. CoreDrive will replace DOA units within 48 hours with a pre-configured "
        "loan unit at no charge to the buyer.",
        LEGAL))
    story.append(sp())

    story.append(Paragraph("SECTION 4 — PAYMENT TERMS", H2))
    story.append(Paragraph(
        "CoreDrive offers the following buyer-friendly payment structure, designed to align cash outflows "
        "with physical delivery milestones:",
        NORMAL))
    pay = [
        ["Milestone", "Trigger", "% of Contract", "Amount (₹)", "Credit Window"],
        ["Tranche I — On Delivery",
         "Payable upon physical delivery of all 10 units at buyer's site, counter-signed delivery challan",
         "60%", "₹ 13,80,780.00", "Net 15 days from delivery date"],
        ["Tranche II — Post-Commissioning",
         "Payable upon successful completion of 48-hour load test and SAT sign-off",
         "30%", "₹ 6,90,390.00", "Net 30 days from SAT date"],
        ["Tranche III — Retention",
         "Final retention released 12 months from SAT date, confirming satisfactory field performance",
         "10%", "₹ 2,30,130.00", "Net 60 days from end of 12-month retention period"],
    ]
    story.append(make_table(pay, [3*cm, 5*cm, 2.5*cm, 3*cm, 3*cm]))
    story.append(sp(0.3))
    story.append(Paragraph(
        "<b>Important:</b> No mobilisation advance is required. CoreDrive bears all manufacturing finance costs. "
        "Late payment beyond the Net 15 / Net 30 / Net 60 windows shall attract interest at the prevailing "
        "RBI Repo Rate plus 100 basis points per annum, calculated on a 365-day basis, non-compounding.",
        LEGAL))
    story.append(sp())

    story.append(Paragraph("SECTION 5 — LIQUIDATED DAMAGES (SUPPLIER DELAY)", H2))
    story.append(Paragraph(
        "CoreDrive voluntarily accepts an aggressive LD regime as a demonstration of delivery confidence. "
        "The LD schedule below shall be the buyer's sole remedy for delay, unless delay exceeds the "
        "termination trigger defined herein:",
        LEGAL))
    story.append(sp(0.3))
    ld = [
        ["Delay Band", "LD Rate", "Basis", "Equivalent Annual Rate"],
        ["Day 1 – Day 5\n(Zero Grace Period)", "₹ 5,000 per calendar day",
         "Fixed daily penalty; does not compound\nNote: payable in INR only, regardless of any EUR reference pricing",
         "≈ ₹ 18,25,000 annualised (illustrative only)"],
        ["Day 6 – Day 21", "0.5% per week (or part thereof)",
         "On the total contract value (₹ 23,01,300)",
         "≈ 26% per annum; deliberately punitive to incentivise performance"],
        ["Day 22 – Day 42", "1.0% per week (or part thereof)",
         "On total contract value; CoreDrive may also offer substitute units\nat its own cost",
         "≈ 52% per annum"],
        ["Beyond Day 42", "Buyer may terminate for cause",
         "CoreDrive liable for return of all payments received plus LD accrued",
         "No further cap applies post-termination trigger"],
        ["Aggregate LD Cap\n(pre-termination)", "10% of total contract value",
         "₹ 2,30,130.00 — among the highest caps in the industry",
         "Cap applies to LD only; does not limit termination damages"],
    ]
    story.append(make_table(ld, [3*cm, 3.5*cm, 5*cm, 4.5*cm]))
    story.append(sp(0.3))
    story.append(Paragraph(
        "<i>Note on Currency:</i> All pricing and LD calculations are in Indian Rupees (INR). Any references "
        "to EUR in CoreDrive's global product datasheets or warranty certificates relate to the European "
        "market and are not applicable to this purchase order. INR values take precedence in all disputes.",
        LEGAL))
    story.append(sp())

    story.append(Paragraph("SECTION 6 — FORCE MAJEURE", H2))
    story.append(Paragraph(
        "6.1 CoreDrive accepts a narrow definition of force majeure. The following events shall qualify "
        "as force majeure: (a) Natural disasters (floods, earthquakes above Richter 5.5, cyclones) "
        "affecting CoreDrive's Navi Mumbai manufacturing facility directly; (b) National lockdowns "
        "imposed by the Government of India; (c) War or armed conflict on Indian territory. "
        "The following shall explicitly <b>NOT</b> qualify: sub-vendor delays, port congestion, "
        "customs clearance delays, semiconductor lead-time changes, and IGBT module import delays. "
        "CoreDrive maintains safety stock to mitigate these.",
        LEGAL))
    story.append(sp(0.3))
    story.append(Paragraph(
        "6.2 <b>Notice Requirement:</b> CoreDrive shall notify the buyer by registered email and "
        "telephone within 6 hours of a force majeure event's occurrence, with documentary evidence "
        "submitted within 24 hours. CoreDrive shall also submit a recovery plan within 48 hours. "
        "Failure to comply with this notice timeline voids the force majeure claim entirely.",
        LEGAL))
    story.append(sp())

    story.append(Paragraph("SECTION 7 — LIMITATION OF LIABILITY", H2))
    story.append(Paragraph(
        "7.1 <b>Standard Cap:</b> CoreDrive's aggregate liability under this contract is capped at "
        "<b>200% of the total PO value</b> (i.e., ₹ 46,02,600.00 approximately). This enhanced cap "
        "reflects the safety-critical nature of the equipment and CoreDrive's confidence in its product.",
        LEGAL))
    story.append(sp(0.3))
    story.append(Paragraph(
        "7.2 <b>Safety Incident Carve-Out — Expanded Liability:</b> Notwithstanding clause 7.1, in the "
        "event that a failure of the CDX-22 unit, attributable to a manufacturing defect or design "
        "fault as determined by an independent NABL-accredited laboratory, directly causes: (i) "
        "personal injury requiring hospitalisation, or (ii) a fire or explosion at the buyer's facility "
        "resulting in property damage exceeding ₹ 10 lakhs, CoreDrive's liability cap under 7.1 shall "
        "be lifted and replaced with CoreDrive's product liability insurance policy limit, which is "
        "currently ₹ 5 crores per occurrence (as per policy document available on request). "
        "This carve-out is unconditional and cannot be waived by either party.",
        LEGAL))
    story.append(sp(0.3))
    story.append(Paragraph(
        "7.3 Consequential loss exclusion applies in all standard cases, except where the consequential "
        "loss arises directly from the safety incident carve-out under 7.2.",
        LEGAL))
    story.append(sp(2))
    story.append(Paragraph("For COREDRIVE TECHNOLOGIES LTD.", BOLD))
    story.append(Paragraph("Authorised Signatory: __________________ | Designation: Chief Commercial Officer", SMALL))
    story.append(Paragraph("Company Seal: [affixed]", SMALL))

    doc.build(story)
    print(f"✓ Generated: {path}")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating complex vendor quotation PDFs...")
    generate_vendor_a()
    generate_vendor_b()
    generate_vendor_c()
    print("\n✅ All 3 PDFs generated successfully in backend/sample_data/")
