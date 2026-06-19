"""
Vendor Quotation Schema.
Defines the structured format that all extracted vendor data MUST conform to.
This is the reliability firewall — no free-form extraction allowed.
"""

from pydantic import BaseModel, Field
from typing import Optional


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
