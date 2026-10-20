# PRDB

**Read papers with your agent.** Search PRDB, upload your own private PDFs, highlight exact passages, write comments and save private reviews beside the web Reader.

![PRDB](plugins/prdb/assets/icon.png)

**Public trial 0.2.0 for Codex Desktop.** Connects to [prdb.ai](https://prdb.ai). This repository contains only the plugin, skills and optional file helpers; no application server, accounts or private material. It has not been submitted to the OpenAI public directory.

## Start here

1. [Register and verify your ordinary PRDB account](https://prdb.ai/register).
2. Follow [the step-by-step quickstart](QUICKSTART.md) to install the pinned PRDB plugin and authorize it in your browser.
3. Upload one PDF, save highlights/comments/private review and check the same content in PRDB Reader.
4. [Report your experience](https://github.com/prdb-ai/prdb-plugin/issues/new/choose); keep private material out of public issues.

Ask Codex:

> Install the PRDB public trial from https://github.com/prdb-ai/prdb-plugin, pinned to v0.2.0. You may add this marketplace and install prdb@prdb, preserving other settings. Check the Codex CLI first, then tell me when to start a new chat and authorize PRDB in my browser.

For an available Codex CLI:

```sh
codex plugin marketplace add prdb-ai/prdb-plugin --ref v0.2.0
codex plugin add prdb@prdb
```

## Downloads and status

[Release v0.2.0](https://github.com/prdb-ai/prdb-plugin/releases/tag/v0.2.0) contains the Codex ZIP, SHA256SUMS and file manifest. Repository installation uses the same package at `plugins/prdb`. [Release notes](CHANGELOG.md) distinguish plugin versions from website releases.

Remote reading requires no local MCP server or Python package. A single PDF can be imported in your browser; the optional OS picker requires Python 3. Explicitly granted POSIX files/directories are supported through an optional Python 3 helper; direct chat attachments require client file access and real-user acceptance. Other clients have not been accepted. Fresh-machine human testing is the purpose of this trial; automated parsing is not a human reading test.

## Repository contents

- [QUICKSTART](QUICKSTART.md): install, OAuth, upload, reading, update and removal.
- [plugins](plugins/README.md): PRDB manifest, production MCP connection, skills and icon.
- [.agents](.agents/README.md): installable Codex marketplace.
- [.github](.github/README.md): bug and trial feedback templates.
- [SECURITY](SECURITY.md): private reporting channel.
- [LICENSE-NOTICE](LICENSE-NOTICE.md): current distribution notice.

Use [PRDB Support](https://prdb.ai/support) or issues@prdb.ai for private reports. Do not include passwords, tokens, private PDFs or notes in public issues.

The repository moved to the PRDB organization on2026-10-20. Existing v0.1.0/v0.2.0 tags, plugin files and release assets are unchanged. Older packaged links redirect to the new repository; do not replace a fixed release ZIP just to change those links. New installations may use prdb-ai/prdb-plugin with the same v0.2.0 pin and prdb@prdb identity. Production registration is currently paused; existing users can sign in.

Recent update: 2026-10-20 organization repository/install links updated; fixed plugin releases unchanged.
