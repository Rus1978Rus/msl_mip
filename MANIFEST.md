ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED
AUTHORITATIVE LANGUAGE: RU · ENGLISH: PRIMARY TRANSLATION · OTHER LANGUAGES: WORKING_DRAFT
NOT A FINAL STANDARD · NOT A SECURITY CERTIFICATE · NOT A PRODUCTION VALIDATOR
DOCUMENT ORDER: EN first for international readability; RU remains authoritative

# MSL/MIP Sign Alphabet

## Manifest · Манифест · Manifeste · Manifest · Manifiesto · Manifesto · घोषणापत्र · 宣言 · بيان

---

---
---

## ENGLISH

### MSL/MIP Sign Alphabet: A Conceptual System Manifesto

**Version 0.1 / Working Draft**  
*Author: Ruslan Malyavsky*  
*Status: WORKING_DRAFT — not yet conveyor-reviewed*

---

#### I. The Problem

Modern security systems work with words, domain reputation, and databases of known threats. They ask: *what is this?* — and look for the answer in lists.

MSL/MIP asks a different question: *what does this sign do in this context?*

This is not lookup. This is structural analysis.

---

#### II. The Central Idea

A sign is not a letter or a symbol in the ordinary sense. A sign is an object with a history, a function, and a context. The dot in an email address is not the same dot as the one ending a sentence. The slash in a file path is not the same slash as in a URL. The skull 💀 in a medical warning is not the same skull as in a teenager's chat message.

**A sign changes meaning depending on its substrate.**

This observation is not linguistic theory. It is a tool.

---

#### III. System Principles

**1. SUBSTRATE_INDEPENDENCE**  
The structural pattern of a sign is independent of the substrate in which it appears. For example, a generic TLD in a non-final position within a domain chain is a structural signal of mimicry — regardless of whether the text is an email, SMS, banking message, or chat. The responsibility for domain assessment lies with the dot sign, not the slash — the slash only marks the URL path boundary. The substrate changes — the pattern remains.

*Based on FO-013 SUBSTRATE_INDEPENDENCE (Foundation Layer of the project)*

**2. SIGN_OUTLIVES_FUNCTION**  
A sign outlives its original function. @ began as a commercial symbol in 1536, became an email address marker in 1971, became a mention sign in 2006. Each new function inherits recognizability, not semantics. The system must understand this history to avoid confusing epochs.

*Based on FO-099 SIGN_OUTLIVES_FUNCTION (Foundation Layer of the project)*

**3. SEQUENCE_OVER_ISOLATION**  
A sign in isolation is almost always safe. Danger is born in sequence. `..` is safe. `/` is safe. `../../../` is an attack. The system analyzes not signs, but their combinations.

**4. REVIEW_NOT_VALIDATION**  
The system does not issue verdicts. It raises flags. The decision to act belongs to a human or the next layer. This is a principled position: automation detects, humans decide.

**5. HONEST_UNCERTAINTY**  
If the system cannot determine a risk — it says so explicitly. Silent degradation is worse than openly admitting ignorance. Every output status contains a data source, confidence level, and justification.

---

#### IV. Architecture

MSL/MIP operates in three layers:

**Layer 1 — Single Sign**  
Each sign is processed independently: substrate, epoch, interpretation, and risk level are determined. A sign is not judged by its neighbors — only by its immediate context.

**Layer 2 — Sequence**  
Signs from different cards are assembled into sequence candidates. Cross-sign patterns emerge here: path traversal, protocol injection, epoch_mismatch. This layer cannot fire without the first — a sequence match is only counted if all signs within it have been validated.

**Layer 3 — Integration**  
Final verdict: PASS / QUEUE_FOR_REVIEW / HOLD_PENDING_REVIEW. Not binary "safe/dangerous" — a graduated scale that preserves space for human judgment.

---

#### V. Sign Cards

Each sign is described in a separate document — a Sign Core Card. The card contains:

- Codepoint and visible form
- Epoch history (CAPTURE_HISTORY): when the sign appeared, how its function evolved, which epochs are currently active
- Safe cases (SAFE_CASES) and risk cases (RISK_CASES) with examples
- Sequence candidates (SEQUENCE_CANDIDATES)
- Confirmation status: WORKING_DRAFT → WORKINGLY_CLOSED → ARTIFACT_CONFIRMED

A card is not code. A card is knowledge, formalized enough to become data.

---

#### VI. Conveyor Discipline

No change enters the system without independent review. This is not bureaucracy — it is protection against hallucinations, including one's own.

Conveyor principles:
- **VERIFY_BEFORE_TRUST**: every claim is verified by direct code execution, not logical tracing
- **AUTHOR_DECISION_STATUS_AUTHORITY**: only the author assigns final status
- **NO_EXCEPTIONS**: the conveyor rule has no exceptions based on change size

---

#### VII. What This Is Not

MSL/MIP is not an antivirus.  
MSL/MIP is not an NLP system.  
MSL/MIP is not a replacement for reputation databases.  
MSL/MIP is not a semantic analyzer.

The system works exclusively with structure. It does not know what "PayPal" is as a brand. It knows that "com" in a non-final position within a domain chain is a structural signal of mimicry. The difference is fundamental.

---

#### VIII. Current State

At the time of this manifesto's publication, the system contains:
- 3 signs with confirmed cards: `.` (U+002E), `/` (U+002F), `💀` (U+1F480)
- 1 test card: `☠` (U+2620) — WORKING_DRAFT, for testing cross-card sequence logic
- A working Python runtime requiring no external dependencies
- Three-level data protection (live fetch → cache → embedded minimum)
- Core modules and selected patches that have passed multi-round conveyor review

