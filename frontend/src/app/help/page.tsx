"use client";

import React, { useState } from 'react';
import { Hexagon, ArrowLeft, BookOpen, HelpCircle, Info } from 'lucide-react';
import Link from 'next/link';
import './page.css';
import '../page.css'; // inherit header styles

export default function HelpCenter() {
  const [activeTab, setActiveTab] = useState<'help' | 'faq' | 'about'>('help');

  return (
    <main className="app-main help-main">
      <header className="app-header">
        <div className="header-brand">
          <Hexagon size={28} className="brand-icon" />
          <div className="brand-text">
            <h1>ProcurePilot <span>AI</span></h1>
            <span className="brand-tagline">Knowledge Base</span>
          </div>
        </div>
        <div className="header-actions">
          <Link href="/">
            <button className="btn-secondary">
              <ArrowLeft size={16} /> Back to Dashboard
            </button>
          </Link>
        </div>
      </header>

      <div className="help-container">
        <aside className="help-sidebar">
          <nav className="help-nav">
            <button 
              className={`help-nav-btn ${activeTab === 'help' ? 'active' : ''}`}
              onClick={() => setActiveTab('help')}
            >
              <BookOpen size={18} /> User Guide
            </button>
            <button 
              className={`help-nav-btn ${activeTab === 'faq' ? 'active' : ''}`}
              onClick={() => setActiveTab('faq')}
            >
              <HelpCircle size={18} /> FAQ
            </button>
            <button 
              className={`help-nav-btn ${activeTab === 'about' ? 'active' : ''}`}
              onClick={() => setActiveTab('about')}
            >
              <Info size={18} /> About
            </button>
          </nav>
        </aside>

        <section className="help-content">
          {activeTab === 'help' && (
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
          )}

          {activeTab === 'faq' && (
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
          )}

          {activeTab === 'about' && (
            <div className="content-card animate-fade-in">
              <h2>About ProcurePilot</h2>
              <p>Procurement is currently stuck in the dark ages of manual data entry, endless Excel spreadsheets, and missing crucial contract clauses.</p>
              <p><strong>ProcurePilot</strong> was built to transform this process into an autonomous, intelligent command center. By combining state-of-the-art LLM extraction with rigorous deterministic scoring engines, we allow procurement teams to compare vendors, assess enterprise risk, and model negotiation strategies in seconds rather than weeks.</p>
              
              <div className="team-box" style={{ marginTop: '32px', padding: '24px', background: 'var(--surface-color)', border: '1px dashed var(--accent-primary)', borderRadius: '12px' }}>
                <h4>Hackathon Team</h4>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '8px' }}>
                  [Placeholder: Add your team names and roles here. Explain why you are passionate about solving procurement inefficiencies!]
                </p>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
