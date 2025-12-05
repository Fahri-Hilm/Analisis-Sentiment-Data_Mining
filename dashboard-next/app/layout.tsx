import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Garuda: Mimpi Dunia yang Tertunda",
  description: "Analisis sentimen dan opini publik di balik kegagalan kualifikasi Timnas Indonesia",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
