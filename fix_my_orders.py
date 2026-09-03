path = r'c:/Users/sasi6/OneDrive/Desktop/loop & leisure ~mithra/app/templates/customer/my_orders.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the escaped block with proper HTML
# The tool wrote literal \u003c sequences instead of <
content = content.replace('\\u003cdiv style="display: flex; gap: var(--spacing-sm); flex-wrap: wrap;"\\u003e', '<div style="display: flex; gap: var(--spacing-sm); flex-wrap: wrap;">')
content = content.replace('\\u003c/div\\u003e\n                             </div>', '</div>\n                             </div>')
content = content.replace("\\u003ca href=\"{{ url_for('customer.order_detail', order_number=order.order_number) }}\" class=\"btn btn-secondary btn-sm\"\\u003eTrack Order\\u003c/a\\u003e",
    "<a href=\"{{ url_for('customer.order_detail', order_number=order.order_number) }}\" class=\"btn btn-secondary btn-sm\">Track Order</a>")
content = content.replace("\\u003ca href=\"{{ url_for('customer.payment', order_number=order.order_number) }}\" class=\"btn btn-primary btn-sm\"\\u003ePay Advance (\\u0026#8377;{{ '%.2f' % order.advance_amount }})\\u003c/a\\u003e",
    "<a href=\"{{ url_for('customer.payment', order_number=order.order_number) }}\" class=\"btn btn-primary btn-sm\">Pay Advance (&#8377;{{ '%.2f' % order.advance_amount }})</a>")
content = content.replace("\\u003ca href=\"{{ url_for('customer.payment', order_number=order.order_number) }}\" class=\"btn btn-primary btn-sm\" style=\"background-color: var(--color-accent-gold); border-color: var(--color-accent-gold);\"\\u003ePay Remaining (\\u0026#8377;{{ '%.2f' % order.remaining_amount }})\\u003c/a\\u003e",
    "<a href=\"{{ url_for('customer.payment', order_number=order.order_number) }}\" class=\"btn btn-primary btn-sm\" style=\"background-color: var(--color-accent-gold); border-color: var(--color-accent-gold);\">Pay Remaining (&#8377;{{ '%.2f' % order.remaining_amount }})</a>")
content = content.replace("\\u003ca href=\"/product?slug=crochet-rose-bouquet#reviews\" class=\"btn btn-secondary btn-sm\"\\u003eWrite Review\\u003c/a\\u003e",
    "<a href=\"/product?slug=crochet-rose-bouquet#reviews\" class=\"btn btn-secondary btn-sm\">Write Review</a>")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify no escaped sequences remain
remaining = content.count('\\u003c')
print(f"Fix applied. Remaining escaped sequences: {remaining}")

# Quick sanity check
if 'Track Order' in content and 'order_detail' in content:
    print("Track Order link confirmed present.")
else:
    print("ERROR: Track Order link not found!")
