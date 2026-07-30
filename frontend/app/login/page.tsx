"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, setToken, ApiError } from "@/lib/api";
import { PrisentIcon } from "@/components/PrisentIcon";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.login(email, password);
      setToken(res.token);
      router.push("/dashboard");
    } catch (err) {
      if (err instanceof ApiError) setError(err.message);
      else setError("System authentication failed");
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
          <h1 className="text-xl font-medium tracking-tight text-textPrimary">Log In</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-textMuted uppercase mb-1">Email address</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary placeholder:text-textMuted focus:border-accent focus:outline-none"
              placeholder="name@company.com"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-textMuted uppercase mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary placeholder:text-textMuted focus:border-accent focus:outline-none"
              placeholder="••••••••"
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
            {loading ? "AUTHENTICATING..." : "Log in"}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-textMuted">
          <Link href="/register" className="text-accent hover:underline">
            Create account
          </Link>
        </div>
      </div>
    </div>
  );
}
