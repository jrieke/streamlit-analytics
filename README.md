# streamlit-analytics

**👀 Track & visualize user inputs to your streamlit app**

This is a small extension for the fantastic [streamlit](https://www.streamlit.io/) 
framework. With just one line of code, it tracks and counts all user inputs to your 
streamlit app and visualizes the results directly in your browser. Think Google 
Analytics but for streamlit.

<p align="center">
    <img src="images/example.png" width=500>
</p>


## Installation

Coming soon!


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

If you don't want a huge `with` block, you can also manually call 
`streamlit_analytics.start_tracking()` at the beginning of your app and
`streamlit_analytics.stop_tracking()` at the end.
