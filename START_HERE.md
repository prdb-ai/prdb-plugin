# Start plugin development

This is the public PRDB client package. Users should follow [QUICKSTART](QUICKSTART.md); this page is for maintainers and agents.

1. Read [AGENTS](AGENTS.md), [CONTRIBUTING](CONTRIBUTING.md) and [ROADMAP](ROADMAP.md). Inspect git status, identity and remote; preserve unrelated work.
2. Update a clean main with git pull --ff-only and create a task branch such as codex/plugin-onboarding. Separate concurrent worktrees; do not reset another session.
3. Inspect [plugins](plugins/README.md), the distributed manifest/MCP connection and the marketplace. No server checkout or service credentials are needed to validate this package.
4. Run the independent offline checks:

```sh
python3 .github/check_plugin.py
python3 -m unittest discover -s .github -p 'test_*.py' -v
```

5. Document actual local checks and remaining client acceptance. When the owner authorizes source handoff, commit/push and open a PR with the repository template. Ready PRs run the same checks automatically.
6. A candidate ZIP is an optional separate workflow_dispatch input. It is an Actions artifact, not a published plugin version. Follow CONTRIBUTING for deliberate new-version publication and human installation acceptance.

Do not change installed user plugins, global client settings, browser authorization or public Release assets merely to run offline checks.