The system is under active development. Next directions: Unicode confusables, expanded sign registry, new cards.

---

#### IX. An Invitation

MSL/MIP is a private authored project. The methodology is open for study. The code may be made available to researchers upon request.

If you see a structural pattern the system should know — that is a conversation worth starting.


---
---

## РУССКИЙ

### MSL/MIP Sign Alphabet: Манифест концептуальной системы

**Версия 0.1 / Рабочий черновик**  
*Автор: Руслан Малявский*  
*Статус: WORKING_DRAFT — не прошёл конвейерный прогон*

---

#### I. Исходная проблема

Современные системы безопасности работают со словами, с репутацией доменов, с базами данных известных угроз. Они спрашивают: *что это такое?* — и ищут ответ в списках.

MSL/MIP задаёт другой вопрос: *что делает этот знак в этом контексте?*

Это не поиск по базе. Это анализ структуры.

---

#### II. Центральная идея

Знак — это не буква и не символ в обычном смысле. Знак — это объект с историей, функцией и контекстом. Точка в адресе электронной почты — не та же точка, что в конце предложения. Слеш в пути к файлу — не тот же слеш, что в URL. Череп 💀 в медицинском предупреждении — не тот же череп, что в переписке подростков.

**Знак меняет значение в зависимости от субстрата.**

Это наблюдение — не лингвистическая теория. Это инструмент.

---

#### III. Принципы системы

**1. SUBSTRATE_INDEPENDENCE**  
Структурный паттерн знака независим от субстрата, в котором он проявляется. Правило «generic-TLD в непоследней позиции доменной цепочки указывает на имитацию» работает в email, в SMS, в банковском сообщении, в чате. При этом ответственность за оценку домена лежит на знаке-точке, а не на слеше — слеш фиксирует лишь факт границы URL-пути. Субстрат меняется — паттерн остаётся.

*Основан на FO-013 SUBSTRATE_INDEPENDENCE (Foundation Layer проекта)*

**2. SIGN_OUTLIVES_FUNCTION**  
Знак переживает исходную функцию. @ начинался как торговый символ в 1536 году, стал адресом email в 1971-м, стал знаком упоминания в 2006-м. Каждая новая функция наследует узнаваемость, не семантику. Система должна понимать эту историю, чтобы не путать эпохи.

*Основан на FO-099 SIGN_OUTLIVES_FUNCTION (Foundation Layer проекта)*

**3. SEQUENCE_OVER_ISOLATION**  
Знак в изоляции почти всегда безопасен. Опасность рождается в последовательности. `..` безопасна. `/` безопасна. `../../../` — это уже атака. Система анализирует не знаки, а их сочетания.

**4. REVIEW_NOT_VALIDATION**  
Система не выносит приговор. Она расставляет флаги. Решение о действии — за человеком или за следующим слоем. Это принципиальная позиция: автоматика выявляет, человек решает.

**5. HONEST_UNCERTAINTY**  
Если система не может определить риск — она говорит об этом явно. Молчаливая деградация хуже открытого признания незнания. Каждый выходной статус содержит источник данных, уровень уверенности и обоснование.

---

#### IV. Архитектура

MSL/MIP работает в трёх слоях:

**Слой 1 — Одиночный знак (Single Sign)**  
Каждый знак обрабатывается отдельно: определяется субстрат, эпоха, интерпретация, уровень риска. Знак не судится по соседям — только по своему непосредственному контексту.

**Слой 2 — Последовательность (Sequence)**  
Знаки из разных карточек собираются в кандидаты-последовательности. Здесь возникают межзнаковые паттерны: path traversal, protocol injection, epoch_mismatch. Этот слой не может сработать без первого — последовательность засчитывается только если все знаки внутри неё прошли валидацию.

**Слой 3 — Интеграция (Integration)**  
Финальный вердикт: PASS / QUEUE_FOR_REVIEW / HOLD_PENDING_REVIEW. Не бинарное "безопасно/опасно" — градуированная шкала, сохраняющая возможность для человеческого суждения.

---

#### V. Карточки знаков

Каждый знак описывается в отдельном документе — Sign Core Card. Карточка содержит:

- Кодпоинт и видимую форму
- Историю эпох (CAPTURE_HISTORY): когда знак появился, как менялась его функция, какие эпохи активны сейчас
- Безопасные случаи (SAFE_CASES) и рисковые случаи (RISK_CASES) с примерами
- Кандидаты-последовательности (SEQUENCE_CANDIDATES)
- Статус подтверждения: WORKING_DRAFT → WORKINGLY_CLOSED → ARTIFACT_CONFIRMED

Карточка — не код. Карточка — это знание, формализованное настолько, чтобы стать данными.

---

#### VI. Конвейерная дисциплина

Ни одно изменение не входит в систему без независимого ревью. Это не бюрократия — это защита от галлюцинаций, в том числе собственных.

Принципы конвейера:
- **VERIFY_BEFORE_TRUST**: любое утверждение проверяется прямым прогоном кода, не логической трассировкой
- **AUTHOR_DECISION_STATUS_AUTHORITY**: только автор присваивает финальный статус
- **NO_EXCEPTIONS**: правило конвейера не имеет исключений по размеру изменения

---

#### VII. Что это не есть

MSL/MIP — не антивирус.  
MSL/MIP — не NLP-система.  
MSL/MIP — не замена репутационным базам данных.  
MSL/MIP — не семантический анализатор.

