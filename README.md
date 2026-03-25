# 🏪 POS System - Point of Sale Terminal

A comprehensive Point of Sale (POS) system built in Python that supports cashier operations, administrative functions, payment processing, and coupon management. This system provides a terminal-based interface for retail businesses to manage sales transactions, inventory, users, and discounts efficiently.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Database Structure](#database-structure)
- [Sample Data](#sample-data)
- [Development Team](#development-team)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 👤 Cashier Functions
- **Start New Sales Transaction**: Create and manage new sales with line items
- **Product Scanning**: Add products by barcode with automatic price lookup
- **Quantity Management**: Adjust quantities for each product
- **Coupon Application**: Apply percentage-based discounts to transactions
- **Multiple Payment Methods**:
  - 💵 **Cash**: Accept cash payments with automatic change calculation
  - 📝 **Check**: Process checks with bank name and check number tracking
  - 💳 **Credit Card**: Handle credit card payments with card details
- **Returns Processing**: Handle product returns and refunds
- **Receipt Generation**: Print detailed transaction receipts

### 👨‍💼 Administrator Functions
- **User Management**:
  - Create new cashiers and administrators
  - Edit existing user details (name, password)
  - Delete users from the system
- **Security Configuration**:
  - Set password requirements
  - Configure session timeouts
  - Enable login attempt locking
- **Coupon Management**:
  - Create new discount coupons
  - View all active coupons
  - Delete expired or unused coupons

### 🔧 System Features
- **Role-Based Access Control**: Different permissions for cashiers and admins
- **Secure Authentication**: Password-protected user login
- **Clean Console Interface**: Formatted tables and boxes for better readability
- **Transaction History**: Track all completed sales

## 📁 Project Structure

| File | Description |
|------|-------------|
| `main.py` | Main application entry point & UI logic |
| `database.py` | Database schemas (users, products, coupons, sales) |
| `users.py` | User classes (Cashier, Administrator) |
| `transactions.py` | Transaction and product catalog classes |
| `payments.py` | Payment processing classes |
| `README.md` | Project documentation |

All Python files are located in the root directory for easy access and execution.

## 🛠 Prerequisites

- **Python 3.6 or higher**
- No external dependencies required (uses only Python standard library)

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/sabell77/OOSE-Project.git
cd OOSE-Project















 
