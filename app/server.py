import datetime
from fastmcp import FastMCP
from starlette.responses import JSONResponse
from scrapling.fetchers import Fetcher, StealthyFetcher
from duckduckgo_search import DDGS
from markdownify import markdownify as md

mcp = FastMCP("scrapling-knowledge-engine")

# -------------------------------------------------------------
# Lightsail Health Check Route
# -------------------------------------------------------------
@mcp.custom_route("/healthz", methods=["GET"])
async def health_check(request):
    return JSONResponse({
        "status": "healthy",
        "engine": "scrapling",
        "service": "scrapling-knowledge-engine",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })

# -------------------------------------------------------------
# Tool 1: Real-Time Web Search
# -------------------------------------------------------------
@mcp.tool()
def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the live web anonymously for current events, technical docs, or real-time data.
    Returns a list of results with title, snippet, and target URL.
    """
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body")
                })
        return results
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]

# -------------------------------------------------------------
# Tool 2: High-Speed Web Content Extractor (Scrapling HTTP)
# -------------------------------------------------------------
@mcp.tool()
def fetch_page_knowledge(url: str, max_length: int = 6000) -> dict:
    """
    Ultra-fast web content and knowledge extractor using Scrapling's high-speed HTTP engine.
    Extracts page title, metadata, main text, and clean LLM-ready markdown.
    """
    try:
        # Initialize Scrapling Fast Fetcher
        fetcher = Fetcher(auto_match=False)
        page = fetcher.get(url, stealthy_headers=True)

        if not page or page.status >= 400:
            return {"error": f"Failed to fetch page. HTTP Status: {page.status if page else 'Unknown'}"}

        # Extract title and headings
        title = page.css("title::text").get() or "No title"
        
        # Scrapling isolates main article/body content cleanly
        main_content = (
            page.css("article").get() or 
            page.css("main").get() or 
            page.css("#content").get() or 
            page.css("body").get() or ""
        )

        # Convert clean HTML to LLM Markdown
        clean_markdown = md(main_content, heading_style="ATX", strip=['script', 'style', 'nav', 'footer', 'aside'])
        
        # Format and truncate for token-budget optimization
        lines = [line.strip() for line in clean_markdown.splitlines() if line.strip()]
        formatted_output = "\n\n".join(lines)

        if len(formatted_output) > max_length:
            formatted_output = formatted_output[:max_length] + f"\n\n[... Truncated to fit token budget (max: {max_length} chars)]"

        return {
            "title": title,
            "url": url,
            "char_count": len(formatted_output),
            "content": formatted_output or "No text could be extracted."
        }
    except Exception as e:
        return {"error": f"Scrapling extraction error: {str(e)}"}

# -------------------------------------------------------------
# Tool 3: Stealth Extractor for Bot-Protected / Cloudflare Sites
# -------------------------------------------------------------
@mcp.tool()
def fetch_stealth_knowledge(url: str, max_length: int = 6000) -> dict:
    """
    Bypasses aggressive anti-bot protections (Cloudflare, Akamai, PerimeterX)
    using Scrapling's StealthyFetcher engine with real browser fingerprinting.
    """
    try:
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True)
        
        title = page.css("title::text").get() or "No title"
        main_content = page.css("article").get() or page.css("main").get() or page.css("body").get() or ""
        
        clean_markdown = md(main_content, heading_style="ATX", strip=['script', 'style', 'nav', 'footer', 'aside'])
        lines = [line.strip() for line in clean_markdown.splitlines() if line.strip()]
        formatted_output = "\n\n".join(lines)

        if len(formatted_output) > max_length:
            formatted_output = formatted_output[:max_length] + "\n\n[... Truncated]"

        return {
            "title": title,
            "url": url,
            "mode": "stealth",
            "content": formatted_output or "No text could be extracted."
        }
    except Exception as e:
        return {"error": f"Stealth extraction error: {str(e)}"}

# -------------------------------------------------------------
# Tool 4: Parallel Batch Knowledge Research
# -------------------------------------------------------------
@mcp.tool()
def batch_knowledge_extract(urls: list[str]) -> list[dict]:
    """
    Extracts structured content from multiple URLs in a single call for comparative RAG and synthesis.
    """
    results = []
    fetcher = Fetcher(auto_match=False)
    for target in urls[:5]:
        try:
            page = fetcher.get(target, stealthy_headers=True)
            title = page.css("title::text").get() or "No title"
            content = page.css("article").get() or page.css("main").get() or page.css("body").get() or ""
            clean_md = md(content, heading_style="ATX", strip=['script', 'style', 'nav', 'footer'])
            
            results.append({
                "url": target,
                "title": title,
                "summary_content": clean_md[:2000]
            })
        except Exception as e:
            results.append({"url": target, "error": str(e)})
    return results

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
