# Third-party notices

Several skills in this kit are close adaptations of skills from the projects below. They include substantial portions of the originals: rules, procedures, tables, red-flag lists, and output formats. They were edited for OpenAI Codex (tool names, subagent mechanics) and for a timed, offline-push setting. Each project is distributed under the MIT License; the copyright notices are listed below and the license text follows.

| Project | Copyright | Adapted into |
|---|---|---|
| https://github.com/obra/superpowers | Copyright (c) 2025 Jesse Vincent | `tdd` (test-driven-development), `debugging` (systematic-debugging), `delegate-build` and its templates (subagent-driven-development: task loop, implementer and task-reviewer prompts; codex-tools), `lean-plan` (writing-plans), `verify-and-wrap` (verification-before-completion) |
| https://github.com/mattpocock/skills | Copyright (c) 2026 Matt Pocock | `requirements-interview` (grilling, to-questionnaire), `tdd` (tdd: seams, vertical slices, anti-patterns), `lean-plan` (to-tickets, ADR format), `quality-gate` (code-review: two axes, smell baseline), `handoff` (handoff), `delegate-build` (implement-spec: context pointers) |
| https://github.com/DietrichGebert/ponytail | Copyright (c) 2026 DietrichGebert | `AGENTS.md` "Engineering defaults: ponytail" (ponytail AGENTS.md v5.2.0, copied verbatim), `quality-gate/references/review-quality.md` (ponytail-review: priorities, concrete-case rule, output format), `verify-and-wrap` (ponytail-debt) |
| https://github.com/affaan-m/ECC | Copyright (c) 2026 Affaan Mustafa | `.codex/agents` role file shape; reviewer confidence filter; security, database, and verification checklists |
| https://github.com/cloudflare/security-audit-skill | Copyright (c) 2025-2026 Cloudflare, Inc. | `quality-gate/references/security.md` (finding validation rules, attack classes) |
| https://github.com/softaworks/agent-toolkit | Copyright (c) 2026 Leonardo Flores | `lean-plan/references/data-model.md` (normalization and index checklist) |
| https://github.com/juxt/allium | Copyright (c) 2026 JUXT Ltd | `requirements-interview/references/question-techniques.md` (elicitation techniques) |
| https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | Copyright (c) 2024 Next Level Builder | `ui-design` (SKILL.md adapted from ui-ux-pro-max: priority table, query contract, design-system workflow, master and page overrides, 0-results rule, tips; `scripts/`, `data/`, `references/` copied unchanged except line endings) |

## MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
