"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { clearToken } from "@/lib/api";
import { PrisentIcon } from "@/components/PrisentIcon";
import { Home, FileText, BarChart3, Settings, Bell, HelpCircle, User, LogOut, PanelLeftClose, Moon, Sun, Sunset } from "lucide-react";

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
  const [collapsed, setCollapsed] = useState(false);
  const [theme, setTheme] = useState<"dark" | "light" | "sunny">("dark");

  useEffect(() => {
    const savedTheme = localStorage.getItem("prisent_theme") as "dark" | "light" | "sunny";
    if (savedTheme) {
      setTheme(savedTheme);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("prisent_theme", theme);
    const root = document.documentElement;
    if (theme === "dark") {
      root.style.setProperty("--color-background", "#09090B");
      root.style.setProperty("--color-surface", "#18181B");
      root.style.setProperty("--color-border-muted", "#27272A");
      root.style.setProperty("--color-text-primary", "#FAFAFA");
      root.style.setProperty("--color-text-muted", "#A1A1AA");
      root.style.setProperty("--sidebar-bg", "#18181B");
      root.style.setProperty("--sidebar-border", "#27272A");
      root.style.setProperty("--text-main", "#FAFAFA");
    } else if (theme === "light") {
      root.style.setProperty("--color-background", "#F4F4F5");
      root.style.setProperty("--color-surface", "#FFFFFF");
      root.style.setProperty("--color-border-muted", "#E4E4E7");
      root.style.setProperty("--color-text-primary", "#09090B");
      root.style.setProperty("--color-text-muted", "#71717A");
      root.style.setProperty("--sidebar-bg", "#FFFFFF");
      root.style.setProperty("--sidebar-border", "#E4E4E7");
      root.style.setProperty("--text-main", "#09090B");
    } else if (theme === "sunny") {
      root.style.setProperty("--color-background", "#FEF3C7");
      root.style.setProperty("--color-surface", "#FFFBEB");
      root.style.setProperty("--color-border-muted", "#FDE68A");
      root.style.setProperty("--color-text-primary", "#78350F");
      root.style.setProperty("--color-text-muted", "#B45309");
      root.style.setProperty("--sidebar-bg", "#FFFBEB");
      root.style.setProperty("--sidebar-border", "#FDE68A");
      root.style.setProperty("--text-main", "#78350F");
    }
  }, [theme]);

  useEffect(() => {
    const token = localStorage.getItem("prisent_token");
    if (!token) router.push("/login");
  }, [router]);

  function handleLogout() {
    clearToken();
    router.push("/login");
  }

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "var(--color-background)" }}>
      {/* Sidebar navigation panel - Dynamic Width */}
      <aside
        style={{
          width: collapsed ? 64 : 240,
          flexShrink: 0,
          background: "var(--sidebar-bg)",
          borderRight: "1px solid var(--sidebar-border)",
          display: "flex",
          flexDirection: "column",
          padding: "24px 0",
          transition: "width 200ms cubic-bezier(0.4, 0, 0.2, 1)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: collapsed ? "column" : "row",
            gap: 12,
            justifyContent: collapsed ? "center" : "space-between",
            alignItems: "center",
            padding: "0 16px 24px",
          }}
        >
          {/* Prisent "P" icon glyph */}
          <PrisentIcon size={24} color="#FAFAFA" />
          <button
            onClick={() => setCollapsed(!collapsed)}
            style={{
              background: "none",
              border: "none",
              color: "var(--color-text-muted)",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: 6,
              borderRadius: 4,
            }}
            className="hover:bg-surface hover:text-text-primary transition-colors"
          >
            <PanelLeftClose
              size={20}
              strokeWidth={2}
              style={{
                transform: collapsed ? "rotate(180deg)" : "none",
                transition: "transform 200ms",
              }}
            />
          </button>
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
                  justifyContent: collapsed ? "center" : "flex-start",
                  gap: collapsed ? 0 : 12,
                  height: 40,
                  padding: collapsed ? "0" : "0 16px",
                  borderRadius: 4,
                  fontSize: 16,
                  fontWeight: active ? 600 : 500,
                  textDecoration: "none",
                  color: active ? "#D97706" : "var(--color-text-muted)",
                  borderLeft: !collapsed && active ? "3px solid #D97706" : "3px solid transparent",
                  background: active ? "var(--color-surface)" : "transparent",
                  transition: "background 150ms, color 150ms",
                }}
                className={!active ? "hover:bg-surface hover:text-text-primary" : ""}
              >
                <item.Icon size={20} strokeWidth={2} />
                {!collapsed && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        <div style={{ borderTop: "1px solid var(--color-border-muted)", padding: "16px 12px 0" }}>
          <button
            onClick={handleLogout}
            onMouseEnter={() => setLogoutHovered(true)}
            onMouseLeave={() => setLogoutHovered(false)}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: collapsed ? "center" : "flex-start",
              gap: collapsed ? 0 : 12,
              width: "100%",
              height: 40,
              padding: collapsed ? "0" : "0 16px",
              borderRadius: 4,
              fontSize: 16,
              fontWeight: 500,
              color: logoutHovered ? "var(--color-text-primary)" : "var(--color-text-muted)",
              background: logoutHovered ? "var(--color-surface)" : "transparent",
              border: "none",
              cursor: "pointer",
              textAlign: "left",
              transition: "background 150ms, color 150ms",
            }}
          >
            <LogOut size={20} strokeWidth={2} />
            {!collapsed && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main dashboard content view */}
      <main style={{ flex: 1, display: "flex", flexDirection: "column", background: "var(--color-background)", color: "var(--text-main)" }}>
        {/* Top Navbar */}
        <header
          style={{
            height: 56,
            borderBottom: "1px solid var(--color-border-muted)",
            display: "flex",
            alignItems: "center",
            justifyContent: "flex-end",
            padding: "0 24px",
            gap: 16,
            background: "var(--color-background)",
          }}
        >
          {/* Theme Mode Toggle Button */}
          <button
            onClick={() => {
              setTheme(prev => (prev === "dark" ? "light" : prev === "light" ? "sunny" : "dark"));
            }}
            style={{
              background: "none",
              border: "none",
              color: "var(--color-text-muted)",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: 6,
              borderRadius: 4,
            }}
            className="hover:bg-surface hover:text-text-primary transition-colors"
            title={`Switch to ${theme === "dark" ? "Light" : theme === "light" ? "Sunny" : "Dark"} mode`}
          >
            {theme === "dark" && <Moon size={20} strokeWidth={2} />}
            {theme === "light" && <Sun size={20} strokeWidth={2} />}
            {theme === "sunny" && <Sunset size={20} strokeWidth={2} />}
          </button>

          <button
            style={{
              background: "none",
              border: "none",
              color: "var(--color-text-muted)",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: 6,
              borderRadius: 4,
            }}
            className="hover:bg-surface hover:text-text-primary transition-colors"
          >
            <Bell size={20} strokeWidth={2} />
          </button>
          <button
            style={{
              background: "none",
              border: "none",
              color: "var(--color-text-muted)",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: 6,
              borderRadius: 4,
            }}
            className="hover:bg-surface hover:text-text-primary transition-colors"
          >
            <HelpCircle size={20} strokeWidth={2} />
          </button>
          <div
            style={{
              width: 32,
              height: 32,
              borderRadius: "50%",
              background: "var(--color-border-muted)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "var(--color-text-primary)",
              cursor: "pointer",
            }}
            className="hover:bg-surface hover:text-text-primary transition-colors"
          >
            <User size={16} strokeWidth={2} />
          </div>
        </header>

        <div style={{ flex: 1, overflowY: "auto" }}>
          {children}
        </div>
      </main>
    </div>
  );
}
