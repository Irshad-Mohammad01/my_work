# SSJewellery — Complete Technical & System Documentation

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Complete Technology Stack](#2-complete-technology-stack)
3. [Project Directory Structure](#3-project-directory-structure)
4. [User-Side Features](#4-user-side-features)
5. [Admin Panel](#5-admin-panel)
6. [Database Documentation](#6-database-documentation)
7. [API Documentation](#7-api-documentation)
8. [Authentication & Authorization](#8-authentication--authorization)
9. [OTP System](#9-otp-system)
10. [Email / SMTP System](#10-email--smtp-system)
11. [Order System](#11-order-system)
12. [Product System](#12-product-system)
13. [Category & Collection System](#13-category--collection-system)
14. [Notification System](#14-notification-system)
15. [Audit Trail](#15-audit-trail)
16. [Analytics](#16-analytics)
17. [UI / Responsive System](#17-ui--responsive-system)
18. [Environment Variables](#18-environment-variables)
19. [DEV / QA / Production Architecture](#19-dev--qa--production-architecture)
20. [Deployment Architecture](#20-deployment-architecture)
21. [Error Handling](#21-error-handling)
22. [Security Documentation](#22-security-documentation)
23. [Data Flow Diagrams](#23-data-flow-diagrams)
24. [Complete User Journeys](#24-complete-user-journeys)
25. [Complete Admin Journeys](#25-complete-admin-journeys)
26. [Known Limitations / Not Found](#26-known-limitations--not-found)
27. [File-to-Feature Mapping](#27-file-to-feature-mapping)
28. [Glossary](#28-glossary)
29. [Final System Summary](#29-final-system-summary)

---

## 1. Project Overview

### Project Name
**SSJewellery**

### Project Purpose & Business Objective
SSJewellery is an enterprise-grade luxury e-commerce platform designed for fine gold, diamond, and luxury jewellery retail. The application facilitates full digital customer engagement—including product showcase browsing, dynamic gold weight and price calculation, real-time live chat customer support, customized buy requests, automated order placement, invoice generation, user notification delivery, and admin management.

### Main Users
- **End Customers (Users)**: Browse luxury collections, search/filter products, request custom buy orders, add items to cart/wishlist, place orders, receive real-time notifications, track shipments, download invoices, and manage profile security settings.
- **Administrators (Admins)**: Manage product catalogs, inventory, pricing, order fulfillment, shipment tracking, user accounts, homepage configuration, category & collection banners, site-wide maintenance and high-demand modes, manual/auto gold rate synchronization, and audit trail logs.

### User-Side System vs. Admin-Side System
- **User-Side System**: Single Page Application (SPA) providing an immersive luxury UI featuring dynamic banners, interactive product cards, occasion showcases, gold weight/purity calculators, multi-language support (English/Hindi), cart/wishlist management, checkout flow, profile setting controls, order history tracking, and support ticket creation.
- **Admin-Side System**: Dedicated security portal (`/admin`) requiring administrative role authorization (`is_admin=True` or admin JWT token). Includes summary analytics dashboards, interactive product & stock management tabs, user access controls, order status & tracking ID managers, category/collection banner uploaders, site settings switchers, and audit log tables.

### Overall Architecture & Technology Stack
- **Architecture**: Decoupled Client-Server Architecture (RESTful JSON API backend with React SPA frontend).
- **Backend Framework**: Python 3.12 Flask REST API framework.end Stack (Source: `frontend/package.json`)
- **Core Framework**: React `^19.2.6`
- **Frontend Framework**: React 19 SPA built with Vite 8.
- **Database Architecture**: PostgreSQL (hosted on Neon Serverless PostgreSQL with fallback IPv4 connection pool resolving) or SQLite (for offline/dev environments), managed via SQLAlchemy 3.1 ORM and Flask-Migrate / Alembic.
- **External Services**:
  - **SMTP**: Gmail SMTP (`smtp.gmail.com:587`) for OTP, account alerts, and order confirmations via Flask-Mail.
  - **Media Storage**: Cloudinary SDK (`cloudinary 1.40.0`) for luxury product, banner, and owner image uploads.
  - **Live Gold Rate**: RapidAPI Gold Rate API integration.
  - **Payments**: Razorpay Payment Gateway integration (environment configurable).

---

## 2. Complete Technology Stack

### Frontend Stack (Source: `frontend/package.json`)
- **Core Framework**: React `^19.2.6`
- **Build Tool & Dev Server**: Vite `^8.0.12`
- **Language**: JavaScript (ES6+ / JSX) with `@types/react` `^19.2.14`
- **Routing**: `react-router-dom` `^7.15.1`
- **HTTP/API Client**: `axios` `^1.16.1`
- **Styling System**:
  - CSS3 (Vanilla CSS + Modern Fluid `clamp()` typography & layouts)
  - `tailwindcss` `^4.3.0`
  - `@tailwindcss/vite` `^4.3.0`
  - `postcss` `^8.5.15`
  - `autoprefixer` `^10.5.0`
- **Animations & Icons**:
  - `framer-motion` `^12.40.0`
  - `gsap` `^3.15.0`
  - `lucide-react` `^1.16.0`
- **Linting**: ESLint `^10.3.0` with `eslint-plugin-react-hooks` and `eslint-plugin-react-refresh`

### Backend Stack (Source: `requirements.txt` & `backend/app.py`)
- **Core Language**: Python `3.12+`
- **Web Framework**: Flask `3.0.3`
- **ORM & Database Manager**: Flask-SQLAlchemy `3.1.1` (SQLAlchemy 2.0+ core engine)
- **Database Migrations**: Flask-Migrate `4.1.0` (Alembic engine)
- **Database Connectors**: `psycopg2-binary` (PostgreSQL) and `PyMySQL` `1.2.0` / SQLite
- **Security & Authentication**:
  - `bcrypt` `4.1.3` (Password hashing)
  - `PyJWT` `2.8.0` (JSON Web Token signing and verification)
  - `cryptography` `48.0.0` (Data encryption)
- **Middleware & Utility**:
  - `Flask-Cors` `4.0.1` (Cross-Origin Resource Sharing)
  - `python-dotenv` `1.0.1` (Environment variable loader)
  - `pytz` (Timezone calculations — Asia/Kolkata IST)
  - `Werkzeug ProxyFix` (Trusted proxy header management for Render/Oracle Cloud/Nginx)
- **Email Transmission**: `Flask-Mail` / Python `smtplib` (Gmail SMTP)
- **Cloud Media Storage**: `cloudinary` `1.40.0`
- **Data Export & Reporting**: `pandas`, `matplotlib`, `openpyxl`

### Infrastructure & Deployment
- **Hosting**: Compatible with Render, Railway, VPS (Nginx + Gunicorn), or Docker containers.
- **Database Hosting**: Neon PostgreSQL Serverless DB.
- **Environment Configuration**: Multi-environment deployment architecture (`ENVIRONMENT` = `DEV` | `QA` | `PROD`).

---

## 3. Project Directory Structure

```
/home/irshad-mohammad/Videos/My_Work/
├── backend/
│   ├── app.py                      # Application entry point, Flask initialization, CORS, compression
│   ├── config.py                   # Centralized multi-environment configuration & validation
│   ├── extensions.py               # Shared extension instances (db, migrate, mail)
│   ├── update_db.py                # Database migration runner & site settings seeder
│   ├── middleware/
│   │   └── maintenance.py          # Maintenance and high-demand mode request interceptors
│   ├── models/                     # SQLAlchemy Database Models
│   │   ├── __init__.py             # Model exports registry
│   │   ├── admin.py                # AdminModel, AdminAuditLog, AdminNotification
│   │   ├── banner.py               # BannerModel (Homepage Hero Banners)
│   │   ├── category.py             # Category model
│   │   ├── category_banner.py      # CategoryBanner model
│   │   ├── collection.py           # CollectionModel model
│   │   ├── collection_banner.py    # CollectionBanner model
│   │   ├── coupon.py               # CouponModel model
│   │   ├── email_log.py            # EmailLog model
│   │   ├── notification.py         # NotificationModel
│   │   ├── order.py                # OrderModel, OrderItem, Transaction
│   │   ├── otp_verification.py     # OTPVerification model
│   │   ├── product.py              # ProductModel, ProductImageModel, StockHistoryModel, ProductAuditLogModel, ProductVariantModel, BuyRequestModel
│   │   ├── review.py               # ReviewModel
│   │   ├── settings.py             # SiteSettingModel
│   │   ├── support.py              # SupportModel, FAQModel, SupportLinkModel, SupportReplyModel
│   │   ├── transaction.py          # TransactionModel
│   │   ├── user.py                 # UserModel, DeliveryAddress, UserStatusAuditLog
│   │   └── user_attempt.py         # UserAttempt model (Consolidated rate limiting & lockouts)
│   ├── routes/                     # REST API Blueprints
│   │   ├── admin.py                # Admin dashboard, users, products, site settings APIs
│   │   ├── auth.py                 # Authentication, registration, login, OTP, forgot password
│   │   ├── banners.py              # Homepage hero banners APIs
│   │   ├── category_banners.py     # Category banners management APIs
│   │   ├── collection_banners.py   # Collection banners management APIs
│   │   ├── collections.py          # Collection management APIs
│   │   ├── coupons.py              # Coupon validation APIs
│   │   ├── high_demand.py          # High-demand traffic control APIs
│   │   ├── maintenance.py          # Site maintenance mode management APIs
│   │   ├── orders.py               # Order creation, tracking, user order history APIs
│   │   ├── payments.py             # Razorpay payment verification & admin transaction APIs
│   │   ├── products.py             # Public product browsing, filtering, search APIs
│   │   └── support.py              # Support tickets, live chat, FAQs, support links APIs
│   └── utils/                      # Utilities & Helpers
│       ├── email_service.py        # Mail transmission service & HTML email templates
│       ├── helpers.py              # OTP generators, validators, normalizers, token helpers
│       ├── security.py             # Encryption & JWT verification wrappers
│       └── timezone.py             # IST (Asia/Kolkata) datetime utility
├── frontend/
│   ├── package.json                # Frontend dependencies & Vite scripts
│   ├── vite.config.js              # Vite build configuration & server proxies
│   ├── index.html                  # Main HTML document entry point
│   ├── src/
│   │   ├── main.jsx                # React app root bootstrap
│   │   ├── App.jsx                 # Main application routes & global state providers
│   │   ├── index.css               # Global design tokens, CSS reset, custom utility classes
│   │   ├── components/             # Reusable UI components
│   │   │   ├── Navbar.jsx          # Dynamic responsive navigation header & user menu
│   │   │   ├── Footer.jsx          # Site footer component
│   │   │   ├── ProductCard.jsx     # Luxury product display card with quick action buttons
│   │   │   ├── CategoryBanner.jsx  # Dynamic banner renderer for category view
│   │   │   ├── CollectionBanner.jsx# Dynamic banner renderer for collection view
│   │   │   ├── HighDemandOverlay.jsx# High demand traffic modal overlay
│   │   │   ├── ProtectedRoute.jsx  # Route guard for authenticated users & admins
│   │   │   └── admin/              # Admin dashboard tab modules
│   │   │       ├── AnalyticsTab.jsx
│   │   │       ├── CategoryBannerManagement.jsx
│   │   │       ├── CollectionBannerManagement.jsx
│   │   │       ├── OrderManagementTab.jsx
│   │   │       ├── ProductManagementTab.jsx
│   │   │       ├── SupportTicketsTab.jsx
│   │   │       ├── TrackingInfoModal.jsx
│   │   │       └── UserManagementTab.jsx
│   │   ├── context/
│   │   │   ├── AuthContext.jsx     # Authentication state & JWT context provider
│   │   │   └── LanguageContext.jsx # English/Hindi translation context provider
│   │   ├── pages/                  # Page route views
│   │   │   ├── Home.jsx            # Luxury homepage view
│   │   │   ├── Login.jsx           # User login view
│   │   │   ├── Register.jsx        # User registration view
│   │   │   ├── ForgotPassword.jsx  # Password reset OTP request view
│   │   │   ├── ResetPassword.jsx   # New password submission view
│   │   │   ├── ProductDetails.jsx  # Deep product details & buy request view
│   │   │   ├── Cart.jsx            # User shopping cart view
│   │   │   ├── Checkout.jsx        # Order checkout & address entry view
│   │   │   ├── MyOrders.jsx        # User order tracking & invoice download view
│   │   │   ├── Profile.jsx         # User account settings & notification view
│   │   │   ├── Support.jsx         # User support tickets view
│   │   │   ├── SupportCenter.jsx   # Public FAQ & support links view
│   │   │   ├── AdminDashboard.jsx  # Primary admin panel overview
│   │   │   └── AdminControl.jsx    # Full admin control & system configuration view
│   │   └── utils/
│   │       └── api.js              # Axios instance configured with environment baseURL
└── migrations/                     # Alembic migration scripts
```

---

## 4. User-Side Features

### 1. Homepage & Navigation
- **Hero Banners**: Dynamic carousel showcasing luxury banners uploaded by administrators. Supports custom call-to-action buttons, subtitles, desktop/mobile responsive image rendering, and click-through links.
- **Navbar**: Sticky header with logo, live gold rate ticker, search bar, language switcher (English/Hindi), navigation links, wishlist badge counter, cart badge counter, user notifications popup menu, and profile/login button.
- **Occasion Showcase & Luxury Gallery**: Interactive galleries filtering products by occasions (Wedding, Anniversary, Daily Wear, Festive) and collections.
- **Owner Showcase**: Dedicated section displaying company leadership, heritage, and values.

### 2. Product Search & Catalog Browsing
- **Search & Filtering**: Real-time client & server-side search input supporting product title, category, metal type (Gold, Diamond, Platinum, Silver), purity (18K, 22K, 24K), price range sliders, and sorting options (Newest, Price: Low to High, Price: High to Low).
- **Product Card**: Luxury display card featuring image hover zoom, gold purity badge, calculated price, stock availability badge, wishlist toggle icon, and "View Details" button.

### 3. Product Details & Live Gold Calculation
- **Interactive Image Gallery**: Multi-image thumbnail selector with full-screen lightbox zoom.
- **Dynamic Price Calculation**: Price updates dynamically based on gold weight (grams), making charges, metal purity, and real-time live gold market rate.
- **Buy Request Modal**: Modal form allowing users to submit direct buy enquiries with custom weight/size requests to administrators.

### 4. Cart & Wishlist Management
- **Cart**: Allows users to add products, modify quantities, view itemized price breakdowns (making charges, estimated taxes), apply promotional coupon codes, and proceed to checkout.
- **Wishlist**: Allows authenticated users to bookmark favorite items for future viewing and quick transfer to cart.

### 5. Checkout & Order Placement
- **Address Selection**: Select existing saved delivery address or enter a new address with full postal validation.
- **Payment Methods**: Supports Cash on Delivery (COD), Online Payment (Razorpay integration), and Direct Bank Transfer options based on system feature flags.
- **Order Summary**: Full breakdown of items, shipping fees, tax, applied coupon discounts, and grand total.

### 6. User Profile & Order History (`/orders`, `/profile`)
- **Order Tracking**: Timeline view displaying order status progression (`PENDING` → `CONFIRMED` → `PROCESSING` → `SHIPPED` → `DELIVERED`). Includes tracking carrier name and direct tracking URL link.
- **Invoice Download**: Generate and print formatted PDF/HTML purchase invoice for completed orders.
- **Security & Password Update**: Change account password and manage notification preferences.

### 7. Support & Live Chat
- **Support Tickets**: Submit customer support tickets with status tracking (`OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`).
- **Live Chat**: Interactive floating chat widget communicating directly with store administration.

---

## 5. Admin Panel

### Overview
Accessible at `/admin` or `/admin/control`, restricted strictly to users with `is_admin=True` or valid admin authentication tokens.

### Key Admin Modules
1. **Dashboard & Analytics (`AnalyticsTab.jsx`)**:
   - Real-time key performance indicator (KPI) cards: Total Revenue, Total Orders, Active Products, Total Registered Users.
   - Graphical charts for revenue trends, sales breakdown by category, low-stock inventory warnings, and recent transaction logs.
2. **Product Management (`ProductManagementTab.jsx`)**:
   - Create, edit, soft-delete, or permanently delete product catalog items.
   - Upload multiple product images directly to Cloudinary.
   - Adjust pricing, gold weight, making charges, metal type, stock quantities, and feature flags (`is_featured`, `is_trending`, `show_on_homepage`).
3. **Order Management (`OrderManagementTab.jsx`)**:
   - View all customer orders with filter tabs by status (`ALL`, `PENDING`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELLED`).
   - Update order status, attach carrier name and tracking ID, and send automated email/SMS status notifications to customers.
4. **User Management (`UserManagementTab.jsx`)**:
   - Inspect registered user details, account verification status, total orders placed, and last login timestamps.
   - Toggle account block status (`is_blocked`) to suspend or restore user access.
5. **Banner Management (`CategoryBannerManagement.jsx`, `CollectionBannerManagement.jsx`)**:
   - Manage Category and Collection visual hero banners. Upload desktop and mobile banner images, specify title overlays, descriptions, target CTA URLs, display order, and active/inactive status.
6. **Support Ticket & Live Chat Manager (`SupportTicketsTab.jsx`)**:
   - Inspect open customer support tickets, reply to customer inquiries, and mark issues resolved.
7. **System & Maintenance Controls**:
   - Toggle Site Maintenance Mode (restricts user access with custom maintenance message modal).
   - Toggle High-Demand Traffic Mode (enforces traffic throttling modal overlay during sale launches).
   - Live Gold Rate Refresh (manual trigger or automatic polling interval).
8. **Audit Trail**:
   - Immutable audit logs capturing administrative actions, field changes, previous vs. new values, admin ID, and timestamps.

---

## 6. Database Documentation

### Overview
Managed via Flask-SQLAlchemy 3.1. Tables utilize integer auto-increment primary keys (`id`), foreign key constraints with indexes, timestamp tracking (`created_at`, `updated_at`), and JSON/Text storage for flexible payload metadata.

### Core Database Tables

#### 1. `users`
- **Purpose**: Stores registered customer and administrative user account records.
- **Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `full_name` (VARCHAR(100), Nullable=False)
  - `email` (VARCHAR(120), Unique=True, Index=True, Nullable=False) — Encrypted/Normalized
  - `password_hash` (VARCHAR(255), Nullable=False)
  - `phone` (VARCHAR(20), Unique=True, Index=True, Nullable=True) — Encrypted/Normalized
  - `notifications` (BOOLEAN, Default=True)
  - `is_blocked` (BOOLEAN, Default=False)
  - `is_admin` (BOOLEAN, Default=False)
  - `email_verified` (BOOLEAN, Default=False)
  - `first_login` (BOOLEAN, Default=True)
  - `last_login` (DATETIME, Nullable=True)
  - `preferred_language` (VARCHAR(10), Default='en')
  - `created_at` (DATETIME, Default=IST Now)
  - `updated_at` (DATETIME, Default=IST Now)
- **Relationships**: Has many `orders`, `delivery_addresses`, `cart_items`, `wishlist_items`, `support_tickets`, `notifications`, `user_attempts`.

#### 2. `user_attempts` (Formerly `user_login_attempts`)
- **Purpose**: Consolidated thread-safe table for login rate-limiting, failed authentication counting, and Forgot Password OTP request rate limiting.
- **Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `user_id` (INTEGER, FK -> `users.id`, Unique=True, Index=True, Nullable=False)
  - `failed_login_attempts` (INTEGER, Default=0)
  - `first_failed_at` (DATETIME, Nullable=True)
  - `last_failed_at` (DATETIME, Nullable=True)
  - `otp_request_attempts` (INTEGER, Default=0)
  - `first_otp_request_at` (DATETIME, Nullable=True)
  - `last_otp_request_at` (DATETIME, Nullable=True)
  - `blocked_at` (DATETIME, Nullable=True)
  - `blocked_until` (DATETIME, Nullable=True)
  - `reason` (VARCHAR(50), Nullable=True) — e.g. `'LOGIN_FAILED_ATTEMPTS'`, `'FORGOT_PASSWORD_OTP_LIMIT'`
  - `updated_at` (DATETIME, Default=IST Now)

#### 3. `products`
- **Purpose**: Stores luxury jewellery product catalog data.
- **Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `name` (VARCHAR(150), Index=True, Nullable=False)
  - `description` (TEXT, Nullable=True)
  - `price` (FLOAT / NUMERIC(10,2), Nullable=False)
  - `category_id` (INTEGER, FK -> `categories.id`, Nullable=True)
  - `collection_id` (INTEGER, FK -> `collections.id`, Nullable=True)
  - `metal_type` (VARCHAR(50), Default='Gold')
  - `purity` (VARCHAR(20), Default='22K')
  - `weight` (FLOAT, Default=0.0) — Gold weight in grams
  - `making_charge` (FLOAT, Default=0.0)
  - `stock` (INTEGER, Default=1)
  - `is_featured` (BOOLEAN, Default=False)
  - `is_trending` (BOOLEAN, Default=False)
  - `show_on_homepage` (BOOLEAN, Default=False)
  - `is_deleted` (BOOLEAN, Default=False)
  - `created_at` (DATETIME, Default=IST Now)
  - `updated_at` (DATETIME, Default=IST Now)
- **Relationships**: Has many `product_images`, `order_items`, `cart_items`, `wishlist_items`, `reviews`, `audit_logs`.

#### 4. `product_images`
- **Purpose**: Multi-image storage links for products.
- **Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `product_id` (INTEGER, FK -> `products.id`, Nullable=False)
  - `image_url` (VARCHAR(500), Nullable=False) — Cloudinary URL
  - `is_primary` (BOOLEAN, Default=False)
  - `created_at` (DATETIME, Default=IST Now)

#### 5. `categories` & `collections`
- **Purpose**: Taxonomy tables for product classification.
- **Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `name` (VARCHAR(100), Unique=True, Nullable=False)
  - `slug` (VARCHAR(100), Unique=True, Nullable=False)
  - `description` (TEXT, Nullable=True)
  - `image_url` (VARCHAR(500), Nullable=True)
  - `is_active` (BOOLEAN, Default=True)

#### 6. `category_banners` & `collection_banners`
- **Purpose**: Admin-configurable visual hero banners for category and collection landing pages.
- **Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `category_id` / `collection_id` (INTEGER, FK, Nullable=False)
  - `title` (VARCHAR(150), Nullable=True)
  - `description` (TEXT, Nullable=True)
  - `desktop_image_url` (VARCHAR(500), Nullable=False)
  - `mobile_image_url` (VARCHAR(500), Nullable=True)
  - `cta_text` (VARCHAR(50), Default='Explore Collection')
  - `cta_link` (VARCHAR(255), Nullable=True)
  - `sort_order` (INTEGER, Default=0)
  - `is_active` (BOOLEAN, Default=True)
  - `created_at`, `updated_at`

#### 7. `orders` & `order_items`
- **Purpose**: Customer purchase transactions and itemized order lines.
- **`orders` Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `order_number` (VARCHAR(50), Unique=True, Index=True, Nullable=False)
  - `user_id` (INTEGER, FK -> `users.id`, Nullable=False)
  - `total_amount` (FLOAT, Nullable=False)
  - `status` (VARCHAR(50), Default='PENDING', Index=True) — (`PENDING`, `CONFIRMED`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELLED`)
  - `payment_method` (VARCHAR(50), Default='COD')
  - `payment_status` (VARCHAR(50), Default='PENDING')
  - `delivery_address_json` (TEXT / JSON, Nullable=False)
  - `tracking_carrier` (VARCHAR(100), Nullable=True)
  - `tracking_number` (VARCHAR(100), Nullable=True)
  - `tracking_url` (VARCHAR(500), Nullable=True)
  - `created_at`, `updated_at`
- **`order_items` Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `order_id` (INTEGER, FK -> `orders.id`, Nullable=False)
  - `product_id` (INTEGER, FK -> `products.id`, Nullable=False)
  - `quantity` (INTEGER, Nullable=False)
  - `unit_price` (FLOAT, Nullable=False)
  - `making_charge` (FLOAT, Default=0.0)

#### 8. `otp_verifications`
- **Purpose**: Stores active OTP codes for email verification and password reset.
- **Columns**:
  - `id` (INTEGER, PK, Auto-increment)
  - `email` (VARCHAR(120), Index=True, Nullable=False)
  - `otp_code` (VARCHAR(10), Nullable=False)
  - `expires_at` (DATETIME, Nullable=False)
  - `is_verified` (BOOLEAN, Default=False)
  - `attempts` (INTEGER, Default=0)
  - `resend_attempts` (INTEGER, Default=0)
  - `user_id` (INTEGER, FK -> `users.id`, Nullable=True)
  - `created_at` (DATETIME, Default=IST Now)

#### 9. `site_settings`
- **Purpose**: Key-value store for global platform settings (maintenance mode, high demand status, owner showcase data, occasion list JSON).
- **Columns**: `key` (VARCHAR(100), PK), `value` (TEXT, Nullable=True), `updated_at`

---

## 7. API Documentation

### Authentication APIs (`/api/auth`)
| Method | Endpoint | Purpose | Auth | Status |
|--------|----------|---------|------|--------|
| POST | `/api/auth/register` | Register new user account | None | 201, 400, 409 |
| POST | `/api/auth/login` | Authenticate user via email/password | None | 200, 401, 403, 429 |
| POST | `/api/auth/user-login` | Authenticate user via email or phone | None | 200, 401, 403, 429 |
| POST | `/api/auth/forgot-password` | Request password reset OTP | None | 200, 404, 429 |
| POST | `/api/auth/resend-reset-otp` | Resend password reset OTP | None | 200, 400, 404, 429 |
| POST | `/api/auth/verify-reset-otp` | Verify password reset OTP code | None | 200, 400, 404 |
| POST | `/api/auth/reset-password` | Submit new account password | None | 200, 400, 404 |
| GET | `/api/auth/me` | Fetch authenticated user profile | Bearer JWT | 200, 401 |
| POST | `/api/auth/change-password` | Update current password | Bearer JWT | 200, 400, 401 |

### Product APIs (`/api/products`)
| Method | Endpoint | Purpose | Auth | Status |
|--------|----------|---------|------|--------|
| GET | `/api/products/` | Public product catalog search & filter | None | 200 |
| GET | `/api/products/<id>` | Fetch detailed product information | None | 200, 404 |
| POST | `/api/products/buy-request` | Submit custom buy request | None / User | 201, 400 |

### Order APIs (`/api/orders`)
| Method | Endpoint | Purpose | Auth | Status |
|--------|----------|---------|------|--------|
| POST | `/api/orders/` | Place a new product order | Bearer JWT | 201, 400, 401 |
| GET | `/api/orders/my-orders` | Fetch user's order history | Bearer JWT | 200, 401 |
| GET | `/api/orders/<id>` | Fetch single order details & tracking | Bearer JWT | 200, 401, 404 |

### Admin APIs (`/api/admin`)
| Method | Endpoint | Purpose | Auth | Status |
|--------|----------|---------|------|--------|
| POST | `/api/admin/login` | Administrative login | None | 200, 401, 403 |
| GET | `/api/admin/analytics` | Summary analytics KPI data | Admin JWT | 200, 401, 403 |
| GET | `/api/admin/users` | List registered user accounts | Admin JWT | 200, 401, 403 |
| PUT | `/api/admin/users/<id>/block` | Toggle user block status | Admin JWT | 200, 404 |
| POST | `/api/admin/products` | Create product catalog item | Admin JWT | 201, 400 |
| PUT | `/api/admin/products/<id>` | Edit product catalog item | Admin JWT | 200, 404 |
| DELETE | `/api/admin/products/<id>` | Soft-delete product catalog item | Admin JWT | 200, 404 |
| GET | `/api/admin/orders` | List all customer orders | Admin JWT | 200, 401, 403 |
| PUT | `/api/admin/orders/<id>/status` | Update order status & tracking info | Admin JWT | 200, 400, 404 |
| GET | `/api/admin/audit-logs` | Retrieve system audit logs | Admin JWT | 200, 401, 403 |

### Category & Collection Banner APIs (`/api/category-banners`, `/api/collection-banners`)
| Method | Endpoint | Purpose | Auth | Status |
|--------|----------|---------|------|--------|
| GET | `/api/category-banners/` | Fetch active category banners | None | 200 |
| POST | `/api/category-banners/` | Create category banner | Admin JWT | 201, 400 |
| PUT | `/api/category-banners/<id>` | Update category banner | Admin JWT | 200, 404 |
| DELETE | `/api/category-banners/<id>` | Delete category banner | Admin JWT | 200, 404 |
| GET | `/api/collection-banners/` | Fetch active collection banners | None | 200 |
| POST | `/api/collection-banners/` | Create collection banner | Admin JWT | 201, 400 |
| PUT | `/api/collection-banners/<id>` | Update collection banner | Admin JWT | 200, 404 |
| DELETE | `/api/collection-banners/<id>` | Delete collection banner | Admin JWT | 200, 404 |

---

## 8. Authentication & Authorization

### Password Hashing
- Utilizes `bcrypt 4.1.3`. Passwords are salted and hashed via `bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())`. Password verification uses `bcrypt.checkpw(password.encode('utf-8'), hashed_bytes)`.

### JWT Architecture
- Signed using HS256 algorithm with secret dynamically resolved from `JWT_SECRET` / `SECRET_KEY` environment variables.
- Payload includes `user_id`, `email`, `is_admin`, `iat` (issued at), and `exp` (expiration timestamp).
- Authentication header: `Authorization: Bearer <jwt_token>`.

### User Lockout & Rate Limiting (`UserAttempt`)
- **Login Rate Limiting**: Max 5 consecutive failed password login attempts triggers a 15-minute account lock (`reason = "LOGIN_FAILED_ATTEMPTS"`).
- **Forgot Password Rate Limiting**: Max 3 OTP requests within 15 minutes triggers a 15-minute account lockout (`reason = "FORGOT_PASSWORD_OTP_LIMIT"`).
- Thread-safe, row-level locking via SQLAlchemy `with_for_update()`.

---

## 9. OTP System

### Architecture & Rules
- **Length**: 6-digit numeric OTP generated via `random.randint(100000, 999999)`.
- **Validity Window**: 5 minutes (`expires_at = current_time + timedelta(minutes=5)`).
- **Max Verification Attempts**: 3 failed verification entries invalidates the OTP record.
- **Max Resend Attempts**: 3 resends allowed per reset session.

### Environment Behaviors
- **DEV Mode (`IS_DEV=True`)**: Bypasses external SMTP email delivery for developer convenience; returns `dev_otp` directly in the JSON API response for immediate testing.
- **QA & PROD Modes**: Transmits OTP securely to the user's registered email address via Gmail SMTP.

---

## 10. Email / SMTP System

### SMTP Architecture
- Uses Gmail SMTP (`smtp.gmail.com:587` with TLS encryption) managed through Flask-Mail and `backend/utils/email_service.py`.
- **Environment Variables**: `SMTP_EMAIL`, `SMTP_PASSWORD` (App Password), `SMTP_FROM`.
- **Startup Validation**: `validate_smtp_configuration()` inspects OS runtime environment variables upon backend initialization and logs status.

### Supported HTML Email Notifications
1. **Forgot Password OTP Email**: Transmits 6-digit verification code with 5-minute expiry warning.
2. **Order Confirmation Email**: Transmits order receipt with itemized line breakdown, shipping address, total price, and tracking link.
3. **Buy Request Confirmation Email**: Transmits acknowledgement receipt for custom jewellery requests.

---

## 11. Order System

### Order Lifecycle Flow
```
Product Selection (Cart / Buy Now)
  ↓
Address Selection / Entry
  ↓
Order Creation & Validation (/api/orders)
  ↓
Payment Processing (COD / Razorpay / Bank Transfer)
  ↓
Status: PENDING -> Email Notification Sent
  ↓
Admin Review & Processing (Status: PROCESSING)
  ↓
Carrier Dispatch & Tracking Assignment (Status: SHIPPED -> Carrier + Tracking URL)
  ↓
Final Delivery Confirmation (Status: DELIVERED)
```

---

## 12. Product System

### Capabilities
- **Catalog Management**: Admin interface to add, edit, or soft-delete products.
- **Multi-Image Support**: Primary thumbnail selection + high-resolution Cloudinary image gallery.
- **Dynamic Pricing Engine**:
  $$\text{Final Price} = (\text{Gold Weight (g)} \times \text{Live Gold Rate for Purity}) + \text{Making Charges} + \text{Taxes}$$
- **Inventory Tracking**: Stock quantities automatically adjust upon order placement; low-stock triggers warnings in admin analytics.

---

## 13. Category & Collection System

### Taxonomy Architecture
- **Categories**: Core product types (e.g., Rings, Necklaces, Earrings, Bangles, Bracelets).
- **Collections**: Curated seasonal or designer lines (e.g., Bridal Heritage, Royal Antique, Daily Solitaire).
- **Dedicated Landing Banners**: Independent `CategoryBanner` and `CollectionBanner` models support dedicated hero images, titles, and CTA links on category/collection filter pages, distinct from Homepage hero banners.

---

## 14. Notification System

### Structure
- Stores user notifications in `notifications` table (`id`, `user_id`, `title`, `message`, `type`, `is_read`, `created_at`).
- **User Interface**: Navbar bell icon displays unread count badge and interactive drop-down list with "Mark All as Read" and "Clear Read" actions.

---

## 15. Audit Trail

### System Logging Architecture
- Administrative actions (product modifications, order status updates, user blocking, price adjustments) are captured in `admin_audit_logs` and `product_audit_logs`.
- **Recorded Fields**: `admin_id`, `action`, `target_type`, `target_id`, `old_values_json`, `new_values_json`, `ip_address`, `timestamp`.
- Displayed in the Admin Panel under the Audit Trail table with syntax-highlighted change diffs.

---

## 16. Analytics

### System Metrics
- **Sales Analytics**: Revenue totals, daily order volumes, average order value.
- **Product Performance**: Top-selling products, category sales distribution, inventory turnover.
- **User Metrics**: Registered user growth, active user sessions, account block counts.
- **Time Range Filters**: 7 Days, 30 Days, All Time.

---

## 17. UI / Responsive System

### Design Language
- **Color Palette**: Luxury Gold (`#D4AF37`, `#FFD700`), Deep Charcoal/Black background modes, Warm Cream accents.
- **Typography**: Fluid `clamp()` font scale with Inter / Outfit clean typography.
- **Responsive Layout**: Mobile-first design; adapts seamlessly from 320px mobile screens up to 4K ultra-wide monitors. Supports dark and light theme modes.

---

## 18. Environment Variables

| Variable | Purpose | Required / Optional | Default Value |
|----------|---------|--------------------|---------------|
| `ENVIRONMENT` / `ENV` | Set runtime environment (`DEV`, `QA`, `PROD`) | Required | `DEV` |
| `FRONTEND_URL` | Base URL of frontend application for CORS | Required in PROD | `http://localhost:5173` |
| `DATABASE_URL` / `PROD_DATABASE_URL` | Primary database connection string | Required | Neon Postgres / SQLite |
| `JWT_SECRET` / `SECRET_KEY` | Secret key for signing JWT tokens | Required | Hardened random string |
| `SMTP_EMAIL` | Sender email address for Gmail SMTP | Required for Email | `ssjewellerysystem@gmail.com` |
| `SMTP_PASSWORD` | App Password for Gmail SMTP | Required for Email | None |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud account name | Required for Uploads | None |
| `CLOUDINARY_API_KEY` | Cloudinary API Key | Required for Uploads | None |
| `CLOUDINARY_API_SECRET` | Cloudinary API Secret | Required for Uploads | None |
| `RAZORPAY_KEY_ID` | Razorpay payment gateway key ID | Optional (Payment) | None |
| `RAZORPAY_KEY_SECRET` | Razorpay payment gateway key secret | Optional (Payment) | None |
| `RAPID_API_KEY` | RapidAPI key for Live Gold Rate | Optional (Gold Rate) | None |

---

## 19. DEV / QA / Production Architecture

- **DEV**: `IS_DEV=True`. Uses SQLite or Dev Neon DB, verbose SQL logging (`SQLALCHEMY_ECHO=True`), OTP bypass via API response payload for rapid frontend development.
- **QA**: `IS_QA=True`. Pre-production staging environment; strictly validates SMTP credentials and DB connections.
- **PROD**: `IS_PROD=True`. Enforces HTTPS cookies, production CORS origin validation, strict environment variable verification (aborts startup if default dev keys are detected).

---

## 20. Deployment Architecture

### Server Setup (Production)
```
Client Browser
  ↓ HTTPS
Reverse Proxy (Nginx / Cloudflare / Render Router)
  ↓ WSS/HTTP (WSGI ProxyFix)
Gunicorn / Flask Server (Backend REST API)
  ↓ Pooler Connection (IPv4 Resolution)
Neon PostgreSQL Database
```

### Build & Run Commands
- **Frontend Build**: `npm run build` (Outputs bundle to `frontend/dist`)
- **Backend Run**: `gunicorn backend.app:app` or `python -m backend.app`
- **Database Migration**: `python -m backend.update_db` or `flask db upgrade`

---

## 21. Error Handling

### HTTP Status Code Mapping
- `400 Bad Request`: Missing payload parameters or invalid field format.
- `401 Unauthorized`: Missing or expired JWT authentication token.
- `403 Forbidden`: Insufficient permissions (e.g. non-admin accessing admin route).
- `404 Not Found`: Account, product, or order record does not exist.
- `409 Conflict`: Duplicate registration email or phone number.
- `429 Too Many Requests`: Account locked due to rate limiting (5 login failures or 3 OTP requests within 15 minutes).
- `500 Internal Server Error`: Unhandled database or system exception; details logged to server log.

---

## 22. Security Documentation

### Implemented Controls
- **Password Security**: Bcrypt salted hashing.
- **Token Security**: Cryptographically signed JWT tokens with runtime secret key resolution.
- **Rate Limiting & Lockouts**: Database-enforced atomic row locking (`UserAttempt`) protecting against brute force login and OTP spam.
- **CORS Protection**: Environment-aware strict origin whitelist credentials control.
- **SQL Injection Defense**: Standardized ORM parameter binding via SQLAlchemy.
- **XSS & Headers**: ProxyFix middleware, HTTP-only cookie options, strict content headers.

### Security Deficiencies / Not Found
- *Web Application Firewall (WAF)*: Not implemented / Not confirmed in source code.
- *Two-Factor Authentication (2FA) for Admins*: Not implemented / Not confirmed in source code.

---

## 23. Data Flow Diagrams

### Forgot Password & OTP Flow (ASCII Diagram)
```
User (ForgotPassword.jsx)
  │
  ├─► POST /api/auth/forgot-password { email }
  │     │
  │     ├─► Lookup User in Database
  │     ├─► Check UserAttempt (Row Lock with_for_update)
  │     │     ├─► If > 3 requests in 15 mins ──► Return HTTP 429
  │     │     └─► If Allowed ──► Increment Counter
  │     │
  │     ├─► Generate 6-digit OTP & Store in otp_verifications
  │     └─► Send Email via Gmail SMTP (or return dev_otp in DEV)
  │
  ├─► POST /api/auth/verify-reset-otp { email, otp_code }
  │     └─► Validate Expiry & Code Match ──► Set is_verified = True
  │
  └─► POST /api/auth/reset-password { email, otp_code, new_password }
        └─► Update password_hash in users table ──► Return 200 Success
```

---

## 24. Complete User Journeys

### User Purchase Journey
1. Customer visits homepage and browses products by category or occasion.
2. Selects a product card to open `ProductDetails.jsx`.
3. Interacts with the live gold calculator to estimate price based on weight and purity.
4. Clicks "Add to Cart" or "Buy Now".
5. Navigates to `/checkout`, enters or selects a delivery address, and chooses payment method.
6. Confirms order placement; receives instant order confirmation email and notification.
7. Tracks order progress in `/orders` and downloads HTML/PDF invoice upon fulfillment.

---

## 25. Complete Admin Journeys

### Product & Order Management Journey
1. Administrator logs into `/admin` using admin credentials.
2. Navigates to Product Management tab to add a new gold necklace item with weight and image uploads.
3. Views new customer order in Order Management tab.
4. Updates order status from `PENDING` to `SHIPPED` and inputs shipment tracking carrier and tracking URL.
5. System logs action into `admin_audit_logs` and sends updated tracking email to customer.

---

## 26. Known Limitations / Not Found

1. **Automated Refund Processing**: Real-time automated gateway refund execution is *Not found / Not confirmed in the current source code* (order cancellation marks status in DB but manual gateway refund is required).
2. **Third-Party Logistics (3PL) API Sync**: Direct API auto-dispatch with logistics providers (e.g., Shiprocket) is *Not found / Not confirmed in the current source code*.
3. **Multi-Currency Auto-Conversion**: Native currency switching beyond INR (₹) is *Not found / Not confirmed in the current source code*.

---

## 27. File-to-Feature Mapping

| Feature | Frontend Files | Backend Files | Database Tables | Primary APIs |
|---------|----------------|---------------|-----------------|--------------|
| Authentication & Rate Limit | `Login.jsx`, `Register.jsx`, `AuthContext.jsx` | `routes/auth.py`, `models/user_attempt.py` | `users`, `user_attempts` | `/api/auth/login`, `/api/auth/register` |
| Forgot Password OTP | `ForgotPassword.jsx`, `ResetPassword.jsx` | `routes/auth.py`, `models/otp_verification.py` | `users`, `user_attempts`, `otp_verifications` | `/api/auth/forgot-password`, `/api/auth/verify-reset-otp` |
| Product Catalog & Search | `Home.jsx`, `ProductDetails.jsx`, `ProductCard.jsx` | `routes/products.py`, `models/product.py` | `products`, `product_images`, `categories` | `/api/products/`, `/api/products/<id>` |
| Order & Checkout | `Cart.jsx`, `Checkout.jsx`, `MyOrders.jsx` | `routes/orders.py`, `models/order.py` | `orders`, `order_items`, `delivery_addresses` | `/api/orders/`, `/api/orders/my-orders` |
| Admin Panel & Analytics | `AdminDashboard.jsx`, `AdminControl.jsx`, `admin/*` | `routes/admin.py`, `models/admin.py` | `users`, `products`, `orders`, `admin_audit_logs` | `/api/admin/analytics`, `/api/admin/orders` |
| Banners Management | `CategoryBanner.jsx`, `CollectionBanner.jsx` | `routes/category_banners.py`, `routes/collection_banners.py` | `category_banners`, `collection_banners` | `/api/category-banners`, `/api/collection-banners` |

---

## 28. Glossary

- **OTP**: One-Time Password used for identity verification.
- **JWT**: JSON Web Token used for stateless REST API authentication.
- **IST**: Indian Standard Time (`Asia/Kolkata`, UTC+5:30) used for all system timestamps.
- **Making Charges**: Crafting and labor fee added to raw gold material cost.
- **Row-Level Locking (`with_for_update`)**: Database locking mechanism ensuring atomic thread-safe updates to attempt records under concurrent access.

---

## 29. Final System Summary

- **Architecture**: Enterprise Decoupled Client-Server E-Commerce System (React 19 SPA + Python 3.12 Flask REST API).
- **Core Database**: PostgreSQL (Neon Serverless DB) with SQLAlchemy ORM and Alembic migrations.
- **Security Baseline**: Bcrypt password hashing, HS256 JWT tokens, thread-safe database rate limiting and lockout protection (`UserAttempt`), strict environment CORS origin validation.
- **Business Capability**: Complete luxury jewellery e-commerce workflow covering catalog search, live gold calculation, buy requests, cart/checkout, tracking, admin fulfillment, banner customization, and audit logging.

---
*Documentation Compiled & Verified Against Source Code: August 2026*
