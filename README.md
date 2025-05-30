# Django Testing Framework Showcase

A comprehensive testing implementation for Django applications demonstrating best practices with both **unittest** and **pytest** frameworks. This project showcases advanced testing techniques for two distinct Django applications with different testing approaches.

## 🎯 Project Overview

This repository contains a complete testing suite for two Django applications:
- **YaNews** - News portal with commenting system (tested with pytest)
- **YaNote** - Personal notes management (tested with unittest)

## 🏗️ Architecture

```
django_testing/
├── ya_news/                    # News Application
│   ├── news/                   
│   │   ├── pytest_tests/       # Pytest implementation
│   │   │   ├── conftest.py     # Fixtures and configuration
│   │   │   ├── test_routes.py  # URL routing tests
│   │   │   ├── test_content.py # Template and context tests
│   │   │   └── test_logic.py   # Business logic tests
│   │   ├── models.py           # News and Comment models
│   │   ├── views.py            # Class-based views
│   │   └── forms.py            # Comment validation forms
│   └── templates/              # News application templates
│
├── ya_note/                    # Notes Application
│   ├── notes/                  
│   │   ├── tests/              # Unittest implementation
│   │   │   ├── test_routes.py  # URL access control tests
│   │   │   ├── test_content.py # Content isolation tests
│   │   │   └── test_logic.py   # CRUD operations tests
│   │   ├── models.py           # Note model with slug generation
│   │   ├── views.py            # CRUD views with permissions
│   │   └── forms.py            # Note creation/editing forms
│   └── templates/              # Notes application templates
│
├── requirements.txt            # Project dependencies
├── setup.cfg                   # Linting configuration
└── run_tests.sh               # Automated test runner
```

## 🧪 Testing Coverage

### YaNews (Pytest Framework)
- **Route Testing**: Anonymous/authenticated user access patterns
- **Content Validation**: News pagination, comment sorting, form availability
- **Business Logic**: Comment creation, moderation, CRUD permissions
- **Advanced Features**: Profanity filtering, user isolation

### YaNote (Unittest Framework)
- **Access Control**: Note ownership and permission validation
- **Content Management**: CRUD operations with proper authorization
- **Slug Generation**: Automatic URL-friendly slug creation from titles
- **Data Isolation**: User-specific note visibility

## 🔧 Key Features

### Advanced Testing Patterns
- **Parametrized Tests**: Efficient testing of multiple scenarios
- **Fixture Management**: Reusable test data with proper cleanup
- **Permission Testing**: Comprehensive access control validation
- **Form Validation**: Input sanitization and error handling

### Security Testing
- **Authentication**: Login/logout flow validation
- **Authorization**: Resource access control
- **Data Isolation**: Cross-user data protection
- **Input Validation**: XSS and injection prevention

### Performance Considerations
- **Optimized Queries**: Prefetch related objects to avoid N+1 problems
- **Efficient Fixtures**: Minimal database operations in tests
- **Proper Cleanup**: Transaction rollback between tests

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Django 3.2.15
- pytest 7.1.3

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd django_testing

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

#### Complete Test Suite
```bash
# Run all tests with linting
./run_tests.sh
```

#### Individual Applications
```bash
# YaNote (unittest)
cd ya_note
python manage.py test

# YaNews (pytest)
cd ya_news
pytest
```

#### Test Coverage Analysis
```bash
# Run with coverage report
cd ya_news
pytest --cov=news --cov-report=html

cd ya_note
coverage run --source='.' manage.py test
coverage html
```

## 📊 Testing Metrics

| Application | Framework | Test Files | Test Cases | Coverage |
|-------------|-----------|------------|------------|----------|
| YaNews      | pytest    | 3          | 15+        | ~95%     |
| YaNote      | unittest  | 3          | 20+        | ~95%     |

## 🛠️ Technical Implementation

### Database Strategy
- **SQLite**: Lightweight testing database
- **Transactions**: Automatic rollback between tests
- **Fixtures**: Consistent test data setup

### Authentication System
- **Django Auth**: Built-in user management
- **Permission Mixins**: LoginRequiredMixin for protected views
- **Session Management**: Proper login/logout handling

### Form Validation
- **Custom Validators**: Profanity filtering, slug uniqueness
- **Error Handling**: User-friendly error messages
- **CSRF Protection**: Cross-site request forgery prevention

## 📈 Best Practices Demonstrated

### Test Organization
- **Clear Naming**: Descriptive test method names
- **Logical Grouping**: Related tests in same class
- **Documentation**: Comprehensive docstrings

### Code Quality
- **PEP8 Compliance**: Automated linting with flake8
- **DRY Principles**: Reusable test utilities and fixtures
- **Separation of Concerns**: Clear test responsibility boundaries

### Maintainability
- **Modular Design**: Independent test modules
- **Configuration Management**: Centralized settings
- **Version Control**: Proper .gitignore and structure

## 🔍 Code Quality Tools

- **flake8**: Style guide enforcement
- **pytest-django**: Django-specific pytest features
- **pytest-lazy-fixture**: Dynamic fixture loading
- **pytils**: Russian language transliteration

## 🎓 Learning Outcomes

This project demonstrates mastery of:
- **Testing Frameworks**: Both unittest and pytest methodologies
- **Django Patterns**: Class-based views, model relationships, form handling
- **Security Practices**: Authentication, authorization, data validation
- **Code Organization**: Clean architecture and separation of concerns

## 👨‍💻 Author

**Grigoriy Sokolov**  
Python Developer | Fintech Specialist  

---

This project serves as a comprehensive demonstration of Django testing capabilities and modern Python development practices, suitable for portfolio presentation and technical interviews.
