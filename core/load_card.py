"""
Loads a SignCoreCard from a sign-card markdown file.

load_card(path) -> SignCoreCard

Uses tree_parser (an indent-based structural parser), not regexes
tied to a specific card format — robust to per-card format drift
(confirmed in practice: SKULL keeps SEQUENCE_CANDIDATES directly under
SEQUENCE_LAYER_BOUNDARY with no intermediate node, unlike DOT and
SOLIDUS; SOLIDUS epochs have no NAME field while SKULL's do).
"""

from __future__ import annotations

import re

from sign_core_card import (
    SignCoreCard, SafeCase, RiskCase, Confusable, SignRelation, ContradictionGuard,
    SequenceCandidate, EpochDefinition, RiskLevel, Zone,
)
from tree_parser import parse_indented_tree, Node


def _parse_risk(raw: str):
    """Returns a RiskLevel if raw is an exact enum value or starts
    with one (e.g. 'LOW / CONTEXT_DEPENDENT' from SKULL.SAFE_CASE_004
    -> RiskLevel.LOW).

    If the first token is not a RiskLevel member (e.g.
    SEQUENCE_CANDIDATE values such as 'intensity-dependent',
    'spam-like', 'combined idiom', 'epoch_mismatch', or
    'seasonal_context'), the original string is returned as is.

    ENUM_GUARD in sequence_module.py must explicitly check this
    distinction and never compare such string values with the enum."""

    raw = raw.strip()
    if not raw:
        return RiskLevel.NONE
    first_token = re.split(r"[\s/(]", raw, maxsplit=1)[0]
    if RiskLevel.is_enum_value(first_token):
        return RiskLevel(first_token)
    return raw  # non-enum value — kept as a string


def _parse_zone(raw: str) -> Zone:
    raw = raw.strip().upper()
    return {
        "ZONE_1": Zone.ZONE_1,
        "ZONE_2": Zone.ZONE_2,
        "ZONE_3": Zone.ZONE_3,
    }[raw]


def _extract_safe_cases(root: Node) -> list:
    section = root.child("SAFE_CASES")
    if not section:
        return []
    out = []
    for sc in section.children_with_prefix("SAFE_CASE_"):
        out.append(SafeCase(
            case_id=sc.key,
            input_example=sc.child("INPUT").text() if sc.child("INPUT") else "",
            context=sc.child("CONTEXT").text() if sc.child("CONTEXT") else "",
            risk=_parse_risk(sc.child("RISK").text() if sc.child("RISK") else "NONE"),
            guard=sc.child("GUARD").text() if sc.child("GUARD") else "",
        ))
    return out


def _extract_risk_cases(root: Node) -> list:
    section = root.child("RISK_CASES")
    if not section:
        return []
    out = []
    for rc in section.children_with_prefix("RISK_CASE_"):
        out.append(RiskCase(
            case_id=rc.key,
            name=rc.child("NAME").text() if rc.child("NAME") else "",
            input_example=rc.child("INPUT").text() if rc.child("INPUT") else "",
            context=rc.child("CONTEXT").text() if rc.child("CONTEXT") else "",
            risk=_parse_risk(rc.child("RISK").text() if rc.child("RISK") else "NONE"),
            attack=rc.child("ATTACK").text() if rc.child("ATTACK") else "",
            guard=rc.child("GUARD").text() if rc.child("GUARD") else "",
        ))
    return out


def _extract_confusables(root: Node) -> list:
    section = root.child("CONFUSABLES")
    if not section:
        return []
    out = []
    for cf in section.children_with_prefix("CONFUSABLE_"):
        out.append(Confusable(
            confusable_id=cf.key,
            visible_form=cf.child("VISIBLE_FORM").text() if cf.child("VISIBLE_FORM") else "",
            codepoint=cf.child("CODEPOINT").text() if cf.child("CODEPOINT") else "",
            name=cf.child("NAME").text() if cf.child("NAME") else "",
            risk=_parse_risk(cf.child("RISK").text() if cf.child("RISK") else "NONE"),
            rule=cf.child("RULE").text() if cf.child("RULE") else "",
        ))
    return out