Система работает исключительно со структурой. Она не знает, что такое "PayPal" как бренд. Она знает, что "com" в непоследней позиции доменной цепочки — это структурный сигнал имитации. Разница принципиальная.

---

#### VIII. Текущее состояние

На момент публикации этого манифеста система содержит:
- 3 знака с подтверждёнными карточками: `.` (U+002E), `/` (U+002F), `💀` (U+1F480)
- 1 тестовая карточка: `☠` (U+2620) — WORKING_DRAFT, для проверки межкарточной логики
- Рабочий runtime на Python, не требующий внешних зависимостей
- Трёхуровневую защиту данных (живая загрузка → кэш → встроенный минимум)
- Отдельные ключевые модули и патчи, прошедшие многораундовый конвейерный прогон

Система находится в стадии активной разработки. Следующие направления: Unicode confusables, расширение реестра знаков, новые карточки.

---

#### IX. Приглашение

MSL/MIP — частный авторский проект. Методология открыта для изучения. Код может быть предоставлен исследователям по запросу.

Если вы видите структурный паттерн, который система должна знать — это разговор, который стоит начать.


---
---

## PORTUGUÊS (BRASIL)

### MSL/MIP Sign Alphabet: Manifesto de um sistema conceitual

**Versão 0.1 / Rascunho de trabalho**  
*Autor: Ruslan Malyavsky*  
*Status: WORKING_DRAFT — ainda não revisado pelo conveyor*

> *Versão completa. Idioma autoritativo: Russo. Inglês: tradução primária. Ordem de apresentação: EN primeiro para legibilidade internacional*

---

#### I. O problema

Os sistemas de segurança modernos trabalham com palavras, reputação de domínios e bancos de dados de ameaças conhecidas. Eles perguntam: *o que é isso?* — e buscam a resposta em listas.

O MSL/MIP faz uma pergunta diferente: *o que este sinal faz neste contexto?*

Isso não é uma busca. É análise estrutural.

---

#### II. A ideia central

Um sinal não é uma letra nem um símbolo no sentido comum. Um sinal é um objeto com história, função e contexto. O ponto em um endereço de e-mail não é o mesmo ponto que termina uma frase. A barra em um caminho de arquivo não é a mesma barra de uma URL. A caveira 💀 em um aviso médico não é a mesma caveira em uma mensagem de adolescente.

**Um sinal muda de significado dependendo do substrato.**

Essa observação não é teoria linguística. É uma ferramenta.

---

#### III. Princípios do sistema

**1. SUBSTRATE_INDEPENDENCE**  
O padrão estrutural de um sinal é independente do substrato em que aparece. Um TLD genérico em posição não final dentro de uma cadeia de domínio é um sinal estrutural de imitação — independentemente do substrato. A avaliação do domínio pertence ao sinal ponto, não à barra; a barra apenas marca a fronteira do caminho URL. O substrato muda — o padrão permanece.

*Baseado em FO-013 SUBSTRATE_INDEPENDENCE (Foundation Layer do projeto)*

**2. SIGN_OUTLIVES_FUNCTION**  
Um sinal sobrevive à sua função original. @ começou como símbolo comercial em 1536, tornou-se marcador de endereço de e-mail em 1971, tornou-se sinal de menção em 2006. Cada nova função herda o reconhecimento, não a semântica.

*Baseado em FO-099 SIGN_OUTLIVES_FUNCTION (Foundation Layer do projeto)*

**3. SEQUENCE_OVER_ISOLATION**  
Um sinal isolado é quase sempre seguro. O perigo nasce na sequência. `..` é seguro. `/` é seguro. `../../../` é um ataque. O sistema analisa não os sinais, mas suas combinações.

**4. REVIEW_NOT_VALIDATION**  
O sistema não emite veredictos. Levanta bandeiras. A decisão de agir pertence a um humano ou à próxima camada. Esta é uma posição de princípio: a automação detecta, os humanos decidem.

**5. HONEST_UNCERTAINTY**  
Se o sistema não consegue determinar um risco — diz isso explicitamente. A degradação silenciosa é pior do que admitir abertamente a ignorância.

---

#### IV. Arquitetura

MSL/MIP opera em três camadas:

**Camada 1 — Sinal único (Single Sign)**  
Cada sinal é processado independentemente: substrato, época, interpretação e nível de risco são determinados. Um sinal não é julgado por seus vizinhos — apenas pelo seu contexto imediato.

**Camada 2 — Sequência (Sequence)**  
Sinais de diferentes cartões são montados em candidatos de sequência. Padrões entre sinais emergem aqui: travessia de caminho, injeção de protocolo, conflito de época. Esta camada não pode disparar sem a primeira — uma correspondência de sequência só é contada se todos os sinais nela foram validados.

**Camada 3 — Integração**  
Veredicto final: PASS / QUEUE_FOR_REVIEW / HOLD_PENDING_REVIEW. Não binário "seguro/perigoso" — uma escala graduada que preserva espaço para o julgamento humano.

---

#### V. Cartões de sinais

Cada sinal é descrito em um documento separado — um Sign Core Card. O cartão contém:

- Ponto de código e forma visível
- Histórico de épocas (CAPTURE_HISTORY)
- Casos seguros (SAFE_CASES) e casos de risco (RISK_CASES) com exemplos
- Candidatos de sequência (SEQUENCE_CANDIDATES)
- Status de confirmação: WORKING_DRAFT → WORKINGLY_CLOSED → ARTIFACT_CONFIRMED

