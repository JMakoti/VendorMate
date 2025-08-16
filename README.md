# VendorMate – Your Vendor Management Companion

## 📌 Overview
VendorMate is a friendly and reliable companion for small business vendors.  
It assists vendors in managing **sales**, **payments**, and **inventory** efficiently, making daily business operations easier and more organized.

---

## 🛠 Problem Statement
Small business vendors often struggle to keep track of sales and payments manually. This can lead to:
- ❌ Errors in record-keeping  
- ⏳ Delays in processing  
- ❓ Confusion about revenue and inventory levels  

---

## 💡 Tech Solution
A **Django-based** digital platform that:
- 📊 Automates sales and payment tracking  
- 📈 Provides simple, clear reports  
- 🛒 Helps vendors manage their businesses efficiently  

---

## 🎯 Objective
Build a **web-based platform** to help small vendors:
- Track sales  
- Manage payments  
- Monitor inventory efficiently  

---

## 🚀 Key Features

### **1. User Management**
**Overview:**  
The User App manages authentication, profile management, and account security for vendors using **JWT-based authentication**.

**Features:**
- ✅ **Authentication**
  - User Registration – `POST /Createuser`
  - User Login – `POST /loginuser`
  - JWT-Secured Endpoints – All protected routes require a valid JWT token

- ✅ **Profile Management**
  - Add Profile Details – `POST /add-profile-details`
  - Update Profile – `PUT /update-profile`

- ✅ **Security & Utilities**
  - Change Password – `PUT /change-password`

---

### **2. Product Management**
**Overview:**  
The Product App manages **categories**, **product details**, and **inventory**. It supports CRUD operations and ensures data validation.

**Main Features:**
- Category Management – Create, list, update, and delete product categories  
- Product Management – Manage products, including price, stock, and category association  
- Validation – Ensures product price and stock are positive integers  
- API Endpoints – RESTful endpoints for category and product operations  

---

### **3. Sales Management**
**Overview:**  
The Sales App handles the complete sales workflow — from recording transactions to managing items and payments.

**Core Models:**
- **Sale** – Represents a pending or completed transaction  
- **SaleItem** – Links a sale to a product and quantity sold  
- **SaleEvent** – Logs key events (creation, payment, cancellation)  

**API Features:**
- CRUD Operations – List, create, retrieve, update sales  
- Custom Actions:
  - Mark as Paid – Updates sale status after payment  
  - Cancel Sale – Reverses a sale and restores stock  

**Business Rules:**
- Atomic Transactions – Prevents overselling by locking product stock during processing  
- Stock Management – Deducts stock on sale creation and restores it if canceled  
- Service Layer – Handles payment processing and sale cancellations  

---

### **4. Reports**
**Overview:**  
The Report App provides vendors with **sales** and **inventory insights**.

**Main Features:**
- 📊 **Sales Summaries**
  - Total Sales Revenue – Value of sales in a given date range  
  - Sales by Product – Revenue and quantity sold per product  
  - Number of Orders – Count of orders placed  

- 📦 **Inventory Summaries**
  - Current Stock per Product – Displays quantities in stock  
  - Low Stock Alerts – Highlights products below minimum stock threshold  

**Authorization:**
- Role-Based Access Control (RBAC) – Only the logged-in vendor can view their own reports  

---

## 🖥 Tech Stack
- **Backend:** Django + Django REST Framework  
- **Database:** SQLite3  
- **Payment Integration:** Daraja API  

---

## 📋 Task Distribution

| Task                        | Person Responsible | Description |
|-----------------------------|-------------------|-------------|
| Vendor Registration & Login | Person 1 | Implement signup, login, logout, and password management |
| Profile Management          | Person 2 | Create profile editing, update vendor details, manage settings |
| Add Products                | Person 3 | Add new products (name, price, category) |
| Update Products             | Person 4 | Update product details and images |
| Track Stock Levels          | Person 5 | Implement inventory tracking and low-stock alerts |
| Record Sales                | Person 6 | Sales recording with product selection and quantities |
| Accept Payments             | Person 7 | Integrate Daraja API for online transactions |
| Generate Reports            | Person 8 | Sales and inventory summary reporting |

---

## 📂 GitHub Repository
🔗 [VendorMate Repository](https://github.com/JMakoti/VendorMate)

---

## 🤝 Team & Collaborators
Developed by **SecretStartApp Django Intermediate Members**, working collaboratively to design, build, and deliver **VendorMate** as a practical solution for small business vendors.

---

## ✅ Conclusion
VendorMate offers a **simple yet powerful solution** for small business vendors struggling with manual sales and inventory tracking.  
By leveraging **Django** and integrating **Daraja API** for payments, it enables vendors to:
- Save time  
- Reduce errors  
- Gain valuable business insights  

The platform empowers vendors to operate efficiently and **scale with confidence**.
