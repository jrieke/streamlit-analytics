from typing import Union
from contextlib import contextmanager
from pathlib import Path
import json
import datetime

import streamlit as st

from . import session_state


# Dict that holds all analytics results. Note that this is persistent across users,
# as modules are only imported once by a streamlit app.
counts = {"pageviews": 0, "script_runs": 0, "widgets": {}}

# Store original streamlit functions. They will be monkey-patched with some wrappers
# in `start_tracking` (see wrapper functions below).
_orig_button = st.button
_orig_checkbox = st.checkbox
_orig_radio = st.radio
_orig_selectbox = st.selectbox
_orig_multiselect = st.multiselect
_orig_slider = st.slider
_orig_select_slider = st.select_slider
_orig_text_input = st.text_input
_orig_number_input = st.number_input
_orig_text_area = st.text_area
_orig_date_input = st.date_input
_orig_time_input = st.time_input
_orig_file_uploader = st.file_uploader
_orig_color_picker = st.color_picker

_orig_sidebar_button = st.sidebar.button
_orig_sidebar_checkbox = st.sidebar.checkbox
_orig_sidebar_radio = st.sidebar.radio
_orig_sidebar_selectbox = st.sidebar.selectbox
_orig_sidebar_multiselect = st.sidebar.multiselect
_orig_sidebar_slider = st.sidebar.slider
_orig_sidebar_select_slider = st.sidebar.select_slider
_orig_sidebar_text_input = st.sidebar.text_input
_orig_sidebar_number_input = st.sidebar.number_input
_orig_sidebar_text_area = st.sidebar.text_area
_orig_sidebar_date_input = st.sidebar.date_input
_orig_sidebar_time_input = st.sidebar.time_input
_orig_sidebar_file_uploader = st.sidebar.file_uploader
_orig_sidebar_color_picker = st.sidebar.color_picker


def _track_user(sess):
    """Track individual pageviews by storing user id to session state."""
    counts["script_runs"] += 1
    if not sess.user_tracked:
        sess.user_tracked = True
        counts["pageviews"] += 1
        # print("Tracked new user")


def _wrap_bool(func, state_dict):
    """
    Wrap a streamlit function that returns a bool, e.g. st.button, st.checkbox.
    """

    def new_func(label, *args, **kwargs):
        checked = func(label, *args, **kwargs)
        state_dict[label] = checked
        if label not in counts["widgets"]:
            counts["widgets"][label] = 0
        if checked:
            counts["widgets"][label] += 1
        return checked

    return new_func


def _wrap_file_uploader(func, state_dict):
    """
    Wrap st.file_uploader.
    """

    def new_func(label, *args, **kwargs):
        uploaded_file = func(label, *args, **kwargs)
        state_dict[label] = uploaded_file is not None
        if label not in counts["widgets"]:
            counts["widgets"][label] = 0
        if uploaded_file is not None:
            counts["widgets"][label] += 1
        return uploaded_file

    return new_func


def _wrap_select(func, state_dict):
    """
    Wrap a streamlit function that returns one selected element out of multiple options,
    e.g. st.radio, st.selectbox, st.select_slider.
    """

    def new_func(label, options, *args, **kwargs):
        selected = func(label, options, *args, **kwargs)
        state_dict[label] = selected
        if label not in counts["widgets"]:
            counts["widgets"][label] = {}
        for option in options:
            if option not in counts["widgets"][label]:
                counts["widgets"][label][option] = 0
        counts["widgets"][label][selected] += 1
        return selected

    return new_func


def _wrap_multiselect(func, state_dict):
    """
    Wrap a streamlit function that returns multiple selected elements out of multiple 
    options, e.g. st.multiselect.
    """

    def new_func(label, options, *args, **kwargs):
        selected = func(label, options, *args, **kwargs)
        state_dict[label] = selected
        if label not in counts["widgets"]:
            counts["widgets"][label] = {}
        for option in options:
            if option not in counts["widgets"][label]:
                counts["widgets"][label][option] = 0
        for sel in selected:
            counts["widgets"][label][sel] += 1
        return selected

    return new_func


