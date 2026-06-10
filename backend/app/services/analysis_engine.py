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
    ScoringWeights
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
        
        return ProcurementAnalysis(
            vendor_scores=vendor_scores,
            recommended_vendor=recommended_vendor,
            recommendation_reason=rec_reason,
            risk_flags=risk_flags,
            savings_opportunities=savings,
            cost_comparison=cost_comparison,
            warranty_comparison=warranty_comparison,
            delivery_comparison=delivery_comparison
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

analysis_engine = AnalysisEngine()
