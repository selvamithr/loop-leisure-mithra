css_to_append = """

/* =====================================================================
   ORDER DETAIL / TRACKING PAGE  (order_detail.html)
   ===================================================================== */

/* Page wrapper uses existing .section padding */
.od-page { min-height: 75vh; }

/* ── Back link ── */
.od-back-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.875rem;
    font-weight: var(--fw-medium);
    color: var(--color-text-secondary);
    text-decoration: none;
    margin-bottom: 1.5rem;
    transition: color var(--transition-fast);
}
.od-back-link:hover { color: var(--color-primary); }

/* ── Page header ── */
.od-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--color-border-light);
}
.od-order-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    margin-bottom: 4px;
}
.od-order-number {
    font-family: var(--font-family-logo);
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 600;
    color: var(--color-primary);
    margin: 0;
    line-height: 1.2;
}
.od-header-meta { text-align: right; }
.od-meta-value {
    font-size: 0.9375rem;
    font-weight: var(--fw-medium);
    color: var(--color-text-primary);
    margin: 0;
}

/* ── Two-column layout ── */
.od-layout {
    display: grid;
    gap: 1.75rem;
}
@media (min-width: 900px) {
    .od-layout {
        grid-template-columns: 1fr 1.4fr;
        align-items: start;
    }
}

/* ── Card shell ── */
.od-card {
    background-color: var(--color-card-bg);
    border: 1px solid var(--color-border-light);
    border-radius: var(--border-radius-lg);
    padding: 1.75rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.25rem;
}
.od-card:last-child { margin-bottom: 0; }
.od-card-title {
    font-family: var(--font-family-headings);
    font-size: 0.8125rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    margin-bottom: 1.5rem;
}

/* ── Tracking stepper ── */
.od-stepper {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0;
}

.od-step {
    position: relative;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding-bottom: 1.75rem;
}
.od-step:last-child { padding-bottom: 0; }

/* connector line between steps */
.od-step-connector {
    position: absolute;
    left: 15px;
    top: 32px;
    width: 2px;
    bottom: 0;
    border-radius: 2px;
}
.od-step-connector--done     { background: var(--color-primary); }
.od-step-connector--upcoming { background: var(--color-border); }

/* circle icon */
.od-step-icon {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
    position: relative;
    transition: background-color var(--transition-normal), border-color var(--transition-normal);
}

/* done state */
.od-step--done .od-step-icon {
    background-color: var(--color-primary);
    border: 2px solid var(--color-primary);
    color: white;
}

/* active / current state */
.od-step--active .od-step-icon {
    background-color: var(--color-card-bg);
    border: 2px solid var(--color-primary);
    color: var(--color-primary);
}

/* upcoming state */
.od-step--upcoming .od-step-icon {
    background-color: var(--color-bg-secondary);
    border: 2px solid var(--color-border);
    color: var(--color-text-muted);
}

/* Pulsing dot for active step */
.od-step-pulse {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: var(--color-primary);
    animation: od-pulse 1.8s ease-in-out infinite;
}
@keyframes od-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}

/* Small dot for upcoming steps */
.od-step-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--color-border);
}

/* Label + description text */
.od-step-body {
    display: flex;
    flex-direction: column;
    gap: 3px;
    padding-top: 5px;
}
.od-step-label {
    font-family: var(--font-family-headings);
    font-size: 0.9375rem;
    font-weight: var(--fw-semibold);
    line-height: 1.2;
}
.od-step--done .od-step-label     { color: var(--color-text-primary); }
.od-step--active .od-step-label   { color: var(--color-primary); }
.od-step--upcoming .od-step-label { color: var(--color-text-muted); }

.od-step-desc {
    font-size: 0.8125rem;
    line-height: 1.5;
    color: var(--color-text-muted);
}
.od-step--active .od-step-desc { color: var(--color-text-secondary); }

/* Cancelled notice */
.od-cancelled-notice {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background-color: hsl(8, 45%, 95%);
    border: 1px solid hsl(8, 35%, 85%);
    border-radius: var(--border-radius-md);
    color: var(--color-error);
    padding: 0.875rem 1rem;
    font-size: 0.9375rem;
    font-weight: var(--fw-medium);
}

/* Courier info block */
.od-courier-block {
    margin-top: 1.75rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--color-border-light);
}
.od-courier-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    margin-bottom: 0.25rem;
}
.od-courier-value {
    font-weight: var(--fw-semibold);
    color: var(--color-text-primary);
    margin-bottom: 2px;
}
.od-courier-tracking {
    font-family: monospace;
    font-size: 0.9375rem;
    background: var(--color-bg-secondary);
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 4px;
}
.od-courier-date { font-size: 0.8125rem; color: var(--color-text-muted); margin: 0; }

/* ── Order items list ── */
.od-items-list { list-style: none; margin: 0 0 1rem; padding: 0; }
.od-item-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.625rem 0;
    border-bottom: 1px solid var(--color-border-light);
}
.od-item-row:last-child { border-bottom: none; }
.od-item-info { display: flex; flex-direction: column; gap: 2px; }
.od-item-name { font-weight: var(--fw-medium); font-size: 0.9375rem; color: var(--color-text-primary); }
.od-item-qty  { font-size: 0.8125rem; color: var(--color-text-muted); }
.od-item-price { font-weight: var(--fw-semibold); color: var(--color-text-primary); white-space: nowrap; }

/* ── Totals ── */
.od-totals { margin-top: 0.75rem; }
.od-total-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    padding: 4px 0;
}
.od-total-row--grand {
    font-size: 1rem;
    font-weight: var(--fw-bold);
    color: var(--color-text-primary);
    border-top: 1px solid var(--color-border);
    padding-top: 0.5rem;
    margin-top: 0.25rem;
}

/* ── Payment summary ── */
.od-payment-pill-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}
.od-payment-pill-label { font-size: 0.875rem; color: var(--color-text-secondary); }
.od-pill {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    padding: 4px 10px;
    border-radius: var(--border-radius-round);
}
.od-pill--ok   { background: hsl(98, 15%, 90%);  color: var(--color-success); }
.od-pill--warn { background: hsl(28, 55%, 92%);  color: var(--color-warning); }
.od-pill--err  { background: hsl(8, 45%, 92%);   color: var(--color-error); }
.od-pill--muted{ background: var(--color-bg-secondary); color: var(--color-text-muted); }

.od-payment-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    padding: 3px 0;
}
.od-rejection-notice {
    margin-top: 0.75rem;
    background: hsl(8, 45%, 95%);
    border: 1px solid hsl(8, 35%, 85%);
    border-radius: var(--border-radius-sm);
    padding: 0.625rem 0.875rem;
    font-size: 0.875rem;
    color: var(--color-error);
}
.od-payment-cta { margin-top: 1.25rem; }
.od-pay-btn { width: 100%; justify-content: center; }

/* ── Delivery address ── */
.od-address {
    font-style: normal;
    font-size: 0.9375rem;
    line-height: 1.75;
    color: var(--color-text-secondary);
}
.od-address strong { color: var(--color-text-primary); }

/* ── Review card ── */
.od-review-card { text-align: center; }
.od-review-prompt {
    font-size: 0.9375rem;
    color: var(--color-text-secondary);
    margin-bottom: 1rem;
}
.od-review-btn { margin: 0.25rem 0; width: 100%; justify-content: center; }
"""

path = r'c:/Users/sasi6/OneDrive/Desktop/loop & leisure ~mithra/app/static/css/components.css'
with open(path, 'a', encoding='utf-8') as f:
    f.write(css_to_append)
print("CSS appended successfully.")
