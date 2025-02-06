# **API Documentation**

## **Base URL**
```
http://127.0.0.1:8000/
```

---

## **User APIs**

### **1. View Profile**
- **Endpoint:** `/user/profile/`
- **Method:** `GET`
- **Description:** Retrieves the profile information of the currently logged-in user (customer or owner).
- **Authorization:** Required (JWT token or session-based).
- **Response Example:**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_owner": true
}
```

---

### **2. Login**
- **Endpoint:** `/user/login/`
- **Method:** `POST`
- **Description:** Authenticates a user and provides a token or session.
- **Request Body Example:**
```json
{
    "username": "john_doe",
    "password": "password123"
}
```
- **Response Example:**
```json
{
    "message": "Login successful",
    "token": "your.jwt.token"
}
```

---

### **3. Sign Out**
- **Endpoint:** `/user/logout/`
- **Method:** `POST`
- **Description:** Logs out the current user.
- **Authorization:** Required (JWT token or session-based).
- **Response Example:**
```json
{
    "message": "Successfully logged out."
}
```

---

### **4. Register (Owner Only)**
- **Endpoint:** `/user/register/`
- **Method:** `POST`
- **Description:** Allows an owner to register new users (customers or owners).
- **Authorization:** Required (Owner only).
- **Request Body Example:**
```json
{
    "username": "new_user",
    "email": "new_user@example.com",
    "password": "password123",
    "is_owner": false
}
```
- **Response Example:**
```json
{
    "message": "User registered successfully."
}
```

---

### **5. Delete Account**
- **Endpoint:** `/user/deactivate-account/`
- **Method:** `DELETE`
- **Description:** Deletes the account of the currently logged-in user.
- **Authorization:** Required (JWT token or session-based).
- **Response Example:**
```json
{
    "message": "Account successfully deleted."
}
```

---

### **6. Update Profile**
- **Endpoint:** `/user/update-profile/`
- **Method:** `PUT`
- **Description:** Updates the profile of the currently logged-in user.
- **Authorization:** Required (JWT token or session-based).
- **Request Body Example:**
```json
{
    "username": "updated_username",
    "email": "updated_email@example.com"
}
```
- **Response Example:**
```json
{
    "message": "Profile updated successfully."
}
```

---

## **Product APIs**

### **1. Add Product (Owner Only)**
- **Endpoint:** `/product/products/add/`
- **Method:** `POST`
- **Description:** Allows an owner to add a new product.
- **Authorization:** Required (Owner only).
- **Request Body Example:**
```json
{
    "title": "Sample Product",
    "selling_price": 99.99,
    "MRP": 120.00,
    "GST": 18.00,
    "link": "http://example.com/product",
    "description": "This is a sample product.",
    "is_stock": true,
    "priority": 1,
    "product_category": "Electronics"
}
```
- **Response Example:**
```json
{
    "message": "Product added successfully.",
    "product_id": 1
}
```

---

### **2. View Products**
- **Endpoint:** `/product/products/`
- **Method:** `GET`
- **Description:** Retrieves the list of all available products.
- **Authorization:** Optional.
- **Response Example:**
```json
[
    {
        "id": 1,
        "title": "Sample Product",
        "selling_price": 99.99,
        "MRP": 120.00,
        "GST": 18.00,
        "link": "http://example.com/product",
        "description": "This is a sample product.",
        "is_stock": true,
        "priority": 1,
        "product_category": "Electronics"
    },
    {
        "id": 2,
        "title": "Another Product",
        "selling_price": 199.99,
        "MRP": 220.00,
        "GST": 18.00,
        "link": "http://example.com/another-product",
        "description": "This is another product.",
        "is_stock": true,
        "priority": 2,
        "product_category": "Home Appliances"
    }
]
```

---
