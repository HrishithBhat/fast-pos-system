from ..schemas.order import PriceRequest, PriceResponse

TAX_DEFAULT = 0.0

def price_cart(req: PriceRequest, tax_rate: float = TAX_DEFAULT) -> PriceResponse:
    subtotal = 0.0
    tax_total = 0.0
    discount_total = 0.0
    for item in req.items:
        # Simplified pricing: unit price must be supplied by caller in full implementation
        # Here assume product price is sent pre-fetched; in production, fetch product by id
        # and compute taxes/discounts per tenant settings.
        unit_price = 0.0
        qty = item.quantity
        subtotal += unit_price * qty
    tax_total = subtotal * tax_rate / 100.0
    grand_total = subtotal + tax_total - discount_total
    return PriceResponse(subtotal=subtotal, tax_total=tax_total, discount_total=discount_total, grand_total=grand_total)
