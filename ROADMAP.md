# Roadmap

`oss-maintainer-compass` evolves based on maintainer needs and Codex/AI integration opportunities.

## Current Status: MVP (v0.1)

- ✅ JSON issue/PR export analysis
- ✅ Staleness detection
- ✅ Review queue prioritization
- ✅ Label trend aggregation
- ✅ Markdown report generation
- ✅ Agent handoff sections
- ✅ Zero dependencies
- ✅ Basic GitHub Actions CI
- ✅ Issue/PR templates
- ✅ Contributing guidelines

## Phase 1: GitHub API Integration (v0.2-0.3)

**Goal:** Eliminate need for manual exports; work directly with GitHub.

- [ ] GitHub API authentication (PAT, oauth)
- [ ] Live repository issue/PR fetching
- [ ] Rate limit handling and retry logic
- [ ] Multi-repository support
- [ ] Caching for performance
- [ ] Configuration file support (`.compass.yml`)
- [ ] Environment variable configuration

## Phase 2: Advanced Triage (v0.4-0.5)

**Goal:** Deeper insights for complex maintenance workflows.

- [ ] Author/contributor analysis (most active, inactive)
- [ ] Review turn-around time metrics
- [ ] Priority scoring algorithm
- [ ] Custom rule engine (label-based, author-based, size-based)
- [ ] Complexity estimation (size, changed files, test impact)
- [ ] Dependency impact detection
- [ ] Release blocker identification

## Phase 3: Codex/AI Integration (v0.6-0.7)

**Goal:** Structured handoff to Codex for automated review/actions.

- [ ] OpenAI API integration (for Codex)
- [ ] Prompt templates for:
  - Suggested PR review points
  - Issue triage recommendations
  - Release checklist generation
- [ ] AI-generated summary caching
- [ ] Feedback loop (user ratings on AI suggestions)
- [ ] Security: API key management, rate limiting

## Phase 4: Workflow Automation (v0.8-0.9)

**Goal:** From reports to action – automate maintenance tasks.

- [ ] GitHub Actions native integration
- [ ] Auto-label stale issues
- [ ] Auto-comment on PRs needing review
- [ ] Weekly digest notifications (Slack/Discord)
- [ ] Release checklist workflow
- [ ] Automated stale detection workflow
- [ ] Custom action hooks (webhooks)

## Phase 5: Ecosystem (v1.0+)

**Goal:** Integrate with broader maintainer tools.

- [ ] GitHub Project (v2) board integration
- [ ] Zulip/Discord/Slack plugins
- [ ] Grafana/Prometheus metrics export
- [ ] Pre-commit hook support
- [ ] GitHub App marketplace listing
- [ ] Community rule library
- [ ] Dashboard UI (optional, lightweight)

## Research & Exploration

- **Codex Assisted Review** – Can Codex understand context-diff and suggest review comments?
- **Auto-Release Notes** – Generate release notes from labeled issues/PRs?
- **Team Burndown** – Track velocity and capacity over time?
- **Issue Forecasting** – Predict when backlog will be resolved?
- **Contributor Health** – Detect risk of burnout or abandonment?

## Non-Goals

- Full-featured project management UI (that's GitHub's job)
- Real-time monitoring/dashboards (see Grafana)
- Community/social features beyond issues/PRs
- Advanced ML/predictive features (not for v1)
- Multi-language support (English first, markdown later)

## How to Propose Changes

See the [CONTRIBUTING.md](CONTRIBUTING.md) guide.

1. Check existing [issues](https://github.com/Psymath-code/oss-maintainer-compass/issues) and [discussions](https://github.com/Psymath-code/oss-maintainer-compass/discussions)
2. Propose in Discussions if exploratory
3. File an Issue if ready for implementation
4. Align with roadmap before major work

## Contributing to Roadmap Items

We welcome:
- Implementation of planned features
- Proof-of-concept work
- Bug fixes and documentation
- Community feedback and ideas

Large features may be broken into smaller tasks – check for related issues.
