# US tariffs in your AI agent, over MCP

TariffTrust is a remote [Model Context Protocol](https://modelcontextprotocol.io) server. Your agent
gets the operations of the API as tools: it can estimate a product or a whole declaration, search the
HTS, and read each duty's official source, instead of guessing a rate.

- **Address:** `https://api.tarifftrust.com/mcp/` (Streamable HTTP)
- **Authentication:** your API key, as a Bearer token

## Claude Code

```bash
claude mcp add --transport http tarifftrust https://api.tarifftrust.com/mcp/ --header "Authorization: Bearer $TARIFFTRUST_API_KEY"
```

## Claude Desktop

Add [claude_desktop_config.json](claude_desktop_config.json) to your configuration, with your key, then
restart the application. It reaches the server through
[`mcp-remote`](https://github.com/geelen/mcp-remote), so it needs Node.js.

## Cursor

Copy [cursor_mcp.json](cursor_mcp.json) to `.cursor/mcp.json` in your project, or to `~/.cursor/mcp.json`
for all of them, and set `TARIFFTRUST_API_KEY` in your environment.

## Try it

Ask your agent: *"What is the US duty on $10,000 of cotton T-shirts from China, HTS 6109.10.00.12, and
what would it be from Vietnam? Cite the source of each amount."*

Tools are counted as the API's operations are; pass `"save": true` to keep an estimate. See
[the guide](https://tarifftrust.com/guides/#mcp).
