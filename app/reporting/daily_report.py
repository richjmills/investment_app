from datetime import datetime

def build_decision_summary(signals, risk, allocation, holding_review, strategy_state):
    lines = []
    lines.append("DAILY DECISION SUMMARY")
    lines.append("")

    # --- Market stance ---
    lines.append("Market stance:")
    lines.append(f"→ {signals['action'].upper()} (confidence: {signals['confidence']:.2f})")
    lines.append("")

    # --- Top issues ---
    issues = []

    # Risk issues (priority)
    if risk.get("flags"):
        issues.extend(risk["flags"][:2])

    # Allocation issues
    if allocation.get("flags"):
        issues.extend(allocation["flags"][:1])

    # Regime change
    state = strategy_state.get("pending_regime_review", {})
    if state.get("active"):
        issues.append(f"Regime shift: {state.get('candidate_regime')} (review required)")

    lines.append("Top issues:")
    if issues:
        for i, issue in enumerate(issues[:3], 1):
            lines.append(f"{i}. {issue}")
    else:
        lines.append("None")

    lines.append("")

    # --- Recommended actions ---
    actions = []

    # Hard rules (priority)
    if risk.get("flags"):
        actions.append("Reduce concentration / trim oversized positions")

    if "cash" in str(risk.get("flags", [])):
        actions.append("Raise cash buffer")

    # Soft rules
    if signals["action"] == "de-risk":
        actions.append("Avoid adding new risk")

    if signals["action"] == "risk_on":
        actions.append("Look for selective buying opportunities")

    lines.append("Recommended actions:")
    if actions:
        for action in actions[:3]:
            lines.append(f"→ {action}")
    else:
        lines.append("→ Hold current positioning")

    lines.append("")

    # --- Risk warning ---
    lines.append("Risk warning:")
    if risk.get("risk_level") == "Elevated":
        lines.append("→ Portfolio risk elevated — downside vulnerability")
    else:
        lines.append("→ No major risk warning")

    lines.append("")
    lines.append("=" * 60)
    lines.append("")

    return "\n".join(lines)

def build_daily_report(

    strategy_state: dict,
    themes: dict,
    regime: str,
    signals: dict,
    allocation: dict,
    risk: dict,
    holding_review: dict,
    performance: dict,
    actions: dict
) -> str:

    """Build a simple terminal-friendly daily report."""
    lines = []

    summary = build_decision_summary(
    signals,
    risk,
    allocation,
    holding_review,
    strategy_state
)
    lines.append(summary)

    confirmed_regime = strategy_state.get("current_regime", {}).get("name", "Unknown")
    pending_review = strategy_state.get("pending_regime_review", {})
    performance_band = performance.get("performance_band", "Unknown")

    # --- KEY ISSUES ---
    key_issues = []

    if pending_review.get("active"):
        key_issues.append(
            f"Regime review pending: {confirmed_regime} -> {pending_review.get('candidate_regime')}"
        )

    if risk.get("risk_level") == "Elevated":
        key_issues.append("Portfolio risk elevated")

    if allocation.get("flags"):
        for flag in allocation["flags"][:2]:
            key_issues.append(flag)

    if risk.get("flags"):
        for flag in risk["flags"][:2]:
            if flag not in key_issues:
                key_issues.append(flag)

    if not key_issues:
        key_issues.append("No major issues detected")

    # --- PERFORMANCE WORDING ---
    if performance.get("absolute_return_pct") == 0.0:
        performance_summary = "Early tracking period"
        performance_note = "Baseline established; long-term tracking not yet meaningful"
    else:
        performance_summary = performance_band
        performance_note = ""

    lines.append("=" * 60)
    lines.append("INVESTMENT APP - DAILY REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)

    lines.append("")
    lines.append("KEY ISSUES")
    for issue in key_issues:
        lines.append(f"- {issue}")

    lines.append("")
    lines.append("REGIME")
    lines.append(f"Confirmed: {confirmed_regime}")
    lines.append(f"Suggested: {regime}")
    lines.append(
        f"Signal: {signals.get('action', 'Unknown')} "
        f"(confidence: {signals.get('confidence', 0):.2f})"
    )
    signal_notes = signals.get("notes", [])
    lines.append(f"Signal notes: {', '.join(signal_notes) if signal_notes else 'None'}")

    lines.append("")
    lines.append("THEMES")
    for key, value in themes.items():
        lines.append(f"- {key}: {value}")

    lines.append("")
    lines.append("PERFORMANCE")
    lines.append(f"Current value: {performance.get('current_value')}")
    lines.append(f"Baseline value: {performance.get('baseline_value')}")
    lines.append(f"Return: {performance.get('absolute_return_pct')}%")
    lines.append(f"Performance status: {performance_summary}")
    if performance_note:
        lines.append(f"Note: {performance_note}")

    lines.append("")
    lines.append("ALLOCATION")
    lines.append(f"Current: {allocation.get('current_weights')}")
    lines.append(f"Target: {allocation.get('target_weights')}")
    lines.append(f"Deviation: {allocation.get('deviations')}")
    if allocation.get("flags"):
        lines.append("Flags:")
        for flag in allocation["flags"]:
            lines.append(f"- {flag}")

    lines.append("")
    lines.append("RISK")
    lines.append(f"Risk level: {risk.get('risk_level')}")
    lines.append(
        f"Metrics: cash={risk.get('cash_weight')}%, "
        f"max_single_position={risk.get('max_single_position')}%, "
        f"crypto={risk.get('crypto_weight')}%"
    )
    if risk.get("flags"):
        lines.append("Flags:")
        for flag in risk["flags"]:
            lines.append(f"- {flag}")

    lines.append("")
    lines.append("HOLDING REVIEW")
    for item in holding_review.get("evaluations", []):
        lines.append(
            f"- {item['symbol']}: {item['recommendation']} | "
            f"{item['priority']} | {item['weight_pct']}%"
        )

        hard_notes = []
        soft_notes = []

        for note in item.get("notes", []):
            note_lower = note.lower()
            if (
                "exceeds" in note_lower
                or "limit" in note_lower
                or "cash floor" in note_lower
                or "concentration" in note_lower
            ):
                hard_notes.append(note)
            else:
                soft_notes.append(note)

        if hard_notes:
            lines.append("  HARD:")
            for note in hard_notes:
                lines.append(f"  - {note}")

        if soft_notes:
            lines.append("  SOFT:")
            for note in soft_notes:
                lines.append(f"  - {note}")

    lines.append("")
    lines.append("ACTIONS")
    for recommendation in actions.get("recommendations", []):
        lines.append(f"- {recommendation}")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)