Excellent question.
This is exactly the question you should ask before writing a single line of code.
Because once you understand the tools and skills required, you'll realize something important:
ProcurePilot is not one project.
It is 5–6 smaller systems working together.
--------------------------------------------------------------------------------
High-Level Architecture
User
 ↓
Procurement Agent
 ↓
----------------------------------
| Document Extraction Tool       |
| Vendor Comparison Tool         |
| Risk Analysis Tool             |
| Negotiation Tool               |
| Report Generation Tool         |
----------------------------------
 ↓
Results
The agent acts as the brain.
The tools do the work.
--------------------------------------------------------------------------------
Tool 1: Document Extraction Tool
Purpose
Convert vendor quotations into structured data.
Example:
PDF:
Vendor: ABC Motors

Motor X200
Qty: 5
Price: ₹50,000
Warranty: 24 months
Output:
{
  "vendor":"ABC Motors",
  "product":"Motor X200",
  "quantity":5,
  "price":50000,
  "warranty":24
}
--------------------------------------------------------------------------------
Skills Needed
Python
Must know:
file handling
JSON
APIs
--------------------------------------------------------------------------------
PDF Processing
Libraries:
pdfplumber
PyMuPDF
Camelot
--------------------------------------------------------------------------------
OCR (if needed)
Libraries:
Tesseract
EasyOCR
--------------------------------------------------------------------------------
Difficulty
Medium
This is the hardest component.
--------------------------------------------------------------------------------
Tool 2: Vendor Comparison Tool
Purpose
Compare vendors objectively.
Input:
Vendor A
Vendor B
Vendor C
Output:
Vendor B cheapest.

Vendor A fastest delivery.

Vendor C longest warranty.
--------------------------------------------------------------------------------
Skills Needed
Python Logic
dictionaries
sorting
ranking
Data Analysis
Pandas
--------------------------------------------------------------------------------
Difficulty
Easy
No AI needed.
--------------------------------------------------------------------------------
Tool 3: Risk Analysis Tool
Purpose
Find hidden issues.
Example:
Vendor B:
Warranty: 6 months
Others:
Warranty: 24 months
Agent flags risk.
--------------------------------------------------------------------------------
Skills Needed
Prompt Engineering
LLM API Usage
Examples:
OpenAI
Gemini
--------------------------------------------------------------------------------
Difficulty
Medium
--------------------------------------------------------------------------------
Tool 4: Negotiation Tool
Purpose
Generate procurement negotiation strategies.
Example:
Vendor B is cheaper.

Request warranty extension.
Generate:
strategy
email
talking points
--------------------------------------------------------------------------------
Skills Needed
LLM APIs
Prompt Design
Structured Output
--------------------------------------------------------------------------------
Difficulty
Easy-Medium
--------------------------------------------------------------------------------
Tool 5: Report Generator
Purpose
Create executive summary.
Example:
Recommended Vendor:
ABC Motors

Reason:
15% lower cost
24-month warranty
Fastest delivery
--------------------------------------------------------------------------------
Skills Needed
HTML
or
PDF generation
Libraries:
ReportLab
WeasyPrint
--------------------------------------------------------------------------------
Difficulty
Easy
--------------------------------------------------------------------------------
The Agent Layer
This is what makes the project feel modern.
User asks:
Which vendor should I choose?
Agent decides:
Need extraction
 ↓
Need comparison
 ↓
Need risk analysis
 ↓
Need recommendation
Then responds.
--------------------------------------------------------------------------------
Skills Needed
Agent Framework (Optional)
You can use:
LangGraph
CrewAI
PydanticAI
OR
Build simple orchestration yourself.
--------------------------------------------------------------------------------
My recommendation
For a hackathon:
Don't use CrewAI.
Don't use AutoGen.
Don't use complex frameworks.
Build simple orchestration yourself.
You'll finish faster.
--------------------------------------------------------------------------------
Frontend
Needed because judges will see it.
--------------------------------------------------------------------------------
Skills
React
or
Next.js
--------------------------------------------------------------------------------
Components
Upload PDF
Chat window
Analysis page
Recommendation page
--------------------------------------------------------------------------------
Difficulty
Medium
--------------------------------------------------------------------------------
Backend
Skills
FastAPI
Recommended.
Endpoints:
/upload
/analyze
/compare
/negotiate
--------------------------------------------------------------------------------
Difficulty
Medium
--------------------------------------------------------------------------------
Database
Honestly?
For hackathon MVP:
You barely need one.
Use:
SQLite
or
simple JSON files
Initially.
--------------------------------------------------------------------------------
Skills You Will Learn
This project teaches:
AI Skills
LLM APIs
Prompt Engineering
Structured Outputs
Evaluation
--------------------------------------------------------------------------------
ML Engineering Skills
Data pipelines
OCR
Document processing
Model integration
--------------------------------------------------------------------------------
Software Engineering Skills
FastAPI
Frontend-backend communication
Deployment
Testing
--------------------------------------------------------------------------------
Product Skills
UX design
Business thinking
System design
--------------------------------------------------------------------------------
What You DO NOT Need
You do NOT need:
❌ Deep Learning training
❌ CNNs
❌ Transformers from scratch
❌ Fine-tuning
❌ Distributed training
❌ Kubernetes
❌ Multi-agent research frameworks
❌ Vector databases
❌ RAG
A lot of students add these because they sound impressive.
They are not required for winning this hackathon.
--------------------------------------------------------------------------------
If I Were Planning the First 3 Days
I'd focus only on:
Day 1
Understand procurement workflow
Collect sample quotations
Day 2
Extract structured JSON from PDFs
Day 3
Compare vendors automatically
If you can reach:
PDF
 ↓
JSON
 ↓
Vendor Ranking
by Day 3, the project becomes very achievable.
Everything else can be layered on top afterward.
