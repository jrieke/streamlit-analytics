class FuncWrapper:
    def __init__(self, container, func_name: str, counts: dict, state_dict: dict):
        """
        Initializes an object that wraps a streamlit widget function (e.g. `st.button`).
        
        After calling `wrap`, it replaces the function with `self.wrapper_func`, 
        which can add some additional logic and then call the function itself.
        With `unwrap` it reinstalls the original function. 

        Args:
            container: The streamlit container or module which owns the function to 
                wrap (can also be `st` or `st.sidebar`)
            func_name (str): Name of the function to wrap (e.g. "button")
            counts (dict): The dict to add interaction counts to
            state_dict (dict): The dict to store all widget states
        """
        self.container = container
        self.func_name = func_name
        self.orig_func = getattr(container, func_name)
        self.counts = counts
        self.state_dict = state_dict

    def wrap(self):
        setattr(self.container, self.func_name, self.wrapper_func)
        return self

    def unwrap(self):
        setattr(self.container, self.func_name, self.orig_func)
        return self

    def wrapper_func(self, *args, **kwargs):
        # This is an example which just prints something. Subclasses should overwrite
        # this to do something meaningful (=track stats).
        print("Registered function call")
        return self.orig_func(*args, **kwargs)


class CheckboxWrapper(FuncWrapper):
    """
    Wrap st.checkbox.
    """

    def wrapper_func(self, label, *args, **kwargs):
        checked = self.orig_func(label, *args, **kwargs)
        if label not in self.counts["widgets"]:
            self.counts["widgets"][label] = 0
        if checked != self.state_dict.get(label, None):
            self.counts["widgets"][label] += 1
        self.state_dict[label] = checked
        return checked


class ButtonWrapper(FuncWrapper):
    """
    Wrap st.button.
    """

    def wrapper_func(self, label, *args, **kwargs):
        clicked = self.orig_func(label, *args, **kwargs)
        if label not in self.counts["widgets"]:
            self.counts["widgets"][label] = 0
        if clicked:
            self.counts["widgets"][label] += 1
        self.state_dict[label] = clicked
        return clicked


class FileUploaderWrapper(FuncWrapper):
    """
    Wrap st.file_uploader.
    """

    def wrapper_func(label, *args, **kwargs):
        uploaded_file = self.orig_func(label, *args, **kwargs)
        if label not in self.counts["widgets"]:
            self.counts["widgets"][label] = 0
        # TODO: Right now this doesn't track when multiple files are uploaded one after
        #   another. Maybe compare files directly (but probably not very clever to
        #   store in session state) or hash them somehow and check if a different file
        #   was uploaded.
        if uploaded_file and not self.state_dict.get(label, None):
            self.counts["widgets"][label] += 1
        self.state_dict[label] = bool(uploaded_file)
        return uploaded_file


class SelectWrapper(FuncWrapper):
    """
    Wrap a streamlit function that returns one selected element out of multiple options,
    e.g. st.radio, st.selectbox, st.select_slider.
    """

    def wrapper_func(label, options, *args, **kwargs):
        selected = self.orig_func(label, options, *args, **kwargs)
        if label not in self.counts["widgets"]:
            self.counts["widgets"][label] = {}
        for option in options:
            if option not in self.counts["widgets"][label]:
                self.counts["widgets"][label][option] = 0
        if selected != self.state_dict.get(label, None):
            self.counts["widgets"][label][selected] += 1
        self.state_dict[label] = selected
        return selected


class MultiSelectWrapper(FuncWrapper):
    """
    Wrap a streamlit function that returns multiple selected elements out of multiple 
    options, e.g. st.multiselect.
    """

    def wrapper_func(label, options, *args, **kwargs):
        selected = self.orig_func(label, options, *args, **kwargs)
        if label not in self.counts["widgets"]:
            self.counts["widgets"][label] = {}
        for option in options:
            if option not in self.counts["widgets"][label]:
                self.counts["widgets"][label][option] = 0
        for sel in selected:
            if sel not in self.state_dict.get(label, []):
                self.counts["widgets"][label][sel] += 1
        self.state_dict[label] = selected
        return selected


class ValueWrapper(FuncWrapper):
    """
    Wrap a streamlit function that returns a single value (str/int/float/datetime/...),
    e.g. st.slider, st.text_input, st.number_input, st.text_area, st.date_input, 
    st.time_input, st.color_picker.
    """

    def wrapper_func(label, *args, **kwargs):
        value = self.orig_func(label, *args, **kwargs)
        if label not in self.counts["widgets"]:
            self.counts["widgets"][label] = {}

        # st.date_input and st.time return datetime object, convert to str
        formatted_value = value
        if (
            isinstance(value, datetime.datetime)
            or isinstance(value, datetime.date)
            or isinstance(value, datetime.time)
        ):
            formatted_value = str(value)

        if formatted_value not in self.counts["widgets"][label]:
            self.counts["widgets"][label][formatted_value] = 0
        if formatted_value != self.state_dict.get(label, None):
            self.counts["widgets"][label][formatted_value] += 1
        self.state_dict[label] = formatted_value
        return value


# TODO: This wraps a container creator function, i.e. it's not possible to throw this
# on st or st.sidebar. Maybe split it up into this wrapper + a separate wrapper, which
# assigns all wrappers to the finished container (and which could then also be applied
# to st or st.sidebar directly).
class ContainerWrapper(FuncWrapper):
    def __init__(self, container, func_name, counts, state_dict):
        super().__init__(container, func_name, counts, state_dict)
        self.wrappers = []

    def wrapper_func(self, *args, **kwargs):
        new_container = self.orig_func(*args, **kwargs)
        # TODO: Assign wrappers to all relevant functions in new_container and store them in self.wrappers.
        self.wrappers.append(CheckboxWrapper(new_container, "checkbox"))
        self.wrappers.append(ButtonWrapper(new_container, "button"))
        return new_container

    def wrap(self):
        for wrapper in self.wrappers:
            wrapper.wrap()
        return super().wrap()

    def unwrap(self):
        for wrapper in self.wrappers:
            wrapper.unwrap()
        self.wrappers = []
        return super().unwrap()
