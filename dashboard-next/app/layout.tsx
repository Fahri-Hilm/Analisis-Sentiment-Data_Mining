import type { Metadata } from "next";
import { JetBrains_Mono } from "next/font/google"; // Import font
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
import dynamic from "next/dynamic";
import { CommandCenter } from "@/components/CommandCenter";

// Lazy load 3D background
const Background3D = dynamic(() => import("@/components/Background3D"), {
  ssr: false,
  loading: () => <div className="fixed inset-0 bg-[#020617] -z-10" />, // Placeholder
});

// Configure font
const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "Sentiment Analysis Dashboard",
  description: "Advanced AI Sentiment Analysis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`flex h-screen overflow-hidden bg-[#020617] text-slate-200 ${jetbrainsMono.variable}`}>
        <Background3D />
        <CommandCenter />
        <Sidebar />
        <main className="flex-1 overflow-y-auto relative z-10 ml-72">
          {children}
        </main>
      </body>
    </html>
  );
}
