
# 🛍️ E-Commerce Backend API

A clean, beginner-friendly **e-commerce backend** built with **FastAPI + SQLite**. It supports users, admins, products, cart, checkout, and orders — all designed to be simple, secure, and fully documented.

---

## 🌟 Features

### Authentication & Roles
- User signup, login, JWT-based auth
- Role-based access (`admin`, `user`)
- Refresh tokens & password reset

### Admin Panel
- Add, update, delete products
- Access protected via RBAC

### User Flow
- Browse/search products
- Manage cart
- Checkout & view orders

### System
- SQLite DB (easy setup)
- `.env` support (via `python-dotenv`)
- Logging to file & console
- Docstrings everywhere ✔️

---

## 📁 Project Structure

```
ecommerce_api/
├── app/
│   ├── auth/            # Auth routes, models, utils
│   ├── cart/            # Cart routes and models
│   ├── checkout/        # Checkout logic
│   ├── core/            # DB, config, .env support
│   ├── orders/          # Orders + items
│   ├── products/        # Admin + public product APIs
│   └── main.py          # App entrypoint
├── .env                 # Secret settings
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1.Create Environment

```bash
cd ecommerce_api
python -m venv venv
venv\Scripts\Activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run It

```bash
uvicorn app.main:app --reload
```

Now open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 🚀

---

## 🔐 Auth & Roles

| Endpoint                | Who     | Purpose                   |
|-------------------------|----------|----------------------------|
| `POST /auth/signup`     | Any      | Register new user          |
| `POST /auth/signin`     | Any      | Login and get tokens       |
| `POST /auth/refresh`    | Any      | Get new access token       |
| `POST /auth/forgot-password` | Any | Request password reset     |
| `POST /auth/reset-password`  | Any | Complete reset             |

---

## 🛍️ Core APIs

### Admin (Requires admin JWT)

- `GET/POST /admin/products/`
- `PUT/DELETE /admin/products/{id}`

### Public

- `GET /products/` - All products with filters/sort/pagination
- `GET /products/search?keyword=...` - Search by name
- `GET /products/{id}` - Single product

### User Cart & Orders

- `POST/PUT/DELETE /cart/` - Manage cart
- `POST /checkout/` - Convert cart to order
- `GET /orders/` - View order history
- `GET /orders/{id}` - View order detail

---

## 📦 Tech Stack

- **FastAPI** - web framework
- **SQLAlchemy** - database ORM
- **JWT** - token-based auth
- **Pydantic** - schema validation
- **Passlib** - secure password hashing
- **python-dotenv** - env config
- **Logging** - app & auth logs in terminal

---

## ✨ Author

Built by **Saket Kumar Jain**  
         **Trainee, NucleusTeq**
         
---
