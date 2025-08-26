# 🛒 MyShop - Modern Django E-commerce Platform

> A complete, feature-rich online shopping platform built with Django, featuring beautiful UI, secure payments, and intelligent recommendations.

**🎬 Watch Demo Video Here**

[![IMAGE ALT TEXT HERE](https://github.com/dennismbugua/online-shop/blob/main/imgs/django%20ecommerce%20shop.PNG?raw=true)](https://www.youtube.com/watch?v=ANTjtaUuXeo)

---

## 👋 Welcome to MyShop!

Whether you're a **business owner** looking to sell online, a **developer** learning e-commerce, or just **curious about modern web applications**, this guide will help you get MyShop up and running in no time!

### 🎯 Who is this for?
- **Small Business Owners** - Launch your online store quickly
- **Developers** - Learn Django and e-commerce best practices  
- **Students** - Study real-world web development
- **Entrepreneurs** - Get a head start on your e-commerce venture

---

## ✨ What Can MyShop Do?

### 🛍️ **For Your Customers**
- **Browse Products** with beautiful, responsive design
- **Smart Shopping Cart** that saves items between visits
- **Secure Checkout** with multiple payment options
- **Coupon Codes** for discounts and promotions
- **Multi-language Support** (English & Spanish included)
- **PDF Receipts** sent automatically via email

### 💼 **For Store Owners**
- **Easy Product Management** through admin interface
- **Order Processing** with automatic email notifications
- **Sales Analytics** and reporting
- **Coupon Management** for marketing campaigns
- **Inventory Tracking** and low-stock alerts
- **Customer Database** with purchase history

### 🔧 **For Developers**
- **Modern Django 4.x** with best practices
- **Asynchronous Tasks** using Celery
- **Payment Integration** with Braintree
- **Internationalization** ready out of the box
- **Redis Caching** for performance
- **Comprehensive Testing** suite included

---

## 🚀 Quick Start Guide

### Step 1: Check Your Computer Setup

Before we begin, make sure you have these installed:

**For Everyone:**
- A computer with internet connection
- A web browser (Chrome, Firefox, Safari, etc.)

**For Technical Setup:**
- Python 3.8 or newer ([Download here](https://python.org))
- Git ([Download here](https://git-scm.com))

**Not sure if you have Python?** Open your terminal/command prompt and type:
```bash
python --version
```

### Step 2: Download MyShop

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/dennismbugua/online-shop.git
cd myshop
```

**Option B: Download ZIP**
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the files to your desired location

### Step 3: Set Up Your Development Environment

**Create a Virtual Environment** (This keeps your project isolated)
```bash
# Create virtual environment
python -m venv myshop-env

# Activate it (Windows)
myshop-env\Scripts\activate

# Activate it (Mac/Linux)
source myshop-env/bin/activate
```

**Install Required Packages**
```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Settings

**Create Environment File**
```bash
# Copy the example file
cp .env.example .env
```

**Edit Your Settings** (Open `.env` file in any text editor)
```bash
# Basic Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# Email Settings (Optional for testing)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Settings (Use Braintree Sandbox for testing)
BRAINTREE_MERCHANT_ID=your-sandbox-merchant-id
BRAINTREE_PUBLIC_KEY=your-sandbox-public-key
BRAINTREE_PRIVATE_KEY=your-sandbox-private-key
```

**Don't worry!** These settings are optional for basic testing. The app will work without them.

### Step 5: Set Up the Database

```bash
# Navigate to the main project folder
cd myshop

# Create database tables
python manage.py migrate

# Create an admin user (you'll use this to manage your store)
python manage.py createsuperuser
```

**When creating superuser:**
- Enter a username (e.g., "admin")
- Enter your email
- Create a password (you'll need this later!)

### Step 6: Add Sample Products (Optional)

Want to see MyShop in action immediately? Load some sample data:

```bash
python manage.py loaddata sample_products.json
```

This adds example products so you can test the shopping experience right away!

### Step 7: Launch Your Store!

```bash
python manage.py runserver
```

**🎉 Congratulations!** Your store is now running at:
- **Main Store**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## 🎮 Using MyShop

### 👑 **Store Management (Admin Panel)**

Visit http://127.0.0.1:8000/admin and log in with your superuser credentials.

**Adding Products:**
1. Click "Products" → "Add Product"
2. Fill in product details:
   - Name and description
   - Price and category
   - Upload product images
   - Set availability
3. Click "Save"

**Managing Orders:**
1. Go to "Orders" section
2. View all customer orders
3. Update order status
4. Export to CSV for accounting

**Creating Coupons:**
1. Navigate to "Coupons"
2. Set discount percentage
3. Choose validity dates
4. Share codes with customers

### 🛒 **Customer Experience**

**Shopping Flow:**
1. Browse products by category
2. Add items to cart
3. Apply coupon codes (optional)
4. Proceed to checkout
5. Fill shipping information
6. Complete secure payment
7. Receive confirmation email with PDF receipt

**Special Features:**
- **Smart Recommendations**: "Customers who bought this also bought..."
- **Multi-language**: Switch between English and Spanish
- **Mobile Friendly**: Works perfectly on phones and tablets
- **Fast Loading**: Optimized for speed

---

## ⚙️ Advanced Configuration

### 💳 **Setting Up Real Payments**

1. **Sign up for Braintree** at [braintreepayments.com](https://braintreepayments.com)
2. **Get your credentials** from the Braintree dashboard
3. **Update your .env file** with real credentials
4. **Test with real cards** in sandbox mode first

**Security Note**: Never commit real payment credentials to version control!

### 📧 **Email Configuration**

**For Gmail:**
1. Enable 2-factor authentication
2. Create an "App Password"
3. Use the app password in your .env file

**For Other Providers:**
Update the EMAIL_HOST settings in your .env file accordingly.

### 🚀 **Performance Optimization**

**Set up Redis (Optional but Recommended):**
```bash
# Install Redis
# Ubuntu/Debian:
sudo apt-get install redis-server

# macOS:
brew install redis

# Start Redis
redis-server
```

**Set up Background Tasks:**
```bash
# In a new terminal, start Celery worker
celery -A myshop worker -l info

# Optional: Start monitoring interface
celery -A myshop flower
```

## 🎨 Customization Guide

### 🎭 **Changing the Look**

**Colors and Styling:**
- Edit `static/css/style.css` for global styles
- Modify templates in `templates/` folder
- Add your logo to `static/images/`

**Adding Your Branding:**
1. Replace logo in header template
2. Update color scheme in CSS
3. Modify email templates with your branding

### 🌍 **Adding New Languages**

```bash
# Create translation files
python manage.py makemessages -l fr  # French example

# Edit translations in locale/fr/LC_MESSAGES/django.po

# Compile translations
python manage.py compilemessages
```

### 🔧 **Adding New Features**

The codebase is designed to be extensible:
- **Product Reviews**: Add rating system
- **Wishlist**: Let customers save favorites  
- **Social Login**: Integrate with Google/Facebook
- **Analytics**: Add Google Analytics tracking

---

## 🚨 Troubleshooting

### Common Issues and Solutions

**"Port already in use" Error:**
```bash
# Kill process on port 8000
sudo lsof -t -i tcp:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 8001
```

**"Module not found" Errors:**
```bash
# Make sure virtual environment is activated
source myshop-env/bin/activate  # Mac/Linux
myshop-env\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

**Database Issues:**
```bash
# Reset database (WARNING: This deletes all data!)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Email Not Sending:**
- Check your email settings in .env
- For Gmail, ensure you're using an App Password
- Check spam folder for test emails

## 🌟 What's Next?

### 📈 **Growing Your Business**

1. **Add More Products** using the admin interface
2. **Set Up Analytics** to track sales and customer behavior
3. **Create Marketing Campaigns** using the coupon system
4. **Optimize for Search Engines** with product descriptions
5. **Scale Your Infrastructure** when you get more traffic

### 🙏 **Built With Love Using:**
- **Django** - The web framework for perfectionists with deadlines
- **Bootstrap** - Beautiful, responsive design components
- **Braintree** - Secure payment processing
- **Celery** - Distributed task queue
- **Redis** - In-memory data structure store

## 🚀 Ready to Start Selling?

### Quick Checklist:
- [ ] Followed the installation steps
- [ ] Added your first product
- [ ] Tested the checkout process
- [ ] Configured email settings
- [ ] Set up payment processing

---

**⭐ If MyShop helped you, please star this repository and share it with others!**

**Happy Selling! 🎉**

Made with ❤️ by [Dennis](https://github.com/dennismbugua)
