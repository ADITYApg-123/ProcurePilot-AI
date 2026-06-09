ProcurePilot AI
Technical Architecture Document (Hackathon MVP)
Version
Hackathon MVP v1.0
Project Category
Open Innovation
Project Type
AI Procurement Decision & Negotiation Copilot
1. Technical Goals
The technical architecture is designed to achieve four primary objectives:
Reliability
Procurement decisions must be grounded in validated data and deterministic calculations.
Explainability
Every recommendation must be traceable to extracted procurement information.
Hackathon Feasibility
The system must be realistically buildable within an 18-day hackathon timeline.
User Experience
Users should receive procurement insights through a fast, intuitive, and conversational interface.
2. Technology Stack
Frontend
Framework
Next.js
UI Library
React
Language
TypeScript
Styling
Tailwind CSS
Backend
Framework
FastAPI
Language
Python
Database
Primary Database
Supabase PostgreSQL
Purpose:
Job tracking Vendor records Analysis results Evaluation metrics Chat history
AI Layer
AI System 1
Vision-Based Document Intelligence Model
Purpose:
Procurement document understanding Table extraction Commercial field extraction
AI System 2
Procurement Copilot Model
Purpose:
Recommendations Negotiation support Procurement Q&A Executive summaries
Validation Layer
Schema Validation
Pydantic
Purpose:
Structured outputs Type validation Reliability enforcement
Monitoring
Platform
Langfuse
Purpose:
Prompt tracing Cost tracking Latency tracking
Response monitoring
Deployment
Frontend
Vercel
Backend
Render
Database
Supabase
3. High-Level Technical Flow
User Uploads Quotations
↓Document Intake
↓Document Intelligence Pipeline
↓Validation Layer
↓Procurement Analysis Engine
↓Procurement Copilot
↓Dashboard & Chat Interface
↓Final Recommendation
4. Frontend Architecture
Purpose
Provide an intuitive procurement analysis experience.
The frontend is responsible only for:
User interaction
https://lh3.googleusercontent.com/notebooklm/AKXwDQEuO71MgEDEFnLTAnH_FOHh-x1bWcTkmkBaslsk_axF7U8FGZg6zCzYHKz6ZzbcLVZBsLpx65Zx_FrL1gDuZZEt6UMY8njxMg86P59AFfu0wggmiiRTWnbEYzTqh-6lGaQM5E5hdg=w619-h317-v0
Progress visualization Results presentation
All intelligence resides in the backend.
Screen 1: Landing Page
Purpose:
Introduce ProcurePilot.
Contents:
Project overview Key capabilities Upload entry point
Screen 2: Upload Workspace
Purpose:
Receive procurement documents.
Features:
Drag-and-drop upload Multi-file support Upload validation Analysis initiation
Screen 3: Procurement Dashboard
Displays:
Vendor rankings Cost comparison Savings opportunities Procurement risks Recommended vendor
Screen 4: Copilot Workspace
Allows users to:
Ask procurement questions Request explanations Generate negotiation strategies Create supplier emails
Frontend State Management
Tracks:
Uploaded files Job status Analysis progress Results Chat interactions
5. Backend Architecture
The backend consists of five major services.
Service 1: API Gateway
Purpose:
Serve as the communication layer between frontend and backend.
Responsibilities:
Request handling Response delivery Authentication (future) Validation
Core Endpoints
Upload
Receives procurement documents.
Job Status
Returns processing progress.
Analysis Results
Returns completed procurement intelligence.
Copilot Chat
Handles procurement conversations.
Service 2: Job Management Service
Purpose:
Manage long-running procurement analysis.
Job States
UPLOADED
EXTRACTING
VALIDATING
ANALYZING
GENERATING_RECOMMENDATION
COMPLETED
FAILED
Responsibilities
Job creation Progress tracking Status updates Result management
https://lh3.googleusercontent.com/notebooklm/AKXwDQFakDGmMfXubmbc0EPC0U8x-qbu0sB7H9uFzDLeCRXNhB9mPUFXHWhtByClfF2UKyUzjRnhh4SdurCvWmmxFT69EpTecplWn718cGelPS1SjAu96nhwMtJsjAqDa5uuMC0w9slR=w619-h275-v0
Service 3: Document Intelligence Service
Most critical component.
Responsible for converting procurement documents into structured data.
Step 1
Document Intake
Receives uploaded quotations.
Step 2
PDF Pre-Filtering
Identifies:
Pricing pages Warranty pages Delivery pages Commercial summary pages
Removes irrelevant pages where possible.
Purpose:
Reduce processing time and token usage.
Step 3
PDF-to-Image Conversion
Converts relevant pages into images.
Step 4
Vision Extraction
Extracts:
Vendor Name Product Name
Quantity Unit Price Total Price Warranty Delivery Time Payment Terms
Step 5
Structured Output Generation
Outputs must conform to:
Vendor Quote Schema
No free-form extraction is allowed.
Service 4: Validation Service
Purpose:
Act as the reliability firewall.
Schema Validation
Verifies:
Required fields Data types Missing values Structural correctness
Business Validation
Verifies:
Vendor exists Pricing exists Warranty exists Delivery information exists
Recovery Workflow
Attempt 1
↓
Attempt 2
↓
Attempt 3
↓
Manual Review Required
Purpose:
Prevent infinite extraction loops.
Service 5: Procurement Analysis Engine
Purpose:
Generate procurement intelligence.
Architectural Rule
No LLMs are allowed inside this engine.
All calculations are deterministic.
Responsibilities
Vendor Comparison
Compare:
Cost Warranty Delivery Payment Terms
https://lh3.googleusercontent.com/notebooklm/AKXwDQGNrZYU85LUmzCHYJuqPsQTylij7GG5B8QyCaaoZtbkfZ4dLWs5Uwjwhqxc5Yu5HpvTm4V-xpIWPrxJ24y9_2QzQWL8n63HwxKIn-ErU9M9NRURWeeuGT4yKJjZ1lkoTGEx9Xp53w=w619-h277-v0
Procurement Scoring
Generate:
Cost Score Warranty Score Delivery Score Overall Score
Savings Analysis
Calculate:
Cost differences Savings opportunities Pricing advantages
Threshold Risk Detection
Identify:
Warranty below threshold Delivery delay Missing commercial fields Pricing anomalies
Outputs
Procurement Intelligence Package
Contains:
Rankings Scores Savings Risk flags
6. Procurement Copilot Architecture
The system uses a single Procurement Copilot Agent.
Not a multi-agent architecture.
Purpose
Convert procurement intelligence into actionable decisions.
Inputs
Receives only:
Vendor rankings Procurement scores Savings estimates Risk flags
The copilot never receives raw PDFs.
Capabilities
Recommendation Generation
Answers:
Which vendor should be selected? Why?
Trade-Off Analysis
Explains:
Cost vs warranty Cost vs delivery Risk vs savings
Semantic Risk Analysis
Detects:
Ambiguous warranty language Missing commitments Unclear procurement terms
Negotiation Support
Generates:
Negotiation strategy Procurement talking points Supplier communication drafts
Procurement Q&A
Answers:
Why was Vendor B selected? What should we negotiate? What are the major risks? How much can we save?
7. Database Architecture
Database
Supabase PostgreSQL
Table 1: Jobs
Stores:
Job ID Status Progress Creation Time
Table 2: Vendor Quotes
Stores:
Vendor Information Pricing Information Warranty Information Delivery Information
Table 3: Analysis Results
Stores:
Rankings Scores Risk Flags Savings Estimates
Table 4: Chat History
Stores:
User Questions Copilot Responses
Table 5: Evaluation Records
Stores:
Accuracy Metrics Latency Metrics Validation Metrics
8. Evaluation Architecture
Evaluation is a core differentiator of ProcurePilot.
Most hackathon projects provide AI outputs.
ProcurePilot measures AI performance.
Evaluation Dataset
Manually labeled procurement quotations.
Ground-truth procurement records.
Reliability Metrics
Extraction Accuracy
Measures extraction correctness.
Schema Validation Pass Rate
Measures output validity.
Field Completion Rate
Measures extraction completeness.
Vendor Ranking Accuracy
Measures recommendation quality.
Operational Metrics
Processing Latency
Upload→Recommendation
Retry Frequency
Validation failure rate.
Average Extraction Time
Measures extraction performance.
Monitoring
Langfuse automatically tracks:
Prompt execution Model responses Latency Cost
Token usage
9. Deployment Architecture
User
│ ▼ Frontend (Vercel)
│ ▼ FastAPI Backend (Render)
│ ├────────► Supabase PostgreSQL │ ├────────► Vision Model API │ ├────────► Copilot Model API │ └────────► Langfuse Monitoring
10. Demo-Day Architecture
The MVP intentionally supports a constrained environment.
Supported Domain
Industrial Equipment Procurement
Demo Scenario
Industrial Motor Procurement
Supported Inputs
Digitally Generated PDF Quotations
Vendor Count
Three Vendor Quotations
https://lh3.googleusercontent.com/notebooklm/AKXwDQEzSdW3g07w-gxsLoenVjFRKeXptTrwWkmLTmd8pFtCgmJ37KLguHdVK-KAFnb0pSLQwyRFAhcg-0zYVmT6Ay9SYlIxxehvssGK6hrHTCQTV_JBiP5fVpFpzBAovL1-Q85e9kLhgw=w619-h320-v0
Supported Outputs
Vendor Comparison
Procurement Recommendation
Risk Assessment
Negotiation Strategy
Executive Summary
Not Supported
SAP Integration Oracle Integration Handwritten Documents Multi-language Procurement Supplier Discovery Procurement Forecasting
11. Technical Risks & Mitigations
Risk 1
Document Extraction Failure
Mitigation
Validation Layer
Recovery Workflow
Structured Outputs
Risk 2
LLM Hallucination
Mitigation
Deterministic Analysis Engine
Grounded Procurement Context
Structured Inputs
Risk 3
Long Processing Times
Mitigation
Job-Based Architecture
Progress Tracking
PDF Pre-Filtering
Risk 4
Invalid Procurement Recommendations
Mitigation
Recommendation Grounding
Traceability
Procurement Intelligence Package
12. Final Technical Principles
ProcurePilot follows five non-negotiable technical principles:
Principle 1
Vision AI extracts information.
Principle 2
Validation verifies information.
Principle 3
Deterministic logic performs calculations.
Principle 4
The Copilot reasons using validated procurement intelligence.
Principle 5
Every recommendation must be explainable, traceable, and grounded in procurement data.
Technical Outcome
The final system demonstrates how modern AI systems can combine document intelligence, deterministic analytics, and conversational decision support to transform procurement workflows into reliable, explainable, and actionable procurement intelligence.