def _extract_relations(root: Node) -> list:
    """SIGN_RELATIONS block — runtime SOURCE OF TRUTH for relations
    (relation axis, D-REL-2). Absence of the block = empty list
    (legacy/standalone sign, D1 via non-intervention).
    CONFUSABLES is NOT read here — it is documentation/provenance."""
    section = root.child("SIGN_RELATIONS")
    if not section:
        return []
    _VALID_SCOPE = {"URL", "HOST", "PORT", "PATH", "EMAIL", "IDENTIFIER",
                    "IDN", "CODE", "FREE_TEXT", "ANY"}
    _VALID_TYPE = {"CONFUSABLE_OF", "NFKC_MAPS_TO", "VISUAL_MIMIC_OF"}
    out = []
    for rel in section.children_with_prefix("RELATION_"):
        scope_raw = rel.child("CONTEXT_SCOPE").text() if rel.child("CONTEXT_SCOPE") else ""
        scope = [s.strip() for s in scope_raw.replace(",", " ").split() if s.strip()]
        rtype = rel.child("RELATION_TYPE").text() if rel.child("RELATION_TYPE") else ""
        reffect = (rel.child("RUNTIME_EFFECT").text()
                   if rel.child("RUNTIME_EFFECT") else "RELATION_ONLY")
        active_raw = (rel.child("IS_ACTIVE").text() if rel.child("IS_ACTIVE") else "")
        is_active = active_raw.strip().upper() not in ("FALSE", "NO", "0", "OFF")
        # Edge field validation — bad values are flagged but do NOT
        # break loading (the card stays readable; warning visible on
        # inspection). Invariant RUNTIME_EFFECT=RELATION_ONLY.
        warnings = []
        if not scope:
            warnings.append("RELATION_WITHOUT_SCOPE: edge has no CONTEXT_SCOPE — will not match any context (except ANY) and silently yields no verdict; check whether scope was omitted")
        bad_scope = [s for s in scope if s not in _VALID_SCOPE]
        if bad_scope:
            warnings.append(f"UNKNOWN_CONTEXT_SCOPE: {bad_scope}")
        if rtype and rtype not in _VALID_TYPE:
            warnings.append(f"UNKNOWN_RELATION_TYPE: {rtype!r}")
        if reffect != "RELATION_ONLY":
            warnings.append(f"RUNTIME_EFFECT_MUST_BE_RELATION_ONLY: got {reffect!r}")
        out.append(SignRelation(
            relation_id=rel.key,
            relation_type=rtype,
            target=rel.child("TARGET").text() if rel.child("TARGET") else "",
            context_scope=scope,
            verification_status=(rel.child("VERIFICATION_STATUS").text()
                                 if rel.child("VERIFICATION_STATUS") else ""),
            runtime_effect=reffect,
            is_active=is_active,
            validation_warnings=warnings,
        ))
    return out


def _extract_contradiction_guards(root: Node) -> list:
    section = root.child("CONTRADICTION_GUARDS")
    if not section:
        return []
    out = []
    for cg in section.children_with_prefix("CG"):
        out.append(ContradictionGuard(
            guard_id=cg.key,
            trigger=cg.child("TRIGGER").text() if cg.child("TRIGGER") else "",
            response=cg.child("RESPONSE").text() if cg.child("RESPONSE") else "",
            rule=cg.child("RULE").text() if cg.child("RULE") else "",
        ))
    return out


