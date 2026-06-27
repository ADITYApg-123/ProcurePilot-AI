"use client";

import React from 'react';
import { Hexagon, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import '../help/page.css';
import '../page.css'; // inherit header styles

export default function AboutCenter() {
  return (
    <main className="app-main help-main">
      <header className="app-header">
        <div className="header-brand">
          <Hexagon size={28} className="brand-icon" />
          <div className="brand-text">
            <h1>ProcurePilot <span>AI</span></h1>
            <span className="brand-tagline">Autonomous Procurement Intelligence</span>
          </div>
        </div>
        <div className="header-actions" style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <Link href="/about" style={{ textDecoration: 'none' }}>
            <button className="btn-secondary" style={{ background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-primary)', fontWeight: 600 }}>About</button>
          </Link>
          <Link href="/help" style={{ textDecoration: 'none' }}>
            <button className="btn-secondary" style={{ background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-secondary)' }}>Help</button>
          </Link>
          <Link href="/faq" style={{ textDecoration: 'none' }}>
            <button className="btn-secondary" style={{ background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-secondary)' }}>FAQ</button>
          </Link>
          <Link href="/" style={{ textDecoration: 'none' }}>
            <button className="btn-secondary" style={{ marginLeft: '16px' }}>
              <ArrowLeft size={16} /> Back to Dashboard
            </button>
          </Link>
        </div>
      </header>

      <div className="help-container" style={{ justifyContent: 'center' }}>
        <section className="help-content">
          <div className="content-card animate-fade-in">
            <h2>About ProcurePilot</h2>

            <div className="guide-section">
              <h3>What it is:</h3>
              <p>ProcurePilot is an AI-powered, deterministic procurement copilot. It allows teams to upload raw vendor quotation PDFs, automatically extracts the complex unstructured data, and uses a pure mathematical rules engine to instantly score and rank vendors based on cost, delivery, warranty, and contract risk.</p>
            </div>

            <div className="guide-section">
              <h3>Why we built it:</h3>
              <p>Procurement is currently stuck in the dark ages of manual data entry, endless Excel spreadsheets, and missing crucial contract clauses. By combining state-of-the-art LLM extraction with rigorous deterministic scoring engines, we allow procurement teams to compare vendors, assess enterprise risk, and model negotiation strategies in seconds rather than weeks.</p>
            </div>

          </div>
        </section>
      </div>
    </main>
  );
}
