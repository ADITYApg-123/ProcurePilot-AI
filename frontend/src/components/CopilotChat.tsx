"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, FileText, Calculator } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Card } from './ui/Card';
import { Spinner } from './ui/Spinner';
import { apiClient } from '../services/apiClient';
import { ProcurementAnalysis } from '../services/types';
import './CopilotChat.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

interface Props {
  jobId: string;
  analysis: ProcurementAnalysis;
  onSimulate?: (vendorName: string, newCost: number) => void;
}

export function CopilotChat({ jobId, analysis, onSimulate }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: `Hello! I'm ProcurePilot. I've analyzed your quotations and recommend **${analysis.recommended_vendor}**. How can I assist you with this procurement decision?`
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isGeneratingNegotiation, setIsGeneratingNegotiation] = useState<string | null>(null);
  
  // Negotiation Simulator State
  const [simVendor, setSimVendor] = useState<string>('');
  const [simDiscount, setSimDiscount] = useState<number>(10);

  // Set default vendor on mount or when analysis changes
  useEffect(() => {
    if (analysis.vendor_scores.length > 0 && !simVendor) {
      setSimVendor(analysis.vendor_scores[0].vendor_name);
    }
  }, [analysis, simVendor]);

  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await apiClient.askCopilot(jobId, userMessage.content, analysis);
      setMessages(prev => [
        ...prev, 
        { 
          id: (Date.now() + 1).toString(), 
          role: 'assistant', 
          content: response.response,
          sources: response.sources
        }
      ]);
    } catch (error) {
      setMessages(prev => [
        ...prev, 
        { id: (Date.now() + 1).toString(), role: 'assistant', content: 'Sorry, I encountered an error communicating with the server.' }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleGenerateNegotiation = async (vendorName: string) => {
    setIsGeneratingNegotiation(vendorName);
    
    setMessages(prev => [
      ...prev, 
      { id: Date.now().toString(), role: 'user', content: `Please generate a negotiation strategy for ${vendorName}.` }
    ]);
    
    try {
      const response = await apiClient.generateNegotiationStrategy(jobId, vendorName, analysis);
      setMessages(prev => [
        ...prev, 
        { 
          id: (Date.now() + 1).toString(), 
          role: 'assistant', 
          content: `**Negotiation Strategy for ${vendorName}:**\n\n${response.strategy}`
        }
      ]);
    } catch (error) {
      setMessages(prev => [
        ...prev, 
        { id: (Date.now() + 1).toString(), role: 'assistant', content: `Sorry, I failed to generate a strategy for ${vendorName}.` }
      ]);
    } finally {
      setIsGeneratingNegotiation(null);
    }
  };

  const handleRunSimulation = () => {
    if (!simVendor || !analysis.cost_comparison[simVendor]) return;
    if (!onSimulate) return;

    const currentCost = analysis.cost_comparison[simVendor];
    const savings = currentCost * (simDiscount / 100);
    const newCost = currentCost - savings;

    // Add user message
    const userMessage: Message = { 
      id: Date.now().toString(), 
      role: 'user', 
      content: `Simulate a ${simDiscount}% price drop for ${simVendor}.` 
    };
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    // Apply simulation (triggers global dashboard update via page.tsx)
    onSimulate(simVendor, newCost);

    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: `**Simulation Applied!** ⚡\n\nI've applied a ${simDiscount}% discount to ${simVendor}.\n- **Previous Cost:** ₹${currentCost.toLocaleString(undefined, {maximumFractionDigits:0})}\n- **Savings:** ₹${savings.toLocaleString(undefined, {maximumFractionDigits:0})}\n- **New Cost:** ₹${newCost.toLocaleString(undefined, {maximumFractionDigits:0})}\n\nThe main dashboard has been instantly updated to reflect this new price. Check the **What-If Scenario Engine** and **Vendor Comparison Matrix** to see if this discount changes the overall rankings!`
        }
      ]);
      setIsTyping(false);
    }, 1200); // Artificial delay to simulate thinking
  };


  return (
    <div className="copilot-wrapper animate-fade-in">
      <Card className="copilot-container tour-step-copilot">
        <div className="copilot-header">
          <Bot size={24} className="text-accent" />
          <h3>Procurement Copilot</h3>
        </div>
      
        <div className="negotiation-prompts">
          <p>Quick Actions:</p>
          <div className="prompt-buttons">
            {analysis.vendor_scores.map(v => (
              <button 
                key={v.vendor_name}
                className="prompt-chip"
                onClick={() => handleGenerateNegotiation(v.vendor_name)}
                disabled={!!isGeneratingNegotiation}
              >
                <FileText size={14} />
                Negotiate with {v.vendor_name}
              </button>
            ))}
          </div>
        </div>

        <div className="negotiation-simulator-panel">
          <div className="simulator-header">
            <Calculator size={16} className="text-accent" />
            <h4>Negotiation Simulator</h4>
          </div>
          <div className="simulator-controls">
            <select 
              value={simVendor} 
              onChange={e => setSimVendor(e.target.value)}
              className="sim-select"
            >
              {analysis.vendor_scores.map(v => (
                <option key={v.vendor_name} value={v.vendor_name}>{v.vendor_name}</option>
              ))}
            </select>
            <div className="discount-input-wrapper">
              <span className="minus-sign">-</span>
              <input 
                type="number" 
                value={simDiscount} 
                onChange={e => setSimDiscount(Number(e.target.value))}
                min="1" max="50"
                className="sim-input"
              />
              <span className="percent-sign">%</span>
            </div>
            <button className="btn-simulate" onClick={handleRunSimulation} disabled={isTyping}>
              Simulate
            </button>
          </div>
        </div>

        <div className="chat-history">
        {messages.map(msg => (
          <div key={msg.id} className={`message-wrapper ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'assistant' ? <Bot size={20} /> : <User size={20} />}
            </div>
            <div className="message-content">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
              {msg.sources && msg.sources.length > 0 && (
                <div className="message-sources">
                  <strong>Sources:</strong> {msg.sources.join(', ')}
                </div>
              )}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="message-wrapper assistant">
            <div className="message-avatar"><Bot size={20} /></div>
            <div className="message-content typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <input 
          type="text" 
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder="Ask a question about the analysis..."
          disabled={isTyping}
        />
        <button 
          className="send-btn" 
          onClick={handleSend}
          disabled={!input.trim() || isTyping}
        >
          <Send size={20} />
        </button>
      </div>
      </Card>
    </div>
  );
}
