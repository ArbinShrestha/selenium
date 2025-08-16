# Selenium Automation Framework

A comprehensive Selenium WebDriver automation framework for testing web applications, built with Python, Pytest, and Page Object Model design pattern.

## 🚀 Features

- **Page Object Model (POM)** - Clean separation of test logic and page elements
- **Comprehensive Test Coverage** - Login, Company Registration, Bulletin Management, Admin Operations, CMS, and Role Management
- **Multiple Test Execution Options** - Smoke tests, regression tests, parallel execution
- **Rich Reporting** - HTML reports, Allure reports, JUnit XML
- **Cross-browser Support** - Chrome WebDriver with automatic driver management
- **Environment Configuration** - Environment variables for credentials and settings
- **Test Data Management** - Centralized test data and fixtures
- **Error Handling** - Robust error handling and validation
- **Performance Testing** - Page load time measurements
- **Internationalization Support** - Japanese language support

## 📁 Project Structure

```
Willc-Functional/
├── pages/                     # Page Object classes
│   ├── __init__.py
│   ├── login_page.py         # Login functionality
│   ├── companyRegistration_page.py  # Company registration
│   ├── bulletin_page.py      # Bulletin management
│   ├── admin_page.py         # Admin operations
│   ├── cms_page.py           # Content management
│   └── roles_page.py         # Role management
├── tests/                    # Test files
│   ├── test_login.py         # Login tests
│   ├── test_companyRegistration.py  # Company registration tests
│   ├── test_bulletin.py      # Bulletin tests
│   ├── test_admin.py         # Admin tests
│   ├── test_cms.py           # CMS tests
│   └── test_roles.py         # Role management tests
├── utils/                    # Utility functions
│   ├── __init__.py
│   └── driver_setup.py       # WebDriver configuration
├── images/                   # Test images
│   ├── test_logo.png
│   ├── company_banner.jpg
│   └── profile_image.png
├── allure-results/           # Allure report results
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini              # Pytest settings
├── run_tests.py             # Test runner script
└── README.md               # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Willc-Functional
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv selenium-env
   source selenium-env/bin/activate  # On Windows: selenium-env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   EMAIL=your-admin-email@example.com
   PASSWORD=your-admin-password
   ```

## 🧪 Running Tests

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py

# Run smoke tests only
python run_tests.py --smoke

# Run regression tests
python run_tests.py --regression

# Run tests for specific module
python run_tests.py --module login
python run_tests.py --module company
python run_tests.py --module bulletin
python run_tests.py --module admin
python run_tests.py --module cms
python run_tests.py --module roles

# Run specific test
python run_tests.py --test test_valid_login

# Run tests in parallel
python run_tests.py --parallel 4

# Run tests in headless mode
python run_tests.py --headless

# Generate HTML report
python run_tests.py --html

# Generate Allure report
python run_tests.py --allure
```

### Using Pytest Directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run tests with specific marker
pytest -m smoke
pytest -m regression
pytest -m login
pytest -m company

# Run tests in parallel
pytest -n 4

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Generate Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

## 📊 Test Categories

### Smoke Tests
- Basic login functionality
- Navigation tests
- Essential admin operations

### Regression Tests
- All functionality tests
- Edge cases
- Error handling
- Performance tests

### Module-specific Tests

#### Login Tests (`test_login.py`)
- Valid login
- Invalid login
- Empty credentials
- Logout functionality

#### Company Registration Tests (`test_companyRegistration.py`)
- Company information registration
- User account creation
- File uploads (logo, banner, profile)
- Validation testing

#### Bulletin Tests (`test_bulletin.py`)
- Bulletin creation
- Different statuses and designations
- Content validation
- Special characters handling

#### Admin Tests (`test_admin.py`)
- Dashboard navigation
- Company management
- Search functionality
- Table operations

#### CMS Tests (`test_cms.py`)
- Content creation and editing
- Category management
- Tag functionality
- Content filtering

#### Role Management Tests (`test_roles.py`)
- Role creation and editing
- Permission assignment
- User role assignment
- Role validation

## 🔧 Configuration

### Pytest Configuration (`pytest.ini`)
- Test discovery patterns
- Markers definition
- Report generation settings
- Warning filters

### Environment Variables (`.env`)
```env
EMAIL=admin@example.com
PASSWORD=admin_password
BASE_URL=https://willc.tai.com.np
```

### WebDriver Configuration (`utils/driver_setup.py`)
- Chrome options
- Driver management
- Headless mode support

## 📈 Reporting

### HTML Reports
- Self-contained HTML reports
- Test results with screenshots
- Detailed test information

### Allure Reports
- Interactive test reports
- Test execution timeline
- Environment information
- Screenshots and logs

### JUnit XML
- CI/CD integration
- Test result parsing
- Build system compatibility

## 🎯 Test Data Management

### Fixtures (`conftest.py`)
- Reusable test data
- WebDriver fixtures
- Authentication fixtures
- Image path management

### Test Data Structure
```python
test_data = {
    "company": {
        "name": "Test Company",
        "email": "test@example.com",
        # ... more fields
    },
    "user": {
        "lastname": "山田",
        "firstname": "太郎",
        # ... more fields
    }
}
```

## 🔍 Debugging and Troubleshooting

### Common Issues

1. **WebDriver Issues**
   - Ensure Chrome browser is installed
   - Check ChromeDriver compatibility
   - Verify PATH environment variable

2. **Element Not Found**
   - Check element selectors
   - Verify page load timing
   - Review dynamic content handling

3. **Test Failures**
   - Check environment variables
   - Verify test data
   - Review application state

### Debug Mode
```bash
# Run with verbose output
pytest -v -s

# Run specific failing test
pytest -k "test_name" -v -s

# Run with maximum verbosity
pytest -vvv
```

## 🚀 CI/CD Integration

### GitHub Actions Example
```yaml
name: Selenium Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python run_tests.py --headless
    - name: Upload reports
      uses: actions/upload-artifact@v2
      with:
        name: test-reports
        path: reports/
```

## 📝 Best Practices

1. **Page Object Model**
   - Keep page elements in page classes
   - Separate test logic from page interactions
   - Use descriptive method names

2. **Test Organization**
   - Group related tests together
   - Use meaningful test names
   - Add proper documentation

3. **Data Management**
   - Use fixtures for test data
   - Avoid hardcoded values
   - Centralize configuration

4. **Error Handling**
   - Implement proper wait strategies
   - Handle dynamic content
   - Add meaningful error messages

5. **Maintenance**
   - Regular selector updates
   - Test data refresh
   - Framework updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review existing test examples

## 🔄 Version History

- **v1.0.0** - Initial release with basic functionality
- **v1.1.0** - Added CMS and Role management
- **v1.2.0** - Enhanced reporting and parallel execution
- **v1.3.0** - Added performance testing and error handling
