# Human-Led Fiction Drafting

Load this reference for fiction setup, outlining, drafting, continuation, revision, and review. It turns “emotion first” into an executable scene workflow and prevents a long prompt from becoming a substitute for authorial decisions.

## Governing Principle

The model may expand a decided scene; it must not invent the story's emotional logic, character limits, plot causality, prose voice, and publication judgment in one pass.

Separate the work into four layers:

1. **Story truth** — premise, point of view, theme, ending direction, facts that cannot change, and the human author's intended effect.
2. **Emotional causality** — what each scene makes the viewpoint character expect, fear, choose, and lose; emotion changes because an event changes the character's options.
3. **Scene execution** — action, dialogue, setting, and interiority for one scene or one coherent beat cluster.
4. **Editorial judgment** — continuity, originality, voice, platform compliance, and whether the passage deserves to remain.

Do not collapse all four layers into “write a chapter about X in an engaging style.” A longer prompt does not repair missing decisions.

## 1. Build the Emotional Beat Sheet Before Prose

An emotion label alone is not a beat. For each scene, record:

```text
Entry state: what the viewpoint character expects at the door
Wanted outcome: what they need from this encounter
Pressure source: who or what can deny it
Tactic: what they actually try
Trigger: the fact, gesture, or demand that changes their reading of the scene
Exit state: the new specific emotion, belief, or decision
Visible consequence: what option, relationship, resource, deadline, or risk changed
```

The entry and exit states must differ for a reason visible on the page. “Sad → angrier” is incomplete; “performed calm → exposed panic after the rival names the hidden account” is draftable.

For a chapter, sequence scene rows so the exit state of one scene creates the pressure entering the next. For long-form work, keep a chapter-level emotional curve in the outline rather than asking the model to infer one from plot labels.

## 2. Replace Personality Adjectives With Trigger Contracts

Adjectives such as `brave`, `kind`, `cold`, or `smart` do not predict behavior. Give every major character a trigger contract:

```text
Public mask: what other characters think this person is
Private want: what they protect or pursue
Principle: what they normally refuse to do
Trigger: the situation that makes the mask or principle fail
Default defense: attack / appease / withdraw / bargain / perform / investigate
Tell: one observable behavior under pressure
Breaking action: what they may do only after the trigger
Cost and repair: what the breach damages and what recovery would require
```

A character may break pattern only when the triggering event is present and the cost survives the scene. Do not use a trigger contract as a deterministic gimmick; different stakes and relationships may produce different tactics while preserving the same underlying want.

## 3. Design Dialogue Through Asymmetry

“Write tense, powerful dialogue” usually produces explicit speeches. Before a consequential exchange, define both sides:

| Field | Character A | Character B |
|---|---|---|
| Wants from this exchange | | |
| Believes about the other | | |
| Knows but will not say | | |
| Must prevent the other from learning | | |
| Leverage available now | | |
| Line or topic used as cover | | |

Then draft dialogue under these constraints:

1. The spoken topic and the real negotiation are not identical.
2. At least one reply changes tactic instead of answering the literal question.
3. Action beats show control, avoidance, or status; they do not translate the line's emotion for the reader.
4. Exposition appears only when a speaker has a reason to disclose it now.
5. Remove any line that both characters already know and say only for the reader.

Subtext is not obscurity. The reader should be able to infer the concealed want from specific choices, not from random evasiveness.

## 4. Draft in Controlled Units

Generate or write one scene, one beat cluster, or roughly 500–800 Chinese characters at a time when the model or context is unstable. Longer units are acceptable when the scene's causal spine stays visible; the unit boundary follows a turn, not an arbitrary quota.

For each unit:

1. Provide only the relevant story truth, active character contracts, incoming state, scene objective, turn, and forbidden contradictions.
2. Draft the unit without asking for critique, scoring, outline repair, and final prose simultaneously.
3. Stop at the planned turn.
4. Read the actual output and update continuity from what happened, not from what the outline hoped would happen.
5. Repair the current unit before generating the next one when causality, point of view, voice, or character behavior has drifted.

Do not repeatedly regenerate a whole chapter with the same prompt. Diagnose the failing layer and change its input: missing event, weak trigger, absent leverage, contradictory fact, or generic prose instruction.

## 5. Run a Decision Pass, Not a Synonym Pass

Human revision must add or confirm decisions. For every scene, audit in this order:

1. **Causality:** can each choice be traced to knowledge, pressure, and motive available at that moment?
2. **Character:** did behavior follow the trigger contract, or did the scene earn and retain the cost of a breach?
3. **Information gain:** what new fact, option, relationship state, or risk exists at the end? Cut repeated explanation and recap.
4. **Dialogue:** can the reader infer wants and withheld information without characters announcing their inner state?
5. **Embodiment:** replace abstract emotion with one consequential action, perception, mistake, or restraint; do not stack decorative sensory detail.
6. **Voice and rhythm:** remove interchangeable phrasing, uniform paragraph cadence, template transitions, moral summaries, and generic reaction loops using `story-deslop.md`.
7. **Original contribution:** identify the author's specific premise choices, scene decisions, observations, and revisions. If none are visible, the passage is not publication-ready.

Changing vocabulary while preserving generic causality is not meaningful revision.

## 6. AI Detection and Platform Use

An AI-detector percentage is not a reliable measure of authorship, originality, quality, or policy compliance. Never promise a target such as “below 30%,” rewrite to evade detection, or treat a detector result as proof that prose is human-written.

If the user explicitly requests detector use, treat it only as a noisy symptom locator:

1. Record the detector, version, date, text span, and result.
2. Inspect flagged passages for observable defects such as repeated syntax, generic transitions, over-explanation, style discontinuity, or copied phrasing.
3. Revise the underlying writing defect only when the text itself supports the diagnosis.
4. Re-review the prose normally; a lower score is not a pass condition.

Before publishing to a named platform such as 番茄小说, 起点, or 公众号, verify the platform's current official rules and available AI-content declaration or labeling controls. Preserve truthful authorship and assistance records. Never remove, hide, or falsify required labels or provenance metadata.

Platform acceptance is a separate gate from manuscript quality. A clean prose review does not prove signing, recommendation, distribution, or monetization eligibility.

## Required Artifacts

For new fiction, keep the smallest artifacts that fit the project:

1. `setup.md` or equivalent: story truth and authorial intent.
2. `outline/outline.md` or `beat-outline.md`: emotional beat rows with visible consequences.
3. Character files: trigger contracts for active characters.
4. A scene brief for the unit being drafted; this may live inline in the outline.
5. `tracking/context.md`: actual last beat, changed facts, relationship state, open threads, and next incoming emotion.
6. `tracking/quality-gates.md` when the project has a publication pipeline: record human decision pass, deslop/review coverage, platform-rule check date, and unresolved risks.

Do not create empty artifacts solely to satisfy the list. Existing project formats take precedence when they carry the same decisions.

## Source and Adaptation Note

This workflow adapts the useful drafting ideas demonstrated in 熊叔的茅草屋's video [“为什么AI写的番茄、起点和公众号小说全是废话，指令框架出了问题”](https://www.bilibili.com/video/BV1HnzWBeEz4): emotional beats before plot expansion, dialogue subtext, layered generation, character triggers, and a final logic/persona/dialogue read-through. The detector-percentage recommendation is intentionally not adopted as a quality or compliance target.
