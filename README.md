<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">YNAB MCP Server</h3>

  <p align="center">
    A Model Context Protocol (MCP) server for the YNAB (You Need A Budget) API, enabling AI assistants like Claude to interact with your budget data.
    <br />
    <a href="https://github.com/Npab19/ynab-mcp"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Npab19/ynab-mcp/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Npab19/ynab-mcp/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#claudeai-web-connectors-recommended">Claude.ai web connectors</a></li>
        <li><a href="#claude-desktop">Claude Desktop</a></li>
      </ul>
    </li>
    <li><a href="#available-tools">Available Tools</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

YNAB MCP is a [Model Context Protocol](https://modelcontextprotocol.io) server that exposes your YNAB budget data to AI assistants. It runs as a Docker container and is made publicly accessible via a Cloudflare Tunnel, allowing tools like Claude to query budgets, transactions, accounts, categories, and more over a streamable HTTP connection.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python]][Python-url]
* [![Docker][Docker]][Docker-url]
* [![Cloudflare][Cloudflare]][Cloudflare-url]
* [![YNAB][YNAB]][YNAB-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Docker and Docker Compose
* A [YNAB Personal Access Token](https://app.ynab.com/settings/developer)
* A [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) token (for remote access)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Npab19/ynab-mcp.git
   cd ynab-mcp
   ```

2. Copy the example environment file and fill in your credentials
   ```sh
   cp .env.example .env
   ```

3. Edit `.env` with your credentials
   ```env
   YNAB_API_KEY=your_ynab_personal_access_token_here
   Cloudflare_Token=your_cloudflare_tunnel_token_here
   MCP_BEARER_TOKEN=your_random_secret_token_here
   ```

   Generate a secure token with:
   ```sh
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

4. Start the server
   ```sh
   docker compose up -d
   ```

The MCP server will be available at `http://localhost:8000` locally, or via your Cloudflare Tunnel URL remotely.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage

The server requires authentication on all requests. The `MCP_BEARER_TOKEN` you set in `.env` is used to authenticate MCP clients.

### Claude.ai web connectors (recommended)

Add a custom connector in Claude.ai settings with the URL:

```
https://<your-tunnel-url>/mcp?api_key=<MCP_BEARER_TOKEN>
```

This syncs across all your devices automatically.

### Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ynab": {
      "type": "http",
      "url": "https://<your-tunnel-url>/mcp",
      "headers": {
        "Authorization": "Bearer <MCP_BEARER_TOKEN>"
      }
    }
  }
}
```

Restart Claude Desktop after saving.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- AVAILABLE TOOLS -->
## Available Tools

The server exposes tools across the following YNAB resource categories:

| Category | Description |
|---|---|
| **Budgets** | List and retrieve budgets |
| **Accounts** | View accounts within a budget |
| **Transactions** | Query and filter transactions |
| **Categories** | Browse category groups and categories |
| **Months** | Access monthly budget summaries |
| **Payees** | List payees |
| **Scheduled Transactions** | View upcoming scheduled transactions |
| **User** | Retrieve authenticated user info |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Streamable HTTP transport
- [x] Cloudflare Tunnel support
- [x] Core YNAB resource coverage (budgets, accounts, transactions, categories, months, payees, scheduled transactions)
- [x] Bearer token authentication (Authorization header + ?api_key query param)
- [ ] Write support (create/update transactions)
- [ ] Category budget assignment tools

See the [open issues](https://github.com/Npab19/ynab-mcp/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are welcome! If you have a suggestion, please fork the repo and create a pull request or open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Npab19/ynab-mcp](https://github.com/Npab19/ynab-mcp)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [YNAB API Documentation](https://api.ynab.com/)
* [Model Context Protocol](https://modelcontextprotocol.io)
* [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
* [Img Shields](https://shields.io)
* [Best-README-Template](https://github.com/Npab19/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/Npab19/ynab-mcp.svg?style=for-the-badge
[contributors-url]: https://github.com/Npab19/ynab-mcp/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Npab19/ynab-mcp.svg?style=for-the-badge
[forks-url]: https://github.com/Npab19/ynab-mcp/network/members
[stars-shield]: https://img.shields.io/github/stars/Npab19/ynab-mcp.svg?style=for-the-badge
[stars-url]: https://github.com/Npab19/ynab-mcp/stargazers
[issues-shield]: https://img.shields.io/github/issues/Npab19/ynab-mcp.svg?style=for-the-badge
[issues-url]: https://github.com/Npab19/ynab-mcp/issues
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org
[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://docker.com
[Cloudflare]: https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=cloudflare&logoColor=white
[Cloudflare-url]: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
[YNAB]: https://img.shields.io/badge/YNAB-678D41?style=for-the-badge&logo=ynab&logoColor=white
[YNAB-url]: https://api.ynab.com/
