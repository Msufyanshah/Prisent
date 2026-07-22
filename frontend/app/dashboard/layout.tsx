"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { clearToken } from "@/lib/api";
import { PrisentIcon } from "@/components/PrisentIcon";
import { Home, FileText, BarChart3, Settings } from "lucide-react";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Home", Icon: Home },
  { href: "/dashboard/posts", label: "Posts", Icon: FileText },
  { href: "/dashboard/analytics", label: "Analytics", Icon: BarChart3 },
  { href: "/dashboard/settings", label: "Settings", Icon: Settings },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [logoutHovered, setLogoutHovered] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("prisent_token");
    if (!token) router.push("/login");
  }, [router]);

  function handleLogout() {
    clearToken();
    router.push("/login");
  }

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#09090B" }}>
      {/* Sidebar navigation panel - Fixed 240px */}
      <aside
        style={{
          width: 240,
          flexShrink: 0,
          background: "#18181B",
          borderRight: "1px solid #27272A",
          display: "flex",
          flexDirection: "column",
          padding: "24px 0",
        }}
      >
        <div style={{ padding: "0 24px 24px" }}>
          {/* Prisent "P" icon glyph — flat, no background tile */}
          <PrisentIcon size={24} color="#FAFAFA" />
        </div>

        <nav style={{ display: "flex", flexDirection: "column", gap: 4, padding: "0 12px", flex: 1 }}>
          {NAV_ITEMS.map(item => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  height: 40,
                  padding: "0 16px",
                  borderRadius: 4,
                  fontSize: 15,
                  textDecoration: "none",
                  color: active ? "#D97706" : "#A1A1AA",
                  borderLeft: active ? "3px solid #D97706" : "3px solid transparent",
                  background: active ? "#18181B" : "transparent",
                  transition: "background 150ms, color 150ms",
                }}
                className={!active ? "hover:bg-[#1F1F23] hover:text-[#FAFAFA]" : ""}
              >
                <item.Icon size={18} strokeWidth={1.5} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div style={{ borderTop: "1px solid #27272A", padding: "16px 12px 0" }}>
          <button
            onClick={handleLogout}
            onMouseEnter={() => setLogoutHovered(true)}
            onMouseLeave={() => setLogoutHovered(false)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              width: "100%",
              height: 40,
              padding: "0 16px",
              borderRadius: 4,
              fontSize: 15,
              color: logoutHovered ? "#D97706" : "#A1A1AA",
              background: logoutHovered ? "#1F1F23" : "transparent",
              border: "none",
              cursor: "pointer",
              textAlign: "left",
              transition: "background 150ms, color 150ms",
            }}
          >
            <PrisentIcon size={18} color={logoutHovered ? "#D97706" : "#A1A1AA"} />
            <span>Log out</span>
          </button>
        </div>
      </aside>

      {/* Main dashboard content view */}
      <main style={{ flex: 1, background: "#09090B", color: "#FAFAFA" }}>
        {children}
      </main>
    </div>
  );
}
