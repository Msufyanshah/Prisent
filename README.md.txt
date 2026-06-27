# AutoPost AI — SpecKit-Plus v2.0

> Spec-driven, AI-native development system.
> Version: 2.0 | Upgraded: June 2026
> Owner: Muhammad Sufyan

---

## What Changed in v2.0

| Problem Identified | Solution Added |
|---|---|
| Testing only at the end → bugs pile up | Inline Task Verification (ITV) after every task |
| Tasks too shallow for AI agents to implement | Deep Task Format with code skeletons, file paths, commands |
| No daily health check | PHR (Progress Health Report) after every task completion |
| Too many tasks per day → overwhelm | Hard cap: max 5 tasks per day |
| No cross-layer integration checks | Integration Checkpoint after every day |
| Hallucinated implementations → silent failures | Mandatory smoke test commands per task |
| No frontend-backend sync verification | Contract Compliance Check before and after each layer |

---

## The 8 Layers

```
01-CONSTITUTION    ← The law. All other layers obey this.
       ↓
02-CONTRACTS       ← Interfaces. What every piece promises to do.
       ↓
03-SPECIFICATION   ← Features. What the system does.
       ↓
04-PLAN            ← Timeline. When we build what.
       ↓
05-TASKS           ← Work. Deep, atomic, testable tasks. Max 5/day.
       ↓
06-IMPLEMENTATION  ← Code. Maps every file to its task.
       ↓
07-DECISIONS       ← Why. Architecture Decision Records.
       ↓
08-PHR             ← Health. Progress report after every task.
```

---

## The Golden Rules

1. **Read Constitution before writing any code.**
2. **Max 5 tasks per day. No exceptions.**
3. **Every task has a smoke test. Run it before marking done.**
4. **Fill a PHR after every completed task, not at end of day.**
5. **Never change a Contract without updating Spec and adding an ADR.**
6. **Frontend and backend must verify against the same Contract shapes.**
7. **If a task takes more than its estimate × 1.5 — stop, log a blocker in PHR.**
8. **BACKLOG.md for new ideas. No scope additions mid-sprint.**

---

## PHR Protocol (New in v2.0)

After every completed task, fill `08-phr/PHR-[TASK-ID].md`:

```
Status: PASS | FAIL | PARTIAL
Smoke test result: PASS | FAIL
Time taken vs estimate: Xh / Xh
Deviations from spec: none | [description]
Blockers for next task: none | [description]
Notes: [anything unusual]
```

If Status = FAIL or PARTIAL → **do not start next task** until resolved.

---

## Stitch Design Integration

Sufyan has built frontend templates in Google Stitch.
Before implementing any frontend task (D11–D15):
1. Reference the Stitch design for that page
2. Match component structure to the design
3. Note any gaps between design and spec in PHR

---

## File Index

| Layer | File | Purpose |
|---|---|---|
| 01 | `01-constitution/CONSTITUTION.md` | Core law, principles, success definition |
| 02 | `02-contracts/CONTRACTS.md` | Agent + API + data contracts |
| 03 | `03-specification/SPEC.md` | Full feature specification |
| 04 | `04-plan/PLAN.md` | Sprint plan, milestones, risk register |
| 05 | `05-tasks/TASKS.md` | Deep task definitions, max 5/day |
| 06 | `06-implementation/IMPL.md` | File map, dev log, code patterns |
| 07 | `07-decisions/DECISIONS.md` | ADRs — why we chose what |
| 08 | `08-phr/PHR-TEMPLATE.md` | PHR template + all reports |
| — | `BACKLOG.md` | Deferred ideas — do not touch until Day 22 |
