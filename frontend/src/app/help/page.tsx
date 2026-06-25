"use client";

import React from 'react';
import { Hexagon, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import './page.css';
import '../page.css'; // inherit header styles

export default function HelpCenter() {
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
            <button className="btn-secondary" style={{ background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-secondary)' }}>About</button>
          </Link>
          <Link href="/help" style={{ textDecoration: 'none' }}>
            <button className="btn-secondary" style={{ background: 'transparent', border: 'none', boxShadow: 'none', color: 'var(--text-primary)', fontWeight: 600 }}>Help</button>
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
            <h2>User Guide</h2>
            <p className="lead-text">Welcome to ProcurePilot. This guide explains how to get the most out of our deterministic AI procurement engine.</p>
            
            <div className="guide-section">
              <h3>1. Uploading Documents</h3>
              <p>Upload your vendor quotation PDFs using the drag-and-drop zone. Our pipeline uses AI purely as an <strong>extraction layer</strong> to pull structured data (pricing, delivery dates, warranty, and contract clauses).</p>
              <div className="tip-box">
                <strong>Pro Tip:</strong> Watch the live terminal to see exactly how the AI hands off the data to the deterministic math engine. No hallucinations!
              </div>
            </div>

            <div className="guide-section">
              <h3>2. The What-If Scenario Engine</h3>
              <p>On the main dashboard, you'll see sliders for <strong>Cost</strong>, <strong>Delivery</strong>, and <strong>Warranty</strong>. Drag these sliders to instantly recalculate the vendor rankings. This is powered entirely by math running locally in your browser.</p>
            </div>

            <div className="guide-section">
              <h3>3. Contract Clause Risk Matrix</h3>
              <p>Beyond pricing, the AI extracts key legal clauses. The engine automatically flags risky enterprise terms (like uncapped liabilities or aggressive penalty structures) in red, helping you spot traps instantly.</p>
            </div>

            <div className="guide-section">
              <h3>4. The Negotiation Simulator</h3>
              <p>In the Copilot Chat, select a vendor and enter a target discount percentage. The simulator will instantly update the main dashboard to show you if that price drop is enough to push that vendor into 1st place.</p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
