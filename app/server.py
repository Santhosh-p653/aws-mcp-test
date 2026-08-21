import os
import httpx
import platform
import psutil
import datetime
from fastmcp import FastMCP
from starlette.responses import JSONResponse

# Initialize FastMCP Server
mcp = FastMCP("my-custom-server")

# -------------------------------------------------------------
# 1. AWS Lightsail Health Check Endpoint
# -------------------------------------------------------------
@mcp.custom_route("/healthz", methods=["GET"])
async def health_check(request):
    """Health check endpoint required by AWS Lightsail."""
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "service": "mcp-server"
    })

# -------------------------------------------------------------
# 2. Production-Ready Tools
# -------------------------------------------------------------

@mcp.tool()
async def fetch_web_page(url: str, max_chars: int = 4000) -> str:
    """Fetch and return the text content of any public URL or API endpoint."""
    headers = {"User-Agent": "FastMCP-Bot/1.0"}
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            text = response.text
            if len(text) > max_chars:
                return text[:max_chars] + f"\n\n[... Truncated: showing first {max_chars} characters]"
            return text
        except Exception as e:
            return f"Error fetching URL '{url}': {str(e)}"

@mcp.tool()
def get_system_metrics() -> dict:
    """Get live compute metrics from the hosting container (CPU, Memory, Disk)."""
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory": {
            "total_mb": round(psutil.virtual_memory().total / (1024 * 1024), 2),
            "available_mb": round(psutil.virtual_memory().available / (1024 * 1024), 2),
            "used_percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total_gb": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
            "free_gb": round(psutil.disk_usage('/').free / (1024 ** 3), 2),
            "used_percent": psutil.disk_usage('/').percent
        }
    }

@mcp.tool()
def evaluate_math_expression(expression: str) -> str:
    """Safely calculate a mathematical expression without raw arbitrary execution."""
    allowed_chars = set("0123456789+-*/().,% eE")
    if not all(c in allowed_chars for c in expression):
        return "Error: Expression contains unsupported or unsafe characters."
    try:
        # Safe math evaluation namespace
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"

@mcp.tool()
def analyze_text_statistics(text: str) -> dict:
    """Compute word count, character count, estimated reading time, and lexical density."""
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))
    unique_words = len(set(word.lower() for word in words))
    
    # 200 WPM average reading speed
    reading_time_seconds = round((word_count / 200) * 60, 1) if word_count > 0 else 0

    return {
        "word_count": word_count,
        "unique_words": unique_words,
        "lexical_diversity": round(unique_words / word_count, 3) if word_count > 0 else 0,
        "char_count_with_spaces": char_count,
        "char_count_no_spaces": char_count_no_spaces,
        "est_reading_time_seconds": reading_time_seconds
    }

# -------------------------------------------------------------
# 3. Dynamic Resources
# -------------------------------------------------------------

@mcp.resource("system://env")
def get_environment_info() -> str:
    """Return non-sensitive runtime container environment properties."""
    return f"Container Host: {platform.node()} | Architecture: {platform.machine()}"

# -------------------------------------------------------------
# 4. Entrypoint
# -------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
