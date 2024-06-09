"""Demystify-lite Pyscript front-end.

The form for Demystify is cleared and a user can then provide the
page with a File handle to a file-format analysis report on their own
file-system. The file is processed and the results returned to the page.
"""

import json
import tempfile

from js import document, console, window
from pyodide.ffi import create_proxy

from demystify.demystify import analysis_from_csv_lite
from demystify.libs.outputhandlers.htmloutputclass import FormatAnalysisHTMLOutput


from pyscript import when, display


def clear_data():
    """Clear the metadata fields associated with the file input and
    output.
    """
    document.getElementById("filename").innerHTML = ""
    document.getElementById("filesize").innerHTML = ""
    document.getElementById("filetype").innerHTML = ""
    document.getElementById("filedate").innerHTML = ""
    document.getElementById("results").innerHTML = ""


async def deny_list(event):
    """Handle file select and follow-on actions from HTML/Pyscript."""
    use_deny_list = document.getElementById("use_deny_list").checked
    if not use_deny_list:
        document.getElementById("denylistTextBox").style.display = "none"
        return

    document.getElementById("denylistTextBox").style.display = ""

    content = document.getElementById("denylist").value
    if content.strip() == "":
        with open("default_denylist.cfg", encoding="utf-8") as default_deny_list:
            content = default_deny_list.read()
            deny_list_json = json.dumps(json.loads(content), indent=2)
            document.getElementById("denylist").value = deny_list_json




@when("click", "#my_button")
async def click_handler(event):
    """
    Event handlers get an event object representing the activity that raised
    them.

    https://github.com/exponential-decay
    """
    await file_select()


async def file_select():
    """Handle file select and follow-on actions from HTML/Pyscript."""

    clear_data()
    #event.stopPropagation()
    #event.preventDefault()

    deny_list = "{}"
    use_deny_list = document.getElementById("use_deny_list").checked
    if use_deny_list:
        deny_list = document.getElementById("denylist").value

    try:
        deny_list = json.loads(deny_list)
    except json.decoder.JSONDecodeError as err:
        console.log(f"denylist error: {err}")
        document.getElementById("results").innerHTML = (
            "<br/>"
            "<h1>Processing Error</h1>"
            "deny list JSON is invalid, please check, e.g. via "
            "<a href='https://jsonlint.com/' target='_blank', rel='noopener'>JSONLint.com</a>"
            "<br/>"
        )
        return

    results = document.getElementById("sf-results");

    content = results.innerHTML;
    content = content.strip()

    console.log(content.startswith("---"))
    #console.log(content)

    import binascii
    b = content[:25]
    a = binascii.hexlify(b.encode())
    #console.log(f"{a}")

    c = b"2d2d2d0a7369656766726965642020203a"
    console.log(c in a)

    console.log(f"{a}")
    console.log(f"{c}")

    if not content:
        console.log("you need to click the button")
        return

    #with open("test.sf", "w", encoding="utf-8") as test_sf:
    #    test_sf.write(report)


    #console.log(content.strip())
    #return

    #document.getElementById("filename").innerHTML = f"<b>File Name:</b> {file.name}"
    #document.getElementById("filesize").innerHTML = f"<b>File Size:</b> {file.size}"
    #if file.type:
    #    document.getElementById(
    #        "filetype"
    #    ).innerHTML = f"<b>File Type:</b> {file.type}"
    #document.getElementById(
    #    "filedate"
    #).innerHTML = f"<b>File date:</b> {file.lastModified}"
    #content = await file.text()

    with tempfile.NamedTemporaryFile("w", encoding="UTF8", delete=False) as temp_file:
        temp_file.write(content)

    with open(temp_file.name, "r", encoding="utf8") as test:
        console.log(test.read())

    analysis = analysis_from_csv_lite(
        temp_file.name,
        label="SFWASM",
        denylist=deny_list,
    )
    out = ""
    try:
        out = FormatAnalysisHTMLOutput(
            analysis.analysis_results
        ).printHTMLResults()
    except AttributeError:
        out = (
            f"<b>{analysis}</b>"
            "Error processing content. Press F12 on your keyboard to open"
            "developer tools, then select the console tab to view"
            "additional debug output."
        )

    document.getElementById("results").innerHTML = out


def setup_button():
    """Create a Python proxy for the callback function."""
    deny_list_proxy = create_proxy(deny_list)
    document.querySelector("#deny_list input[type='checkbox']").addEventListener(
        "change",
        deny_list_proxy,
    )


if __name__ == "__main__":
    setup_button()
