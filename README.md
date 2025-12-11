# Testing Platform

A secure web-based testing platform with AES-256 encryption for questions, answers, and results.

## Features

- **Three User Roles**: Admin, Teacher, and Student
- **AES-256 Encryption**: All questions, answers, and results are encrypted
- **Secure Authentication**: Bcrypt password hashing with account lockout
- **Role-Based Access Control**: Different permissions for each user type
- **Session Management**: Secure session handling with timeout
- **Audit Logging**: Complete audit trail of all actions
- **Rate Limiting**: Protection against brute force attacks

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite/MySQL (configurable)
- **Encryption**: AES-256-GCM
- **Authentication**: Flask-Login, bcrypt
- **Frontend**: Bootstrap 5, jQuery

## Installation

### Prerequisites

- Python 3.9 or higher
- pip
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd testing-platform
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example environment file
   copy .env.example .env
   
   # Edit .env and set your values:
   # - SECRET_KEY (generate a strong random key)
   # - ENCRYPTION_KEY (exactly 32 characters for AES-256)
   # - DATABASE_URI (if using MySQL)
   ```

5. **Initialize database**
   ```bash
   python scripts/init_db.py
   ```

6. **Create admin user**
   ```bash
   python scripts/create_admin.py
   ```

## Running the Application

### Development Mode

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`

### Production Mode

```bash
# Set environment
set FLASK_ENV=production

# Run with Gunicorn (Linux/Mac)
gunicorn wsgi:app -w 4 -b 0.0.0.0:5000

# Run with waitress (Windows)
waitress-serve --host 0.0.0.0 --port 5000 wsgi:app
```

## Default Credentials

After running `create_admin.py`:

- **Username**: admin
- **Password**: Admin@123 (or the one you set)

**⚠️ Change the password immediately after first login!**

## Project Structure

```
testing-platform/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config/              # Configuration files
│   ├── models/              # Database models
│   ├── services/            # Business logic
│   ├── api/                 # API endpoints
│   ├── middleware/          # Middleware (to be implemented)
│   ├── extensions/          # Flask extensions
│   ├── utils/               # Utilities
│   ├── static/              # CSS, JS, images
│   └── templates/           # HTML templates
├── scripts/                 # Utility scripts
├── tests/                   # Test files
├── docs/                    # Documentation
├── storage/                 # File storage
├── logs/                    # Log files
├── requirements.txt         # Python dependencies
├── run.py                   # Development server
└── wsgi.py                  # Production server
```

## Security Features

✅ **Encryption**: AES-256-GCM for all sensitive data  
✅ **Password Hashing**: bcrypt with salt  
✅ **Session Security**: Secure cookies, HTTPOnly, SameSite  
✅ **CSRF Protection**: Enabled in production  
✅ **Rate Limiting**: Login attempts and API requests  
✅ **Audit Logging**: All actions logged with IP and timestamp  
✅ **Account Lockout**: After 5 failed login attempts  
✅ **Input Validation**: All user inputs validated  

## Team Division

This project is divided into 5 parts for team collaboration:

- **Part 1**: Core Infrastructure & Security (You are here!)
- **Part 2**: Admin Module
- **Part 3**: Teacher Module
- **Part 4**: Student Module
- **Part 5**: Testing & Documentation

See `PROJECT_DIVISION.md` for detailed task breakdown.

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to all functions
- Keep functions small and focused

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Description of changes"

# Push to remote
git push origin feature/your-feature-name

# Create pull request for review
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app
```

## Common Issues

### Database Connection Error

If you get a database connection error:
- Check your `DATABASE_URI` in `.env`
- Make sure SQLite file has write permissions
- For MySQL: ensure service is running

### Encryption Key Error

If you get encryption errors:
- Ensure `ENCRYPTION_KEY` in `.env` is exactly 32 characters
- Don't change the key after encrypting data

### Import Errors

If you get import errors:
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Documentation

- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Security Guide](docs/SECURITY.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [User Manual](docs/USER_MANUAL.md)

## Contributing

1. Read the project division document
2. Pick up a task from your assigned part
3. Create a feature branch
4. Write code and tests
5. Submit pull request
6. Wait for review

## License

This project is created for educational purposes.

## Support

For issues and questions:
- Check the documentation in `docs/`
- Review task files: `PART_X_*.md`
- Ask team members on your communication channel

---

**Good luck with your project! 🚀**
