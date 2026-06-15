import { ProcurementAnalysis, VendorScore } from '../services/types';

export function recalculateScores(
  analysis: ProcurementAnalysis,
  costWeight: number,
  warrantyWeight: number,
  deliveryWeight: number
): ProcurementAnalysis {
  // 1. Calculate the sum of weights to normalize them to 1.0 (100%)
  const totalWeight = costWeight + warrantyWeight + deliveryWeight;
  const cw = costWeight / totalWeight;
  const ww = warrantyWeight / totalWeight;
  const dw = deliveryWeight / totalWeight;

  // 2. Find min/max for normalization
  const vendorNames = Object.keys(analysis.cost_comparison);
  
  const costs = vendorNames.map(v => analysis.cost_comparison[v]);
  const warranties = vendorNames.map(v => analysis.warranty_comparison[v]);
  const deliveries = vendorNames.map(v => analysis.delivery_comparison[v]);

  const minCost = Math.min(...costs);
  const maxCost = Math.max(...costs);
  const minWarranty = Math.min(...warranties);
  const maxWarranty = Math.max(...warranties);
  const minDelivery = Math.min(...deliveries);
  const maxDelivery = Math.max(...deliveries);

  // 3. Recalculate scores
  const newScores: VendorScore[] = vendorNames.map(vendor_name => {
    const cost = analysis.cost_comparison[vendor_name];
    const warranty = analysis.warranty_comparison[vendor_name];
    const delivery = analysis.delivery_comparison[vendor_name];

    const costRange = maxCost - minCost;
    const cScore = costRange === 0 ? 100.0 : 100.0 * (maxCost - cost) / costRange;

    const warrantyRange = maxWarranty - minWarranty;
    const wScore = warrantyRange === 0 ? 100.0 : 100.0 * (warranty - minWarranty) / warrantyRange;

    const deliveryRange = maxDelivery - minDelivery;
    const dScore = deliveryRange === 0 ? 100.0 : 100.0 * (maxDelivery - delivery) / deliveryRange;

    const overall = (cScore * cw) + (wScore * ww) + (dScore * dw);

    return {
      vendor_name,
      cost_score: parseFloat(cScore.toFixed(2)),
      warranty_score: parseFloat(wScore.toFixed(2)),
      delivery_score: parseFloat(dScore.toFixed(2)),
      overall_score: parseFloat(overall.toFixed(2)),
      rank: 1 // placeholder, set after sorting
    };
  });

  // 4. Sort and assign ranks
  newScores.sort((a, b) => b.overall_score - a.overall_score);
  newScores.forEach((score, index) => {
    score.rank = index + 1;
  });

  const recommendedVendor = newScores[0].vendor_name;

  // We could also recalculate savings and recommendation reasons here,
  // but for the hackathon MVP, just updating the scores, ranks, and 
  // top vendor name is enough to show the What-If engine working.
  
  // Create a new updated analysis object
  return {
    ...analysis,
    vendor_scores: newScores,
    recommended_vendor: recommendedVendor,
    // Provide a dynamic recommendation reason based on the new priorities
    recommendation_reason: `${recommendedVendor} achieved the highest overall score based on your custom What-If scenario priorities.`
  };
}
