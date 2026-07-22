"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, setToken, ApiError } from "@/lib/api";
import { PrisentIcon } from "@/components/PrisentIcon";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: "", password: "", name: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.register(form.email, form.password, form.name);
      setToken(res.token);
      router.push("/dashboard");
    } catch (err) {
      if (err instanceof ApiError) setError(err.message);
      else setError("Workspace registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="w-full max-w-[380px] rounded-container border border-borderMuted bg-surface p-6">
        <div className="mb-6 flex flex-col items-center">
          <div className="mb-3">
            <PrisentIcon size={32} color="#D97706" />
          </div>
          <div className="font-mono text-xs tracking-[0.2em] text-accent uppercase mb-2">Prisent</div>
          <h1 className="text-xl font-medium tracking-tight text-textPrimary">Create account</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-textMuted uppercase mb-1">Full name</label>
            <input
              type="text"
              value={form.name}
              onChange={e => setForm({ ...form, name: e.target.value })}
              className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary placeholder:text-textMuted focus:border-accent focus:outline-none"
              placeholder="Jane Doe"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-textMuted uppercase mb-1">Email address</label>
            <input
              type="email"
              value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })}
              className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary placeholder:text-textMuted focus:border-accent focus:outline-none"
              placeholder="name@company.com"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-textMuted uppercase mb-1">Password</label>
            <input
              type="password"
              value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })}
              className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary placeholder:text-textMuted focus:border-accent focus:outline-none"
              placeholder="••••••••"
              minLength={8}
              required
            />
          </div>

          {error && (
            <div className="text-xs text-danger border border-danger/20 bg-danger/5 p-2 rounded-interactive font-mono">
              [ERR] {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-interactive bg-accent py-2 text-sm font-medium text-background hover:bg-accent-hover transition-colors disabled:opacity-40"
          >
            {loading ? "CREATING..." : "Create account"}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-textMuted">
          <Link href="/login" className="text-accent hover:underline">
            Back to log in
          </Link>
        </div>
      </div>
    </div>
  );
}
