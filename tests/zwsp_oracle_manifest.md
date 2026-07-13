ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

# ZWSP TIER_2 ORACLE MANIFEST (v0_1)

Независимый третий эталон, написан ДО прогона. Для каждого кейса — ожидаемый
кортеж, закреплённый по Unicode-свойству/структуре, НЕ выведенный ни из BY_CODE,
ни из BY_SPEC. Защита от «обе ноги ошиблись одинаково».

ACCEPTABLE-множества: измеренное значение обязано попасть внутрь. `-` = вердикта
по ребру ZWSP не ожидается. witness — точное множество кодпоинтов.

| CASE | CLASS | INPUT (codepoints) | EXP_CONTEXT | EXP_RISK | EXP_VERDICT | EXP_WITNESS | FORBIDDEN | BASIS |
|---|---|---|---|---|---|---|---|---|
| R1 | registrar | `goog<U+2800>le.com` | - | - | pass | U+2800 | — | U+2800 BRAILLE PATTERN BLANK (cat So). Renders empty; OUTSIDE Cf/Zs. A witness system should surface it (explicit exception) as UNVERIFIABLE. |
| R2 | registrar | `paypal<U+00A0>.com` | - | - | pass | U+00A0 | — | U+00A0 NO-BREAK SPACE (cat Zs). Invisible-width, evasion-capable. |
| R3 | registrar | `admin<U+202F>panel` | - | - | pass | U+202F | — | U+202F NARROW NO-BREAK SPACE (cat Zs). Distinct codepoint, not R2. |
| R4 | registrar | `line1<U+2028>line2` | - | - | pass | U+2028 | — | U+2028 LINE SEPARATOR (cat Zl). |
| R5 | registrar | `para<U+2029>break` | - | - | pass | U+2029 | — | U+2029 PARAGRAPH SEPARATOR (cat Zp). |
| R6 | registrar | `text<U+200B>here` | BYTE_EXACT_TOKEN | MEDIUM | queue_for_review | — | — | ZWSP is CARDED -> NO witness; but the card verdict must NOT be lost. 'texthere' is a no-space word to exact-compare -> BYTE_EXACT_TOKEN/MEDIUM. |
| P1 | positions | `<U+200B>paypal.com` | BYTE_EXACT_TOKEN | MEDIUM | queue_for_review | — | risk∉HIGH; verdict∉hold_pending_review | LEADING hidden padding. U+200B is NOT White_Space (trim won't remove). Domain 'paypal.com' is intact after the pad -> NOT a label break -> MEDIUM, not HOST/HIGH. |
| P2 | positions | `paypal.com<U+200B>` | BYTE_EXACT_TOKEN,PATH | MEDIUM | queue_for_review | — | risk∉HIGH; verdict∉hold_pending_review | TRAILING hidden padding. Domain intact -> not a label break -> MEDIUM. |
| P4 | positions | `paypal.com<U+200B>/path` | BYTE_EXACT_TOKEN,PATH | MEDIUM | queue_for_review | — | ctx∉HOST; risk∉HIGH; verdict∉hold_pending_review | ZWSP AFTER a whole domain, before '/'. Does NOT break the label. FORBIDDEN HOST/HIGH/HOLD. |
| P5 | positions | `docs.example.com/guide/very-long<U+200B>-section` | PATH | MEDIUM | queue_for_review | — | ctx∉HOST; risk∉HIGH; verdict∉hold_pending_review | R8/deep-path: schemeless domain + ZWSP DEEP in path. ZWSP is in the path, not the host -> PATH/MEDIUM. FORBIDDEN HOST/HIGH/HOLD. |
| K1 | combo | `goog<U+200B><U+200D>le.com` | HOST | HIGH | hold_pending_review | U+200D | — | ZWSP breaks the host label -> HOST/HIGH. U+200D (ZWJ) has NO card -> witness. Record actual (if a ZWJ card exists it routes differently). |
| K3 | combo | `goog<U+200B><U+2062>le.com` | HOST | HIGH | hold_pending_review | U+2062 | — | known(ZWSP)+unknown(U+2062): ZWSP -> HOST/HIGH AND the U+2062 witness must NOT be suppressed by the strong known verdict. |
| U1 | url | `https://site.example/?q=bad<U+200B>word` | QUERY_VALUE | MEDIUM | queue_for_review | — | ctx∉HOST; risk∉HIGH | Full URL. ZWSP in the QUERY value 'bad<ZWSP>word' -> QUERY_VALUE/MEDIUM. FORBIDDEN HOST/HIGH. |
| U2 | url | `us<U+200B>er@example.com` | EMAIL | MEDIUM | queue_for_review | — | — | ZWSP BEFORE @ -> email local-part split -> EMAIL/MEDIUM. |
| D1 | dangerous | `paypal<U+200B>.com` | HOST | HIGH | hold_pending_review | — | — | ZWSP inside the domain label -> HOST/HIGH, NEVER a silent PASS. Double assert: (1) source has U+200B; (2) reconstructed host != raw. |
| D2 | dangerous | `http://paypal.com<U+200B>@evil.com` | EMAIL,USERINFO | MEDIUM | queue_for_review | — | ctx∉HOST | userinfo@host: real host is evil.com, paypal.com is USERINFO. ZWSP in userinfo -> MEDIUM. FORBIDDEN: treat paypal.com as HOST. |
| D3 | dangerous | `paypal<U+200B>.com.` | HOST | HIGH | hold_pending_review | — | — | Trailing FQDN dot adds a canonicalization boundary (not a dup of D1). Still HOST/HIGH. |
| D4 | dangerous | `paypal%E2%80%8Bl.com ⟶decode⟶ paypal<U+200B>l.com` | - | - | pass | — | — | Stage1 RAW: no literal U+200B (percent-escaped) -> ZWSP card must NOT falsely fire on %E2%80%8B. Stage2 POST-DECODE: bytes -> U+200B -> HOST/HIGH. |
| D4·2 | (decoded) | `paypal<U+200B>l.com` | HOST | HIGH | hold_pending_review | — | — | POST-DECODE stage |
| D5 | dangerous | `goog<U+200B><U+2800>le.com` | HOST | HIGH | hold_pending_review | U+2800 | — | Stacking: ZWSP breaks the label -> HOST/HIGH; braille U+2800 is outside the OLD Cf/Zs predicate -> is it seen by the (extended?) witness net? |
| T1 | controls | `日本語<U+200B>のテキスト` | -,FREE_TEXT | -,NONE | pass | — | — | Legit typography: U+200B line-break opportunity in CJK (SAFE_CASE_002). RISK=NONE, no witness (carded). Catches the F2 regression. |
| N1 | controls | `<U+043E>бычный текст с пр<U+043E>белами` | - | - | pass | — | — | Negative control: ordinary U+0020 spaces (Zs, White_Space) must NOT create a witness-flood if the predicate is widened to Zs. No witness. |

_21 кейсов. Сгенерировано из zwsp_oracle_manifest.py (машинный источник истины)._