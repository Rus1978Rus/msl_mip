W7 CONVEYOR LEG 05
REVIEWER: GPT-5.6 Thinking / MODEL_FAMILY: OpenAI GPT
RECEIVED: 2026-08-03
PACKET: CONVEYOR_PACKET_W7_CONFUSABLE_2026-07-26
NOTE: web-verified against official Unicode (UTS#39, UTS#46, UAX#24). Deepest leg.

VERDICT: APPROVE_WITH_MAJOR_ARCHITECTURAL_PATCHES. дизайн верен, LOOPHOLE НЕТ.

POSITIONS:
  V1 MECHANISM  -> C two-tier: TIER1 CLASS/AXIS card VISIBLE_CONFUSABLE_RELATION (holds UTS39_VERSION,
                   UCD_VERSION, CONFUSABLES_DATA_HASH, SKELETON_ALGO_ID, SCRIPT_PROFILE, TARGET_CONTRACT,
                   SEVERITY_POLICY) + generated per-detection CONFUSABLE_RELATION_RECORD + THIN per-sign
                   exception cards ONLY where needed (disputed/known-attack/legit-linguistic/severity).
                   ***SOURCE OF TRUTH = FULL PINNED UTS#39 confusables DATA, NOT the handwritten 81***;
                   81 Vakhter = activation nursery / test corpus / curated first-cut ONLY.
                   A-alone REJECT (no card gate), B-alone REJECT (81 full cards).
  V2 FP-GRANITSA-> gates: (1) trusted HOST only; (2) analyze EACH DNS label separately; (3) use
                   RESOLVED script set / Script_Extensions (UAX#24) -- Common/Inherited (hyphen, digit,
                   punctuation) NOT a separate script; (4) ***require an ACTUAL UTS#39 confusable
                   mapping, NOT mixed-script presence alone***; (5) target-collision required for hold.
                   CANDIDATE = context==HOST AND label has >=2 resolved explicit scripts AND >=1
                   cross-script char participates in UTS#39 confusable mapping. Reject "HAS_LATIN AND
                   HAS_NON_LATIN" as sufficient. sber.рф per-label mono => pass; alpha-testing free text
                   => front inactive (no host) => measured Vakhter FP killed WITHOUT greek-prefix lists.
  V3 TARGET-LIST-> TWO-LEVEL: generic mixed-script confusable in host label + no target collision ->
                   POSSIBLE/QUEUE (no list). skeleton(input_label)==skeleton(protected_target) AND
                   raw!=target -> REAL/HOLD. Target list REQUIRED for HOLD, NOT for generic queue.
                   ***SECURITY: user text MUST NOT define its own protected targets*** (else attacker
                   forges collisions to force HOLD); targets come from trusted caller layer only.
                   TARGET_PROFILE contract {PROFILE_ID,OWNER,VERSION,TARGETS[],NORM_PROFILE,PROVENANCE,
                   TRUST_STATUS}. skeleton alone is over-inclusive (transitivity) -> hold needs a NAMED target.
  V4 LEVEL/SCOPE-> host/domain labels ONLY first-cut; generic -> MEDIUM/queue; protected-target
                   collision -> HIGH/hold; free text -> no severity change. Witness shows
                   ORIGINAL_LABEL / REVEALED (per-codepoint) / SCRIPTS / SKELETON / TARGET_COLLISION.
  F1 FULLWIDTH  -> SAME visible-spoof umbrella but SEPARATE separator subfront. ***CORRECTION: canonical
                   op = UTS#46/IDNA mapping, NOT "NFKC alone"*** -- U+FF0E, U+3002, U+FF61 all map to
                   U+002E under UTS#46. DOMAIN_SEPARATOR_EQUIVALENCE -> existing DOT relation/card path;
                   alt separator in host -> MEDIUM/queue; collision with protected domain -> HIGH/hold.
  V5 BATTERIES  -> pin UCD + UTS39 + confusables-hash + Script_Extensions-hash + UTS46 + target-profile.
                   Table update = MIGRATION event w/ own delta-census (not silent latest). Positive +
                   negative cells enumerated (incl paypal。com / paypal｡com / arabic / greek prose /
                   Latin+CyrillicTLD-separate-labels / digits-hyphen-common). Zero-delta ZWSP 21/21,
                   ZWJ/BOM/DOT/SOLIDUS/AT identical; only AUTHORIZED_CONFUSABLE_DELTA_MANIFEST cases move.
                   MUTATION MANIFEST MUT-CF-01..10 (ready adversarial battery): disable host gate /
                   whole-domain-not-per-label / Common-as-script / unpinned-latest / generic->HIGH /
                   ignore-target-provenance / suppress-positions / NFKC-instead-of-skeleton /
                   miss-U+3002 / run-on-alpha-testing-free-text -- each must fail a distinct test.
  V6 OSTATOK    -> canonical data = FULL pinned UTS39; first active policy = curated mixed-script host
                   subset; 4 disputed (ѡ→w η→n ա→a ս→u) PRESERVED as data, generic HIGH disabled,
                   witness/target-collision review only. whole-script spoof = PHASE 2 (needs target list
                   + whole-label skeleton collision; mixed-script detector can't catch mono-script label).
  V-OTHER-1     -> RAW/MAPPED DUAL VIEW: keep raw_host, IDNA_mapped_host, raw_label, unicode_label,
                   punycode_label, skeleton; never replace original with skeleton/IDNA view.
  V-OTHER-2     -> target-collision PER LABEL not substring (else notpaypal / paypal-support /
                   research-google-like false collisions). First increment EXACT_LABEL only.
  V-OTHER-3     -> FAIL-VISIBLE migration: version mismatch -> UNVERIFIABLE, NO silent fallback to
                   handcrafted maps; source conflict -> POLICY_CONFLICT, author review.

CONVERGENCE (4 семейства Grok+Gemini+Qwen+GPT): V1=C two-tier класс ось; V2 host + per-label +
  ">=2 script"; V3 generic mixed-script -> queue БЕЗ списка; V4 queue not hold, host-only; V6 4 спорных
  отложить + whole-script = отдельная фаза (нужен target-list).
GPT PATCHES beyond consensus (проверить/принять):
  P1 V2: require ACTUAL UTS#39 confusable mapping + resolved-script (Script_Extensions), NOT bare
     has-Latin+has-non-Latin. (строже всех; Common/Inherited не считать скриптом.)
  P2 V3: two-level -- HOLD gated on caller PROTECTED target; user text must NOT set targets (attack
     surface none of the others named).
  P3 V1/V6: full pinned UTS39 table = DATA layer; curated subset = ACTIVE policy (разводит "Unicode
     says confusable" vs "MSL/MIP has evidence to raise"). Qwen сказал "77 curated"; GPT = full-as-data.
  P4 F1: separators via UTS#46/IDNA mapping, NOT NFKC (technical correction to packet + Grok + Qwen).
  P5 V-OTHER-2: target match EXACT_LABEL, per-label not substring.
FORK STATUS after 5 legs:
  F1 fullwidth-точки: Grok=в фронт via NFKC(1); Gemini+Qwen=DOT-карта(2); GPT=отдельный separator
     subfront via UTS#46 -> DOT path(1, но техн-корректнее). => СИНТЕЗ: отдельная под-ось separator,
     канон = UTS#46, вешать на DOT-путь. F1b: §1 показал paypal．com silent pass => DOT-карта fullwidth
     в host СЕЙЧАС не эскалирует -> "делегировать" требует ДОРАБОТКИ DOT, не "уже работает".
  F2 hold-tier: только GPT спроектировал HOLD (target-collision). Остальные отложили hold. Для автора:
     брать ли GPT two-level (queue generic + hold on caller-target) в first-cut, или first-cut = queue-only
     и hold отдельным инкрементом.
COORD-FLAGS (проверить ЗАМЕРОМ на живом ядре перед author decision):
  * host/label-детект без разделителя-аномалии (pаypal в URL) -- есть ли надёжный HOST+label в ядре.
  * paypal．com сейчас silent pass -- подтвердить, что DOT-путь fullwidth в host НЕ ловит (F1b).
  * есть ли в ядре Script_Extensions/resolved-script (иначе P1 = новый код), и UTS#46-маппинг vs текущий
    _canon_domain_seps -- что уже канонизирует fullwidth-точку.
  * приходит ли в analyze() доверенный target-профиль от вызывающего слоя (для P2/F2).
