# streamlit-analytics &nbsp;👀

[![PyPi](https://img.shields.io/pypi/v/streamlit-analytics)](https://pypi.org/project/streamlit-analytics/)

**Track & visualize user interactions with your streamlit app.**

This is a small extension for the fantastic [streamlit](https://www.streamlit.io/)
framework. With just one line of code, it counts page views, tracks all widget
interactions across users, and visualizes the results directly in your browser.
Think Google Analytics but for streamlit.

<sup>Alpha version, use with care.</sup>

---

<h3 align="center">
  🎈 <a href="https://share.streamlit.io/jrieke/streamlit-analytics/main/examples/sharing-demo.py?analytics=on">Live Demo</a> 🎈
</h3>

---

<p align="center">
    <a href="https://share.streamlit.io/jrieke/streamlit-analytics/main/examples/sharing-demo.py?analytics=on"><img src="images/example.png" width=600></a>
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

- If you don't want a **huge `with` block**, you can also do:

  ```python
  streamlit_analytics.start_tracking()
  # your streamlit code here
  streamlit_analytics.stop_tracking()
  ```

- You can **password-protect** your analytics results with:

  ```python
  streamlit_analytics.track(unsafe_password="test123")
  # or pass the same arg to `stop_tracking`
  ```

  The app will then ask for this password before showing any results. Do not choose an
  important password here, it's not encrypted. If you push your code to Github, you
  should probably store the password in a `.env` file (which is in `.gitignore`) and
  load it via [dotenv](https://github.com/theskumar/python-dotenv).

- If you don't want the results to get reset after restarting streamlit (e.g. during
  deployment), you can sync them to a **Firestore database**. Follow
  [this blogpost](https://blog.streamlit.io/streamlit-firestore/) to set up the database
  and pass the key file and collection name:

  ```python
  streamlit_analytics.track(firestore_key_file="firebase-key.json", firestore_collection_name="counts")
  # or pass the same args to `start_tracking` AND `stop_tracking`
  ```

- You can **store analytics results as a json file** with:

  ```python
  streamlit_analytics.track(save_to_json="path/to/file.json")
  # or pass the same arg to `stop_tracking`
  ```

  And load with:

  ```python
  streamlit_analytics.track(load_from_json="path/to/file.json")
  # or pass the same arg to `start_tracking`
  ```

  (Thanks to @Uranium2 for implementing loading!)

  You can also combine both args to persist data to a json file. Note that this 
  file might get deleted when doing a fresh deploy on a cloud service. Use Firestore
  instead for persistence, see above. Also note that `load_from_json` will fail silently
  if the JSON file does not exist. Writing to JSON may lead to problems with concurrency 
  if many users access the site at the same time.

## TODO

PRs are welcome! If you want to work on any of these things, please open an issue to coordinate.

- [ ] Pass all settings args in start_tracking and not in stop_tracking
- [ ] Do not track default values for selectbox, text_input etc. This can probably be done easily if I switch to using `on_change`. 
- [ ] Track unique users -> best way is to use cookies (e.g. with [react-cookies](https://www.npmjs.com/package/react-cookie)) but this probably requires to show a consent form (could also build this in with [react-cookie-consent](https://www.npmjs.com/package/react-cookie-consent))
- [ ] Enable tracking on widgets created directly from beta_container, beta_expander, beta_columns
- [ ] Make a demo gif for the readme
- [x] ~~Persist results after re-starting app (e.g. database or file, but where should this be saved/hosted)~~
- [ ] Find an easier alternative to Firestore for saving the data
- [x] ~~Track time the user spent in a session and show as "complete time spent on your app"~~
- [ ] Implement A/B testing, e.g. by choosing one option for a new user randomly, storing it in session object, and then returning the correct bool value for below, and tracking & visualizing stats separately for both options:

  ```python
  if streamlit_analytics.split_test("option a", 2):
      st.button("Is this button text better?")

  if streamlit_analytics.split_test("option b", 2):
      st.button("...or this one?")
  ```

- [ ] Enable tracking to Google Analytics, e.g. via custom component with [react-ga](https://github.com/react-ga/react-ga). Widget interactions could also be tracked via [events](https://github.com/react-ga/react-ga#reactgaeventargs).
- [x] ~~Add a button to reset analytics results (see issue #2, this should probably show another prompt for confirmation, similar to if you delete a Github repo)~~
