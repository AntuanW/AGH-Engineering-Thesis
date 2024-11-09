import type { Metadata } from "next";
import "./globals.css";

import Navbar from "./(components)/navbar/navbar";

export const metadata: Metadata = {
  title: "Network Lab Supoorter",
  description: "Simple UI that supports network lab",
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
