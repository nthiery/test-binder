from __future__ import print_function # py 2.7 compat.
import ipywidgets as widgets # Widget definitions.
from traitlets import Unicode, traitlets # Traitlet needed to add synced attributes to the widget.
from IPython.display import display
import matplotlib.pyplot as plt

class FileWidget(widgets.DOMWidget):
    """
    A file input widget; code taken from the IPywidgets tutorial
    """
    _view_name = Unicode('FilePickerView').tag(sync=True)
    _view_module = Unicode('filepicker').tag(sync=True)

    value = Unicode().tag(sync=True)
    filename = Unicode().tag(sync=True)

    def __init__(self, **kwargs):
        """Constructor"""
        widgets.DOMWidget.__init__(self, **kwargs) # Call the base.

        # Allow the user to register error callbacks with the following signatures:
        #    callback()
        #    callback(sender)
        self.errors = widgets.CallbackDispatcher(accepted_nargs=[0, 1])

        # Listen for custom msgs
        self.on_msg(self._handle_custom_msg)

    def _handle_custom_msg(self, content):
        """Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
            Content of the msg."""
        if 'event' in content and content['event'] == 'error':
            self.errors()
            self.errors(self)

class DataSetUploadWidget(FileWidget):
    """
    A data set input widget

    @param data_set_cls: a class for storing the data set

    The widget lets the user pick a file, and then constructs a new
    dataset by passing the file name to ``data_set_cls``
    """
    def __init__(self, data_set_cls, default=None, **kwargs):
        self._data_set_cls = data_set_cls
        FileWidget.__init__(self, **kwargs)
        self.observe(self.file_loading, names='filename')
        self.observe(self.file_loaded,  names='value')
        self.errors.register_callback(self.file_failed)
        if default is not None:
            self.value = default
            self.file_loaded({})

    # Register an event to echo the filename when it has been changed.
    def file_loading(self, change):
        print("Loading %s" % self.filename)

    # Register an event to parse the file content after the upload
    def file_loaded(self, change):
        self.data_set = self._data_set_cls(csv=self.value)

    # Register an event to print an error message when a file could not
    # be opened.  Since the error messages are not handled through
    # traitlets but instead handled through custom msgs, the registration
    # of the handler is different than the two examples above.  Instead
    # the API provided by the CallbackDispatcher must be used.
    def file_failed(self):
        print("Could not load file contents of %s" % self.filename)

class BoundedFloatTextAndSlider(widgets.widget_float._Float, widgets.Box):
    """
    An input widget to pick a float, either by moving a slider or entering an explicit value
    """
    def __init__(self, description="", **args):
        text = widgets.BoundedFloatText(description=description,**args)
        slider = widgets.FloatSlider(**args)
        traitlets.link( (text, 'value'), (slider, 'value') )
        widgets.Box.__init__(self, [text, slider], description=description)
        self.layout.display = 'flex'
        self.layout.align_items = 'stretch'
        traitlets.link( (text, 'value'), (slider, 'value') )
        traitlets.link( (text, 'value'), (self, 'value') )

# Customized widgets to pick values for specific parameters
def rho_widget(value=1000, min=10, max=10**6):
    return BoundedFloatTextAndSlider(value=value, min=min, max=max, description='rho (xxx/sss)')

def t0_widget(value=8, min=1, max=10, step=.1):
    return BoundedFloatTextAndSlider(value=value, min=min, max=max, step=step, description='t0 (sec)')

class DisplayWidget(widgets.Box):
    """
    A widget that displays the data_set and model
    """
    def set(self, data_set, model):
        plt.plot(model.times,data_set.temperature_responses,'.')
        plt.plot(model.times,model.fit_temperature_responses,'r')
        plt.xlabel('Time (sec)')
        plt.ylabel('$\\Delta$ T (Celsius)')
        # display(plt)
