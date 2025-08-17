# CI/CD Setup Guide

This guide will help you set up Continuous Integration/Continuous Deployment (CI/CD) for your Selenium automation framework using GitHub Actions.

## 🚀 Quick Setup

### 1. Repository Setup

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add Selenium automation framework"
   git push origin main
   ```

2. **Verify file structure**:
   ```
   Willc-Functional/
   ├── .github/
   │   └── workflows/
   │       ├── quick-tests.yml
   │       └── selenium-tests.yml
   ├── pages/
   ├── tests/
   ├── utils/
   ├── requirements.txt
   ├── conftest.py
   ├── pytest.ini
   ├── run_tests.py
   └── README.md
   ```

### 2. GitHub Secrets Configuration

1. **Go to your GitHub repository**
2. **Navigate to Settings → Secrets and variables → Actions**
3. **Add the following secrets**:

   | Secret Name | Description | Example |
   |-------------|-------------|---------|
   | `TEST_EMAIL` | Test account email | `admin@example.com` |
   | `TEST_PASSWORD` | Test account password | `your_password_here` |

4. **Click "New repository secret"** for each:
   - Name: `TEST_EMAIL`
   - Value: Your actual test email
   - Name: `TEST_PASSWORD`
   - Value: Your actual test password

### 3. Update Badge URLs

1. **Edit README.md**
2. **Replace `yourusername` with your actual GitHub username**:
   ```markdown
   [![CI/CD](https://github.com/YOUR_ACTUAL_USERNAME/Willc-Functional/actions/workflows/quick-tests.yml/badge.svg)](https://github.com/YOUR_ACTUAL_USERNAME/Willc-Functional/actions/workflows/quick-tests.yml)
   ```

### 4. Trigger First Run

```bash
git add .
git commit -m "Configure CI/CD workflows"
git push origin main
```

## 📋 Workflow Details

### Quick Tests Workflow (`quick-tests.yml`)

**Purpose**: Fast feedback for development
**Triggers**: Push to main/develop, Pull requests
**Execution Time**: ~5-10 minutes

**Features**:
- ✅ Smoke tests only
- ✅ HTML report generation
- ✅ Screenshot capture on failure
- ✅ Dependency caching
- ✅ Chrome browser setup

### Full Test Suite Workflow (`selenium-tests.yml`)

**Purpose**: Comprehensive testing
**Triggers**: Push to main/develop, Pull requests
**Execution Time**: ~15-30 minutes

**Features**:
- ✅ Multiple Python versions (3.9, 3.10, 3.11)
- ✅ Parallel test execution
- ✅ All test modules (login, company, bulletin, admin, cms, roles)
- ✅ Performance testing
- ✅ Multiple report formats (HTML, Allure, JUnit XML)
- ✅ Artifact storage

## 🔧 Customization Options

### 1. Modify Trigger Branches

Edit `.github/workflows/quick-tests.yml`:
```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # Add your branches
  pull_request:
    branches: [ main, develop ]
```

### 2. Change Python Versions

Edit `.github/workflows/selenium-tests.yml`:
```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, 3.10, 3.11]  # Add/remove versions
```

### 3. Add Custom Test Commands

Edit the workflow files to add custom test execution:
```yaml
- name: Run custom tests
  run: |
    python run_tests.py --module login
    python run_tests.py --module company
```

### 4. Configure Notifications

Add notification steps to workflows:
```yaml
- name: Notify on failure
  if: failure()
  run: |
    echo "Tests failed! Check the reports."
    # Add your notification logic here
```

## 📊 Monitoring and Reports

### 1. View Workflow Runs

1. **Go to your GitHub repository**
2. **Click "Actions" tab**
3. **View workflow runs and their status**

### 2. Access Test Reports

1. **Click on a workflow run**
2. **Scroll down to "Artifacts"**
3. **Download test reports**:
   - `quick-test-reports` - HTML reports
   - `failure-screenshots` - Screenshots on failure

### 3. View Allure Reports

1. **Download allure-results artifact**
2. **Install Allure locally**:
   ```bash
   npm install -g allure-commandline
   ```
3. **Generate report**:
   ```bash
   allure serve allure-results/
   ```

## 🚨 Troubleshooting

### Common Issues

#### 1. Workflow Not Triggering
- **Check branch names** in workflow files
- **Verify file paths** are correct
- **Check GitHub Actions permissions**

#### 2. Tests Failing
- **Verify secrets** are set correctly
- **Check test environment** is accessible
- **Review test data** and credentials

#### 3. Chrome Installation Issues
- **Check Chrome installation** steps in workflow
- **Verify DISPLAY environment** variable
- **Review Chrome version** compatibility

#### 4. Dependency Issues
- **Check requirements.txt** is up to date
- **Verify Python version** compatibility
- **Review cache configuration**

### Debug Steps

1. **Check workflow logs**:
   - Go to Actions → Click on failed run → Check step logs

2. **Test locally first**:
   ```bash
   python run_tests.py --smoke
   ```

3. **Verify environment**:
   ```bash
   python -c "import selenium; print(selenium.__version__)"
   ```

4. **Check secrets**:
   - Verify secrets are set correctly
   - Test with dummy values first

## 🔄 Maintenance

### Regular Tasks

1. **Update dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Review test reports**:
   - Check for flaky tests
   - Update selectors if needed
   - Review performance metrics

3. **Update workflow files**:
   - Keep GitHub Actions versions updated
   - Review and optimize execution time
   - Add new test modules as needed

### Best Practices

1. **Keep workflows fast**:
   - Use caching effectively
   - Run only necessary tests
   - Optimize test execution order

2. **Maintain security**:
   - Never commit secrets to code
   - Use GitHub secrets for sensitive data
   - Regularly rotate test credentials

3. **Monitor performance**:
   - Track execution times
   - Identify slow tests
   - Optimize test data and setup

## 📞 Support

If you encounter issues:

1. **Check GitHub Actions documentation**
2. **Review workflow logs** for specific errors
3. **Test locally** to isolate issues
4. **Update this guide** with solutions you find

## 🎯 Next Steps

After successful CI/CD setup:

1. **Add more test modules** as your application grows
2. **Implement test data management** for different environments
3. **Add performance monitoring** and alerts
4. **Set up deployment pipelines** if needed
5. **Configure team notifications** for test results

