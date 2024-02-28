
# Contributing to Streamlit-Analytics

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with GitHub

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use GitHub Flow

All code changes happen through pull requests, so we suggest you familiarize yourself with [GitHub Flow](https://guides.github.com/introduction/flow/). Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. Make sure your code lints.
3. Issue that pull request!

## Any contributions you make will be under the same license as the project

In short, when you submit code changes, your submissions are understood to be under the same [license](LICENSE.md) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/jrieke/streamlit-analytics/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/jrieke/streamlit-analytics/issues/new); it's that easy!

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style

- We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Ensure your code passes flake8 linting:
  ```sh
  pipenv run flake8
  ```
- Format your code with Black:
  ```sh
  pipenv run black .
  ```

## License

By contributing, you agree that your contributions will be licensed under its [License](LICENSE.md).

## Guide to Setting Up a Testing/Dev Environment

1. Navigate to the directory you want to clone the repo into:
    ```sh
    cd path/to/your/project/location
    ```

2. Clone the repo:
    ```sh
    git clone https://github.com/jrieke/streamlit-analytics.git
    ```

3. Navigate into the repo:
    ```sh
    cd streamlit-analytics
    ```

4. Create a new branch:
    ```sh
    git checkout -b name_of_your_new_branch
    ```

5. Ensure you have Python 3.8.x and pipenv installed on your system. If not, you can install pipenv using pip:
    ```sh
    pip install pipenv
    ```

6. Install project dependencies using pipenv. This step will create a virtual environment specific to this project and install all required dependencies within it:
    ```sh
    pipenv install --dev
    ```
    This command installs all regular and development dependencies needed for the project. The `--dev` flag ensures that tools required for development, such as linters and testing frameworks, are also installed.

7. Activate the pipenv virtual environment to start working on the project:
    ```sh
    pipenv shell
    ```
    This command activates the virtual environment. You need to do this before running any project-related commands to ensure they use the correct Python and dependencies versions.

8. Run the minimal example file:
    ```sh
    streamlit run examples/minimal.py
    ```
    At this point, you should see a basic streamlit app and can begin testing any changes you wish to contribute in a PR.
