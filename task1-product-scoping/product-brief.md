# Product Brief: Marketing Performance Intelligence Tool
**Version:** 1.0 (Scoping Document)  
**Author:** Subiksha GD  
**Date:** May 2026

---

## The Problem Worth Solving

Right now, answering the question — *"How is our marketing performing across channels, and where should we focus?"* — requires someone to manually log into multiple tools, pull numbers, and stitch together a response. That answer looks different every time depending on who runs it, how they interpret the data, and what day it is.

Three concrete failure modes exist today:

1. **Single point of failure** — if the person who usually does this is unavailable, the question sits unanswered.
2. **Inconsistency** — the same question asked twice gets two different answers because there's no standardised methodology.
3. **Latency** — by the time the answer is assembled, the moment it was needed has often passed.

The solution is not to replace the analyst. It's to give every team member — and eventually every client — a shared, reliable source of truth they can access without needing to be the analyst.

---

## Who Is This For?

### Primary User: Internal Analyst / Account Manager

This is the person who currently does the manual work. They know what the data means — they just need a faster, more repeatable way to access it. A successful tool for them means: open it, see the current state, make a decision, close it.

**Not** the primary user in v1: the client. Building for both simultaneously creates a tension — clients need more explanation and context, analysts need speed and precision. Trying to serve both in v1 will result in something that serves neither well. We build for internal first, validate the core loop, and open client access in v2 once we know the data is trustworthy.

---

## What v1 Actually Does

A single-screen dashboard that answers one question cleanly.

**The core interaction:**

> A team member opens the tool, selects a client brand and a time window (last 7 days, last 30 days, this month). They see a snapshot: key metrics per channel, a signal for whether each channel is trending up or down vs the prior period, and one recommended action.

That's it. No deep drill-downs. No custom report builder. No alert configuration. Just: current state → trend → next action.

### What the screen shows

**1. Channel health summary**  
Each active marketing channel (paid search, social, email, organic) shown with:
- Primary KPI for that channel (e.g. ROAS for paid, open rate for email)
- Delta vs prior period (e.g. ▲ 12% vs last 30 days)
- Status indicator: On Track / Needs Attention / Critical

**2. One highlighted recommendation**  
The single most important thing to focus on right now, auto-generated based on which channel has the largest negative delta or is furthest from its target. Written in plain English, not data language.

Example: *"Email open rates have dropped 18% over the last 14 days. Consider reviewing subject line strategy for Brand X."*

**3. Data freshness indicator**  
A visible timestamp showing when data was last synced. This is non-negotiable for trust — users need to know they are looking at fresh data, not a stale snapshot.

---

## What v1 Explicitly Does Not Include

These are not oversights. They are deliberate choices to keep v1 shippable and useful.

| Not in v1 | Why |
|---|---|
| Client-facing interface | Serving internal users first allows us to validate data accuracy before exposing it externally |
| Custom date range picker | Predefined windows (7d, 30d, MTD) cover 80% of use cases; a picker adds UI complexity for marginal gain |
| Drill-down by campaign or ad group | Channel-level is the right resolution for the question being asked; deeper requires more data contracts |
| Automated alerts or notifications | Alert fatigue is real; adding push notifications before the core is trusted creates noise |
| Multi-brand comparison view | Each brand has different KPIs and targets; a comparison view requires normalisation logic that belongs in v2 |
| AI-generated narrative summaries | The recommendation field is the only generative element in v1; full narrative generation adds hallucination risk before trust is established |

---

## Where the Data Comes From

The tool must fit around existing workflows — no new tools, no changed processes.

**Data sources (likely):**
- Google Analytics / GA4 for organic and web traffic metrics
- Google Ads / Meta Ads Manager for paid channel performance
- Email platform (Mailchimp, Klaviyo, or similar) for email metrics

**Ingestion approach for v1:**
Flat-file import or scheduled API pull depending on what connectors are already in place. The key constraint is: the data team should not need to change how they currently export or store data. The tool reads from wherever the data already lives.

**Derived calculations the tool handles:**
- Period-over-period delta computation
- Channel status classification (On Track / Needs Attention / Critical) based on configurable thresholds
- Recommendation generation based on ranking channels by negative delta

These are the only transformations happening inside the tool — everything else is display logic.

---

## What Makes a User Trust This Tool

Trust is earned through three things:

1. **Transparency about data age** — always show when data was last updated. If data is stale (>24 hours for daily-refresh sources), flag it visibly rather than silently showing old numbers.

2. **Consistency** — the same inputs always produce the same output. No "it depends on who runs it." The tool's methodology is documented and stable.

3. **Explainability** — every number shown has a visible definition. The user should never have to guess what "ROAS" or "open rate" means in context, or where it came from.

---

## What a Successful Interaction Looks Like

A team member has a client call in 20 minutes. They open the tool, select the client, glance at the channel summary, note that paid search is "Needs Attention," read the recommendation, and go into the call with a specific, data-backed talking point.

Total time: under 2 minutes.  
No analyst required.  
Answer is the same whether it's Monday morning or Friday afternoon.

---

## Open Questions for v2 Planning

- Should the recommendation be manually overridable (so an analyst can add context before client review)?
- What's the right threshold for "Needs Attention" vs "Critical" — and who owns setting that per brand?
- Once trust is established, is there appetite for a read-only client view that shows only the polished summary?
- Should the tool track when recommendations are acted on, so it can surface whether they worked?

---

## What I Would Revisit With More Time

1. **User interviews** — I've made assumptions about what internal analysts need. A 30-minute conversation with two or three of them would either validate this spec or significantly reshape it.

2. **Data contract clarity** — the biggest unknown is the reliability and format of data from each channel's source. The spec assumes clean, consistent exports; reality is usually messier.

3. **Threshold calibration** — the "Needs Attention / Critical" classification only works if the thresholds are calibrated to each brand's actual performance norms. I'd want to understand how targets are currently tracked before baking in defaults.

4. **The recommendation engine** — in v1, the recommendation is essentially rule-based (worst-performing channel gets flagged). With more time, I'd explore whether a lightweight model trained on historical performance patterns could produce meaningfully better recommendations.