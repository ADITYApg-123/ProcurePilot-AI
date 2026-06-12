---
title: ProcurePilot AI
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# ProcurePilot AI

**Intelligent Procurement Decision & Negotiation Copilot**

ProcurePilot AI is an AI-powered procurement assistant that analyzes vendor quotations, compares suppliers, identifies risks, recommends the best vendor, and helps negotiate better deals.

## What It Does

Upload vendor quotation PDFs → Get instant procurement intelligence:

- **Vendor Comparison** — Side-by-side analysis across cost, warranty, delivery, and terms
- **Procurement Scoring** — Deterministic scoring engine with configurable weights
- **Risk Detection** — Flags short warranties, delayed deliveries, and missing information
- **AI Recommendations** — Explainable vendor selection with trade-off analysis
- **Negotiation Support** — Strategy generation, talking points, and email drafts
- **Executive Reports** — One-click procurement summary for management review

## Architecture

```
PDF Upload → Vision Extraction → Pydantic Validation → Deterministic Analysis → AI Copilot → Dashboard + Chat
```

- **Deterministic calculations** — Python handles all scoring, comparisons, and financial math
- **AI reasoning** — Gemini handles document understanding, recommendations, and negotiation
- **Validation layer** — Pydantic schemas enforce data integrity with retry workflows

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js · React · TypeScript · Tailwind CSS |
| Backend | FastAPI · Python |
| Database | Supabase PostgreSQL |
| AI | Google Gemini 2.5 Flash |
| Validation | Pydantic |
| Deployment | Vercel · Render · Supabase |

## Project Structure

```
ProcurePilot-AI/
├── frontend/          # Next.js application
├── backend/           # FastAPI server
├── project details/   # Architecture docs & planning
├── .gitignore
└── README.md
```

## Team

Built for the Open Innovation Hackathon.

## License

This project is developed for hackathon purposes.
