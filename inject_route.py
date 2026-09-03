new_route = '''
@customer_bp.route('/my-orders/<order_number>')
@login_required
def order_detail(order_number):
    """Customer order detail + tracking page.
    Only the owning customer may access this view.
    """
    from app.database.models import Order
    customer = _get_current_customer()
    order = Order.query.filter_by(order_number=order_number).first_or_404()

    # Ownership check - 403 if this order belongs to someone else
    if order.customer_id != customer.id:
        from flask import abort
        abort(403)

    # Compute tracking stage (0-indexed, 0..5)
    # Stages:
    #   0  Order Placed       - always done once order exists
    #   1  Payment Verified   - payment_status in ('Advance Paid', 'Fully Paid')
    #   2  Production Started - production_status in ('Started', 'Completed')
    #   3  Completed          - production_status == 'Completed'
    #   4  Dispatched         - order_status in ('Dispatched', 'Delivered')
    #   5  Delivered          - order_status == 'Delivered'

    ps  = order.payment_status
    prs = order.production_status
    os  = order.order_status

    if os == 'Delivered':
        stage = 5
    elif os == 'Dispatched':
        stage = 4
    elif prs == 'Completed':
        stage = 3
    elif prs == 'Started':
        stage = 2
    elif ps in ('Advance Paid', 'Fully Paid'):
        stage = 1
    else:
        stage = 0

    tracking_stages = [
        {'label': 'Order Placed',       'desc': 'Your order has been received.'},
        {'label': 'Payment Verified',   'desc': 'Advance payment confirmed by Mithra.'},
        {'label': 'Production Started', 'desc': 'Crocheting has begun — made just for you.'},
        {'label': 'Completed',          'desc': 'Your creation is finished and quality-checked.'},
        {'label': 'Dispatched',         'desc': 'Handed to courier and on its way.'},
        {'label': 'Delivered',          'desc': 'Arrived with love. Enjoy your piece!'},
    ]

    return render_template(
        'customer/order_detail.html',
        order=order,
        tracking_stages=tracking_stages,
        current_stage=stage,
    )

'''

path = r'c:/Users/sasi6/OneDrive/Desktop/loop & leisure ~mithra/app/customer/routes.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert after my_orders function (before the /product/<slug>/review route)
marker = "@customer_bp.route('/product/<slug>/review', methods=['POST'])"
if marker not in content:
    print("ERROR: marker not found")
else:
    content = content.replace(marker, new_route + marker)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Route injected successfully.")
