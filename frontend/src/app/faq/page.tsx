"use client";

import React from 'react';
import Link from 'next/link';
import '../help/page.css';
import '../page.css'; // inherit header styles

export default function FAQCenter() {
  return (
    <main className="app-main help-main">
      <header className="app-header">
        <Link href="/" style={{ textDecoration: 'none' }}>
          <div className="logo-container" style={{ cursor: 'pointer' }} title="Return to Home">
            <div className="logo-mark"></div>
            <h1>ProcurePilot</h1>
          </div>
        </Link>
        <div className="header-actions" style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
          <Link href="/about" style={{ textDecoration: 'none' }}>
            <button className="nav-link">About</button>
          </Link>
          <span style={{ color: 'var(--border-color)', userSelect: 'none' }}>|</span>
          <Link href="/help" style={{ textDecoration: 'none' }}>
            <button className="nav-link">Help</button>
          </Link>
          <span style={{ color: 'var(--border-color)', userSelect: 'none' }}>|</span>
          <Link href="/faq" style={{ textDecoration: 'none' }}>
            <button className="nav-link" style={{ fontWeight: 700, color: 'var(--text-primary)' }}>FAQ</button>
          </Link>
          <Link href="/" style={{ textDecoration: 'none' }}>
            <button className="header-back-btn">
              ← Back to Dashboard
            </button>
          </Link>
        </div>
      </header>

      <div className="help-container" style={{ justifyContent: 'center' }}>
        <section className="help-content">
          <div className="content-card animate-fade-in">
            <h2>Frequently Asked Questions</h2>
            
            <details className="faq-item">
              <summary><h4>How is this different from standard ChatGPT?</h4></summary>
              <div className="faq-content">
                <p>Standard LLMs hallucinate numbers and struggle with complex math. ProcurePilot isolates the AI: we use it <strong>only</strong> to extract the data from PDFs into JSON. Once the data is extracted, 100% of the scoring, ranking, and negotiation math is handled by a deterministic rules engine. You get AI speed with calculator accuracy.</p>
              </div>
            </details>

            <details className="faq-item">
              <summary><h4>What do the percentages in the comparison matrix mean?</h4></summary>
              <div className="faq-content">
                <p>That is the <strong>Extraction Confidence Heatmap</strong>. The AI grades its own certainty based on how clearly the data was presented in the original PDF. A 95% means the price was explicitly stated. A 60% means the AI had to infer it from confusing formatting, signaling that you should manually verify that specific cell.</p>
              </div>
            </details>

            <details className="faq-item">
              <summary><h4>Are my confidential contracts secure?</h4></summary>
              <div className="faq-content">
                <p>For this hackathon demo, the PDFs are processed securely and deleted immediately after the structured data is returned. The interactive dashboard runs entirely client-side.</p>
              </div>
            </details>
          </div>
        </section>
      </div>
    </main>
  );
}
