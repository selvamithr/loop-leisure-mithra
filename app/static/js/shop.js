/**
 * ========================================================================
 * Loop & Leisure by Mithra - Shop Page Controller (shop.js)
 * ========================================================================
 * Description: Manages the shop page functionalities:
 *   - Instant product filtering by category
 * ========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    initShopFilters();
});

function initShopFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const products = document.querySelectorAll('.shop-product-card');

    if (!filterBtns.length || !products.length) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            // Filter products
            products.forEach(product => {
                if (filterValue === 'all' || product.getAttribute('data-category') === filterValue) {
                    product.style.display = 'flex';
                    // Add a tiny animation reset for smooth appearing
                    product.style.animation = 'none';
                    product.offsetHeight; /* trigger reflow */
                    product.style.animation = null; 
                } else {
                    product.style.display = 'none';
                }
            });
        });
    });
}