Um cartão não é código. Um cartão é conhecimento, formalizado o suficiente para se tornar dados.

---

#### VI. Disciplina do conveyor

Nenhuma mudança entra no sistema sem revisão independente. Isso não é burocracia — é proteção contra alucinações, incluindo as próprias.

Princípios do conveyor:
- **VERIFY_BEFORE_TRUST**: toda afirmação é verificada por execução direta de código
- **AUTHOR_DECISION_STATUS_AUTHORITY**: apenas o autor atribui o status final
- **NO_EXCEPTIONS**: a regra do conveyor não tem exceções por tamanho de mudança

---

#### VII. O que este sistema não é

MSL/MIP não é um antivírus.  
MSL/MIP não é um sistema NLP.  
MSL/MIP não é um substituto de bancos de dados de reputação.  
MSL/MIP não é um analisador semântico.

O sistema trabalha exclusivamente com estrutura. Não sabe o que é "PayPal" como marca. Sabe que "com" em posição não final em uma cadeia de domínio é um sinal estrutural de imitação. A diferença é fundamental.

---

#### VIII. Estado atual

No momento desta publicação, o sistema contém:
- 3 sinais com cartões confirmados: `.` (U+002E), `/` (U+002F), `💀` (U+1F480)
- 1 cartão de teste: `☠` (U+2620) — WORKING_DRAFT, para testar lógica de sequência entre cartões
- Um runtime Python funcional sem dependências externas
- Proteção de dados em três níveis (busca ao vivo → cache → mínimo embutido)

---

#### IX. Um convite

MSL/MIP é um projeto de autor privado. A metodologia está aberta para estudo. O código está disponível para pesquisadores.

Se você vê um padrão estrutural que o sistema deveria conhecer — essa é uma conversa que vale começar.
---
---

## DEUTSCH

### MSL/MIP Sign Alphabet: Manifest eines konzeptuellen Systems

**Version 0.1 / Arbeitsentwurf**  
*Autor: Ruslan Malyavsky*  
*Status: WORKING_DRAFT — noch nicht durch Förderband-Review geprüft*

---

#### I. Das Problem

Moderne Sicherheitssysteme arbeiten mit Wörtern, Domain-Reputation und Datenbanken bekannter Bedrohungen. Sie fragen: *Was ist das?* — und suchen die Antwort in Listen.

MSL/MIP stellt eine andere Frage: *Was tut dieses Zeichen in diesem Kontext?*

Das ist keine Suche. Das ist Strukturanalyse.

---

#### II. Die zentrale Idee

Ein Zeichen ist kein Buchstabe und kein Symbol im gewöhnlichen Sinne. Ein Zeichen ist ein Objekt mit Geschichte, Funktion und Kontext. Der Punkt in einer E-Mail-Adresse ist nicht derselbe Punkt wie am Ende eines Satzes. Der Schrägstrich in einem Dateipfad ist nicht derselbe Schrägstrich wie in einer URL. Der Totenkopf 💀 in einer medizinischen Warnung ist nicht derselbe Totenkopf wie in der Nachricht eines Teenagers.

**Ein Zeichen ändert seine Bedeutung je nach Substrat.**

Diese Beobachtung ist keine linguistische Theorie. Sie ist ein Werkzeug.

---

#### III. Systemprinzipien

**1. SUBSTRATE_INDEPENDENCE**  
Das strukturelle Muster eines Zeichens ist unabhängig vom Substrat, in dem es erscheint. Ein Generic-TLD in nicht-letzter Position einer Domänenkette ist ein strukturelles Signal für Imitation — unabhängig vom Substrat. Die Verantwortung für die Domänenbewertung liegt beim Punkt-Zeichen, nicht beim Schrägstrich — der Schrägstrich markiert nur die URL-Pfadgrenze. Das Substrat ändert sich — das Muster bleibt.

**2. SIGN_OUTLIVES_FUNCTION**  
Ein Zeichen überlebt seine ursprüngliche Funktion. @ begann 1536 als Handelssymbol, wurde 1971 zur E-Mail-Adressmarkierung, wurde 2006 zum Erwähnungszeichen. Jede neue Funktion erbt die Erkennbarkeit, nicht die Semantik. Das System muss diese Geschichte verstehen, um Epochen nicht zu verwechseln.

**3. SEQUENCE_OVER_ISOLATION**  
Ein Zeichen in Isolation ist fast immer sicher. Gefahr entsteht in Sequenzen. `..` ist sicher. `/` ist sicher. `../../../` ist ein Angriff. Das System analysiert nicht Zeichen, sondern ihre Kombinationen.

**4. REVIEW_NOT_VALIDATION**  
Das System fällt keine Urteile. Es setzt Flags. Die Entscheidung zum Handeln liegt beim Menschen oder bei der nächsten Schicht. Das ist eine grundsätzliche Position: Automatisierung erkennt, Menschen entscheiden.

**5. HONEST_UNCERTAINTY**  
Wenn das System ein Risiko nicht bestimmen kann — sagt es das ausdrücklich. Stille Degradation ist schlimmer als offenes Eingestehen von Unwissen. Jeder Ausgabestatus enthält eine Datenquelle, ein Konfidenzniveau und eine Begründung.

---

#### IV. Architektur

MSL/MIP arbeitet in drei Schichten:

