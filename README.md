Scrapling MCP Server on AWS Lightsail

«A high-performance web extraction MCP server that turns live web content into LLM-ready Markdown — deploy once, then plug it into your AI IDEs, agents, RAG pipelines, and automation workflows.»

""AWS" (https://img.shields.io/badge/AWS-Lightsail-orange?logo=amazon-aws)" (https://aws.amazon.com/lightsail/)
""MCP" (https://img.shields.io/badge/MCP-Compatible-blue)" (https://modelcontextprotocol.io/)
""Python" (https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)" (https://www.python.org/)
""Docker" (https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)" (https://www.docker.com/)
""Scrapling" (https://img.shields.io/badge/Scrapling-Web%20Extraction-green)" (https://scrapling.readthedocs.io/)

Overview

Modern AI applications increasingly need access to fresh, structured, external knowledge.

Instead of implementing web scraping separately inside every RAG system or AI agent, this project exposes Scrapling's web extraction capabilities through the Model Context Protocol (MCP).

Once deployed, any MCP-compatible AI client can connect to the server and use it as a reusable web data-ingestion component.

                    ┌──────────────────────┐
                    │   AI IDE / AI Agent   │
                    │ Claude / MCP Client   │
                    └──────────┬───────────┘
                               │
                               │ MCP
                               ▼
                    ┌──────────────────────┐
                    │   Scrapling MCP      │
                    │       Server         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Web            │
                    │  Dynamic / Static    │
                    │      Content         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Markdown        │
                    │   LLM-ready Data     │
                    └──────────┬───────────┘
                               │
                               ▼
             ┌─────────────────────────────────┐
             │ RAG / Embeddings / Vector DB /  │
             │ Knowledge Base / Agent Memory   │
             └─────────────────────────────────┘

---

Why MCP for Web Extraction?

Traditionally, every AI application that needs web data implements its own:

- HTTP requests
- HTML parsing
- browser automation
- dynamic page handling
- extraction logic
- retry mechanisms
- content normalization

This creates duplicated infrastructure.

With MCP, web extraction becomes a shared capability.

                    Before

RAG App ────────► Scraper
Agent ──────────► Scraper
Research Tool ──► Scraper
AI IDE ──────────► Scraper

                    ↓

             Multiple implementations


                    After

                 ┌──────────────┐
RAG App ────────► │              │
Agent ──────────► │ Scrapling   │
AI IDE ──────────►│ MCP Server  │
Research ────────►│              │
                 └──────────────┘

                 One capability
                 Multiple clients

Deploy the server once and reuse it across MCP-compatible workflows.

---

Not Just a Web Scraper

The core idea behind this project is broader than scraping.

For many LLM applications, external information eventually needs to become a representation that can be:

1. Parsed
2. Cleaned
3. Structured
4. Chunked
5. Embedded
6. Indexed
7. Retrieved

Markdown is particularly useful in this pipeline because it preserves useful document hierarchy:

Web Page
   │
   ▼
Scrapling
   │
   ▼
Markdown
   │
   ├── Heading
   ├── Subheading
   ├── Paragraph
   ├── List
   ├── Table
   └── Links
   │
   ▼
Chunking
   │
   ▼
Embeddings
   │
   ▼
Vector Database
   │
   ▼
RAG / Agent

This makes the MCP server useful as an LLM data insertion / ingestion layer rather than only as a scraping utility.

---

Features

- MCP-compatible web extraction
- Powered by Scrapling
- Designed for AI agents and AI IDEs
- Markdown-oriented output
- Suitable for RAG ingestion pipelines
- Containerized with Docker
- Deployable on AWS Lightsail
- Reusable across multiple AI applications
- Separates data acquisition from the AI application itself
- Can be integrated into agentic workflows

---

Architecture

                         Internet
                            │
                            ▼
                    ┌───────────────┐
                    │      Web      │
                    └───────┬───────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │     Scrapling     │
                  │  Extraction Layer │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    MCP Server     │
                  │   Tool Interface  │
                  └─────────┬─────────┘
                            │
                       MCP Protocol
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
           AI IDE         Agent          RAG
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                    Markdown / Data
                            │
                            ▼
                 ┌────────────────────┐
                 │ LLM Data Pipeline  │
                 └──────────┬─────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │ Embeddings / DB    │
                 └──────────┬─────────┘
                            │
                            ▼
                         LLM / RAG

---

Technology Stack

Component| Technology
Web Extraction| Scrapling
Protocol| Model Context Protocol (MCP)
Language| Python
Containerization| Docker
Cloud| AWS Lightsail
CI/CD| GitHub Actions
Output| Markdown / Structured Content
AI Integration| MCP-compatible clients

---

Project Structure

.
├── src/
│   └── ...
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── .gitignore
├── docker-compose.yml
└── README.md

«Adjust the structure above if your repository uses a different source layout.»

---

Running Locally

1. Clone the repository

git clone https://github.com/Santhosh-p653/aws-mcp-test.git
cd aws-mcp-test

2. Install dependencies

Create a virtual environment:

python -m venv .venv

Activate it:

Linux / macOS

source .venv/bin/activate

Windows

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

---

Run with Docker

Build the image:

docker build -t scrapling-mcp .

Run the container:

docker run -d \
  --name scrapling-mcp \
  -p 8000:8000 \
  scrapling-mcp

Verify that the container is running:

docker ps

---

Deploy to AWS Lightsail

The project is designed to run as a containerized service on AWS Lightsail.

High-level deployment flow:

GitHub
   │
   │ Push
   ▼
GitHub Actions
   │
   │ Build
   ▼
Docker Image
   │
   │ Deploy
   ▼
AWS Lightsail
   │
   ▼
Scrapling MCP Server
   │
   ▼
MCP-Compatible AI Clients

Deployment Steps

1. Create an AWS Lightsail container service

Create a Lightsail container service from the AWS Console or AWS CLI.

2. Build the Docker image

docker build -t scrapling-mcp .

3. Push/deploy the container

Configure the Lightsail container deployment using the image produced by your CI/CD workflow.

4. Configure environment variables

Keep credentials and deployment configuration outside the repository.

For example:

AWS_REGION=
LIGHTSAIL_SERVICE=
CONTAINER_NAME=

Never commit secrets or credentials to Git.

---

GitHub Actions

The repository can use GitHub Actions to automate deployment.

Example workflow:

git push
    │
    ▼
GitHub Actions
    │
    ├── Checkout
    │
    ├── Configure AWS credentials
    │
    ├── Build container
    │
    ├── Push/deploy
    │
    └── Update Lightsail

This means the deployment can follow a simple workflow:

git add .
git commit -m "update scraper"
git push origin main

After the workflow completes, the updated MCP server is deployed.

---

Using the MCP Server

Once the server is deployed, connect its MCP endpoint to an MCP-compatible AI client.

Conceptually:

AI Client
    │
    │ MCP
    ▼
https://your-mcp-server.example.com
    │
    ▼
Scrapling
    │
    ▼
Web Content

The AI client can then invoke the exposed tools as part of its workflow.

This makes the server behave like a plugin for AI applications.

Instead of writing custom scraping code inside every project:

AI Application
      │
      ├── RAG
      ├── Agents
      ├── Research
      └── Automation
             │
             ▼
          MCP Server
             │
             ▼
          Scrapling

---

RAG Integration

A typical RAG pipeline can use this server as the ingestion layer:

                 ┌──────────────┐
                 │ Web Sources  │
                 └──────┬───────┘
                        │
                        ▼
                Scrapling MCP
                        │
                        ▼
                    Markdown
                        │
                        ▼
                 Document Parser
                        │
                        ▼
                    Chunking
                        │
                        ▼
                   Embeddings
                        │
                        ▼
                  Vector Store
                        │
                        ▼
                     Retriever
                        │
                        ▼
                       LLM

Possible downstream components include:

- Qdrant
- PostgreSQL + pgvector
- Elasticsearch
- OpenSearch
- Chroma
- FAISS
- Custom knowledge stores

The MCP server remains independent of the downstream storage layer.

---

Agentic Workflow

The server can also become a tool available to an AI agent.

For example:

User
 │
 ▼
AI Agent
 │
 ├── Decide what information is required
 │
 ├── Call Scrapling MCP
 │
 ├── Extract relevant content
 │
 ├── Transform/use Markdown
 │
 ├── Store information
 │
 └── Generate final response

This allows the agent to dynamically acquire information instead of relying only on static training data or previously indexed documents.

---

Why Markdown?

Markdown provides a useful intermediate representation for LLM pipelines because it preserves semantic structure.

For example:

# AWS Lambda

## Overview

AWS Lambda is a serverless compute service.

## Features

- Event-driven execution
- Automatic scaling
- Pay-per-use pricing

## Architecture

### Invocation

Lambda functions can be invoked through multiple AWS services.

Compared with raw HTML:

<div>
    <h1>AWS Lambda</h1>
    <div>
        <h2>Overview</h2>
        ...
    </div>
</div>

Markdown is generally easier to:

- inspect
- clean
- chunk
- process
- store
- pass to LLM pipelines

The goal is therefore not simply:

«"Scrape a webpage."»

It is:

«Acquire external knowledge in a form that can naturally enter an LLM data pipeline.»

---

Use Cases

RAG Systems

Automatically acquire fresh web information before indexing it.

AI Research Agents

Allow agents to retrieve and analyze information from live websites.

Knowledge Bases

Build continuously updated knowledge repositories.

AI IDEs

Give coding assistants an external web extraction capability through MCP.

Documentation Ingestion

Convert online documentation into Markdown suitable for downstream processing.

Agentic Automation

Use web extraction as one tool among many in an autonomous workflow.

---

Performance-Oriented Design

The architecture separates the web acquisition layer from the AI application.

Instead of:

Every AI Application
        │
        └── Custom Scraper

the approach becomes:

                    ┌───────────────┐
                    │ Scrapling MCP │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
             RAG          Agent         AI IDE

This allows scraping infrastructure to be deployed once and reused across multiple workflows.

---

Security Considerations

When deploying the server publicly:

- Do not expose AWS credentials in the container.
- Use HTTPS in production.
- Restrict network access where appropriate.
- Validate requested URLs.
- Apply rate limits where required.
- Monitor resource consumption.
- Avoid scraping websites in violation of their terms or applicable laws.
- Keep secrets in environment variables or a dedicated secrets manager.

---

Production Recommendations

For a production deployment, consider adding:

- Authentication
- API/MCP access control
- HTTPS
- Rate limiting
- Request logging
- Observability
- Retry policies
- Caching
- URL allowlists
- Resource limits
- Health checks
- Monitoring and alerting

---

Future Improvements

Potential extensions include:

- [ ] Authentication for MCP clients
- [ ] URL/domain allowlisting
- [ ] Content caching
- [ ] Distributed crawling
- [ ] Queue-based ingestion
- [ ] Automatic document chunking
- [ ] Direct vector database integration
- [ ] S3-based document storage
- [ ] Crawl scheduling
- [ ] Observability dashboard
- [ ] Multi-user access control

---

Example End-to-End Workflow

A complete AI knowledge ingestion workflow could look like:

                User / Agent
                     │
                     ▼
              MCP-Compatible IDE
                     │
                     ▼
             Scrapling MCP Server
                     │
                     ▼
                  Website
                     │
                     ▼
                Markdown
                     │
                     ▼
             Document Processing
                     │
                     ▼
                  Chunking
                     │
                     ▼
                Embeddings
                     │
                     ▼
                Vector DB
                     │
                     ▼
                 Retriever
                     │
                     ▼
                    LLM
                     │
                     ▼
               Final Response

---

Repository

GitHub:

https://github.com/Santhosh-p653/aws-mcp-test

---

Technical Article

I documented the architecture, deployment, and motivation behind this project on AWS Builder Center:

https://builder.aws.com/content/3IEgYoU99cYRY2pNQPXqDiqxuTB/ugmdu-supercharging-agentic-ai-with-fast-web-scraping-using-scrapling-mcp-and-aws-lightsail

---

Contributing

Contributions, ideas, improvements, and experiments are welcome.

If you build something using this MCP server, feel free to open an issue or pull request and share the workflow.

---

Author

Santhosh P

Building systems around:

- AI Agents
- RAG
- MCP
- Cloud Infrastructure
- Web Data Pipelines
- AI/ML

GitHub:
https://github.com/Santhosh-p653

---

Key Idea

«Deploy the scraping capability once. Plug it into your AI workflows whenever you need fresh, structured web data.»

Scrapling + MCP turns web extraction into a reusable infrastructure component for the modern LLM stack.