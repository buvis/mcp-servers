We need to create MCP servers proxy based on the research published at:

- <https://artificialcuriositylabs.ai/posts/mcp-progressive-proxy/>
- <https://artificialcuriositylabs.hashnode.dev/the-enterprise-mcp-pattern-proxy-aggregate-host>
- <https://www.synapticlabs.ai/blogs/bounded-context-packs-meta-tool-pattern>

My innovation:

- rely on agent skills to inform LLM about the tools to use to avoid discovery calls at proxy
- payload token reduction
- management dashboard
  - proxied MCP servers installation and updates
  - proxied MCP servers configuration
  - observability
- secrets management
  - vault with connectors to 1Password, KeePass, etc.
  - payload scanning to hide secrets and other sensitive data
- introspection: suggest skill creation or improvement to reduce discovery calls at proxy
- use Jev and its clones for tool selection

Similar projects to get inspiration from and track for evolution:

- <https://github.com/Consiliency/pmcp>
- <https://github.com/karashiiro/my-cool-proxy>
