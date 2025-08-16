#!/usr/bin/env python3
"""
Test Runner Script for Selenium Automation Framework
Provides easy execution of different test suites with various options.
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr

def create_reports_directory():
    """Create reports directory if it doesn't exist"""
    if not os.path.exists("reports"):
        os.makedirs("reports")
        print("Created reports directory")

def run_smoke_tests():
    """Run smoke tests"""
    print("Running smoke tests...")
    command = "pytest -m smoke -v"
    return run_command(command)

def run_regression_tests():
    """Run regression tests"""
    print("Running regression tests...")
    command = "pytest -m regression -v"
    return run_command(command)

def run_specific_module(module):
    """Run tests for a specific module"""
    print(f"Running tests for module: {module}")
    command = f"pytest tests/test_{module}.py -v"
    return run_command(command)

def run_specific_test(test_name):
    """Run a specific test"""
    print(f"Running test: {test_name}")
    command = f"pytest -k {test_name} -v"
    return run_command(command)

def run_with_parallel(workers=4):
    """Run tests in parallel"""
    print(f"Running tests in parallel with {workers} workers...")
    command = f"pytest -n {workers} -v"
    return run_command(command)

def run_with_headless():
    """Run tests in headless mode"""
    print("Running tests in headless mode...")
    os.environ["HEADLESS"] = "true"
    command = "pytest -v"
    return run_command(command)

def generate_allure_report():
    """Generate Allure report"""
    print("Generating Allure report...")
    command = "allure serve allure-results"
    return run_command(command)

def generate_html_report():
    """Generate HTML report"""
    print("Generating HTML report...")
    command = "pytest --html=reports/report.html --self-contained-html"
    return run_command(command)

def main():
    parser = argparse.ArgumentParser(description="Selenium Test Runner")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--regression", action="store_true", help="Run regression tests")
    parser.add_argument("--module", type=str, help="Run tests for specific module (login, company, bulletin, admin, cms, roles)")
    parser.add_argument("--test", type=str, help="Run specific test by name")
    parser.add_argument("--parallel", type=int, default=4, help="Run tests in parallel with specified number of workers")
    parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
    parser.add_argument("--allure", action="store_true", help="Generate Allure report")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    # Create reports directory
    create_reports_directory()
    
    # Set environment variables
    os.environ["PYTHONPATH"] = os.getcwd()
    
    start_time = datetime.now()
    print(f"Test execution started at: {start_time}")
    
    try:
        if args.smoke:
            return_code, stdout, stderr = run_smoke_tests()
        elif args.regression:
            return_code, stdout, stderr = run_regression_tests()
        elif args.module:
            return_code, stdout, stderr = run_specific_module(args.module)
        elif args.test:
            return_code, stdout, stderr = run_specific_test(args.test)
        elif args.parallel:
            return_code, stdout, stderr = run_with_parallel(args.parallel)
        elif args.headless:
            return_code, stdout, stderr = run_with_headless()
        elif args.allure:
            return_code, stdout, stderr = generate_allure_report()
        elif args.html:
            return_code, stdout, stderr = generate_html_report()
        elif args.all:
            return_code, stdout, stderr = run_regression_tests()
        else:
            # Default: run all tests
            return_code, stdout, stderr = run_regression_tests()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\nTest execution completed at: {end_time}")
        print(f"Total duration: {duration}")
        
        if return_code == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            print(f"Return code: {return_code}")
        
        if stdout:
            print("\nOutput:")
            print(stdout)
        
        if stderr:
            print("\nErrors:")
            print(stderr)
        
        return return_code
        
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
