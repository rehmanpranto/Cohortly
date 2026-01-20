# Cohortly - Bootcamp Management System

A complete, production-ready bootcamp management platform built with Python Flask.

## 🚀 Features

- **CRM & Lead Management**: Track leads, manage conversions, and build your student pipeline
- **Learning Management System (LMS)**: Complete course management with modules, lessons, and content delivery
- **Enrollment & Payments**: Secure payment processing and enrollment management
- **Assignment & Grading**: Assignment submission, grading, and feedback system
- **Analytics & Reporting**: Comprehensive dashboards with revenue, enrollment, and performance metrics
- **Certificate Generation**: Automated certificate generation with verification codes
- **Role-Based Access**: 5 user roles (Admin, Sales, Instructor, Mentor, Student) with proper access control
- **Communication**: Announcements, notifications, and messaging system

## 🛠 Tech Stack

- **Backend**: Python 3.11+, Flask 3.0.0
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: Flask-Login + bcrypt password hashing
- **Forms**: Flask-WTF with CSRF protection
- **Migrations**: Alembic
- **Frontend**: Jinja2 templates + Tailwind CSS
- **Server**: Gunicorn (production)

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Neon recommended)
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/rehmanpranto/Cohortly.git
cd Bmc
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `SECRET_KEY`: Generate a secure random key
- `DATABASE_URL`: Your PostgreSQL connection string (already configured for Neon)
- `JWT_SECRET_KEY`: Another secure random key

### 5. Initialize the database

```bash
# Create all tables
python -m app.seeds.init_db
```

### 6. Create admin user

```bash
# Create the initial admin account
python -m app.seeds.create_admin
```

This will create an admin user. Check the script output for login credentials.

⚠️ **Important**: Change the default password immediately after first login!

### 7. Run the application

```bash
# Development server
flask run

# Or with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
Bmc/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuration classes
│   ├── extensions.py         # Flask extensions
│   ├── models.py             # Database models (20+ tables)
│   ├── auth/                 # Authentication module
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── utils.py         # Password hashing, decorators
│   ├── crm/                  # CRM & Lead management
│   │   └── routes.py
│   ├── lms/                  # Learning Management System
│   │   └── routes.py
│   ├── payments/             # Payment processing
│   │   └── routes.py
│   ├── analytics/            # Analytics & reporting
│   │   └── routes.py
│   ├── certificates/         # Certificate generation
│   │   └── routes.py
│   ├── templates/            # Jinja2 templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── admin/
│   │   ├── student/
│   │   └── shared/
│   ├── static/               # Static files (CSS, JS, images)
│   └── seeds/                # Database initialization scripts
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── IMPLEMENTATION_GUIDE.md  # Detailed implementation guide
```

## 👥 User Roles

1. **Admin**: Full system access, analytics, user management
2. **Sales**: Lead management, CRM, conversions
3. **Instructor**: Course management, assignments, grading
4. **Mentor**: Student support, batch monitoring
5. **Student**: Course access, assignment submission

## 🔐 Default Login

After running the setup, check the output of `create_admin.py` for the login credentials.

**Security Note**: Change the default password immediately after first login!

## 📊 Database Models

The system includes 20+ database models:

- **Authentication**: User, RefreshToken
- **CRM**: Lead, LeadLog
- **Bootcamp**: Bootcamp, Batch, InstructorBatch, MentorBatch
- **Enrollment**: Enrollment, Payment
- **LMS**: Module, Lesson, Resource, Attendance
- **Assignments**: Assignment, Submission, Grade
- **Communication**: Announcement, Notification
- **Certificates**: Certificate

All models use UUIDs for primary keys and include proper relationships and cascade deletes.

## 🚀 Deployment

### Production Checklist

1. Set strong `SECRET_KEY` and `JWT_SECRET_KEY`
2. Use production database (not development DB)
3. Set `FLASK_ENV=production`
4. Enable HTTPS
5. Configure proper CORS if needed
6. Set up database backups
7. Configure logging
8. Use Gunicorn with multiple workers
9. Set up reverse proxy (nginx)
10. Enable database connection pooling

### Running with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 main:app
```

## 🧪 Testing

```bash
# Run tests (coming soon)
pytest
```

## 📝 API Documentation

The system uses server-side rendering with Jinja2 templates. For API endpoints, refer to the route files in each module.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check `IMPLEMENTATION_GUIDE.md` for detailed documentation

## 🎯 Roadmap

- [ ] Email notifications
- [ ] File upload for assignments
- [ ] Video streaming integration
- [ ] Mobile responsive improvements
- [ ] API endpoints for mobile app
- [ ] Bulk operations
- [ ] Advanced analytics
- [ ] Payment gateway integrations (Stripe, PayPal)

---

Built with ❤️ for real bootcamp operations.