**Schicht 1 — Einzelzeichen (Single Sign)**  
Jedes Zeichen wird unabhängig verarbeitet: Substrat, Epoche, Interpretation und Risikoniveau werden bestimmt. Ein Zeichen wird nicht nach seinen Nachbarn beurteilt — nur nach seinem unmittelbaren Kontext.

**Schicht 2 — Sequenz (Sequence)**  
Zeichen aus verschiedenen Karten werden zu Sequenzkandidaten zusammengesetzt. Hier entstehen zeichenübergreifende Muster: Path Traversal, Protocol Injection, Epochenkonflikt. Diese Schicht kann ohne die erste nicht auslösen — eine Sequenzübereinstimmung wird nur gezählt, wenn alle Zeichen darin validiert wurden.

**Schicht 3 — Integration**  
Endgültiges Urteil: PASS / QUEUE_FOR_REVIEW / HOLD_PENDING_REVIEW. Nicht binär „sicher/gefährlich" — eine abgestufte Skala, die Raum für menschliches Urteil bewahrt.

---

#### V. Zeichenkarten

Jedes Zeichen wird in einem separaten Dokument beschrieben — einer Sign Core Card. Die Karte enthält:

- Codepunkt und sichtbare Form
- Epochengeschichte (CAPTURE_HISTORY): wann das Zeichen erschien, wie sich seine Funktion entwickelte, welche Epochen aktuell aktiv sind
- Sichere Fälle (SAFE_CASES) und Risikofälle (RISK_CASES) mit Beispielen
- Sequenzkandidaten (SEQUENCE_CANDIDATES)
- Bestätigungsstatus: WORKING_DRAFT → WORKINGLY_CLOSED → ARTIFACT_CONFIRMED

Eine Karte ist kein Code. Eine Karte ist Wissen, formalisiert genug, um Daten zu werden.

---

#### VI. Förderbanddisziplin

Keine Änderung tritt ohne unabhängige Überprüfung in das System ein. Das ist keine Bürokratie — es ist Schutz vor Halluzinationen, einschließlich der eigenen.

Förderbandprinzipien:
- **VERIFY_BEFORE_TRUST**: Jede Behauptung wird durch direkte Codeausführung verifiziert, nicht durch logisches Nachvollziehen
- **AUTHOR_DECISION_STATUS_AUTHORITY**: Nur der Autor vergibt den endgültigen Status
- **NO_EXCEPTIONS**: Die Förderbandregelung kennt keine Ausnahmen nach Änderungsgröße

---

#### VII. Was dieses System nicht ist

MSL/MIP ist kein Antivirusprogramm.  
MSL/MIP ist kein NLP-System.  
MSL/MIP ist kein Ersatz für Reputationsdatenbanken.  
MSL/MIP ist kein semantischer Analysator.

Das System arbeitet ausschließlich mit Struktur. Es weiß nicht, was „PayPal" als Marke ist. Es weiß, dass „com" in nicht-abschließender Position innerhalb einer Domänenkette ein strukturelles Signal für Imitation ist. Der Unterschied ist grundlegend.

---

#### VIII. Aktueller Stand

Zum Zeitpunkt der Veröffentlichung dieses Manifests enthält das System:
- 3 Zeichen mit bestätigten Karten: `.` (U+002E), `/` (U+002F), `💀` (U+1F480)
- 1 Testkarte: `☠` (U+2620) — WORKING_DRAFT, zum Testen kartenübergreifender Sequenzlogik
- Eine funktionierende Python-Laufzeitumgebung ohne externe Abhängigkeiten
- Dreistufigen Datenschutz (Live-Abruf → Cache → eingebettetes Minimum)
- Code, der mehrere Runden Förderband-Review bestanden hat

Das System befindet sich in aktiver Entwicklung. Nächste Richtungen: Unicode Confusables, erweitertes Zeichenregister, neue Karten.

---

#### IX. Eine Einladung

MSL/MIP ist ein privates Autorenprojekt. Die Methodik steht zum Studium offen. Der Code steht Forschern zur Verfügung.

Wenn Sie ein strukturelles Muster sehen, das das System kennen sollte — das ist ein Gespräch, das es wert ist, begonnen zu werden.

---
---

## FRANÇAIS

### MSL/MIP Sign Alphabet : Manifeste d'un système conceptuel

**Version 0.1 / Brouillon de travail**  
*Auteur : Ruslan Malyavsky*  
*Statut : WORKING_DRAFT — non encore examiné par le convoyeur*

---

#### I. Le problème

Les systèmes de sécurité modernes travaillent avec des mots, la réputation des domaines et des bases de données de menaces connues. Ils demandent : *qu'est-ce que c'est ?* — et cherchent la réponse dans des listes.

MSL/MIP pose une question différente : *que fait ce signe dans ce contexte ?*

Ce n'est pas une recherche. C'est une analyse structurelle.

---

#### II. L'idée centrale

Un signe n'est pas une lettre ni un symbole au sens ordinaire. Un signe est un objet avec une histoire, une fonction et un contexte. Le point dans une adresse e-mail n'est pas le même point que celui qui termine une phrase. La barre oblique dans un chemin de fichier n'est pas la même que dans une URL. La tête de mort 💀 dans un avertissement médical n'est pas la même que dans le message d'un adolescent.

**Un signe change de signification selon son substrat.**

Cette observation n'est pas une théorie linguistique. C'est un outil.

---

#### III. Principes du système

**1. SUBSTRATE_INDEPENDENCE**  
Le modèle structurel d'un signe est indépendant du substrat dans lequel il apparaît. Un TLD générique en position non finale dans une chaîne de domaine est un signal structurel d'imitation — quel que soit le substrat. La responsabilité de l'évaluation du domaine incombe au signe point, pas à la barre oblique — la barre oblique marque uniquement la frontière du chemin URL. Le substrat change — le modèle reste.

