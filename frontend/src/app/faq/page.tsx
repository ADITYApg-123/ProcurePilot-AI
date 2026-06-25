"use client";

import React from 'react';
import { Hexagon, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import '../help/page.css';
import '../page.css'; // inherit header styles

export default function FAQCenter() {
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
          <Link href="/help" style={{ textDecoration: 'none' }}>
            <button className="btn-secondary" style={{ background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-secondary)' }}>Help</button>
          </Link>
          <Link href="/faq" style={{ textDecoration: 'none' }}>
            <button className="btn-secondary" style={{ background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-primary)', fontWeight: 600 }}>FAQ</button>
          </Link>
          <Link href="/about" style={{ textDecoration: 'none' }}>
            <button className="btn-secondary" style={{ background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-secondary)' }}>About</button>
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
            <h2>Frequently Asked Questions</h2>
            
            <div className="faq-item">
              <h4>How is this different from standard ChatGPT?</h4>
              <p>Standard LLMs hallucinate numbers and struggle with complex math. ProcurePilot isolates the AI: we use it <strong>only</strong> to extract the data from PDFs into JSON. Once the data is extracted, 100% of the scoring, ranking, and negotiation math is handled by a deterministic rules engine. You get AI speed with calculator accuracy.</p>
            </div>

            <div className="faq-item">
              <h4>What do the percentages in the comparison matrix mean?</h4>
              <p>That is the <strong>Extraction Confidence Heatmap</strong>. The AI grades its own certainty based on how clearly the data was presented in the original PDF. A 95% means the price was explicitly stated. A 60% means the AI had to infer it from confusing formatting, signaling that you should manually verify that specific cell.</p>
            </div>

            <div className="faq-item">
              <h4>Are my confidential contracts secure?</h4>
              <p>For this hackathon demo, the PDFs are processed securely and deleted immediately after the structured data is returned. The interactive dashboard runs entirely client-side.</p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
