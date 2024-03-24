"""Demystify-lite Pyscript front-end.

The form for Demystify is cleared and a user can then provide the
page with a File handle to a file-format analysis report on their own
file-system. The file is processed and the results returned to the page.
"""

import random
import configparser
import json
import tempfile

from js import document, fetch
from pyodide.ffi import create_proxy, to_js

from demystify.demystify import analysis_from_csv_lite
from demystify.libs.outputhandlers.htmloutputclass import FormatAnalysisHTMLOutput


def clear_data():
    """Clear the metadata fields associated with the file input and
    output.
    """
    print("clear clear clear")

    document.getElementById("filename").innerHTML = ""
    document.getElementById("filesize").innerHTML = ""
    document.getElementById("filetype").innerHTML = ""
    document.getElementById("filedate").innerHTML = ""
    document.getElementById("results").innerHTML = ""


async def deny_list(event):
    """Handle file select and follow-on actions from HTML/Pyscript."""

    b = document.getElementById("xx1").checked
    print(b)
    print(event)


    a = ""
    with open("ross.txt", "r", encoding="utf-8") as r:
        a = r.read()


    print(a)

    f = """
    {
        "IDS": [
            "x-fmt/384"
        ],
        "FILENAMES": [
            ".DS_Store",
            "Untitled Document",
            "desktop.ini",
            "(copy",
            "ZbThumbnail.info",
            "lorem",
            "New Microsoft Word Document",
            "Bin.dat",
            "Thumbs.db",
            " vitae",
            " Appointments",
            " CV",
            " Application",
            " Resume",
            " Appointment",
            " Test",
            " list",
            " member",
            " people",
            " address",
            " phone"
        ],
        "DIRECTORIES": [
            "Untitled Folder",
            "New Folder",
            "(copy",
            ".git",
            "lorem"
        ],
        "EXTENSIONS": [
            ".ini",
            ".exe",
            ".cfg",
            ".dll",
            ".lnk",
            ".tmp"
        ]
    }
    """

    #f = "{}"

    x_state = "12344"
    document.getElementById("deny").innerHTML = f.strip();


async def file_select(event):
    """Handle file select and follow-on actions from HTML/Pyscript."""

    clear_data()
    a = document.getElementById("ttt1").value

    b = document.getElementById("xx1").checked
    if b:
        print("vvvvvvvvvvvvvvvvvvvvvvv")
    else:
        print("ffffffffffffffffffffff")
    print("x", b, "x")

    try:
        a = json.loads(a)
        print("using a denylist file")
    except json.decoder.JSONDecodeError:
        print("not using a denylist file...")

    document.getElementById("results").innerHTML = random.choice([1, 2, 3])


    event.target.value = ""
    return


    a = document.getElementById("deny").innerHTML



    try:

        #denylstx = config.read_string(a)
        denylistx = json.loads(a)
    except Exception as err:
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(err)
        print("fff", a, "fff")
        denylistx = {}
    #document.getElementById("results").innerHTML = "hi there!" + x
    #return



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

        with tempfile.NamedTemporaryFile("w", encoding="UTF8") as temp_file:
            temp_file.write(content)


            analysis = analysis_from_csv_lite(temp_file.name, analyze=True, label=file.name, denylist=denylistx)
            try:
                out = FormatAnalysisHTMLOutput(
                    analysis.analysis_results
                ).printHTMLResults()
            except AttributeError:
                # TODO: Consider a more idiomatic approach. We'll supply a
                # string to the function if analysis_results do not exist.
                out = (
                    f"<b>{analysis}</b>"
                    "Error processing content. Press F12 on your keyboard to open"
                    "developer tools, then select the console tab to view"
                    "additional debug output."
                )

            document.getElementById("results").innerHTML = out


def setup_button():
    """Create a Python proxy for the callback function."""
    file_select_proxy = create_proxy(file_select)
    document.querySelector("#file_select input[type='file']").addEventListener(
        "change",
        file_select_proxy,
    )
    deny_list_proxy = create_proxy(deny_list)
    document.querySelector("#deny_list input[type='checkbox']").addEventListener(
        "change",
        deny_list_proxy,
    )


if __name__ == "__main__":
    setup_button()
