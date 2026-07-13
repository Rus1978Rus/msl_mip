"""
MODULE_TEMPLATE_SINGLE_SIGN engine — STAGE_1-8 implementation of
MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1 (with
PATCH_22 — ZONE_1 must check RISK_CASES, and PATCH_23 —
SIGN_OFFSET_START/END in OUTPUT_STATUS).

This module holds NO sign-specific logic — that lives in matchers/.
Only the structural pipeline common to any sign of any ZONE.
"""

from __future__ import annotations

from sign_core_card import SignCoreCard, RiskLevel, Zone
from output_status import OutputStatus, ModuleError
from matchers import dot_matcher, solidus_matcher, skull_matcher

import importlib.util as _importlib_util

_skull_crossbones_path = _importlib_util.find_spec("matchers.skull_crossbones_matcher")
if _skull_crossbones_path is not None:
    # the file exists — import without try/except: if its own import
    # is broken or another error occurs, it must fail LOUDLY, not
    # masquerade as "file missing" (found in code review, 2026-06-29:
    # a broad except ImportError would hide real bugs inside a new
    # matcher)
    from matchers import skull_crossbones_matcher
    _HAS_SKULL_CROSSBONES = True
else:
    # the file is really missing — a legitimate, deliberate fallback
    _HAS_SKULL_CROSSBONES = False

_at_path = _importlib_util.find_spec("matchers.at_matcher")
if _at_path is not None:
    from matchers import at_matcher
    _HAS_AT = True
else:
    _HAS_AT = False

# FIXED (2026-06-29, adding the second ZONE_3 sign ☠️):
# dispatch used to go BY ZONE (ZONE_3 -> skull_matcher only,
# hard-coded). That worked while ZONE_3 had one sign. With
# ☠️ (also ZONE_3, also epochal) a hard if/elif by zone cannot
# choose between two matchers of one zone. Dispatch is now
# by CODEPOINT via an explicit registry. has_epoch=True means the
# matcher takes metadata and returns a 4-tuple (like skull_matcher),
# False — a plain 3-tuple (like dot/solidus_matcher). A new sign
# is added with one registry line, no changes to the logic below.
_MATCHER_REGISTRY = {
    "U+002E": (dot_matcher, False),
    "U+002F": (solidus_matcher, False),
    "U+1F480": (skull_matcher, True),
}
if _HAS_SKULL_CROSSBONES:
    _MATCHER_REGISTRY["U+2620"] = (skull_crossbones_matcher, True)
if _HAS_AT:
    _MATCHER_REGISTRY["U+0040"] = (at_matcher, False)


# STAGE_1: card statuses allowed for loading.
# WORKINGLY_CLOSED / ARTIFACT_CONFIRMED passed STRUCTURAL_PREFLIGHT_
# PASS + CONVEYOR_REVIEW_PASS (at least several independent
# reviewers) and AUTHOR_DECISION. WORKING_DRAFT did NOT pass the
# conveyor; allowed to load ONLY with an explicit loud warning (see
# below) — the system must not silently confuse an unreviewed draft
# with a conveyor-confirmed card. FIXED (2026-06-29): before that
# the coordinator assigned WORKINGLY_CLOSED to cards without an
# actual conveyor run, just so the card would technically load —
# a violation of AUTHOR_DECISION_STATUS_AUTHORITY.
_VALID_STATUSES = {"WORKINGLY_CLOSED", "ARTIFACT_CONFIRMED"}
_DRAFT_STATUSES = {"WORKING_DRAFT"}

def _find_case(card: SignCoreCard, case_id: str):
    """Finds a SAFE_CASE or RISK_CASE by id in the card."""
    for c in card.safe_cases:
        if c.case_id == case_id:
            return c
    for c in card.risk_cases:
        if c.case_id == case_id:
            return c
    return None


