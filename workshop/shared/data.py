"""
Shared mock data for the SupportBot workshop.
Simulates a small e-commerce company's data.
"""

# ──────────────────────────────────────────────
# Product Catalog
# ──────────────────────────────────────────────
PRODUCTS = {
    "SKU-001": {
        "name": "Wireless Noise-Canceling Headphones",
        "price": 149.99,
        "category": "Electronics",
        "in_stock": True,
        "description": "Premium over-ear headphones with active noise cancellation and 30-hour battery life.",
    },
    "SKU-002": {
        "name": "Ergonomic Standing Desk",
        "price": 499.99,
        "category": "Furniture",
        "in_stock": True,
        "description": "Electric height-adjustable desk with memory presets and cable management.",
    },
    "SKU-003": {
        "name": "Mechanical Keyboard (Cherry MX Blue)",
        "price": 89.99,
        "category": "Electronics",
        "in_stock": False,
        "description": "Compact 75% mechanical keyboard with RGB backlighting and USB-C.",
    },
    "SKU-004": {
        "name": "4K Webcam with Ring Light",
        "price": 79.99,
        "category": "Electronics",
        "in_stock": True,
        "description": "Ultra HD webcam with built-in ring light and auto-focus.",
    },
    "SKU-005": {
        "name": "Laptop Backpack (Waterproof)",
        "price": 59.99,
        "category": "Accessories",
        "in_stock": True,
        "description": "Fits up to 17-inch laptops with USB charging port and anti-theft design.",
    },
}

# ──────────────────────────────────────────────
# Customer Orders
# ──────────────────────────────────────────────
ORDERS = {
    "ORD-10001": {
        "customer_name": "Alice Johnson",
        "customer_email": "alice@example.com",
        "items": [
            {"sku": "SKU-001", "name": "Wireless Noise-Canceling Headphones", "qty": 1, "price": 149.99},
        ],
        "total": 149.99,
        "status": "delivered",
        "tracking_number": "TRK-AAA111",
        "order_date": "2026-02-15",
        "delivery_date": "2026-02-20",
    },
    "ORD-10002": {
        "customer_name": "Bob Smith",
        "customer_email": "bob@example.com",
        "items": [
            {"sku": "SKU-002", "name": "Ergonomic Standing Desk", "qty": 1, "price": 499.99},
            {"sku": "SKU-004", "name": "4K Webcam with Ring Light", "qty": 1, "price": 79.99},
        ],
        "total": 579.98,
        "status": "shipped",
        "tracking_number": "TRK-BBB222",
        "order_date": "2026-03-01",
        "delivery_date": None,
    },
    "ORD-10003": {
        "customer_name": "Carol Davis",
        "customer_email": "carol@example.com",
        "items": [
            {"sku": "SKU-003", "name": "Mechanical Keyboard (Cherry MX Blue)", "qty": 2, "price": 89.99},
        ],
        "total": 179.98,
        "status": "processing",
        "tracking_number": None,
        "order_date": "2026-03-10",
        "delivery_date": None,
    },
    "ORD-10004": {
        "customer_name": "David Lee",
        "customer_email": "david@example.com",
        "items": [
            {"sku": "SKU-005", "name": "Laptop Backpack (Waterproof)", "qty": 1, "price": 59.99},
        ],
        "total": 59.99,
        "status": "return_requested",
        "tracking_number": "TRK-DDD444",
        "order_date": "2026-02-28",
        "delivery_date": "2026-03-05",
        "return_reason": "Wrong color received",
    },
}

# ──────────────────────────────────────────────
# FAQ / Knowledge Base
# ──────────────────────────────────────────────
FAQ = [
    {
        "question": "What is your return policy?",
        "answer": "We offer a 30-day return policy for all unused items in original packaging. "
                  "Defective items can be returned within 90 days. Refunds are processed within 5-7 business days.",
    },
    {
        "question": "How long does shipping take?",
        "answer": "Standard shipping takes 5-7 business days. Express shipping (2-3 days) is available "
                  "for an additional $9.99. Free shipping on orders over $100.",
    },
    {
        "question": "Do you offer international shipping?",
        "answer": "Yes, we ship to over 50 countries. International shipping typically takes 10-15 business days. "
                  "Customs duties and taxes are the responsibility of the buyer.",
    },
    {
        "question": "How can I track my order?",
        "answer": "You can track your order using the tracking number provided in your shipping confirmation email. "
                  "Visit our website and enter your order ID or tracking number on the Track Order page.",
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept Visa, Mastercard, American Express, PayPal, Apple Pay, and Google Pay. "
                  "All transactions are secured with SSL encryption.",
    },
    {
        "question": "How do I cancel an order?",
        "answer": "Orders can be cancelled within 2 hours of placement if they haven't been shipped yet. "
                  "Contact our support team or use the Cancel Order button in your account dashboard.",
    },
    {
        "question": "Do you offer warranty on products?",
        "answer": "All electronics come with a 1-year manufacturer warranty. Extended warranty (up to 3 years) "
                  "is available for purchase at checkout. Furniture items have a 2-year warranty.",
    },
    {
        "question": "How do I contact support?",
        "answer": "You can reach us via this chat, email at support@techstore.example.com, "
                  "or phone at 1-800-TECH-HELP (Mon-Fri 9am-6pm EST).",
    },
]

# ──────────────────────────────────────────────
# Support Tickets (for ticket creation demo)
# ──────────────────────────────────────────────
TICKETS: list[dict] = []
_ticket_counter = 5000


def next_ticket_id() -> str:
    global _ticket_counter
    _ticket_counter += 1
    return f"TKT-{_ticket_counter}"
