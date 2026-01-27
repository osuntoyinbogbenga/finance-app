# Personal Finance Tracker

A comprehensive web-based application for managing personal finances with budget tracking, transaction management, and visual analytics.

## 📋 Project Description

The Personal Finance Tracker is a full-stack web application that helps users manage their personal finances effectively. Users can track income and expenses, organize transactions by categories, set monthly budgets, and visualize their spending patterns through interactive charts and reports.

### Key Features

- **User Authentication**: Secure registration and login system with password hashing
- **Transaction Management**: Add, view, filter, and delete financial transactions
- **Category System**: Organize transactions with customizable color-coded categories
- **Budget Tracking**: Set monthly spending limits with real-time progress monitoring
- **Dashboard**: Real-time overview of income, expenses, and balance with pie charts
- **Financial Reports**: Monthly trend analysis with interactive charts and savings rate calculations
- **Profile Management**: User profile page with activity statistics
- **Modern UI**: 40+ CSS animations for smooth, professional user experience
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Technologies Used

### Backend
- **Python 3.x** - Core programming language
- **Flask 3.0.0** - Lightweight web framework for routing and request handling
- **SQLite3** - File-based relational database for data persistence
- **Werkzeug 3.0.1** - Security utilities for password hashing

### Frontend
- **HTML5** - Semantic markup and structure
- **CSS3** - Custom animations and styling (500+ lines)
- **Tailwind CSS** - Utility-first CSS framework via CDN
- **JavaScript** - Client-side interactivity and DOM manipulation
- **Chart.js** - Interactive data visualization library
- **Font Awesome 6.4** - Icon library

### Database Schema
- **users** - User accounts with authentication
- **categories** - Income/expense categories with colors
- **transactions** - Financial transaction records
- **budgets** - Monthly budget limits per category

All tables use foreign key relationships for data integrity.

## 🚀 How to Build/Run

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/osuntoyinbogbenga/finance-app.git
cd finance-tracker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install flask werkzeug
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```
### Live Demo
The application is deployed and accessible online at:
```
http:financeapp.pythonanywhere.com
```
No installation needed - just visit the URL and start using the app!
(Deployed on PythonAnywhere - a free cloud hosting platform for Python web applications)

### First Time Setup
1. Register a new account at `/register`
2. Login with your username or email
3. Start adding transactions and setting budgets!

## 📊 Features in Detail

### User Authentication
- Secure password hashing using Werkzeug's pbkdf2:sha256
- Session-based authentication
- Login with either username or email
- Protected routes using login_required decorator

### Transaction Management
- Add income and expense transactions
- Assign categories with color coding
- Add descriptions and dates
- Filter by type, category, or month
- Delete transactions

### Budget Tracking
- Set monthly budgets per expense category
- Real-time spending progress bars
- Color-coded warnings:
  - Green: Under 80% of budget
  - Yellow: 80-100% of budget
  - Red: Over budget
- Budget vs. actual spending comparison

### Reports & Analytics
- Line charts showing 6-month income/expense trends
- Monthly summary table with savings rate
- Category-wise expense breakdown (pie chart)
- Total statistics across all months

### User Interface
- Gradient animated login/register pages
- Card hover effects (lift + shimmer)
- Button ripple animations
- Smooth page transitions
- Staggered list animations
- Progress bar animations
- Interactive dropdown menus

## ⚠️ Known Limitations

1. **Single User Sessions**: No concurrent user session management
2. **No Transaction Editing**: Transactions can only be deleted, not modified
3. **No Data Export**: Cannot export transactions to CSV/Excel format
4. **Basic Reporting**: Limited to 6-month trends (no custom date ranges)
5. **No Receipt Uploads**: Cannot attach files or images to transactions
6. **Single Currency**: Fixed to USD, no multi-currency support
7. **No Recurring Transactions**: No automatic entry for regular expenses
8. **SQLite Limitations**: Not suitable for high-concurrency multi-user scenarios

## 🔮 Possible Future Improvements

1. **Transaction Editing**: Add ability to modify existing transactions
2. **Data Export/Import**: 
   - Export transactions to CSV, Excel, or PDF
   - Import bank statements
   - Backup and restore functionality
3. **Advanced Reporting**:
   - Custom date range selection
   - Year-over-year comparisons
   - Category trend analysis
   - Spending forecasts and predictions
4. **Recurring Transactions**: Automatic entry for regular income/expenses
5. **Multi-Currency Support**: Handle multiple currencies with conversion rates
6. **Receipt Management**: Upload and attach receipts/invoices to transactions
7. **Savings Goals**: Set financial goals with progress tracking
8. **Mobile Applications**: Native iOS and Android apps
9. **Family Accounts**: Shared budgets and expense tracking for households
10. **Bank Integration**: Automatic transaction import via API
11. **Budget Templates**: Pre-defined budget templates for different lifestyles
12. **Email Notifications**: Alerts for budget limits and spending patterns
13. **Dark Mode**: Theme switcher for better user experience
14. **Two-Factor Authentication**: Enhanced security with 2FA
15. **Tags and Labels**: Additional organization beyond categories

## 🗂️ Project Structure

```
finance-tracker/
├── app.py                      # Main Flask application (400+ lines)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── finance_tracker.db          # SQLite database (auto-created)
├── static/
│   └── css/
│       └── style.css          # Custom CSS with animations (500+ lines)
└── templates/                  # Jinja2 HTML templates
    ├── base.html              # Base template with navigation
    ├── login.html             # Login page
    ├── register.html          # Registration page
    ├── dashboard.html         # Main dashboard with charts
    ├── transactions.html      # Transaction list with filters
    ├── add_transaction.html   # Add transaction form
    ├── categories.html        # Category management
    ├── budgets.html          # Budget tracking page
    ├── reports.html          # Financial reports and trends
    └── profile.html          # User profile page
