"""
Deterministic Analysis Engine.
Calculates scores, detects risks, and ranks vendors deterministically without LLM hallucinations.
"""

from typing import List, Dict, Tuple
from app.schemas.quotation import VendorQuotation
from app.schemas.analysis import (
    ProcurementAnalysis,
    VendorScore,
    RiskFlag,
    RiskLevel,
    SavingsOpportunity,
    ScoringWeights,
    ClauseRisk,
    VendorClauseAnalysis,
)
from app.config import settings

class AnalysisEngine:
    def analyze(self, quotations: List[VendorQuotation], weights: ScoringWeights = None) -> ProcurementAnalysis:
        if not weights:
            weights = ScoringWeights(
                cost_weight=settings.DEFAULT_COST_WEIGHT,
                warranty_weight=settings.DEFAULT_WARRANTY_WEIGHT,
                delivery_weight=settings.DEFAULT_DELIVERY_WEIGHT
            )
            
        cost_comparison = {q.vendor_name: q.grand_total for q in quotations}
        warranty_comparison = {q.vendor_name: q.warranty_months for q in quotations}
        delivery_comparison = {q.vendor_name: q.delivery_days for q in quotations}
        confidence_scores = {q.vendor_name: q.confidence_scores for q in quotations}
        
        
        # 1. Vendor Scoring Engine
        vendor_scores = self._calculate_scores(quotations, weights)
        vendor_scores.sort(key=lambda x: x.overall_score, reverse=True)
        
        # Update ranks
        for i, score in enumerate(vendor_scores):
            score.rank = i + 1
            
        recommended_vendor = vendor_scores[0].vendor_name
        
        # 2. Risk Detection
        risk_flags = self._detect_risks(quotations)
        
        # 3. Savings Calculator
        savings = self._calculate_savings(quotations, recommended_vendor)
        
        # 4. Recommendation Reason (Deterministic)
        rec_reason = self._generate_reason(vendor_scores[0], quotations)
        
        # 5. Clause Risk Matrix
        contract_analysis = self._analyze_clauses(quotations)

        return ProcurementAnalysis(
            vendor_scores=vendor_scores,
            recommended_vendor=recommended_vendor,
            recommendation_reason=rec_reason,
            risk_flags=risk_flags,
            savings_opportunities=savings,
            cost_comparison=cost_comparison,
            warranty_comparison=warranty_comparison,
            delivery_comparison=delivery_comparison,
            confidence_scores=confidence_scores,
            contract_analysis=contract_analysis,
        )

    def _calculate_scores(self, quotations: List[VendorQuotation], weights: ScoringWeights) -> List[VendorScore]:
        if not quotations:
            return []
            
        # Find min/max for normalization
        costs = [q.grand_total for q in quotations]
        warranties = [q.warranty_months for q in quotations]
        deliveries = [q.delivery_days for q in quotations]
        
        min_cost, max_cost = min(costs), max(costs)
        min_warranty, max_warranty = min(warranties), max(warranties)
        min_delivery, max_delivery = min(deliveries), max(deliveries)
        
        scores = []
        for q in quotations:
            # Normalize cost: lower is better (100 is min cost, 0 is max cost)
            cost_range = max_cost - min_cost
            c_score = 100.0 if cost_range == 0 else 100.0 * (max_cost - q.grand_total) / cost_range
            
            # Normalize warranty: higher is better (100 is max warranty, 0 is min)
            warranty_range = max_warranty - min_warranty
            w_score = 100.0 if warranty_range == 0 else 100.0 * (q.warranty_months - min_warranty) / warranty_range
            
            # Normalize delivery: lower is better (100 is min delivery, 0 is max)
            delivery_range = max_delivery - min_delivery
            d_score = 100.0 if delivery_range == 0 else 100.0 * (max_delivery - q.delivery_days) / delivery_range
            
            # Weighted average
            overall = (
                (c_score * weights.cost_weight) +
                (w_score * weights.warranty_weight) +
                (d_score * weights.delivery_weight)
            )
            
            scores.append(VendorScore(
                vendor_name=q.vendor_name,
                cost_score=round(c_score, 2),
                warranty_score=round(w_score, 2),
                delivery_score=round(d_score, 2),
                overall_score=round(overall, 2),
                rank=1 # Set later
            ))
            
        return scores
        
    def _detect_risks(self, quotations: List[VendorQuotation]) -> List[RiskFlag]:
        risks = []
        for q in quotations:
            # Warranty Risk
            if q.warranty_months < 12:
                risks.append(RiskFlag(
                    vendor_name=q.vendor_name,
                    risk_type="SHORT_WARRANTY",
                    description=f"Warranty is only {q.warranty_months} months (standard is 12+).",
                    level=RiskLevel.HIGH if q.warranty_months < 6 else RiskLevel.MEDIUM
                ))
                
            # Delivery Risk
            if q.delivery_days > 30:
                risks.append(RiskFlag(
                    vendor_name=q.vendor_name,
                    risk_type="LONG_DELIVERY",
                    description=f"Delivery time is extremely long ({q.delivery_days} days).",
                    level=RiskLevel.HIGH
                ))
                
            # Payment Risk
            if "100% advance" in (q.payment_terms or "").lower():
                risks.append(RiskFlag(
                    vendor_name=q.vendor_name,
                    risk_type="PAYMENT_TERMS",
                    description="Vendor requires 100% advance payment, which poses a high financial risk.",
                    level=RiskLevel.HIGH
                ))
        return risks
        
    def _calculate_savings(self, quotations: List[VendorQuotation], recommended_vendor: str) -> List[SavingsOpportunity]:
        savings = []
        # Find the recommended quotation
        rec_q = next((q for q in quotations if q.vendor_name == recommended_vendor), None)
        if not rec_q:
            return savings
            
        for q in quotations:
            if q.vendor_name != recommended_vendor and q.grand_total > rec_q.grand_total:
                amount = q.grand_total - rec_q.grand_total
                percentage = (amount / q.grand_total) * 100
                savings.append(SavingsOpportunity(
                    cheaper_vendor=recommended_vendor,
                    expensive_vendor=q.vendor_name,
                    savings_amount=round(amount, 2),
                    savings_percentage=round(percentage, 2)
                ))
        return savings
        
    def _generate_reason(self, top_score: VendorScore, quotations: List[VendorQuotation]) -> str:
        q = next(q for q in quotations if q.vendor_name == top_score.vendor_name)
        reasons = []
        if top_score.cost_score >= 80:
            reasons.append(f"highly competitive pricing (₹{q.grand_total:,.2f})")
        if top_score.warranty_score >= 80:
            reasons.append(f"excellent warranty coverage ({q.warranty_months} months)")
        if top_score.delivery_score >= 80:
            reasons.append(f"fast delivery timeline ({q.delivery_days} days)")
            
        if not reasons:
            return f"{top_score.vendor_name} achieved the highest overall balanced score across cost, warranty, and delivery."
            
        return f"{top_score.vendor_name} is recommended due to its " + " and ".join(reasons) + "."

    def _analyze_clauses(self, quotations: List[VendorQuotation]) -> dict:
        """
        Deterministic clause risk grader.
        Takes the AI-extracted ContractClauses and applies clear thresholds to produce
        a traffic-light risk level for each clause category per vendor.
        """
        result = {}
        for q in quotations:
            cc = q.contract_clauses

            # ── Payment Terms ────────────────────────────────────────────────
            # 0 days = advance required = HIGH risk for buyer
            # 1-7 days = very short window = MEDIUM risk
            # 8+ days = acceptable = LOW risk
            if cc is None or cc.payment_terms_days is None:
                payment = ClauseRisk(
                    extracted_value="Not specified",
                    risk_level=RiskLevel.MEDIUM,
                    note="Payment terms not explicitly stated in the quotation."
                )
            elif cc.payment_terms_days == 0:
                payment = ClauseRisk(
                    extracted_value="100% / Advance required before start",
                    risk_level=RiskLevel.HIGH,
                    note="Full or majority advance payment required before manufacturing begins. Highest buyer risk."
                )
            elif cc.payment_terms_days <= 7:
                payment = ClauseRisk(
                    extracted_value=f"Net {cc.payment_terms_days} days (very short window)",
                    risk_level=RiskLevel.MEDIUM,
                    note=f"First payment due within {cc.payment_terms_days} days of PO — tight window."
                )
            else:
                payment = ClauseRisk(
                    extracted_value=f"Net {cc.payment_terms_days} days from milestone",
                    risk_level=RiskLevel.LOW,
                    note=f"First payment not required until {cc.payment_terms_days} days after a delivery/commissioning milestone."
                )

            # ── Penalty / LD ─────────────────────────────────────────────────
            # High penalty = LOW risk for buyer (vendor is incentivised to deliver on time)
            # Low penalty = HIGH risk for buyer (vendor has little consequence for delay)
            # No penalty = HIGH risk
            if cc is None or cc.penalty_pct_per_week is None:
                penalty = ClauseRisk(
                    extracted_value="Not specified",
                    risk_level=RiskLevel.HIGH,
                    note="No Liquidated Damages clause found. Buyer has no financial recourse for delays."
                )
            elif cc.penalty_pct_per_week >= 0.5:
                penalty = ClauseRisk(
                    extracted_value=f"{cc.penalty_pct_per_week:.2f}% of contract value per week",
                    risk_level=RiskLevel.LOW,
                    note="Strong LD clause — vendor has significant financial incentive to deliver on time."
                )
            elif cc.penalty_pct_per_week >= 0.2:
                penalty = ClauseRisk(
                    extracted_value=f"{cc.penalty_pct_per_week:.2f}% of contract value per week",
                    risk_level=RiskLevel.MEDIUM,
                    note="Moderate LD rate. Provides some recourse but may not fully compensate buyer for delays."
                )
            else:
                penalty = ClauseRisk(
                    extracted_value=f"{cc.penalty_pct_per_week:.2f}% of contract value per week",
                    risk_level=RiskLevel.HIGH,
                    note="Very low LD rate. Minimal deterrent for the vendor to delay delivery."
                )

            # ── Liability Cap ────────────────────────────────────────────────
            # Capped = protects vendor = MEDIUM risk for buyer (some protection, but limited)
            # Uncapped = full exposure = LOW risk for buyer (buyer can recover full losses)
            # No clause = ambiguous = HIGH risk
            if cc is None or cc.liability_capped is None:
                liability = ClauseRisk(
                    extracted_value="Not specified",
                    risk_level=RiskLevel.HIGH,
                    note="No liability clause found. Legal exposure is ambiguous."
                )
            elif cc.liability_capped:
                liability = ClauseRisk(
                    extracted_value="Capped (finite limit stated)",
                    risk_level=RiskLevel.MEDIUM,
                    note="Vendor's liability is capped. Buyer's recovery is limited if losses exceed the cap."
                )
            else:
                liability = ClauseRisk(
                    extracted_value="Uncapped / Unlimited",
                    risk_level=RiskLevel.LOW,
                    note="No cap on vendor's liability. Buyer has maximum legal recourse."
                )

            # ── Force Majeure ─────────────────────────────────────────────────
            # Present = vendor can escape liability for some events = MEDIUM risk
            # Absent = vendor has no FM escape = LOW risk for buyer
            if cc is None or cc.force_majeure_included is None:
                force_majeure = ClauseRisk(
                    extracted_value="Not specified",
                    risk_level=RiskLevel.MEDIUM,
                    note="Force majeure clause not clearly stated."
                )
            elif cc.force_majeure_included:
                force_majeure = ClauseRisk(
                    extracted_value="Included",
                    risk_level=RiskLevel.MEDIUM,
                    note="Vendor can cite force majeure to avoid penalties for some delay events."
                )
            else:
                force_majeure = ClauseRisk(
                    extracted_value="Not included",
                    risk_level=RiskLevel.LOW,
                    note="No force majeure escape clause. Vendor is liable for all delays regardless of cause."
                )

            result[q.vendor_name] = VendorClauseAnalysis(
                payment_terms=payment,
                penalty=penalty,
                liability=liability,
                force_majeure=force_majeure,
            ).model_dump()

        return result

analysis_engine = AnalysisEngine()
