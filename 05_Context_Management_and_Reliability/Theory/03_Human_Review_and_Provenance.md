---
tags: [theory, human-review, confidence-calibration, provenance, reliability]
topic: "05 - Context Management & Reliability"
---

# Human Review & Provenance

Two more reliability disciplines round out this domain: knowing when an extraction or claim is trustworthy enough to skip human review, and preserving *where a claim came from* when combining information from multiple sources. Both fail the same way when done carelessly — an aggregate number or a merged summary looks confident while quietly hiding exactly the detail you'd need to catch a mistake.

---

## Aggregate Accuracy Metrics Mask Poor Segment Performance

A structured-extraction system reporting "97% accuracy overall" sounds production-ready. It can still be badly broken on a subset that the aggregate number hides entirely.

> [!warning] The 97% that isn't what it looks like
> If 97% overall accuracy is really 99.5% accuracy on standard invoices (90% of volume) and 70% accuracy on handwritten receipts (10% of volume), the aggregate number is dominated by the easy majority. Automating review based on the headline figure means the worst-performing document type gets the *least* scrutiny — the opposite of where review effort should go.

**Fix:** validate accuracy **by document type and by field**, not just in aggregate, before reducing human review for any segment. A field or document type only earns reduced review once its *own* measured accuracy — not the system's blended average — clears the bar.

---

## Stratified Random Sampling

Even a field/document-type combination with strong measured accuracy can't be assumed safe to fully automate — measured accuracy on a validation set describes the past, not a guarantee about future documents that don't resemble anything in that set.

**Stratified random sampling** — pulling a random sample from within each segment (not just overall) of *high-confidence* extractions on an ongoing basis — serves two purposes at once:

1. **Ongoing error-rate measurement** — confirms the segment's accuracy is holding up in production, not just in the original validation run.
2. **Novel error-pattern detection** — catches new failure modes that wouldn't show up in an aggregate spot-check, because sampling *within* each stratum guarantees coverage of segments a purely random overall sample might under-sample.

> [!tip] Why "high-confidence" extractions specifically
> It's tempting to only sample extractions the model flagged as *uncertain* — but that misses the more dangerous case: an extraction the model was confidently wrong about. Sampling from the high-confidence bucket is what surfaces silent, confidently-wrong errors before they compound.

---

## Field-Level Confidence Calibration

A single per-document confidence score hides which specific fields are reliable. Two extractions can share the same overall confidence while one has a shaky total and a solid customer name, and the other has it reversed.

The more useful signal is **field-level confidence** — the model outputs a confidence per extracted field, not just per document — calibrated against a labeled validation set so that "confidence 0.9" actually corresponds to a measured ~90% accuracy for that specific field and document type, rather than being an uncalibrated raw model output.

```json
{
  "invoice_total": {"value": 1042.50, "confidence": 0.97},
  "vendor_name":   {"value": "Acme Corp", "confidence": 0.99},
  "line_items":    {"value": [...], "confidence": 0.71}
}
```

Calibrated field-level scores are what makes **routing** meaningful: send low-confidence or ambiguous/contradictory-source fields to human review, and let high-confidence, well-calibrated fields pass through automatically — prioritizing scarce reviewer time on the fields that actually need it instead of re-reviewing everything or nothing.

---

## Claim-Source Mappings Preserved Through Synthesis

When multiple subagents each analyze a source and a synthesis step combines their findings into one report, source attribution is exactly the kind of detail summarization quietly drops — a claim survives, but the citation that justified it doesn't.

**Fix:** require each subagent to output a **structured claim-source mapping** — the claim, the source URL or document name, and the relevant excerpt — and require the synthesis step to preserve (not paraphrase away) that mapping when merging findings from multiple subagents.

```json
{
  "claim": "Global smartphone shipments declined 3.2% year-over-year in Q1.",
  "source": "IDC Worldwide Quarterly Mobile Phone Tracker, 2026-04-15",
  "excerpt": "...worldwide smartphone shipments totaled 287.4 million units, down 3.2% YoY..."
}
```

A synthesized report should read as **structured with explicit sections** distinguishing well-established findings (multiple independent sources agree) from contested ones (sources disagree, or only one source claims it) — preserving each source's own characterization and methodology rather than flattening everything into one undifferentiated narrative voice.

### Conflicting Statistics: Annotate, Don't Arbitrarily Pick

Two credible sources reporting different numbers for the same thing is common and should never be silently resolved by the synthesis step picking one and discarding the other.

> [!warning] Don't let synthesis quietly choose a winner
> If Source A says 3.2% decline and Source B says 4.1% decline, a synthesis agent that just picks one (say, the more recent-looking one) is manufacturing false confidence. The correct output **includes both values, explicitly annotated with their sources**, and leaves reconciliation to whoever is positioned to judge — a downstream coordinator, an analyst, or the report's reader — rather than deciding unilaterally at the synthesis step.

```text
Smartphone shipment decline, Q1 2026: reported as 3.2% (IDC) vs. 4.1% (Canalys).
Difference likely attributable to differing OEM shipment-tracking methodology; see excerpts below.
```

### Temporal Data: Dates Prevent False Contradictions

A number reported in January and the same metric reported in June aren't necessarily in conflict — they may simply describe different points in time. Without a **publication or collection date** attached to each structured claim, a synthesis step (or a human reader) has no way to tell a genuine contradiction apart from a temporal difference that looks like one.

> [!example] Why this matters concretely
> "Company X has 450 employees" (sourced from a press release dated 2025-11-01) and "Company X has 510 employees" (sourced from their 2026-06 careers page) aren't contradictory — the company grew. Without both dates attached, a synthesis agent might flag this as a source conflict requiring reconciliation, when it's actually just two accurate snapshots in time.

Requiring subagents to include publication/collection dates in every structured output is what makes correct temporal interpretation possible downstream.

### Rendering Content Types Appropriately

A final synthesis shouldn't force every kind of finding into the same shape. Financial data reads best as a table; a news narrative reads best as prose; a set of technical findings reads best as a structured list. Forcing a uniform format across all content types (e.g., turning tabular financial data into prose, or turning a narrative into a bulleted fragment list) loses the structure that made the original content legible in the first place.

---

## Related Notes

- [[01_Context_Preservation_and_Escalation|Context Preservation & Escalation]]
- [[02_Error_Propagation_and_Codebase_Context|Error Propagation & Codebase Context]]
- [[../../04_Prompt_Engineering_and_Structured_Output/Theory/02_Structured_Output_and_Validation|Structured Output & Validation]]
- [[../../00_Exam_Guide/Exam_Scenarios|Exam Scenarios — Scenario 3: Multi-Agent Research System · Scenario 6: Structured Data Extraction]]

---

[[../_Index|← Back to Context Management & Reliability Index]]