def _wrap_value(func, state_dict):
    """
    Wrap a streamlit function that returns a single value (str/int/float/datetime/...),
    e.g. st.slider, st.text_input, st.number_input, st.text_area, st.date_input, 
    st.time_input, st.color_picker.
    """

    def new_func(label, *args, **kwargs):
        value = func(label, *args, **kwargs)
        state_dict[label] = value
        if label not in counts["widgets"]:
            counts["widgets"][label] = {}

        # st.date_input and st.time return datetime object, convert to str
        formatted_value = value
        if (
            isinstance(value, datetime.datetime)
            or isinstance(value, datetime.date)
            or isinstance(value, datetime.time)
        ):
            formatted_value = str(value)

        if formatted_value not in counts["widgets"][label]:
            counts["widgets"][label][formatted_value] = 0
        counts["widgets"][label][formatted_value] += 1
        return value

    return new_func


def start_tracking(verbose: bool = False):
    """
    Start tracking user inputs to a streamlit app.
    
    If you call this function directly, you NEED to call 
    `streamlit_analytics.stop_tracking()` at the end of your streamlit script.
    For a more convenient interface, wrap your streamlit calls in 
    `with streamlit_analytics.track():`. 
    """

    sess = session_state.get(user_tracked=False, state_dict={})
    _track_user(sess)

    # Monkey-patch streamlit to call the wrappers above.
    st.button = _wrap_bool(_orig_button, sess.state_dict)
    st.checkbox = _wrap_bool(_orig_checkbox, sess.state_dict)
    st.radio = _wrap_select(_orig_radio, sess.state_dict)
    st.selectbox = _wrap_select(_orig_selectbox, sess.state_dict)
    st.multiselect = _wrap_multiselect(_orig_multiselect, sess.state_dict)
    st.slider = _wrap_value(_orig_slider, sess.state_dict)
    st.select_slider = _wrap_select(_orig_select_slider, sess.state_dict)
    st.text_input = _wrap_value(_orig_text_input, sess.state_dict)
    st.number_input = _wrap_value(_orig_number_input, sess.state_dict)
    st.text_area = _wrap_value(_orig_text_area, sess.state_dict)
    st.date_input = _wrap_value(_orig_date_input, sess.state_dict)
    st.time_input = _wrap_value(_orig_time_input, sess.state_dict)
    st.file_uploader = _wrap_file_uploader(_orig_file_uploader, sess.state_dict)
    st.color_picker = _wrap_value(_orig_color_picker, sess.state_dict)

    st.sidebar.button = _wrap_bool(_orig_sidebar_button, sess.state_dict)
    st.sidebar.checkbox = _wrap_bool(_orig_sidebar_checkbox, sess.state_dict)
    st.sidebar.radio = _wrap_select(_orig_sidebar_radio, sess.state_dict)
    st.sidebar.selectbox = _wrap_select(_orig_sidebar_selectbox, sess.state_dict)
    st.sidebar.multiselect = _wrap_multiselect(
        _orig_sidebar_multiselect, sess.state_dict
    )
    st.sidebar.slider = _wrap_value(_orig_sidebar_slider, sess.state_dict)
    st.sidebar.select_slider = _wrap_select(
        _orig_sidebar_select_slider, sess.state_dict
    )
    st.sidebar.text_input = _wrap_value(_orig_sidebar_text_input, sess.state_dict)
    st.sidebar.number_input = _wrap_value(_orig_sidebar_number_input, sess.state_dict)
    st.sidebar.text_area = _wrap_value(_orig_sidebar_text_area, sess.state_dict)
    st.sidebar.date_input = _wrap_value(_orig_sidebar_date_input, sess.state_dict)
    st.sidebar.time_input = _wrap_value(_orig_sidebar_time_input, sess.state_dict)
    st.sidebar.file_uploader = _wrap_file_uploader(
        _orig_sidebar_file_uploader, sess.state_dict
    )
    st.sidebar.color_picker = _wrap_value(_orig_sidebar_color_picker, sess.state_dict)

    # replacements = {
    #     "button": _wrap_bool,
    #     "checkbox": _wrap_bool,
    #     "radio": _wrap_select,
    #     "selectbox": _wrap_select,
    #     "multiselect": _wrap_multiselect,
    #     "slider": _wrap_value,
    #     "select_slider": _wrap_select,
    #     "text_input": _wrap_value,
    #     "number_input": _wrap_value,
    #     "text_area": _wrap_value,
    #     "date_input": _wrap_value,
    #     "time_input": _wrap_value,
    #     "file_uploader": _wrap_file_uploader,
    #     "color_picker": _wrap_value,
    # }

    if verbose:
        print()
        print("Tracking script execution with streamlit-analytics...")


