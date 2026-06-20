"""
Vendor Quotation Schema.
Defines the structured format that all extracted vendor data MUST conform to.
This is the reliability firewall — no free-form extraction allowed.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ContractClauses(BaseModel):
    """
    Structured extraction of contractual / legal clause data from the quotation.
    Each field must be inferred from the T&C text, even if buried in dense legal language.
    """
    # Payment terms — how many days after PO until first payment is required.
    # 0 means 100% advance before any work starts.
    # Use the FIRST tranche due date as the reference point.
    payment_terms_days: Optional[int] = Field(
        None,
        description=(
            "The number of calendar days after Purchase Order issuance by which the FIRST payment tranche "
            "is due. If the first tranche is required BEFORE or ON the same day as PO (advance/mobilisation), "
            "set this to 0. If payment is due Net 30 from delivery, set to 30 (approximately). "
            "Do not include subsequent tranches — only the first. If absent, return null."
        )
    )

    # Penalty / Liquidated Damages — effective weekly rate as a percentage of contract value.
    # Must be computed from the formula if given in a complex tiered/tranche structure.
    penalty_pct_per_week: Optional[float] = Field(
        None,
        description=(
            "The effective Liquidated Damages (LD) rate expressed as a PERCENTAGE of the total contract value "
            "PER WEEK, for the FIRST tier of delays (i.e., excluding escalation tiers). "
            "If given as 'X% per 3 calendar days', convert: weekly_rate = (X / 3) * 7. "
            "If given as a flat daily amount (e.g. INR 5,000/day) rather than a percentage, "
            "compute the effective rate as: (daily_amount * 7) / total_contract_value * 100. "
            "If there is a grace period (e.g., first 7 days no LD), use the rate that applies after the grace period. "
            "If no penalty clause exists, return null."
        )
    )

    # Liability cap — is the vendor's total liability capped at a finite amount?
    liability_capped: Optional[bool] = Field(
        None,
        description=(
            "True if the vendor's aggregate liability is explicitly capped at a finite amount (e.g., 100% of PO value, "
            "150% of PO value, etc.). False if the contract contains NO liability cap or if the cap is conditional "
            "and can be entirely lifted (e.g., uncapped in safety incidents). "
            "Note: if the cap is normally capped but expands only for extreme safety events (personal injury, fire), "
            "still return True — the standard cap exists. If completely uncapped, return False."
        )
    )

    # Force majeure — is a force majeure clause present?
    force_majeure_included: Optional[bool] = Field(
        None,
        description=(
            "True if the vendor's terms include a force majeure (FM) clause that protects the vendor from liability "
            "for delays caused by events beyond their control. Return False only if there is NO force majeure clause "
            "whatsoever. Note: a narrowly defined FM clause (e.g., only acts of God, not supply chain issues) "
            "still counts as True — evaluate its presence, not its breadth."
        )
    )


class ProductItem(BaseModel):
    """A single product/line item from a vendor quotation."""

    product_name: str = Field(..., description="Name or model of the product")
    specifications: Optional[str] = Field(None, description="Technical specs (power, voltage, RPM, etc.)")
    quantity: int = Field(..., ge=1, description="Number of units quoted")
    unit_price: float = Field(..., ge=0, description="Price per unit in INR")
    total_price: float = Field(..., ge=0, description="Total price for this line item in INR")


class FieldConfidence(BaseModel):
    """Specific confidence scores for critical fields to satisfy Gemini's strict structured output requirements."""
    grand_total: int = Field(100, ge=0, le=100, description="Confidence score for grand_total")
    warranty_months: int = Field(100, ge=0, le=100, description="Confidence score for warranty_months")
    delivery_days: int = Field(100, ge=0, le=100, description="Confidence score for delivery_days")

class VendorQuotation(BaseModel):
    """
    Structured representation of a vendor quotation.
    Extracted by Vision AI and validated by Pydantic.
    """

    # Vendor info
    vendor_name: str = Field(..., description="Name of the vendor/supplier company")
    vendor_contact: Optional[str] = Field(None, description="Contact person, email, or phone")
    vendor_address: Optional[str] = Field(None, description="Vendor address")

    # Quotation metadata
    quotation_number: Optional[str] = Field(None, description="Quotation/reference number")
    quotation_date: Optional[str] = Field(None, description="Date of the quotation")
    validity_period: Optional[str] = Field(None, description="Validity period of the quotation")

    # Product details
    items: list[ProductItem] = Field(..., min_length=1, description="List of quoted products")

    # Commercial terms
    grand_total: float = Field(..., ge=0, description="Grand total amount in INR")
    tax_percentage: Optional[float] = Field(None, ge=0, description="GST/tax percentage")
    tax_amount: Optional[float] = Field(None, ge=0, description="Tax amount in INR")

    # Warranty & Delivery
    warranty_months: int = Field(..., ge=0, description="Warranty period in months")
    warranty_terms: Optional[str] = Field(None, description="Additional warranty conditions")
    delivery_days: int = Field(..., ge=0, description="Delivery time in days")
    delivery_terms: Optional[str] = Field(None, description="Delivery conditions or notes")

    # Payment
    payment_terms: Optional[str] = Field(None, description="Payment terms (e.g., 30 days net, advance)")

    # Additional
    special_conditions: Optional[str] = Field(None, description="Any special terms, notes, or conditions")

    # Contract Clause Extraction (for Clause Risk Matrix)
    contract_clauses: Optional[ContractClauses] = Field(
        None,
        description="Structured extraction of key contractual clauses from the Terms & Conditions section."
    )

    # Extraction Confidence
    confidence_scores: FieldConfidence = Field(
        ..., 
        description="A strictly typed object mapping the critical extracted fields (grand_total, warranty_months, delivery_days) to a confidence score from 0 to 100, indicating how certain you are about the extracted value. For missing values, use 0."
    )


class ExtractionResult(BaseModel):
    """Result of the document extraction process."""

    success: bool
    quotation: Optional[VendorQuotation] = None
    error: Optional[str] = None
    retries_used: int = 0
    source_file: str = ""