**2. SIGN_OUTLIVES_FUNCTION**  
Un signe survit à sa fonction d'origine. @ a commencé comme symbole commercial en 1536, est devenu marqueur d'adresse e-mail en 1971, est devenu signe de mention en 2006. Chaque nouvelle fonction hérite de la reconnaissance, pas de la sémantique. Le système doit comprendre cette histoire pour ne pas confondre les époques.

**3. SEQUENCE_OVER_ISOLATION**  
Un signe isolé est presque toujours sûr. Le danger naît dans la séquence. `..` est sûr. `/` est sûr. `../../../` est une attaque. Le système analyse non pas les signes, mais leurs combinaisons.

**4. REVIEW_NOT_VALIDATION**  
Le système ne rend pas de verdict. Il lève des drapeaux. La décision d'agir appartient à un humain ou à la couche suivante. C'est une position de principe : l'automatisation détecte, les humains décident.

**5. HONEST_UNCERTAINTY**  
Si le système ne peut pas déterminer un risque — il le dit explicitement. La dégradation silencieuse est pire qu'admettre ouvertement l'ignorance. Chaque statut de sortie contient une source de données, un niveau de confiance et une justification.

---

#### IV. Architecture

MSL/MIP fonctionne en trois couches :

**Couche 1 — Signe unique (Single Sign)**  
Chaque signe est traité indépendamment : le substrat, l'époque, l'interprétation et le niveau de risque sont déterminés. Un signe n'est pas jugé par ses voisins — seulement par son contexte immédiat.

**Couche 2 — Séquence (Sequence)**  
Les signes de différentes cartes sont assemblés en candidats-séquences. Des modèles inter-signes émergent ici : traversée de chemin, injection de protocole, conflit d'époque. Cette couche ne peut pas se déclencher sans la première — une correspondance de séquence n'est comptée que si tous les signes en elle ont été validés.

**Couche 3 — Intégration**  
Verdict final : PASS / QUEUE_FOR_REVIEW / HOLD_PENDING_REVIEW. Pas binaire « sûr/dangereux » — une échelle graduée qui préserve l'espace pour le jugement humain.

---

#### V. Cartes de signes

Chaque signe est décrit dans un document séparé — une Sign Core Card. La carte contient :

- Point de code et forme visible
- Histoire des époques (CAPTURE_HISTORY) : quand le signe est apparu, comment sa fonction a évolué, quelles époques sont actuellement actives
- Cas sûrs (SAFE_CASES) et cas à risque (RISK_CASES) avec des exemples
- Candidats-séquences (SEQUENCE_CANDIDATES)
- Statut de confirmation : WORKING_DRAFT → WORKINGLY_CLOSED → ARTIFACT_CONFIRMED

Une carte n'est pas du code. Une carte est de la connaissance, formalisée suffisamment pour devenir des données.

---

#### VI. Discipline du convoyeur

Aucun changement n'entre dans le système sans révision indépendante. Ce n'est pas de la bureaucratie — c'est une protection contre les hallucinations, y compris les siennes propres.

Principes du convoyeur :
- **VERIFY_BEFORE_TRUST** : toute affirmation est vérifiée par exécution directe du code, pas par traçage logique
- **AUTHOR_DECISION_STATUS_AUTHORITY** : seul l'auteur attribue le statut final
- **NO_EXCEPTIONS** : la règle du convoyeur n'a pas d'exceptions selon la taille du changement

---

#### VII. Ce que ce système n'est pas

MSL/MIP n'est pas un antivirus.  
MSL/MIP n'est pas un système NLP.  
MSL/MIP n'est pas un remplacement des bases de données de réputation.  
MSL/MIP n'est pas un analyseur sémantique.

Le système travaille exclusivement avec la structure. Il ne sait pas ce qu'est « PayPal » en tant que marque. Il sait que « com » en position non finale dans une chaîne de domaine est un signal structurel d'imitation. La différence est fondamentale.

---

#### VIII. État actuel

Au moment de la publication de ce manifeste, le système contient :
- 3 signes avec des cartes confirmées : `.` (U+002E), `/` (U+002F), `💀` (U+1F480)
- 1 carte de test : `☠` (U+2620) — WORKING_DRAFT, pour tester la logique de séquence inter-cartes
- Un runtime Python fonctionnel ne nécessitant aucune dépendance externe
- Une protection des données à trois niveaux (récupération en direct → cache → minimum intégré)
- Du code ayant passé plusieurs rounds de révision par convoyeur

Le système est en développement actif. Prochaines directions : Unicode confusables, registre de signes étendu, nouvelles cartes.

---

#### IX. Une invitation

MSL/MIP est un projet d'auteur privé. La méthodologie est ouverte à l'étude. Le code est disponible pour les chercheurs.

Si vous voyez un modèle structurel que le système devrait connaître — c'est une conversation qui mérite d'être entamée.

---

*MSL/MIP Sign Alphabet — версия 0.1*  
*© Руслан Малявский / Ruslan Malyavsky*  
*Проект активен / Project active / Projekt aktiv / Projet actif*

---
---

## ESPAÑOL

> *Versión abreviada / Abridged version — полная версия на русском и английском языках*

### MSL/MIP Sign Alphabet: Manifiesto de un sistema conceptual