def _guards_for_risk_ids(card: SignCoreCard, risk_ids: list) -> list:
    """STAGE_4: GUARD_EVALUATION — which CONTRADICTION_GUARDS are
    logically tied to the fired RISK_CASEs (via the risk_case GUARD
    text matched against the guard RESPONSE)."""
    guards_triggered = []
    for rid in risk_ids:
        rc = _find_case(card, rid)
        if rc is None or not getattr(rc, "guard", ""):
            continue
        for g in card.contradiction_guards:
            if g.response and g.response in rc.guard or rc.guard in (g.response or ""):
                if g.guard_id not in guards_triggered:
                    guards_triggered.append(g.guard_id)
    return guards_triggered


def _risk_level_for_ids(card: SignCoreCard, risk_ids: list) -> RiskLevel:
    levels = []
    for rid in risk_ids:
        rc = _find_case(card, rid)
        if rc is not None and RiskLevel.is_enum_value(rc.risk):
            levels.append(rc.risk if isinstance(rc.risk, RiskLevel) else RiskLevel(rc.risk))
    return RiskLevel.max(*levels) if levels else RiskLevel.NONE


def process_sign(card: SignCoreCard, text: str, offset: int,
                  metadata: dict = None) -> OutputStatus:
    """The whole STAGE_1-8. text[offset] must match the card
    card.visible_form (STAGE_2 CONFUSABLE_CHECK)."""

    # --- STAGE_1: CARD_LOADING ---
    draft_warning = None
    if card.document_status in _DRAFT_STATUSES:
        draft_warning = (
            f"CARD_NOT_CONVEYOR_REVIEWED: {card.card_uid or card.codepoint} "
            f"has WORKING_DRAFT status — did not pass STRUCTURAL_PREFLIGHT_PASS/"
            f"CONVEYOR_REVIEW_PASS. The result for this sign MUST NOT "
            f"be considered reliable."
        )
        print(f"[CARD_WARNING] {draft_warning}")
    elif card.document_status not in _VALID_STATUSES:
        raise ModuleError("CARD_INVALID",
                           f"DOCUMENT_STATUS={card.document_status} is not allowed")

    # --- STAGE_2: ZONE_DETECTION + CONFUSABLE_CHECK ---
    if offset < 0 or offset >= len(text):
        raise ModuleError("CONTEXT_INSUFFICIENT", "offset outside the text")
    if text[offset] != card.visible_form:
        raise ModuleError("CONFUSABLE_DETECTED_REJECTED",
                           f"text[{offset}]={text[offset]!r} != {card.visible_form!r}")

    ambiguity = False
    active_epoch = "NOT_APPLICABLE"

    # --- STAGE_3: dispatch by CODEPOINT (not by ZONE) ---
    entry = _MATCHER_REGISTRY.get(card.codepoint)
    if entry is None:
        # Relation axis (D-REL-1/4/5): the sign has no own matcher.
        # If the card has relations, it is a mask sign. single-sign
        # does NOT decide risk: it emits risk=NONE + RELATION CANDIDATES,
        # the verdict is the sequence layer's job (RELATION_FOUND !=
        # THREAT). If there are no relations, the sign is unknown to the
        # system, prior behaviour (error).
        if card.relations:
            # Mask sign: a card with relations. Even if ALL edges are
            # disabled (is_active=False) it is a known mask with no
            # active relations, NOT an unknown sign. Passes silently:
            # risk=NONE. Candidates carry ALL edges with the is_active
            # flag (disabled ones for debug/audit; the sequence layer
            # IGNORES is_active=False edges when deciding the verdict).
            # Level 3 (Z3-02): a CONTRACT-INVALID edge (bad type/kind, canon
            # mismatch) is neither silently activated nor silently dropped —
            # it is EXCLUDED from the runtime and SURFACED as a warning.
            active_relations = [r for r in card.relations
                                if r.is_active and not r.invalid]
            relation_candidates = [
                {
                    "relation_id": r.relation_id,
                    "relation_type": r.relation_type,
                    "target": r.target,
                    "target_kind": r.target_kind,   # D-INV-3: carried, not dropped at the seam
                    "context_scope": list(r.context_scope),
                    "verification_status": r.verification_status,
                    "runtime_effect": r.runtime_effect,
                    "is_active": r.is_active,   # sequence ignores False when deciding
                    "invalid": r.invalid,       # Level 3: excluded from active, surfaced
                    "at_offset": offset,
                    "visible_form": card.visible_form,
                    "canon_hypothesis": None,   # channel for the canon probe (D-REL-5); filled in the sequence layer where context exists. The fragile canon matcher is not called blindly.
                }
                for r in card.relations
            ]
            mask_warnings = [draft_warning] if draft_warning else []
            for r in card.relations:
                if r.invalid:
                    mask_warnings.append(
                        f"INVALID_EDGE_NOT_ACTIVATED: {r.relation_id} "
                        f"({r.relation_type or 'no-type'}) — {'; '.join(r.validation_warnings)}")
            if not active_relations:
                # No valid+active edge — the mask is silent. Not a risk,
                # but a suspicious config state: a soft trace for audit
                # (risk stays NONE, no candidates for the verdict).
                mask_warnings.append("ALL_RELATIONS_INACTIVE_OR_INVALID")
            return OutputStatus(
                sign_codepoint=card.codepoint,
                card_version=card.card_uid,
                active_epoch="NOT_APPLICABLE",
                interpretation="relation_candidate",   # NOT a verdict
                risk_level=RiskLevel.NONE,              # D-REL-5: mask in single-sign = NONE
                risk_cases_triggered=[],
                guards_triggered=[],
                effect_fields_status="VALID",
                sign_offset_start=offset,
                sign_offset_end=offset + 1,
                output_warnings=mask_warnings,
                relation_candidates=relation_candidates,
                # Barrier N3 (a technical guarantee, not a comment):
                # the sequence layer takes ONLY this list. Disabled/invalid
                # edges physically never reach it -> cannot leak into the
                # verdict. Full relation_candidates stays for debugging.
                active_relation_candidates=[
                    c for c in relation_candidates
                    if c["is_active"] and not c["invalid"]
                ],
            )
        raise ModuleError("MATCHER_NOT_FOUND",
                           f"No registered matcher for {card.codepoint}")
    matcher, has_epoch = entry

    if has_epoch:
        safe_ids, risk_ids, active_epoch, interp = matcher.match(text, offset, metadata)
    else:
        safe_ids, risk_ids, interp = matcher.match(text, offset)
        # the ambiguity flag is specific to SOLIDUS.RISK_CASE_008 —
        # stays a targeted check, not a general ZONE_2 rule
        if card.zone == Zone.ZONE_2 and "RISK_CASE_008" in risk_ids:
            ambiguity = True

    # --- STAGE_4: GUARD_EVALUATION ---
    guards_triggered = _guards_for_risk_ids(card, risk_ids)

    # --- STAGE_5: RISK_ASSESSMENT ---
    risk_level = _risk_level_for_ids(card, risk_ids)

    # --- STAGE_6: EFFECT_VALIDATION ---
    # all three cards have EFFECT_FIELDS_ALL_NONE: YES / CLOSED_SCHEMA: YES
    effect_status = "VALID"

    # --- STAGE_7: OUTPUT_ASSEMBLY ---
    out = OutputStatus(
        sign_codepoint=card.codepoint,
        card_version=card.card_uid,
        active_epoch=active_epoch,
        interpretation=interp,
        risk_level=risk_level,
        risk_cases_triggered=risk_ids,
        guards_triggered=guards_triggered,
        ambiguity_flag=ambiguity,
        effect_fields_status=effect_status,
        sign_offset_start=offset,
        sign_offset_end=offset + 1,
        output_warnings=[draft_warning] if draft_warning else [],
    )

    # --- STAGE_8: CLEANUP --- (stateless, no real cleanup needed)
    return out
