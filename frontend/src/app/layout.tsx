import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ProcurePilot | Deterministic Procurement Copilot",
  description: "Compare vendor quotations in seconds. Deterministic-first procurement copilot: AI extracts data, pure math scores vendors. Zero hallucination risk.",
  openGraph: {
    title: "ProcurePilot | Deterministic Procurement Copilot",
    description: "Compare vendor quotations in seconds. Deterministic-first procurement copilot: AI extracts data, pure math scores vendors. Zero hallucination risk.",
    images: [{ url: '/og-preview.png', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: "ProcurePilot",
    description: "Compare vendor quotations in seconds. Math, not hallucinations.",
    images: ['/og-preview.png'],
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="app-container">
          {children}
        </div>
      </body>
    </html>
  );
}
