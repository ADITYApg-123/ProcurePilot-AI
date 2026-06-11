import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ProcurePilot | AI Procurement Copilot",
  description: "AI-driven procurement analysis and negotiation copilot.",
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
