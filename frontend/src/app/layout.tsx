import type { Metadata } from "next";
import Navbar from "./(components)/navbar/navbar";
import "./globals.css";

export const metadata: Metadata = {
  title: "Network Lab Orchestrator",
  description: "Simple ui for orchestrating network lab"
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Navbar/>
        {children}
      </body>
    </html>
  );
}
