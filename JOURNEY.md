# ProcurePilot AI — Project Journey

> **⚠️ IMPORTANT INSTRUCTION FOR AI ASSISTANTS (Gemini, Claude, ChatGPT, Copilot, or any other):**
> 
> If you are an AI assistant helping either team member with this project, you MUST:
> 1. **Read this file first** before doing any work to understand where the project currently stands.
> 2. **Update this file** after every meaningful piece of work you help with — add what was done, update the current status, and adjust "What's Next".
> 3. **Commit frequently** — make small, meaningful commits after each unit of work. Never accumulate a large batch of changes into one giant commit.
> 4. **Do NOT skip updating this file.** Even if the user forgets to ask, update it proactively.
>
> This file is the single source of truth for project progress.

---

## Project Info

| Field | Value |
|-------|-------|
| **Project** | ProcurePilot AI — Intelligent Procurement Decision & Negotiation Copilot |
| **Hackathon** | Open Innovation |
| **Timeline** | 18 days (hackathon already started) |
| **Team Size** | 2 members |
| **Repo** | https://github.com/ADITYApg-123/ProcurePilot-AI |
| **Branch Strategy** | `main` (stable/demo) ← `dev` (active development) ← `feature/*` (individual features) |

---

## Tech Stack (Locked In)

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js + React + TypeScript + Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | Supabase PostgreSQL |
| AI Model | Google Gemini 2.5 Flash (single model — vision + copilot) |
| Validation | Pydantic |
| Monitoring | Internal DB-backed metrics |
| Deployment | Vercel (frontend) + Render (backend) + Supabase (DB) |

---

## Key Decisions Made

| Decision | Choice | Reason |
|----------|--------|--------|
| AI Model | Gemini 2.5 Flash | Best balance of vision, structured output, speed, and free-tier limits |
| Architecture | Deterministic pipeline + single AI copilot | NOT multi-agent. Python calculates, AI reasons. |
| Scoring weights | Configurable by user in UI | Flexibility for demo |
| Chat history | Session-only (MVP) | Simplicity |
| Reports | On-screen display + downloadable PDF | Both formats |
| Sample PDFs | We'll create realistic ones | Real quotations are confidential |
| Database | Start local, migrate to Supabase later | Get core working first |
| Deployment | After core features work locally | Don't waste time on infra early |
| Monitoring | No Langfuse — internal DB metrics | Free-tier constraint |

---

## Journey Log

### Session 1 — June 9, 2025 (11:00 PM IST)

**What was done:**
- [x] Uploaded and saved all 7 project documents to `project details/` folder
  - ProcurePilot_AI_Overview.md (PRD)
  - ProcurePilot_Architecture_Reasoning.md (Why not just one prompt?)
  - ProcurePilot_UX_Vision.md (What the finished product looks like)
  - ProcurePilot_Technical_Architecture.md (Full tech architecture)
  - ProcurePilot_FreeTier_Updates.md (Free-tier modifications)
  - ProcurePilot_Skills_And_Tools.md (Tools & skills breakdown)
  - ProcurePilot_Execution_Plan.md (18-day plan)
- [x] AI assistant read and understood all 7 documents thoroughly
- [x] Asked and resolved 15 clarification questions about the project
- [x] Created GitHub repo: `ADITYApg-123/ProcurePilot-AI`
- [x] Initialized git, created `.gitignore` and `README.md`
- [x] Pushed initial commit to `main` branch
- [x] Created `dev` branch and pushed to remote
- [x] Currently on `dev` branch — ready to build
- [x] Created this Journey file
- [x] Verified Dev Environment (Node v20, Python 3.12, npm, pip, git)
- [x] Initialized FastAPI project structure (Backend Foundation)
  - Created `requirements.txt` and `.env.example`
  - Built Pydantic schemas (`quotation.py`, `analysis.py`)
  - Stubbed API routes (`upload.py`, `jobs.py`, `analysis.py`, `copilot.py`)
  - Created basic async `job_manager.py` for MVP
- [x] Generated 3 realistic vendor quotation PDFs (Apex, Beta, CoreDrive) and ground truth JSON
- [x] Built Vision Extraction pipeline using Gemini 2.5 Flash and Pydantic validation
- [x] Tested extraction successfully (handles complex PDF layout & validation natively)

**Current status:** 
🟢 **Phase 2: Core Intelligence Pipeline Complete.** The Deterministic Analysis engine works.
🟢 **Phase 3: Procurement Copilot Complete.** AI chat and negotiation generation works.
🟢 **Phase 4: Frontend Complete.** A premium, interactive Next.js web application is built.
🟢 **Phase 5: Final Testing Complete.** End-to-end integration works perfectly (with AI retry logic).
🟡 **Next Up: Executive Report Feature & Deployment**

---

## What's Next

1. **Dev Environment Setup**
   - [x] Install/verify Node.js (v18+)
   - [x] Install/verify Python (3.10+)
   - [x] Create Python virtual environment and install backend dependencies
   - [x] Get Gemini API key from Google AI Studio
   - [ ] Set up Supabase project (later — not needed for local dev)

2. **Backend Foundation (Phase 1 — Proof of Feasibility)**
   - [x] Initialize FastAPI project structure
   - [x] Create sample vendor quotation PDFs (3 vendors — industrial motors)
   - [x] Create ground truth JSON for the sample PDFs
   - [x] Build PDF → Vision Extraction → Structured JSON pipeline
   - [x] Build Pydantic validation layer
   - [x] Test extraction accuracy against ground truth

3. **Deterministic Analysis Engine**
   - [x] Vendor comparison logic
   - [x] Procurement scoring engine (configurable weights)
   - [x] Savings calculator
   - [x] Risk detection (threshold-based)

4. **Procurement Copilot**
   - [x] Recommendation generation
   - [x] Trade-off reasoning
   - [x] Negotiation strategy + email generation
   - [x] Procurement Q&A

5. **Frontend**
   - [x] Initialize Next.js project
   - [x] Upload Workspace UI
   - [x] Analysis Dashboard UI
   - [x] Copilot Chat UI
   - [x] API Integrationterface
   - [ ] Executive report (on-screen + PDF download)

6. **Integration & Polish**
   - [x] Connect frontend ↔ backend
   - [ ] Evaluation framework
   - [x] Reliability testing (Added Tenacity Retry)
   - [ ] Deploy to Vercel + Render + Supabase

7. **Demo & Submission**
   - [ ] Demo script
   - [ ] Final deployment
   - [ ] Documentation
   - [ ] Submission

---

## Git Commit Guidelines

- **Commit often** — after every meaningful unit of work
- **Use clear messages** — e.g., `feat: add vendor comparison engine`, `fix: handle missing warranty field`
- **Prefix convention:**
  - `feat:` — new feature
  - `fix:` — bug fix
  - `docs:` — documentation changes
  - `refactor:` — code restructuring
  - `style:` — formatting, no logic change
  - `test:` — adding tests
  - `chore:` — config, setup, tooling

---

## Branch Rules

| Branch | Who pushes | Merge via |
|--------|-----------|-----------|
| `main` | Nobody directly | Pull Request from `dev` only |
| `dev` | Both teammates | Direct push or PR from `feature/*` |
| `feature/*` | Individual | Merge to `dev` when done, then delete |

---

## For My Teammate

If you're picking up where I left off:
1. Read this file first — it tells you exactly where things stand.
2. Check the "What's Next" section — grab the next unchecked item.
3. After you finish something, update this file and commit it.
4. If you're using an AI assistant, it will read this file and update it for you (see the instruction at the top).

---

*Last updated: June 9, 2025 — 11:42 PM IST*