**Versión 0.1 / Borrador de trabajo**  
*Autor: Ruslan Malyavsky*  
*Estado: WORKING_DRAFT — aún no revisado por el conveyor*

---

#### I. El problema

Los sistemas de seguridad modernos trabajan con palabras, reputación de dominios y bases de datos de amenazas conocidas. Preguntan: *¿qué es esto?* — y buscan la respuesta en listas.

MSL/MIP hace una pregunta diferente: *¿qué hace este signo en este contexto?*

Esto no es una búsqueda. Es análisis estructural.

---

#### II. La idea central

Un signo no es una letra ni un símbolo en el sentido ordinario. Un signo es un objeto con historia, función y contexto. El punto en una dirección de correo electrónico no es el mismo punto que al final de una oración. La barra oblicua en una ruta de archivo no es la misma que en una URL. La calavera 💀 en una advertencia médica no es la misma que en el mensaje de un adolescente.

**Un signo cambia de significado según su substrato.**

Esta observación no es teoría lingüística. Es una herramienta.

---

#### III. Principios del sistema

**1. SUBSTRATE_INDEPENDENCE**  
El patrón estructural de un signo es independiente del substrato en que aparece. Un TLD genérico en posición no final dentro de una cadena de dominio puede ser una señal estructural de imitación — independientemente del substrato. La evaluación del dominio corresponde al signo punto, no a la barra; la barra solo marca la frontera del camino URL. El substrato cambia — el patrón permanece.

**2. SIGN_OUTLIVES_FUNCTION**  
Un signo sobrevive a su función original. @ comenzó como símbolo comercial en 1536, se convirtió en marcador de dirección de correo en 1971, se convirtió en signo de mención en 2006. Cada nueva función hereda el reconocimiento, no la semántica.

**3. SEQUENCE_OVER_ISOLATION**  
Un signo en aislamiento es casi siempre seguro. El peligro nace en la secuencia. `..` es seguro. `/` es seguro. `../../../` es un ataque. El sistema analiza no los signos, sino sus combinaciones.

**4. REVIEW_NOT_VALIDATION**  
El sistema no emite veredictos. Levanta banderas. La decisión de actuar pertenece a un humano o a la siguiente capa. Esta es una posición de principio: la automatización detecta, los humanos deciden.

**5. HONEST_UNCERTAINTY**  
Si el sistema no puede determinar un riesgo — lo dice explícitamente. La degradación silenciosa es peor que admitir abiertamente la ignorancia.

---

#### IV. Arquitectura

MSL/MIP opera en tres capas:

**Capa 1 — Signo único (Single Sign)**  
Cada signo se procesa independientemente: substrato, época, interpretación y nivel de riesgo son determinados.

**Capa 2 — Secuencia (Sequence)**  
Los signos de diferentes tarjetas se ensamblan en candidatos de secuencia. Aquí emergen patrones entre signos: traversal de ruta, inyección de protocolo, conflicto de época.

**Capa 3 — Integración**  
Veredicto final: PASS / QUEUE_FOR_REVIEW / HOLD_PENDING_REVIEW. No binario "seguro/peligroso" — una escala graduada que preserva espacio para el juicio humano.

---

#### V. Lo que este sistema no es

MSL/MIP no es un antivirus.  
MSL/MIP no es un sistema NLP.  
MSL/MIP no es un reemplazo de bases de datos de reputación.  
MSL/MIP no es un analizador semántico.

El sistema trabaja exclusivamente con estructura.

---

#### VI. Una invitación

MSL/MIP es un proyecto de autor privado. La metodología está abierta al estudio. El código está disponible para investigadores.

Si ve un patrón estructural que el sistema debería conocer — esa es una conversación que vale la pena iniciar.

---
---

## हिन्दी

> *संक्षिप्त संस्करण / Abridged version — полная версия на русском и английском языках*
### MSL/MIP Sign Alphabet: एक वैचारिक प्रणाली का घोषणापत्र

**संस्करण 0.1 / कार्य प्रारूप**  
*लेखक: रुस्लान मल्यावस्की*  
*स्थिति: WORKING_DRAFT — NEEDS_NATIVE_REVIEW (मूल वक्ता द्वारा समीक्षा आवश्यक)*

---

#### I. समस्या

आधुनिक सुरक्षा प्रणालियाँ शब्दों, डोमेन प्रतिष्ठा और ज्ञात खतरों के डेटाबेस के साथ काम करती हैं। वे पूछती हैं: *यह क्या है?* — और सूचियों में उत्तर खोजती हैं।

MSL/MIP एक अलग प्रश्न पूछता है: *यह चिह्न इस संदर्भ में क्या करता है?*

यह खोज नहीं है। यह संरचनात्मक विश्लेषण है।

---

#### II. केंद्रीय विचार

एक चिह्न सामान्य अर्थ में न तो एक अक्षर है और न ही एक प्रतीक। एक चिह्न इतिहास, कार्य और संदर्भ वाली एक वस्तु है। ईमेल पते में बिंदु वही बिंदु नहीं है जो वाक्य के अंत में होता है। फ़ाइल पथ में स्लैश वही स्लैश नहीं है जो URL में होता है। चिकित्सा चेतावनी में खोपड़ी 💀 किशोर के संदेश में खोपड़ी से अलग है।

**एक चिह्न अपने सब्सट्रेट के अनुसार अर्थ बदलता है।**

यह अवलोकन भाषाई सिद्धांत नहीं है। यह एक उपकरण है।

---

#### III. मूल सिद्धांत

