"""
Main API functions for the user to start and stop analytics tracking.
"""

import datetime
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Union

import streamlit as st

from . import display, firestore
from .utils import replace_empty

# Dict that holds all analytics results. Note that this is persistent across users,
# as modules are only imported once by a streamlit app.
counts = {"loaded_from_firestore": False}


def reset_counts():
    # Use yesterday as first entry to make chart look better.
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    counts["total_pageviews"] = 0
    counts["total_script_runs"] = 0
    counts["total_time_seconds"] = 0
    counts["per_day"] = {"days": [str(yesterday)], "pageviews": [0], "script_runs": [0]}
    counts["widgets"] = {}
    counts["start_time"] = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")


reset_counts()

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


def _track_user():
    """Track individual pageviews by storing user id to session state."""
    today = str(datetime.date.today())
    if counts["per_day"]["days"][-1] != today:
        # TODO: Insert 0 for all days between today and last entry.
        counts["per_day"]["days"].append(today)
        counts["per_day"]["pageviews"].append(0)
        counts["per_day"]["script_runs"].append(0)
    counts["total_script_runs"] += 1
    counts["per_day"]["script_runs"][-1] += 1
    now = datetime.datetime.now()
    counts["total_time_seconds"] += (now - st.session_state.last_time).total_seconds()
    st.session_state.last_time = now
    if not st.session_state.user_tracked:
        st.session_state.user_tracked = True
        counts["total_pageviews"] += 1
        counts["per_day"]["pageviews"][-1] += 1
        # print("Tracked new user")


def _wrap_checkbox(func):
    """
    Wrap st.checkbox.
    """

    def new_func(label, *args, **kwargs):
        checked = func(label, *args, **kwargs)
        label = replace_empty(label)
        if label not in counts["widgets"]:
            counts["widgets"][label] = 0
        if checked != st.session_state.state_dict.get(label, None):
            counts["widgets"][label] += 1
        st.session_state.state_dict[label] = checked
        return checked

    return new_func


def _wrap_button(func):
    """
    Wrap st.button.
    """

    def new_func(label, *args, **kwargs):
        clicked = func(label, *args, **kwargs)
        label = replace_empty(label)
        if label not in counts["widgets"]:
            counts["widgets"][label] = 0
        if clicked:
            counts["widgets"][label] += 1
        st.session_state.state_dict[label] = clicked
        return clicked

    return new_func


def _wrap_file_uploader(func):
    """
    Wrap st.file_uploader.
    """

    def new_func(label, *args, **kwargs):
        uploaded_file = func(label, *args, **kwargs)
        label = replace_empty(label)
        if label not in counts["widgets"]:
            counts["widgets"][label] = 0
        # TODO: Right now this doesn't track when multiple files are uploaded one after
        #   another. Maybe compare files directly (but probably not very clever to
        #   store in session state) or hash them somehow and check if a different file
        #   was uploaded.
        if uploaded_file and not st.session_state.state_dict.get(label, None):
            counts["widgets"][label] += 1
        st.session_state.state_dict[label] = bool(uploaded_file)
        return uploaded_file

    return new_func


def _wrap_select(func):
    """
    Wrap a streamlit function that returns one selected element out of multiple options,
    e.g. st.radio, st.selectbox, st.select_slider.
    """

    def new_func(label, options, *args, **kwargs):
        orig_selected = func(label, options, *args, **kwargs)
        label = replace_empty(label)
        selected = replace_empty(orig_selected)
        if label not in counts["widgets"]:
            counts["widgets"][label] = {}
        for option in options:
            option = replace_empty(option)
            if option not in counts["widgets"][label]:
                counts["widgets"][label][option] = 0
        if selected != st.session_state.state_dict.get(label, None):
            counts["widgets"][label][selected] += 1
        st.session_state.state_dict[label] = selected
        return orig_selected

    return new_func


def _wrap_multiselect(func):
    """
    Wrap a streamlit function that returns multiple selected elements out of multiple
    options, e.g. st.multiselect.
    """

    def new_func(label, options, *args, **kwargs):
        selected = func(label, options, *args, **kwargs)
        label = replace_empty(label)
        if label not in counts["widgets"]:
            counts["widgets"][label] = {}
        for option in options:
            option = replace_empty(option)
            if option not in counts["widgets"][label]:
                counts["widgets"][label][option] = 0
        for sel in selected:
            sel = replace_empty(sel)
            if sel not in st.session_state.state_dict.get(label, []):
                counts["widgets"][label][sel] += 1
        st.session_state.state_dict[label] = selected
        return selected

    return new_func


def _wrap_value(func):
    """
    Wrap a streamlit function that returns a single value (str/int/float/datetime/...),
    e.g. st.slider, st.text_input, st.number_input, st.text_area, st.date_input,
    st.time_input, st.color_picker.
    """

    def new_func(label, *args, **kwargs):
        value = func(label, *args, **kwargs)
        if label not in counts["widgets"]:
            counts["widgets"][label] = {}

        formatted_value = replace_empty(value)
        if type(value) == tuple and len(value) == 2:
            # Double-ended slider or date input with start/end, convert to str.
            formatted_value = f"{value[0]} - {value[1]}"

        # st.date_input and st.time return datetime object, convert to str
        if (
            isinstance(value, datetime.datetime)
            or isinstance(value, datetime.date)
            or isinstance(value, datetime.time)
        ):
            formatted_value = str(value)

        if formatted_value not in counts["widgets"][label]:
            counts["widgets"][label][formatted_value] = 0
        if formatted_value != st.session_state.state_dict.get(label, None):
            counts["widgets"][label][formatted_value] += 1
        st.session_state.state_dict[label] = formatted_value
        return value

    return new_func


