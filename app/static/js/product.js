/**
 * ========================================================================
 * Loop & Leisure by Mithra - Product Page Controller (product.js)
 * ========================================================================
 * Handles:
 *   - Thumbnail image switching
 *   - Quantity selector (+/-)
 *   - Accordion toggles
 *   - Wishlist heart toggle
 * ========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    initThumbnails();
    initQuantitySelector();
    initAccordions();
    initWishlist();
});

/* ── Thumbnail Gallery ── */
function initThumbnails() {
    const thumbs = document.querySelectorAll('.thumbnail-btn');
    const mainImg = document.getElementById('mainProductImage');
    if (!thumbs.length || !mainImg) return;

    thumbs.forEach(thumb => {
        thumb.addEventListener('click', () => {
            thumbs.forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
            const newSrc = thumb.getAttribute('data-img');
            mainImg.style.opacity = '0';
            setTimeout(() => {
                mainImg.src = newSrc;
                mainImg.style.opacity = '1';
            }, 200);
        });
    });
}

/* ── Quantity Selector ── */
function initQuantitySelector() {
    const minusBtn = document.querySelector('.qty-minus');
    const plusBtn = document.querySelector('.qty-plus');
    const input = document.querySelector('.qty-input');
    if (!minusBtn || !plusBtn || !input) return;

    minusBtn.addEventListener('click', () => {
        let val = parseInt(input.value) || 1;
        if (val > 1) input.value = val - 1;
    });

    plusBtn.addEventListener('click', () => {
        let val = parseInt(input.value) || 1;
        const max = parseInt(input.max) || 10;
        if (val < max) input.value = val + 1;
    });
}

/* ── Accordion Toggles ── */
function initAccordions() {
    const headers = document.querySelectorAll('.accordion-header');
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const body = header.nextElementSibling;
            const isOpen = body.classList.contains('open');
            const icon = header.querySelector('.accordion-icon');

            // Close all
            document.querySelectorAll('.accordion-body').forEach(b => b.classList.remove('open'));
            document.querySelectorAll('.accordion-header').forEach(h => {
                h.setAttribute('aria-expanded', 'false');
                const ic = h.querySelector('.accordion-icon');
                if (ic) ic.textContent = '+';
            });

            // Open clicked if it was closed
            if (!isOpen) {
                body.classList.add('open');
                header.setAttribute('aria-expanded', 'true');
                if (icon) icon.textContent = '−';
            }
        });
    });
}

/* ── Wishlist Heart Toggle ── */
function initWishlist() {
    const btn = document.querySelector('.wishlist-btn');
    if (!btn) return;
    btn.addEventListener('click', () => {
        btn.classList.toggle('wishlisted');
    });
}
