from flask import render_template, session, request, redirect, url_for, flash
from app import app
from models.cart import Cart


# AFTER (fixed)
def get_cart():
    cart_id = session.get('cart_id')
    if cart_id:
        cart = Cart.query.filter_by(id=cart_id, status=0).first()  # ✅ active cart only
        if cart:
            return cart

    # fallback: find active cart by user_id
    user_id = session.get('user_id')
    if user_id:
        return Cart.query.filter_by(user_id=user_id, status=0).first()  # ✅ filter by status

    return None


def get_total():
    cart = get_cart()

    if not cart or not cart.items:
        return 0

    total = 0

    for item in cart.items:
        price = item.price or 0
        quantity = item.quantity or 0
        total += float(price) * quantity

    return total


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    cart = get_cart()

    if not cart or not cart.items:
        flash("Your cart is empty", "warning")
        return redirect('/cart')

    items = cart.items
    total = get_total()

    # FIXED: do not redirect back to /payment
    if total <= 0:
        flash("Cart total is invalid", "warning")
        return redirect('/cart')

    if request.method == 'POST':
        customer_name = request.form.get("customer_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not customer_name or not email or not phone or not address:
            return render_template(
                'front/payment.html',
                cart_total=total,
                cart=cart,
                error="Please fill all fields"
            )

        session['checkout'] = {
            "customer_name": customer_name,
            "email": email,
            "phone": phone,
            "address": address
        }

        # Use this if your qr_payment route is normal @app.route
        return redirect(url_for('qr_payment'))

        # If qr_payment is inside blueprint, use like this instead:
        # return redirect(url_for('payment_bp.qr_payment'))

    return render_template(
        'front/payment.html',
        cart_total=total,
        cart=cart
    )