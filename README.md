# streamlit-analytics &nbsp;👀

[![PyPi](https://img.shields.io/pypi/v/streamlit-analytics)](https://pypi.org/project/streamlit-analytics/)

**Track & visualize user interactions with your streamlit app.**

This is a small extension for the fantastic [streamlit](https://www.streamlit.io/) 
framework. With just one line of code, it counts page views, tracks all widget 
interactions across users, and visualizes the results directly in your browser. 
Think Google Analytics but for streamlit.

<sup>Alpha version, use with care.</sup>

<p align="center">
    <img src="images/example.png" width=600>
</p>


## Installation

```bash
pip install streamlit-analytics
```


## How to use it

```python
import streamlit as st
import streamlit_analytics

with streamlit_analytics.track():
    st.text_input("Write something")
    st.button("Click me")
```

That's it! 🎈 All page views and user inputs are now tracked and counted. Of course, 
you can also use [any other streamlit widget](https://docs.streamlit.io/en/stable/api.html#add-widgets-to-sidebar) 
in the `with` block (both from `st.` and `st.sidebar.`). 

<sub>Note: One thing that doesn't work (yet) is tracking widgets created directly from 
containers, expanders, or columns (e.g. `st.beta_expander().button("foo")`). Instead, 
please use a with statement, e.g. `with st.beta_expander(): st.button("foo")`.</sub>

To view the results, open your app like normal and append `?analytics=on` to the URL 
(e.g. http://localhost:8501/?analytics=on). The results are then shown directly below 
your app (see image above).


## More options

- You can **password-protect** your analytics results with 
`streamlit_analytics.track(unsafe_password="test123")`. The streamlit app will then ask you 
for this password. Do not choose an important password here – it is sent without 
encryption.
- You can persist your analytics results to a **Firestore database**. By default, your results get reset if you restart streamlit (e.g. if you deploy). 
To set up the Firestore database, follow [this blogpost](https://blog.streamlit.io/streamlit-firestore/)
 and pass the key file and collection name as 
`streamlit_analytics.track(firebase_key_file="firebase-key.json" firebase_collection_name="counts")`.
- If you don't want a **huge `with` block**, you can also do:

    ```python
    import streamlit_analytics

    streamlit_analytics.start_tracking()
    # your streamlit code here
    streamlit_analytics.stop_tracking()
    ```

- You can **store analytics results as a json file** by passing 
`save_to_json="path/to/file.json"` to `streamlit_analytics.track` or 
`streamlit_analytics.stop_tracking`. At the moment, this may lead to problems with 
concurrency if many users access the site at the same time. 


## TODO

PRs are welcome! If you want to work on any of these things, please open an issue to coordinate. 

- [ ] Track unique users (probably requires cookies? but would we need to show a consent form then?)
- [ ] Enable tracking on widgets created directly from beta_container, beta_expander, beta_columns
- [ ] Make a demo gif for the readme
- [x] ~~Persist results after re-starting app (e.g. database or file, but where should this be saved/hosted)~~
- [ ] Find an easier alternative to Firestore for saving the data
- [x] ~~Track time the user spent in a session and show as "complete time spent on your app"~~
- [ ] Implement A/B testing, e.g. by choosing one option for a new user randomly, storing it 
in session object, and then returning the correct bool value for below, and tracking
& visualizing stats separately for both options:
 
    ```python
    if streamlit_analytics.split_test("option a", 2):
        st.button("Is this button text better?")

    if streamlit_analytics.split_test("option b", 2):
        st.button("...or this one?")
    ```

- [ ] Enable tracking to Google Analytics, e.g. via custom component with [react-ga](https://github.com/react-ga/react-ga). Widget interactions could also be tracked via [events](https://github.com/react-ga/react-ga#reactgaeventargs).
