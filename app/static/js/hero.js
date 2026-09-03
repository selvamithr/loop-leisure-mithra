/**
 * ========================================================================
 * Loop & Leisure by Mithra - Hero Carousel Controller (hero.js)
 * ========================================================================
 * Description: Manages the hero section image carousel:
 *   - Prev / Next arrow navigation
 *   - Dot indicator sync
 *   - Auto-advance with pause on hover
 *   - Touch / swipe gesture support
 *   - ARIA live-region updates for accessibility
 * ========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    initHeroCarousel();
});

function initHeroCarousel() {
    const track    = document.getElementById('carouselTrack');
    const prevBtn  = document.getElementById('carouselPrev');
    const nextBtn  = document.getElementById('carouselNext');
    const dotsWrap = document.getElementById('carouselDots');

    if (!track || !prevBtn || !nextBtn || !dotsWrap) return;

    const slides     = Array.from(track.querySelectorAll('.carousel-slide'));
    const dots       = Array.from(dotsWrap.querySelectorAll('.carousel-dot'));
    const totalSlides = slides.length;
    let currentIndex  = 0;
    let autoTimer     = null;
    const AUTO_DELAY  = 5000; // ms between auto-advances

    /* ── Core: move to slide at index ── */
    const goTo = (index) => {
        slides.forEach(slide => slide.classList.remove('active'));
        // Wrap around
        currentIndex = (index + totalSlides) % totalSlides;
        
        const activeSlide = slides[currentIndex];
        activeSlide.classList.add('active');
        
        // Update dynamic text
        const badgeEl = document.getElementById('heroBadge');
        const headingEl = document.getElementById('heroHeading');
        const subtextEl = document.getElementById('heroSubtext');
        
        if (badgeEl) {
            const badgeText = activeSlide.getAttribute('data-badge');
            if (badgeText) {
                badgeEl.style.display = 'inline-flex';
                badgeEl.innerHTML = badgeText;
            } else {
                badgeEl.style.display = 'none';
            }
        }
        if (headingEl) {
            headingEl.innerHTML = activeSlide.getAttribute('data-heading') || '';
        }
        if (subtextEl) {
            subtextEl.innerHTML = activeSlide.getAttribute('data-subtext') || '';
        }
        
        syncDots();
        updateAria();
    };

    /* ── Sync dot visual states ── */
    const syncDots = () => {
        dots.forEach((dot, i) => {
            const isActive = i === currentIndex;
            dot.classList.toggle('active', isActive);
            dot.setAttribute('aria-selected', String(isActive));
        });
    };

    /* ── Update ARIA labels for screen readers ── */
    const updateAria = () => {
        slides.forEach((slide, i) => {
            slide.setAttribute('aria-hidden', String(i !== currentIndex));
        });
    };

    /* ── Auto-advance ── */
    const startAuto = () => {
        clearInterval(autoTimer);
        autoTimer = setInterval(() => goTo(currentIndex + 1), AUTO_DELAY);
    };

    const stopAuto = () => clearInterval(autoTimer);

    /* ── Arrow bindings ── */
    prevBtn.addEventListener('click', () => {
        goTo(currentIndex - 1);
        startAuto(); // Reset timer on manual nav
    });

    nextBtn.addEventListener('click', () => {
        goTo(currentIndex + 1);
        startAuto();
    });

    /* ── Dot bindings ── */
    dots.forEach((dot) => {
        dot.addEventListener('click', () => {
            goTo(Number(dot.dataset.index));
            startAuto();
        });
    });

    /* ── Pause auto-advance on hover ── */
    const carousel = document.getElementById('heroCarousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', stopAuto);
        carousel.addEventListener('mouseleave', startAuto);
    }

    /* ── Touch / swipe support ── */
    let touchStartX = 0;

    track.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
    }, { passive: true });

    track.addEventListener('touchend', (e) => {
        const delta = touchStartX - e.changedTouches[0].clientX;
        if (Math.abs(delta) > 40) {
            goTo(delta > 0 ? currentIndex + 1 : currentIndex - 1);
            startAuto();
        }
    }, { passive: true });

    /* ── Keyboard support for arrows ── */
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft')  { goTo(currentIndex - 1); startAuto(); }
        if (e.key === 'ArrowRight') { goTo(currentIndex + 1); startAuto(); }
    });

    /* ── Initialise ── */
    goTo(0);
    startAuto();
}
