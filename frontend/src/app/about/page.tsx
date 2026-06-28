"use client";

import React from 'react';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import '../help/page.css';
import '../page.css'; // inherit header styles

export default function AboutCenter() {
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
            <button className="nav-link" style={{ fontWeight: 700, color: 'var(--text-primary)' }}>About</button>
          </Link>
          <span style={{ color: 'var(--border-color)', userSelect: 'none' }}>|</span>
          <Link href="/help" style={{ textDecoration: 'none' }}>
            <button className="nav-link">Help</button>
          </Link>
          <span style={{ color: 'var(--border-color)', userSelect: 'none' }}>|</span>
          <Link href="/faq" style={{ textDecoration: 'none' }}>
            <button className="nav-link">FAQ</button>
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
