import type { ReactNode } from "react";

export const metadata = { title: "US import duty, with TariffTrust" };

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