```

## 🔐 Security Features

- Password hashing with salt using Werkzeug
- SQL injection prevention via parameterized queries
- Session-based authentication with secure cookies
- CSRF protection through Flask's built-in features
- User data isolation (users can only access their own data)

## 🎨 Design Decisions

### Database Choice
SQLite was chosen for its simplicity, portability, and zero-configuration setup. It stores all data in a single file and is perfect for single-user applications.

### MVC Architecture
The application follows the Model-View-Controller pattern:
- **Model**: SQLite database and queries
- **View**: Jinja2 templates
- **Controller**: Flask routes and business logic

### User Experience
CSS animations were added to create a modern, polished interface that feels responsive and professional. The color-coded system (categories, budgets) provides instant visual feedback.

## 🐛 Troubleshooting

### Database Issues
If you encounter database errors, delete `finance_tracker.db` and restart the application. A fresh database will be created automatically.

### Static Files Not Loading
Ensure the `static/css/` folder exists and contains `style.css`. Clear your browser cache (Ctrl+F5 or Cmd+Shift+R).

### Port Already in Use
If port 5000 is occupied, the app will show an error. Stop any other processes using port 5000 or modify the port in `app.py`.

## 📈 Project Statistics

- **~1,500 lines of code** total
- **400+ lines** of Python
- **800+ lines** of HTML
- **500+ lines** of CSS
- **4 database tables** with relationships
- **14 Flask routes**
- **10 HTML templates**
- **40+ CSS animations**
- **7 major features**

## 👨‍💻 Development

This project was developed as a final project for a Computer Science course, demonstrating:
- Database design and relationships
- Web development with Flask
- User authentication and security
- Data visualization
- Modern UI/UX design principles


### AI Tool Usage
Claude AI was used minimally during development for:
- Debugging assistance and error corrections
- Suggestions for CSS animation improvements
- Code structure ideas and description

All code is fully understood. The core logic, database design, and feature implementation decisions were made independently.

## 📝 License

This project is created for educational purposes as a final project submission.

## 🙏 Acknowledgments

- CS50 Harvard course for inspiration
- Flask documentation for guidance
- Chart.js for visualization library
- Tailwind CSS for utility framework
- Font Awesome for icons

## 📧 Contact

**Project Created By**: 
Gbenga Akinjide Osuntoyinbo  
**Email**: 
o_gbenga_akinjide@cu.edu.ge  
**Course**: Introduction to computer science/ICS 1141  
**Submission Date**: January 31, 2026

---

**GitHub Repository**: https://github.com/osuntoyinbogbenga/finance-app

*Built with ❤️ using Python, Flask, and modern web technologies*