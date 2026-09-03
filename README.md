# Loop & Leisure by Mithra

A premium, production-ready, full-stack web platform for hand-crafted crochet products. Built with Python (Flask), SQLite, and pure vanilla design specifications (HTML5/CSS3).

## Directory Structure

```
loop_leisure/
│
├── app/                              # Core application source
│   ├── __init__.py                   # Application Factory pattern init
│   ├── config.py                     # Configuration settings (Dev, Prod, Test)
│   │
│   ├── admin/                        # Admin operations Blueprint package
│   │   ├── __init__.py
│   │   └── routes.py                 # Admin dashboard endpoints
│   │
│   ├── customer/                     # Customer operations Blueprint package
│   │   ├── __init__.py
│   │   └── routes.py                 # Customer store endpoints
│   │
│   ├── database/                     # ORM and Database modules
│   │   ├── __init__.py               # SQLAlchemy db binding instantiation
│   │   └── models/                   # Database models package
│   │       ├── __init__.py           # Model exports mapping
│   │       ├── admin.py              # Operator credentials structure
│   │       ├── customer.py           # Customer data structure
│   │       ├── product.py            # Inventory items structure
│   │       └── order.py              # Placed order records and states
│   │
│   ├── services/                     # Reusable business service layer (Empty)
│   ├── utils/                        # System utilities (Empty)
│   ├── email_templates/              # Mail client transactional HTML layout templates
│   │   └── base_email.html           # Base layout for system emails
│   │
│   ├── static/                       # Static resource directories
│   │   ├── css/
│   │   │   ├── base.css              # Typography scales, color palettes, reset
│   │   │   └── components.css        # Reusable component designs (pills, cards, fields)
│   │   ├── js/
│   │   │   └── main.js               # Client controller javascript actions
│   │   ├── icons/                    # Vector icons and graphical markers (Empty)
│   │   ├── images/                   # Page photos (Empty)
│   │   └── uploads/                  # Customer upload directory
│   │       ├── products/             # Inventory catalog photos (Empty)
│   │       └── payments/             # Transaction verification files (Empty)
│   │
│   └── templates/                    # Core template layouts
│       ├── layouts/
│       │   └── base.html             # HTML5 master container
│       └── partials/                 # Sub-render fragments (Empty)
│
├── docs/                             # Engineering and architecture documentations
├── instance/                         # Flask relative instance directory (Stores SQLite database)
├── requirements.txt                  # System dependencies list
├── run.py                            # Local runtime initialization script
└── README.md                         # Main readme details
```

## Architectural Design Overview

1. **Flask Application Factory (`app/__init__.py`)**
   - Implements the Application Factory Pattern to support decoupled configuration environments, scalable blueprint registration, and database resource management.
   
2. **Database Models Package (`app/database/models/`)**
   - Keeps entity mappings clean, modularized, and strictly separated by role (Product, Order, Customer, Admin) rather than accumulating in a single long file.

3. **Global Design System (`app/static/css/`)**
   - **`base.css`**: Defines fonts (Outfit for headers, Inter for copy text), layout resets, default focus rings, screen reader utilities, and adaptive grid settings.
   - **`components.css`**: Defines modular component designs like `.btn-primary`, `.form-control`, `.product-card`, `.badge-pending`, `.table`, etc.

4. **SEO & Master Layouts (`app/templates/layouts/base.html`)**
   - Implements a standardized markup blueprint containing dynamic Open Graph elements, title yields, and clean routing link points. No visual body components are rendered by default to avoid placeholder clutter.

## Setup & Running Environment

### Prerequisite
- Python 3.10+ installed.

### Installation
1. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the development server:
   ```bash
   python run.py
   ```
3. Open `http://127.0.0.1:5000` in your web browser.
