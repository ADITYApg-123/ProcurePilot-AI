ProcurePilot AI
18-Day Hackathon Execution Plan
Mission
Build a reliable AI Procurement Decision & Negotiation Copilot capable of:
Processing vendor quotations Extracting procurement information Comparing vendors Identifying procurement risks Recommending suppliers Generating negotiation strategies
while remaining:
Demonstrable Reliable Explainable Feasible within 18 days
Success Criteria
By Demo Day, the system must be capable of:
Input
Three industrial motor quotations.
Processing
Extract procurement information.
Compare vendors.
Analyze procurement risks.
Generate recommendations.
Generate negotiation strategy.
Output
Vendor ranking.
Procurement recommendation.
Negotiation email.
Executive summary.
Non-Negotiable Principle
The project is considered successful if:
PDF
↓Structured Procurement Data
↓Vendor Ranking
↓Recommendation
works reliably.
Everything else is secondary.
Phase Breakdown
Phase 1
Days 1–3
Proof of Feasibility
Phase 2
Days 4–7
Core Intelligence Pipeline
https://lh3.googleusercontent.com/notebooklm/AKXwDQFHUyCjQpnfyB2tCGRNLcHzLZyzXGnY55siGvGap0LwWl9L400LkiNKZA8CUusKnAll2KYgYzMKOY-jZEm1Db3vvg_a-9AKfrduHRXsAjjj8H8j123qFXFheDaz2ocS4CK-sbCb=w619-h162-v0
Phase 3
Days 8–11
Procurement Copilot
Phase 4
Days 12–14
Frontend & User Experience
Phase 5
Days 15–16
Evaluation & Reliability
Phase 6
Days 17–18
Demo Preparation & Submission
DAY 1
Objective
Define procurement scenario and collect documents.
Tasks
Choose:
Procurement Domain
Industrial Motors
Lock permanently.
Create:
Vendor A Quotation
Vendor B Quotation
Vendor C Quotation
Create realistic differences:
Vendor A
Higher cost Better warranty
Vendor B
Lower cost Moderate warranty
Vendor C
Cheapest Delivery risk
Deliverables
Three quotation PDFs.
DAY 2
Objective
Create ground truth dataset.
Tasks
Manually label:
Vendor A
Vendor B
Vendor C
Create structured JSON.
Example:
{
"vendor":"ABC Motors",
"price":100000,
"warranty":24,
"delivery_days":15
}
Deliverables
Ground-truth procurement records.
DAY 3
Objective
Validate extraction viability.
Tasks
Build:
PDF
↓Vision Extraction
↓Structured JSON
pipeline.
Compare extracted JSON against ground truth.
https://lh3.googleusercontent.com/notebooklm/AKXwDQEIxV675nce8e44_PWKooc3OBhnlAoIsdy6rpF6jUZdUbzvh0rZLhHkeUqSkfrwNJ8DCdwyWiXRXnCtdnOWLUk0l3ZmoDhekF57LB9DBcNfAQJMi5g4aFfCsiRljod1SQt7zk67FQ=w619-h142-v0
https://lh3.googleusercontent.com/notebooklm/AKXwDQEBoRCg4VCDCrH8uKbe7K0bF1E1UzIXlHIScD0UdSn0YQJQW5GlofDQK_nqbYDs59oEH57HGMvCyiGCMSJVCOWRyUmgccu_UoxFqRWTg5KP_xBROv7ENcI9OQ9DPygOStf2Rs9Gcw=w619-h124-v0
Success Criteria
At least:
80–90% extraction accuracy.
Critical Decision Point
If extraction fails:
Reduce quotation complexity immediately.
DAY 4
Objective
Build validation layer.
Tasks
Implement:
Required fields.
Missing value checks.
Data type validation.
Retry workflow.
Deliverables
Reliable extraction validation.
DAY 5
Objective
Build procurement analysis engine.
Tasks
Vendor comparison.
Cost comparison.
Warranty comparison.
Delivery comparison.
Outputs
Vendor ranking.
Comparison tables.
DAY 6
Objective
Procurement scoring system.
Tasks
Design scoring logic.
Examples:
Cost Score.
Warranty Score.
Delivery Score.
Generate overall procurement score.
Deliverables
Vendor scoring engine.
DAY 7
Objective
Risk analysis.
Tasks
Implement threshold risks.
Examples:
Warranty below threshold.
Delivery above threshold.
Missing fields.
Deliverables
Risk detection engine.
Phase 1 Milestone
By Day 7:
The system must support:
Quotation
↓Extraction
↓Validation
https://lh3.googleusercontent.com/notebooklm/AKXwDQGvpoPiQ_mhdNFbl9mp5Ye-ogkUu65H5Yj60evDwXTjx-yD0olBMWmOzOwf36LEvRT6Q-PmsYVXbELueZvDUQjZ_Y1tFdg3TkMt0gj9yrGEdAAoiZxWmTGIqBJrn0Z_i-WGVblM1Q=w619-h111-v0
↓Analysis
↓Ranking
DAY 8
Objective
Build Procurement Copilot.
Tasks
Create recommendation generation.
Examples:
Why Vendor A?
Why not Vendor B?
Deliverables
Recommendation engine.
DAY 9
Objective
Trade-off reasoning.
Tasks
Generate explanations.
Example:
https://lh3.googleusercontent.com/notebooklm/AKXwDQEJmMBh542jl2tyyC8mI5DHDpPGJOI1sR9CXtJOpqzpLPf_hLOTCjPyqF6lxPqTAxmSG03v6M0jH14BQ8yTgdAlmdmeHyXxjmRGVIXhgwDUVVcETgbBKjxKghuAvUygdIqNV70C2w=w619-h91-v0
Vendor B cheaper but shorter warranty.
Deliverables
Procurement reasoning.
DAY 10
Objective
Negotiation capability.
Tasks
Generate:
Negotiation strategy.
Negotiation talking points.
Negotiation email.
Deliverables
Negotiation assistant.
DAY 11
Objective
Procurement Q&A.
Tasks
Answer:
Why selected?
What risks?
What savings?
Deliverables
Interactive procurement assistant.
Phase 2 Milestone
By Day 11:
The Copilot must work.
DAY 12
Objective
Frontend foundation.
Tasks
Landing page.
Upload page.
Navigation.
Deliverables
Frontend shell.
DAY 13
Objective
Dashboard.
Tasks
Vendor rankings.
Comparison cards.
Risk summary.
Savings display.
Deliverables
Dashboard complete.
DAY 14
Objective
Copilot interface.
Tasks
Chat window.
Recommendation display.
Negotiation display.
Deliverables
User experience complete.
Phase 3 Milestone
By Day 14:
End-to-end workflow operational.
DAY 15
Objective
Evaluation Framework.
Tasks
Create evaluation dataset.
Run extraction tests.
Measure accuracy.
Metrics
Extraction Accuracy.
Validation Pass Rate.
Ranking Accuracy.
Latency.
Deliverables
Evaluation dashboard.
DAY 16
Objective
Reliability testing.
Tasks
Stress testing.
Edge cases.
Validation failures.
Retry testing.
Deliverables
Reliable system.
DAY 17
Objective
Demo preparation.
Tasks
Prepare:
Demo quotations.
Demo scenario.
Demo script.
Screenshots.
Presentation.
Deliverables
Demo package.
DAY 18
Objective
Submission day.
Tasks
Record final demo.
Deploy application.
Prepare documentation.
Submit project.
Deliverables
Final submission.
Risk Register
Risk 1
Extraction Failure
Mitigation:
Reduce document complexity.
Use structured outputs.
Risk 2
Poor Recommendation Quality
Mitigation:
Improve procurement context.
Improve prompts.
Risk 3
Latency
Mitigation:
Pre-filter PDFs.
Use job-based architecture.
Risk 4
Scope Creep
Mitigation:
No new features after Day 11.
Kill List
Never build these during the hackathon:
❌ SAP Integration
❌ Oracle Integration
❌ Multi-Agent Framework
❌ Authentication System
❌ Multi-Tenant Architecture
❌ Mobile Application
❌ Procurement Forecasting
❌ Supplier Discovery
❌ Custom Monitoring Platform
❌ Complex Workflow Builder
Definition of Done
ProcurePilot is considered complete when:
A user can upload three procurement quotations and receive:
Vendor comparison Procurement ranking Risk assessment Recommendation Negotiation strategy Executive summary
through a reliable and explainable procurement copilot interface.
Final Principle
Do not optimize for feature count.
Do not optimize for architectural beauty.
Optimize for:
Reliability
+
Business Value
+
Demo Quality
+
Completion
A smaller, polished ProcurePilot will outperform a larger, unfinished ProcurePilot every time.
https://lh3.googleusercontent.com/notebooklm/AKXwDQGbra6TCBCHXZ3ih3ZF7_NKD8e4xTIY5A3V43ZscAf-Dt1H33Pf4-Of9-hr8AQrd0yyazmKM3fAjwiMMdOPNxto98z2GZ970UvXNUZu7BHhw25UxEdKDxz2dIYO_d7rkkad4yDl=w619-h161-v0
