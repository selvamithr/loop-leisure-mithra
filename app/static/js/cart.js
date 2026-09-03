/**
 * ========================================================================
 * Loop & Leisure by Mithra - Cart Controller (cart.js)
 * ========================================================================
 * Handles:
 *   - Navbar cart badge count (loaded on every page)
 *   - Add to Cart (from product page)
 *   - Cart page: quantity update, item removal, live totals
 * ========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    updateCartBadge();
    initCartPageControls();
});

/* ── Update Navbar Cart Badge ── */
function updateCartBadge() {
    fetch('/cart/count')
        .then(res => res.json())
        .then(data => {
            const badge = document.getElementById('cartBadge');
            if (!badge) return;
            if (data.cart_count > 0) {
                badge.textContent = data.cart_count;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        })
        .catch(() => {});
}

/* ── Add to Cart (callable from product page) ── */
function addToCart(productId, quantity = 1) {
    fetch('/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(async res => {
        if (res.status === 401) {
            const data = await res.json();
            if (data.redirect) window.location.href = data.redirect;
            return null;
        }
        return res.json();
    })
    .then(data => {
        if (data && data.success) {
            const badge = document.getElementById('cartBadge');
            if (badge) {
                badge.textContent = data.cart_count;
                badge.style.display = 'flex';
            }
            // Show feedback
            showCartNotification('Added to cart!');
        }
    })
    .catch(() => {});
}

/* ── Cart Page Controls ── */
function initCartPageControls() {
    // Plus buttons
    document.querySelectorAll('.qty-plus-cart').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const item = btn.closest('.cart-item');
            const valEl = item.querySelector('.qty-value');
            let qty = parseInt(valEl.textContent) + 1;
            if (qty > 10) qty = 10;
            updateCartItem(id, qty);
        });
    });

    // Minus buttons
    document.querySelectorAll('.qty-minus-cart').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const item = btn.closest('.cart-item');
            const valEl = item.querySelector('.qty-value');
            let qty = parseInt(valEl.textContent) - 1;
            if (qty < 1) qty = 1;
            updateCartItem(id, qty);
        });
    });

    // Remove buttons
    document.querySelectorAll('.cart-item-remove').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            removeCartItem(id);
        });
    });
}

function updateCartItem(productId, quantity) {
    fetch('/cart/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Reload the page to reflect new totals
            window.location.reload();
        }
    })
    .catch(() => {});
}

function removeCartItem(productId) {
    fetch('/cart/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    })
    .catch(() => {});
}

/* ── Toast Notification ── */
function showCartNotification(message) {
    // Remove existing
    const existing = document.querySelector('.cart-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'cart-toast';
    toast.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> ${message}`;
    document.body.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add('show'));

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}
