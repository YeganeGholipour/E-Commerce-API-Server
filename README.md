# **E-Commerce Order Management API**  

## **Overview**  
This is a Django REST Framework (DRF) API for managing orders and shipping in an e-commerce system. The API supports order creation, retrieval, updates, payment handling, order cancellations, and shipping management for both users and admins.  

## **Features**  

### **User Features**  
- **Create an Order**: Users can create new orders linked to their cart.  
- **View Orders**: Users can retrieve and list their own orders.  
- **Update an Order**: Users can update their orders, including modifying the shipping details.  
- **Successful Payment**: Users can mark an order as paid.  
- **Cancel an Order**: Users can cancel an order (instead of deleting it).  
- **View Shipping Details**: Users can retrieve and list their shipping details for orders they own.  

### **Admin Features**  
- **View All Orders**: Admins can list and retrieve any order.  
- **Ship an Order**: Admins can mark an order as “Shipped” (only if the payment is successful).  
- **Deliver an Order**: Admins can mark an order as “Delivered” (only if it has already been shipped).  
- **View Shipping Details**: Admins can list and retrieve all shipping details.  

## **Models**  

### **Order Model**  
- Linked to a **Cart** (owned by a user).  
- Has a **payment status** (`Pending`, `Paid`, `Cancelled`).  
- Linked to a **Shipping** object.  

### **Shipping Model**  
- Includes **delivery date, method, status, cost, and address**.  
- Status options: `Pending`, `Shipped`, `Delivered`.  
- Prevents past delivery dates from being set.  

## **API Endpoints**  

### **User Order Endpoints**  
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/orders/` | `POST` | Create a new order |
| `/orders/` | `GET` | List all user orders |
| `/orders/{id}/` | `GET` | Retrieve a specific user order |
| `/orders/{id}/` | `PUT/PATCH` | Update an order (including shipping details) |
| `/orders/{id}/successful_payment/` | `POST` | Mark an order as paid |
| `/orders/{id}/cancel_payment/` | `POST` | Cancel an order |

### **Admin Order Endpoints**  
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/orders/` | `GET` | List all orders |
| `/admin/orders/{id}/` | `GET` | Retrieve a specific order |
| `/admin/orders/{id}/ship_delivery/` | `POST` | Mark an order as shipped (if paid) |
| `/admin/orders/{id}/deliver_delivery/` | `POST` | Mark an order as delivered (if shipped) |

### **User Shipping Endpoints**  
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/shipping/` | `GET` | List all shipping details for the user |
| `/shipping/{id}/` | `GET` | Retrieve a specific shipping detail |

### **Admin Shipping Endpoints**  
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/shipping/` | `GET` | List all shipping details |
| `/admin/shipping/{id}/` | `GET` | Retrieve a specific shipping detail |

## **Installation & Setup**  

1. **Clone the Repository**  
   ```sh
   git clone <repo-url>
   cd <project-folder>
   ```

2. **Create & Activate Virtual Environment**  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Migrations**  
   ```sh
   python manage.py migrate
   ```

5. **Create a Superuser (for Admin Access)**  
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the Development Server**  
   ```sh
   python manage.py runserver
   ```

7. **Access the API**  
   - **DRF Browsable API**: `http://127.0.0.1:8000/`
   - **Admin Panel**: `http://127.0.0.1:8000/admin/`

## **Authentication**  
- Uses **JWT-based authentication** (or Django’s default authentication).  
- Only **authenticated users** can access order and shipping details.  
- Only **admins** can access and update all orders.  

## **Future Enhancements**  
- Integrate actual payment processing.  
- Add automated order cancellation if unpaid for 24 hours.  
- Implement email notifications for order status updates.  

---

Let me know if you need any modifications! 🚀
