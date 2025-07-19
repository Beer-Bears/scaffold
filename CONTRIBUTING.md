# Contributing to Scaffold

Thank you for your interest in contributing to Scaffold! This guide provides the essential information to get your development environment set up and start contributing.

## Development Setup

Follow these steps to set up the project for local development.

### 1. Fork & Clone the Repository

First, fork the [main repository](https://github.com/Beer-Bears/scaffold) on GitHub, and then clone your fork to your local machine.

~~~bash
git clone https://github.com/YOUR_USERNAME/scaffold.git
cd scaffold
~~~

### 2. Install Dependencies

We use [Poetry](https://python-poetry.org/) to manage project dependencies. Install them by running:

~~~bash
poetry install
~~~
This command will create a virtual environment and install all necessary packages, including development tools.

### 3. Install and Use Pre-commit Hooks

We use pre-commit hooks to ensure code quality and consistent formatting. This is a crucial step. Install the hooks using our Makefile command:

~~~bash
make pre-commit-install
~~~

Now, every time you `git commit`, the pre-commit hooks will run automatically to check and format your changes. If a hook fails, it may modify some files. Simply `git add` the modified files and commit again.

To run the hooks on all files at any time, use:
~~~bash
make pre-commit-run
~~~

### 4. Verify Your Setup

To ensure everything is working correctly, you can run the test suite. You may need to pull the test data first.

~~~bash
# Clone the repository with test projects
make pull-testgroup

# Run the tests
make test
~~~

You are now ready to start developing!