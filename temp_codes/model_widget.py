from __future__ import print_function # py 2.7 compat.
import base64
import ipywidgets as widgets # Widget definitions.
from traitlets import Unicode # Traitlet needed to add synced attributes to the widget.

class FileWidget(widgets.DOMWidget):
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

class ModelUploadWidget(FileWidget):
    def __init__(self, model_cls, **kwargs):
        self._model_cls = model_cls
        FileWidget.__init__(self, **kwargs)
        self.observe(self.file_loading, names='filename')
        self.observe(self.file_loaded,  names='value')
        self.errors.register_callback(self.file_failed)

    # Register an event to echo the filename when it has been changed.
    def file_loading(self, change):
        print("Loading %s" % self.filename)

    # Register an event to parse the file content after the upload
    def file_loaded(self, change):
        self.model = self._model_cls(csv=self.value)

    # Register an event to print an error message when a file could not
    # be opened.  Since the error messages are not handled through
    # traitlets but instead handled through custom msgs, the registration
    # of the handler is different than the two examples above.  Instead
    # the API provided by the CallbackDispatcher must be used.
    def file_failed(self):
        print("Could not load file contents of %s" % self.filename)
