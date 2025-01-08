import json

from .input import InputFile


class JSONWriter(object):
    """
    Provides static methods for writing the AlphaFold3 input data into JSON files.
    """
    @staticmethod
    def write(filename: str, data: InputFile) -> None:
        """
        Writes the contents of an InputFile object to the specified JSON file. The
        data is serialized into a JSON structure with readable indentation and then
        saved to a file.

        Parameters
        ----------
        filename : str
            The name of the file where the JSON data will be written.
        data : InputFile
            The InputFile object containing the data to be serialized and written
            to the JSON file.
        """
        with open(filename, 'w') as json_file:
            json.dump(data.to_dict(), json_file, indent=4)
