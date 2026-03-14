"""
Module 3B: Building an MCP Server
===================================
Create a Model Context Protocol (MCP) server for the product catalog.

This demonstrates:
- Building an MCP server using FastMCP
- Exposing tools and resources via MCP
- The MCP protocol (stdio transport)

Usage (standalone):
    python module_02_tools_mcp/mcp_server.py

Usage (with agent - see agent_with_mcp.py):
    The agent connects to this server via stdio transport.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP
from shared.data import PRODUCTS, ORDERS

# ──────────────────────────────────────────────
# Create the MCP Server
# ──────────────────────────────────────────────
mcp = FastMCP(
    name="TechStore Catalog Server",
    instructions="MCP server providing access to TechStore's product catalog and order system.",
)


# ──────────────────────────────────────────────
# MCP Tools - Exposed to any MCP client (including agents)
# ──────────────────────────────────────────────


@mcp.tool()
def get_product_details(sku: str) -> dict:
    """Get detailed information about a product by SKU.

    Args:
        sku: The product SKU (e.g., SKU-001)
    """
    sku = sku.upper().strip()
    if sku in PRODUCTS:
        return {"sku": sku, **PRODUCTS[sku]}
    return {"error": f"Product {sku} not found"}


@mcp.tool()
def list_all_products(category: str = "") -> list[dict]:
    """List all products, optionally filtered by category.

    Args:
        category: Optional category filter (Electronics, Furniture, Accessories)
    """
    results = []
    for sku, product in PRODUCTS.items():
        if category and product["category"].lower() != category.lower():
            continue
        results.append({"sku": sku, **product})
    return results


@mcp.tool()
def get_order_status(order_id: str) -> dict:
    """Get the current status of a customer order.

    Args:
        order_id: The order ID (e.g., ORD-10001)
    """
    order_id = order_id.upper().strip()
    if order_id in ORDERS:
        order = ORDERS[order_id]
        return {
            "order_id": order_id,
            "status": order["status"],
            "tracking_number": order.get("tracking_number"),
            "items": [item["name"] for item in order["items"]],
            "total": order["total"],
        }
    return {"error": f"Order {order_id} not found"}


@mcp.tool()
def search_catalog(query: str) -> list[dict]:
    """Search products by keyword in name or description.

    Args:
        query: Search keyword
    """
    query_lower = query.lower()
    results = []
    for sku, product in PRODUCTS.items():
        if (query_lower in product["name"].lower()
                or query_lower in product["description"].lower()):
            results.append({"sku": sku, "name": product["name"], "price": product["price"],
                            "in_stock": product["in_stock"]})
    return results if results else [{"message": "No products found"}]


# ──────────────────────────────────────────────
# MCP Resources - Static data the client can read
# ──────────────────────────────────────────────


@mcp.resource("catalog://categories")
def list_categories() -> str:
    """List all available product categories."""
    categories = sorted(set(p["category"] for p in PRODUCTS.values()))
    return ", ".join(categories)


@mcp.resource("catalog://stats")
def catalog_stats() -> str:
    """Get catalog statistics."""
    total = len(PRODUCTS)
    in_stock = sum(1 for p in PRODUCTS.values() if p["in_stock"])
    return f"Total products: {total}, In stock: {in_stock}, Out of stock: {total - in_stock}"


# ──────────────────────────────────────────────
# Run the server
# ──────────────────────────────────────────────
if __name__ == "__main__":
    # Run as stdio MCP server (for connecting from agents)
    mcp.run()