def stop_tracking(
    unsafe_password: str = None,
    save_to_json: Union[str, Path] = None,
    verbose: bool = False,
):
    """
    Stop tracking user inputs to a streamlit app.
    
    Should be called after `streamlit-analytics.start_tracking()`. This method also
    shows the analytics results below your app if you attach `?analytics=on` to the URL.
    """
    if verbose:
        print("Finished script execution. New counts:")
        print(counts)
        print("-" * 80)
        
    sess = session_state.get()
    print(sess.state_dict)

    # Reset streamlit functions.
    st.button = _orig_button
    st.checkbox = _orig_checkbox
    st.radio = _orig_radio
    st.selectbox = _orig_selectbox
    st.multiselect = _orig_multiselect
    st.slider = _orig_slider
    st.select_slider = _orig_select_slider
    st.text_input = _orig_text_input
    st.number_input = _orig_number_input
    st.text_area = _orig_text_area
    st.date_input = _orig_date_input
    st.time_input = _orig_time_input
    st.file_uploader = _orig_file_uploader
    st.color_picker = _orig_color_picker

    st.sidebar.button = _orig_sidebar_button
    st.sidebar.checkbox = _orig_sidebar_checkbox
    st.sidebar.radio = _orig_sidebar_radio
    st.sidebar.selectbox = _orig_sidebar_selectbox
    st.sidebar.multiselect = _orig_sidebar_multiselect
    st.sidebar.slider = _orig_sidebar_slider
    st.sidebar.select_slider = _orig_sidebar_select_slider
    st.sidebar.text_input = _orig_sidebar_text_input
    st.sidebar.number_input = _orig_sidebar_number_input
    st.sidebar.text_area = _orig_sidebar_text_area
    st.sidebar.date_input = _orig_sidebar_date_input
    st.sidebar.time_input = _orig_sidebar_time_input
    st.sidebar.file_uploader = _orig_sidebar_file_uploader
    st.sidebar.color_picker = _orig_sidebar_color_picker

    # Dump the counts to json file if `save_to_json` is set.
    # TODO: Make sure this is not locked if writing from multiple threads.
    if save_to_json is not None:
        with Path(save_to_json).open("w") as f:
            json.dump(counts, f)
        if verbose:
            print("Storing results to file:", save_to_json)

    # Show analytics results in the streamlit app if `?analytics=on` is set in the URL.
    query_params = st.experimental_get_query_params()
    if "analytics" in query_params and "on" in query_params["analytics"]:
        st.write("---")
        st.title("Analytics")
        st.markdown(
            """
            Psst! 👀 You found a secret section generated by 
            [streamlit-analytics](https://github.com/jrieke/streamlit-analytics). 
            If you didn't mean to go here, remove `?analytics=on` from the URL.
            """
        )
        show_results = True
        if unsafe_password is not None:
            password_input = st.text_input("Enter password to show results")
            if password_input != unsafe_password:
                show_results = False
                if len(password_input) > 0:
                    st.write("Nope, that's not correct ☝️")
        if show_results:
            st.markdown(
                """
                <sub>Note: The widget counts add +1 each time streamlit executes your 
                script (= each time the user input changes). E.g. for st.selectbox, it 
                adds +1 for the currently selected option each time a user interacts 
                with ANY component in your app.</sub>
                """,
                unsafe_allow_html=True,
            )
            st.write(counts)


@contextmanager
def track(
    unsafe_password: str = None, save_to_json: Union[str, Path] = None, verbose=False
):
    """
    Context manager to start and stop tracking user inputs to a streamlit app.
    
    To use this, wrap all calls to streamlit in `with streamlit_analytics.track():`. 
    This also shows the analytics results below your app if you attach 
    `?analytics=on` to the URL.
    """
    start_tracking(verbose=verbose)
    # Yield here to execute the code in the with statement. This will call the wrappers
    # above, which track all inputs.
    yield
    stop_tracking(
        unsafe_password=unsafe_password, save_to_json=save_to_json, verbose=verbose
    )