def start_tracking(
    verbose: bool = False,
    firestore_key_file: str = None,
    firestore_collection_name: str = "counts",
    load_from_json: Union[str, Path] = None,
):
    """
    Start tracking user inputs to a streamlit app.

    If you call this function directly, you NEED to call
    `streamlit_analytics.stop_tracking()` at the end of your streamlit script.
    For a more convenient interface, wrap your streamlit calls in
    `with streamlit_analytics.track():`.
    """

    if firestore_key_file and not counts["loaded_from_firestore"]:
        firestore.load(counts, firestore_key_file, firestore_collection_name)
        counts["loaded_from_firestore"] = True
        if verbose:
            print("Loaded count data from firestore:")
            print(counts)
            print()

    if load_from_json is not None:
        if verbose:
            print(f"Loading counts from json:", load_from_json)
        try:
            with Path(load_from_json).open("r") as f:
                json_counts = json.load(f)
                for key in json_counts:
                    if key in counts:
                        counts[key] = json_counts[key]
            if verbose:
                print("Success! Loaded counts:")
                print(counts)
                print()
        except FileNotFoundError as e:
            if verbose:
                print(f"File not found, proceeding with empty counts.")

    # Reset session state.
    if "user_tracked" not in st.session_state:
        st.session_state.user_tracked = False
    if "state_dic" not in st.session_state:
        st.session_state.state_dict = {}
    if "last_time" not in st.session_state:
        st.session_state.last_time = datetime.datetime.now()
    _track_user()

    # Monkey-patch streamlit to call the wrappers above.
    st.button = _wrap_button(_orig_button)
    st.checkbox = _wrap_checkbox(_orig_checkbox)
    st.radio = _wrap_select(_orig_radio)
    st.selectbox = _wrap_select(_orig_selectbox)
    st.multiselect = _wrap_multiselect(_orig_multiselect)
    st.slider = _wrap_value(_orig_slider)
    st.select_slider = _wrap_select(_orig_select_slider)
    st.text_input = _wrap_value(_orig_text_input)
    st.number_input = _wrap_value(_orig_number_input)
    st.text_area = _wrap_value(_orig_text_area)
    st.date_input = _wrap_value(_orig_date_input)
    st.time_input = _wrap_value(_orig_time_input)
    st.file_uploader = _wrap_file_uploader(_orig_file_uploader)
    st.color_picker = _wrap_value(_orig_color_picker)

    st.sidebar.button = _wrap_button(_orig_sidebar_button)
    st.sidebar.checkbox = _wrap_checkbox(_orig_sidebar_checkbox)
    st.sidebar.radio = _wrap_select(_orig_sidebar_radio)
    st.sidebar.selectbox = _wrap_select(_orig_sidebar_selectbox)
    st.sidebar.multiselect = _wrap_multiselect(_orig_sidebar_multiselect)
    st.sidebar.slider = _wrap_value(_orig_sidebar_slider)
    st.sidebar.select_slider = _wrap_select(_orig_sidebar_select_slider)
    st.sidebar.text_input = _wrap_value(_orig_sidebar_text_input)
    st.sidebar.number_input = _wrap_value(_orig_sidebar_number_input)
    st.sidebar.text_area = _wrap_value(_orig_sidebar_text_area)
    st.sidebar.date_input = _wrap_value(_orig_sidebar_date_input)
    st.sidebar.time_input = _wrap_value(_orig_sidebar_time_input)
    st.sidebar.file_uploader = _wrap_file_uploader(_orig_sidebar_file_uploader)
    st.sidebar.color_picker = _wrap_value(_orig_sidebar_color_picker)

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
    firestore_key_file: str = None,
    firestore_collection_name: str = "counts",
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

    # sess = get_session_state
    # print(sess.state_dict)

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

    # Save count data to firestore.
    # TODO: Maybe don't save on every iteration but on regular intervals in a background
    #   thread.
    if firestore_key_file:
        if verbose:
            print("Saving count data to firestore:")
            print(counts)
            print()
        firestore.save(counts, firestore_key_file, firestore_collection_name)

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
        display.show_results(counts, reset_counts, unsafe_password)


@contextmanager
def track(
    unsafe_password: str = None,
    save_to_json: Union[str, Path] = None,
    firestore_key_file: str = None,
    firestore_collection_name: str = "counts",
    verbose=False,
    load_from_json: Union[str, Path] = None,
):
    """
    Context manager to start and stop tracking user inputs to a streamlit app.

    To use this, wrap all calls to streamlit in `with streamlit_analytics.track():`.
    This also shows the analytics results below your app if you attach
    `?analytics=on` to the URL.
    """

    start_tracking(
        verbose=verbose,
        firestore_key_file=firestore_key_file,
        firestore_collection_name=firestore_collection_name,
        load_from_json=load_from_json,
    )

    # Yield here to execute the code in the with statement. This will call the wrappers
    # above, which track all inputs.
    yield
    stop_tracking(
        unsafe_password=unsafe_password,
        save_to_json=save_to_json,
        firestore_key_file=firestore_key_file,
        firestore_collection_name=firestore_collection_name,
        verbose=verbose,
    )
