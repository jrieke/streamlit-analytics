# streamlit-analytics

**👀 Track & visualize user inputs to your streamlit app**

This is a small extension for the fantastic [streamlit](https://www.streamlit.io/) 
framework. With just one line of code, it tracks and counts all user inputs to your 
streamlit app and visualizes the results directly in your browser. Think Google 
Analytics but for streamlit.

<p align="center">
    <img src="images/example.png" width=600>
</p>


## Installation

```bash
pip install git+https://github.com/jrieke/streamlit-analytics.git
```

Requires Python 3.6+


## How to use it

```python
import streamlit_analytics

with streamlit_analytics.track():
    st.text_input("Write something")
    st.button("Click me")
```

That's it! 🎈 All inputs & clicks will now be tracked and counted. Of course, you
can also use any other streamlit component in the `with` block (currently supported:
button, text_input, selectbox). 

To view the results, append `?analytics=on` to your app's URL 
(e.g. http://localhost:8501/?analytics=on). The results are then shown directly below 
your app (see image above).


## More details

- You can **password-protect** your analytics results with 
`streamlit_analytics.track(unsafe_password=...)`. The streamlit app will then ask you 
for this password. Do not choose an important password here – it is sent without 
encryption.
- If you don't want a **huge `with` block**, you can also do:

    ```python
    import streamlit_analytics

    streamlit_analytics.start_tracking()
    # your streamlit code here
    streamlit_analytics.stop_tracking()
    ```

- *Experimental:* You can **store analytics results as a json file** by passing 
`save_to_json="path/to/file.json"` to `streamlit_analytics.track` or 
`streamlit_analytics.stop_tracking`. At the moment, this may lead to problems with 
concurrency.
