import { useState, useCallback, useRef } from "react";
import { api } from "@/lib/api";
import type { GenerationJob } from "@/lib/types";

export function useGenerationPoll() {
  const [job, setJob] = useState<GenerationJob | null>(null);
  const [polling, setPolling] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const start = useCallback(async () => {
    setPolling(true);
    const { job_id } = await api.triggerGeneration();
    setJob({ job_id, status: "pending", progress_message: "Starting...", post_id: null, error: null });

    intervalRef.current = setInterval(async () => {
      try {
        const result = await api.pollGeneration(job_id);
        setJob(result);
        if (result.status === "done" || result.status === "failed") {
          if (intervalRef.current) clearInterval(intervalRef.current);
          setPolling(false);
        }
      } catch (e) {
        if (intervalRef.current) clearInterval(intervalRef.current);
        setPolling(false);
      }
    }, 2000);
  }, []);

  return { job, polling, start };
}