def _extract_sequence_candidates(root: Node) -> list:
    seq = root.child("SEQUENCE_LAYER_BOUNDARY")
    if not seq:
        return []
    # DOT/SOLIDUS: nested SEQUENCE_CANDIDATES node
    sc_container = seq.child("SEQUENCE_CANDIDATES")
    sc_nodes = sc_container.children_with_prefix("SC") if sc_container else []
    # SKULL: SC nodes directly under SEQUENCE_LAYER_BOUNDARY (format
    # drift, confirmed by the structural parser — see module docstring)
    if not sc_nodes:
        sc_nodes = seq.children_with_prefix("SC")

    out = []
    for sc in sc_nodes:
        risk_raw = sc.child("RISK_LEVEL").text() if sc.child("RISK_LEVEL") else "NONE"
        out.append(SequenceCandidate(
            sc_id=sc.key,
            sequence=_strip_quotes(sc.child("SEQUENCE").text() if sc.child("SEQUENCE") else ""),
            name=sc.child("NAME").text() if sc.child("NAME") else "",
            risk_level=_parse_risk(risk_raw),
            possible_contexts=(
                sc.child("POSSIBLE_CONTEXTS").text() if sc.child("POSSIBLE_CONTEXTS")
                else (sc.child("RULE").text() if sc.child("RULE") else "")
            ),
            scope=sc.child("SCOPE").text() if sc.child("SCOPE") else "",
        ))
    return out


def _strip_quotes(s: str) -> str:
    """The SEQUENCE field in cards is written as '"../" (comment)' —
    extract only the literal quoted string."""
    m = re.match(r'^"([^"]*)"', s.strip())
    return m.group(1) if m else s.strip()


def _extract_epochs(root: Node) -> list:
    cap = root.child("CAPTURE_HISTORY")
    if not cap:
        return []
    out = []
    for ep in cap.children_with_prefix("EPOCH_"):
        out.append(EpochDefinition(
            epoch_id=ep.key,
            name=ep.child("NAME").text() if ep.child("NAME") else "",
            date_range=ep.child("DATE_RANGE").text() if ep.child("DATE_RANGE") else "",
            substrate=ep.child("SUBSTRATE").text() if ep.child("SUBSTRATE") else "",
            function=ep.child("FUNCTION").text() if ep.child("FUNCTION") else "",
            status=ep.child("STATUS").text() if ep.child("STATUS") else "",
        ))
    return out


def load_card(path: str) -> SignCoreCard:
    text = open(path, encoding="utf-8").read()
    root = parse_indented_tree(text)

    zone = _parse_zone(root.child("ZONE").text())
    active_epoch_type = None
    if zone == Zone.ZONE_3:
        active_epoch_type = (
            root.child("ACTIVE_EPOCH_TYPE").text()
            if root.child("ACTIVE_EPOCH_TYPE") else None
        )
    elif zone == Zone.ZONE_2:
        active_epoch_type = (
            root.child("EPOCH_TRACKER").text()
            if root.child("EPOCH_TRACKER") else None
        )

    return SignCoreCard(
        card_uid=root.child("CARD_UID").text() if root.child("CARD_UID") else "",
        codepoint=root.child("CODEPOINT").text(),
        visible_form=root.child("VISIBLE_FORM").text(),
        unicode_name=root.child("UNICODE_NAME").text() if root.child("UNICODE_NAME") else "",
        zone=zone,
        document_status=root.child("DOCUMENT_STATUS").text(),
        base_mode=root.child("BASE_MODE").text() if root.child("BASE_MODE") else "",
        base_mode_formula=(
            root.child("BASE_MODE_FORMULA").text()
            if root.child("BASE_MODE_FORMULA") else ""
        ),
        safe_cases=_extract_safe_cases(root),
        risk_cases=_extract_risk_cases(root),
        confusables=_extract_confusables(root),
        relations=_extract_relations(root),
        contradiction_guards=_extract_contradiction_guards(root),
        sequence_candidates=_extract_sequence_candidates(root),
        epochs=_extract_epochs(root),
        active_epoch_type=active_epoch_type,
    )
