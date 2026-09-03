/**
 * ========================================================================
 * Loop & Leisure by Mithra - Global Client Controllers (main.js)
 * ========================================================================
 * Description: Main javascript controller managing frontend micro-interactions,
 * page transitions, accessibility helpers, and image loading optimization.
 * Includes interactive controllers for the responsive navigation bar.
 * ========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize application modules
    initNavbarScroll();
    initMobileMenu();
});

/**
 * ---------------------------------------------------------------------
 * 1. Navbar Scroll Controller
 * ---------------------------------------------------------------------
 * Purpose: Toggle transparency, box shadow, and padding on navbar scroll.
 */
function initNavbarScroll() {
    const navbar = document.getElementById('navbar-header');
    if (!navbar) return;

    // Check scroll offset and toggle class
    const checkScroll = () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    // Run on init and listen to window scroll event
    checkScroll();
    window.addEventListener('scroll', checkScroll, { passive: true });
}

/**
 * ---------------------------------------------------------------------
 * 2. Mobile Navigation Drawer Controller
 * ---------------------------------------------------------------------
 * Purpose: Manage opening/closing mobile overlay drawer with keyboard trapping.
 */
function initMobileMenu() {
    const toggleBtn = document.getElementById('menu-toggle-btn');
    const closeBtn = document.getElementById('menu-close-btn');
    const drawer = document.getElementById('mobile-drawer');
    const overlay = document.getElementById('mobile-drawer-overlay');

    if (!toggleBtn || !drawer || !closeBtn || !overlay) return;

    // Focus Management references
    const focusableElementsString = 'button, a, input, select, textarea';
    let focusableElements = [];
    let firstFocusableElement = null;
    let lastFocusableElement = null;

    const updateFocusableElements = () => {
        focusableElements = Array.from(drawer.querySelectorAll(focusableElementsString));
        firstFocusableElement = focusableElements[0];
        lastFocusableElement = focusableElements[focusableElements.length - 1];
    };

    // Open Mobile Drawer Menu
    const openMenu = () => {
        drawer.classList.add('active');
        toggleBtn.setAttribute('aria-expanded', 'true');
        drawer.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden'; // Stop body scrolling

        // Update target focus list
        updateFocusableElements();
        
        // Trap focus to close button
        if (closeBtn) closeBtn.focus();
    };

    // Close Mobile Drawer Menu
    const closeMenu = () => {
        drawer.classList.remove('active');
        toggleBtn.setAttribute('aria-expanded', 'false');
        drawer.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = ''; // Restore body scrolling
        
        // Restore focus to original trigger toggle
        toggleBtn.focus();
    };

    // Keyboard tab trapping inside modal
    const trapFocus = (e) => {
        if (e.key !== 'Tab') return;
        
        updateFocusableElements();

        if (e.shiftKey) { // Shift + Tab: backwards navigation
            if (document.activeElement === firstFocusableElement) {
                lastFocusableElement.focus();
                e.preventDefault();
            }
        } else { // Tab: forwards navigation
            if (document.activeElement === lastFocusableElement) {
                firstFocusableElement.focus();
                e.preventDefault();
            }
        }
    };

    // Bind Event Listeners
    toggleBtn.addEventListener('click', openMenu);
    closeBtn.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);

    // Escape Key listener to close active drawer
    window.addEventListener('keyup', (e) => {
        if (e.key === 'Escape' && drawer.classList.contains('active')) {
            closeMenu();
        }
    });

    // Keyboard Tab binding inside active drawer
    drawer.addEventListener('keydown', trapFocus);
}
