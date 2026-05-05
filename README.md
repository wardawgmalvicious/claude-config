# Claude Config

Personal Claude Code configuration: skills, modules, CLAUDE.md, and
settings. This repo IS ~/.claude/ — edit in place, commit, push.

## Status

Active personal configuration. The repo is browseable and cherry-pickable
— take what's useful, adapt freely. **No support, no semver, no
backward-compatibility commitment.** Things move; what worked yesterday
may have been rewritten. Skills and rules track Microsoft Fabric / Power
BI / Azure conventions, which themselves drift; verify against current
docs before relying on any specific guidance.

If you find this useful, that's the goal. If you find a bug, an issue
report is welcome but not guaranteed a response. Personal config first,
public artifact second.

## Contents

- `skills/` — 28 skills total: 17 Fabric, 10 Power BI / TMDL, 1 behavioral (code-review)
- `agents/` — 1 subagent (security-reviewer)
- `rules/` — 8 path-scoped coding conventions (T-SQL, Spark SQL, Python/PySpark, KQL, DAX, M, TMDL, Fabric pipeline expressions); auto-load via `paths:` globs when matching files enter session scope
- `CLAUDE.md` — personal-scope instructions; pointer to per-language rules
- `settings.json` — Claude Code settings (permissions, enabled plugins, hook registry)
- `docs/handoff-briefs/` — templates and worked examples for the brief-before-draft pattern (see Handoff discipline below)

## Ongoing workflow

Edit files in place. This repo IS ~/.claude/. git add / commit / push
like any other repo. Claude Code picks up skill changes immediately
(live change detection).

## Handoff discipline

Skills and subagents in this repo are authored via a brief-before-draft
pattern: a chat-Claude session produces a structured handoff brief
covering frontmatter specs, body outline, portability caveats, and
post-draft validation steps; Claude Code then drafts the artifact from
the brief. The two surfaces specialize — chat-Claude has more context
and is better at structural proposal; Claude Code has filesystem access
and is better at drafting + iterating.

The pattern earns its place when an artifact has non-trivial behavioral
contracts — refusal patterns, severity rubrics, scope-enforced read-only
or destructive guards. For pure reference skills (canonical-answer
content), the pattern is overkill; real-use validation suffices.

Templates and worked examples live in `docs/handoff-briefs/`:

- `skill-handoff-template.md` — fill-in template for new skills
- `subagent-handoff-template.md` — fill-in template for new subagents
- `examples/` — reference briefs derived from validated artifacts

The templates are internal tooling. Consumers cherry-picking from this
repo don't need to adopt the brief pattern; the templates are included
in case the discipline is useful elsewhere.

## TODO

- Fresh machine bootstrap procedure — write after first verified
  fresh-machine clone
- License — add a permissive license (MIT or Apache 2.0) when the
  publishable-pack trajectory firms up. Until then, default copyright
  applies; treat as personal use.
