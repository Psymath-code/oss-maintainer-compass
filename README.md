# oss-maintainer-compass

A lightweight CLI tool for open source maintainers to quickly understand GitHub issue and pull request backlogs, prioritize review queues, identify stale items, and generate maintainer reports for AI-assisted workflows.

## 🎯 Purpose

`oss-maintainer-compass` automates open source maintenance workflows by helping maintainers:

- **Quickly assess backlog health** – Understand which PRs need review, which issues are stale, and what labels represent current maintenance pressure
- **Prioritize review queues** – Identify and prioritize pull requests that require attention
- **Generate maintainer handoff reports** – Create structured reports suitable for AI agents (e.g., Codex, ChatGPT) to understand next steps
- **Reduce decision fatigue** – Get data-driven insights instead of manually scrolling through hundreds of items
- **Scale maintenance workflows** – Export structured analysis for automation pipelines and CI/CD systems

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Psymath-code/oss-maintainer-compass.git
cd oss-maintainer-compass

# No external dependencies required – uses Python standard library only
python3 -m src.oss_maintainer_compass.main --help
```

### Basic Usage

#### Analyze GitHub Issues/PRs Export

```bash
# Export issues from GitHub web UI (Settings > Issues > Export)
# Then analyze:
python3 -m src.oss_maintainer_compass.main analyze-export issues.json

# Generate a maintainer report
python3 -m src.oss_maintainer_compass.main generate-report issues.json --output maintainer_report.md

# Identify stale items (not updated for 30 days)
python3 -m src.oss_maintainer_compass.main find-stale issues.json --days 30

# Generate AI agent handoff section
python3 -m src.oss_maintainer_compass.main agent-handoff issues.json --output agent_briefing.md
```

## 📋 Core Features

- **Issue/PR Separation** – Automatically distinguish between issues and pull requests
- **Staleness Detection** – Identify items not updated within a configurable threshold
- **Review Queue Analysis** – Surface PRs needing review with metadata
- **Label Trend Aggregation** – Summarize label distribution to understand maintenance focus areas
- **Markdown Report Generation** – Create reports suitable for repositories, issues, release notes, or AI agent processing
- **Agent Handoff Sections** – Generate structured briefings for Codex and other coding agents
- **Zero Dependencies** – Uses only Python standard library for ease of installation and auditability
- **CI Integration** – GitHub Actions workflow included for automated maintenance reporting

## 🔄 Workflow Example

```bash
# 1. Export from GitHub (manual or via API)
# 2. Run compass analysis
python3 -m src.oss_maintainer_compass.main full-report export.json --output report.md

# 3. Review report locally or in issue
# 4. Optionally feed to AI agent for suggested actions
cat report.md | # pipe to Codex or ChatGPT for analysis
```

## 📁 Project Structure

```
oss-maintainer-compass/
├── README.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── LICENSE
├── SECURITY.md
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── src/
│   └── oss_maintainer_compass/
│       ├── __init__.py
│       ├── main.py
│       ├── analyzer.py
│       ├── reporter.py
│       └── models.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   └── test_reporter.py
├── examples/
│   ├── sample_issues.json
│   └── sample_report.md
└── pyproject.toml
```

## 🛣️ Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed plans, including:

- GitHub API direct integration (no export needed)
- Release checklist automation
- Codex-assisted PR review workflow
- Multi-repository maintenance reports
- Slack/Discord notifications
- Custom label and team-based rules

## 💻 Development

### Run Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### Add a New Feature

1. Fork and create a feature branch
2. Write tests first (TDD approach)
3. Implement feature in `src/`
4. Update documentation
5. Submit PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📜 License

This project is licensed under the [Apache License 2.0](LICENSE) – free to use, modify, and distribute in open source and commercial projects.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code of conduct
- How to report bugs
- How to suggest features
- Development setup
- PR submission guidelines

## 📞 Support

- **Issues** – [GitHub Issues](https://github.com/Psymath-code/oss-maintainer-compass/issues)
- **Discussions** – [GitHub Discussions](https://github.com/Psymath-code/oss-maintainer-compass/discussions)
- **Security** – See [SECURITY.md](SECURITY.md)

## 🎓 Use Cases

- **Small/medium OSS projects** – Quickly triage backlogs without dedicated community managers
- **Maintainer handoff automation** – Generate structured reports for CI/CD and AI workflows
- **Release preparation** – Identify blockers and outstanding PRs before release
- **Team coordination** – Share backlog health snapshots with contributors
- **Codex/AI integration** – Feed reports to Codex for suggested actions and automation

## 🙏 Acknowledgments

Built for the open source community to make maintenance workflows faster, more predictable, and less labor-intensive.

---

**Made with ❤️ for open source maintainers**
