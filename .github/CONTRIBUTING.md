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

All code changes happen through pull requests, so we suggest you familiarize yourself with [GitHub Flow](https://guides.github.com/introduction/flow/). Pull requests are the best way to propose changes to the codebase (we use [GitHub Flow](https://guides.github.com/introduction/flow/)). We actively welcome your pull requests:

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

TO BE DETERMINED

## License

By contributing, you agree that your contributions will be licensed under its [License](LICENSE.md).

## Guide to setting up a testing/dev environment
1. navigate to the directory you want to clone the repo into
```
cd path_to_your_project_location
```

2. clone the repo
```
git clone https://github.com/jrieke/streamlit-analytics.git
```

3. navigate into the repo
```
cd streamlit-analytics
```

4. create a new branch
```
git checkout -b name_of_your_new_branch
```

5. create a venv
```
python3 -m venv env
```

6. activate the virtual environment
```
Linux: source env/bin/activate
Windows: env\Scripts\activate
```
Note: make sure to restart any terminals and make sure the word (env) is in front of the terminal prompt

7. install the requirements
```
pip install -r examples/requirements.txt
```

8. run the minimal.py file
```
streamlit run examples/minimal.py
```

--- 
At this point you should see a basic streamlit app and can begin testing and changes you may wish to contrubute in a PR 

Please note that to accurately test any changes, you need to take into account that the streamlit-analytics package is in your main directory but it is also loaded as a module by pip and when you run streamlit it is using the pip version of streamlit analytics files and NOT the main files you are editing.

Therefore, you will need to test the desired changes by making changes to the env/Lib/streamlit-analytics files *first* to understand what changes are being made.
