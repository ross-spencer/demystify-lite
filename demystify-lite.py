"""Demystify-lite Pyscript front-end.

The form for Demystify is cleared and a user can then provide the
page with a File handle to a file-format analysis report on their own
file-system. The file is processed and the results returned to the page.
"""

import tempfile

from js import document
from pyodide import create_proxy

from demystify.demystify import analysis_from_csv, handle_output


def clear_data():
    """Clear the metadata fields associated with the file input and
    output.
    """
    document.getElementById("filename").innerHTML = ""
    document.getElementById("filesize").innerHTML = ""
    document.getElementById("filetype").innerHTML = ""
    document.getElementById("filedate").innerHTML = ""
    document.getElementById("results").innerHTML = ""


async def file_select(event):
    """Handle file select and follow-on actions from HTML/Pyscript."""

    clear_data()

    event.stopPropagation()
    event.preventDefault()

    files = event.target.files

    for file in files:
        document.getElementById("filename").innerHTML = f"<b>File Name:</b> {file.name}"
        document.getElementById("filesize").innerHTML = f"<b>File Size:</b> {file.size}"
        if file.type:
            document.getElementById(
                "filetype"
            ).innerHTML = f"<b>File Type:</b> {file.type}"
        document.getElementById(
            "filedate"
        ).innerHTML = f"<b>File date:</b> {file.lastModified}"
        content = await file.text()

        a = tempfile.NamedTemporaryFile("w", encoding="UTF8")
        a.write(content)

        analysis = analysis_from_csv(a.name, True, label=file.name)
        try:
            out = handle_output(analysis.analysis_results)
        except AttributeError:
            # TODO: Consider a more idiomatic approach. We'll supply a
            # string to the function if analysis_results do not exist.
            out = f"<b>{analysis}</b> Press F12 on your keyboard to open developer tools, then select the console tab to view additional debug output."

        document.getElementById("results").innerHTML = out


def setup_button():
    """Create a Python proxy for the callback function."""
    file_select_proxy = create_proxy(file_select)
    document.querySelector("#file_select input[type='file']").addEventListener(
        "change", file_select_proxy, False
    )


setup_button()
