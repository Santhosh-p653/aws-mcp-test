from fastmcp import FastMCP

mcp = FastMCP("my-custom-server")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

@mcp.resource("data://example")
def get_example_data() -> str:
    """Return some example resource data."""
    return "This is my custom resource."

if __name__ == "__main__":
    # Run with streamable-http transport on port 8080
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