**1. SUBSTRATE_INDEPENDENCE** — संरचनात्मक पैटर्न सब्सट्रेट से स्वतंत्र है।

**2. SIGN_OUTLIVES_FUNCTION** — चिह्न अपने मूल कार्य से आगे जीता है।

**3. SEQUENCE_OVER_ISOLATION** — खतरा अलगाव में नहीं, अनुक्रम में जन्म लेता है।

**4. REVIEW_NOT_VALIDATION** — प्रणाली निर्णय नहीं देती। वह संकेत उठाती है।

**5. HONEST_UNCERTAINTY** — यदि प्रणाली जोखिम निर्धारित नहीं कर सकती — वह स्पष्ट रूप से कहती है।

---

#### IV. निमंत्रण

MSL/MIP एक निजी लेखक परियोजना है। पद्धति अध्ययन के लिए खुली है। कोड शोधकर्ताओं के लिए उपलब्ध है।

यदि आप एक संरचनात्मक पैटर्न देखते हैं जो प्रणाली को जानना चाहिए — यह एक बातचीत शुरू करने योग्य है।

---
---

## 中文

> *简略版本 / Abridged version — полная версия на русском и английском языках*

### MSL/MIP Sign Alphabet：概念系统宣言

**版本 0.1 / 工作草稿**  
*作者：鲁斯兰·马利亚夫斯基*  
*状态：WORKING_DRAFT — NEEDS_NATIVE_REVIEW（需要母语者审校）*

---

#### 一、问题所在

现代安全系统使用单词、域名信誉和已知威胁数据库工作。它们问：*这是什么？* — 并在列表中寻找答案。

MSL/MIP 提出了一个不同的问题：*这个符号在这个语境中做什么？*

这不是查找。这是结构分析。

---

#### 二、核心思想

符号不是普通意义上的字母或符号。符号是具有历史、功能和语境的对象。电子邮件地址中的点与句子末尾的点不同。文件路径中的斜杠与URL中的斜杠不同。医学警告中的骷髅 💀 与青少年聊天中的骷髅不同。

**符号根据其基底改变含义。**

这一观察不是语言学理论。它是一种工具。

---

#### 三、系统原则

**1. SUBSTRATE_INDEPENDENCE** — 符号的结构模式独立于其出现的基底。

**2. SIGN_OUTLIVES_FUNCTION** — 符号比其原始功能活得更长。

**3. SEQUENCE_OVER_ISOLATION** — 危险在序列中诞生，而非孤立中。

**4. REVIEW_NOT_VALIDATION** — 系统不做裁决。它举起标志。

**5. HONEST_UNCERTAINTY** — 如果系统无法确定风险——它明确说明。

---

#### 四、邀请

MSL/MIP 是一个私人作者项目。方法论开放供研究。代码供研究人员使用。

如果您看到系统应该了解的结构模式——这是一个值得开始的对话。

---
---

## العربية

> *نسخة مختصرة / Abridged version — полная версия на русском и английском языках*

### أبجدية العلامات MSL/MIP: بيان نظام مفاهيمي

**الإصدار 0.1 / مسودة عمل**  
*المؤلف: روسلان ماليافسكي*  
*الحالة: WORKING_DRAFT — NEEDS_NATIVE_REVIEW (تتطلب مراجعة من متحدث أصلي)*

---

#### أولاً: المشكلة

تعمل أنظمة الأمن الحديثة مع الكلمات وسمعة النطاقات وقواعد بيانات التهديدات المعروفة. تسأل: *ما هذا؟* — وتبحث عن الإجابة في القوائم.

يطرح MSL/MIP سؤالاً مختلفاً: *ماذا تفعل هذه العلامة في هذا السياق؟*

هذا ليس بحثاً. هذا تحليل هيكلي.

---

#### ثانياً: الفكرة المحورية

العلامة ليست حرفاً ولا رمزاً بالمعنى المعتاد. العلامة هي كيان له تاريخ ووظيفة وسياق. النقطة في عنوان البريد الإلكتروني ليست النقطة ذاتها في نهاية الجملة. الشرطة المائلة في مسار الملف ليست الشرطة ذاتها في عنوان URL. الجمجمة 💀 في تحذير طبي ليست الجمجمة ذاتها في رسالة مراهق.

**تغيّر العلامة معناها بحسب الركيزة التي تظهر فيها.**

هذه الملاحظة ليست نظرية لغوية. إنها أداة.

---

#### ثالثاً: مبادئ النظام

**1. SUBSTRATE_INDEPENDENCE** — النمط الهيكلي للعلامة مستقل عن الركيزة التي يظهر فيها.

**2. SIGN_OUTLIVES_FUNCTION** — العلامة تتجاوز وظيفتها الأصلية.

**3. SEQUENCE_OVER_ISOLATION** — الخطر يولد في التسلسل، لا في العزلة.

**4. REVIEW_NOT_VALIDATION** — النظام لا يُصدر أحكاماً. يرفع أعلاماً.

**5. HONEST_UNCERTAINTY** — إذا لم يستطع النظام تحديد خطر — يقوله صراحة.

---

#### رابعاً: دعوة

MSL/MIP مشروع مؤلف خاص. المنهجية مفتوحة للدراسة. الكود متاح للباحثين.

إذا رأيت نمطاً هيكلياً يجب أن يعرفه النظام — فهذه محادثة تستحق البدء.

---

*MSL/MIP Sign Alphabet — الإصدار 0.1*  
*© روسلان مالياڤسكي / Ruslan Malyavsky*
