// Siegfried functions for demystify-lite.

function getArgs() {
    const args = [];
    var e = document.getElementById("format");
    var val = e.options[e.selectedIndex].value;
    args.push(val);
    e = document.getElementById("hash");
    val = e.options[e.selectedIndex].value;
    if (val != "none") {
        args.push(val);
    }
    val = document.querySelector('input[name="z"]:checked').value;
    if (val == "true") {
        args.push("z")
    }
    console.log(args);
    return args;
}

function downloadResults() {
    let res = document.getElementById("sf-results").value.trim();
    var base64doc = btoa(unescape(encodeURIComponent(res))),
        a = document.createElement('a'),
        e = new MouseEvent('click');
    a.download = 'results.yaml';
    a.href = 'data:text/html;base64,' + base64doc;
    a.dispatchEvent(e);
}


function toggleInit() {
    let sf = true;
    toggleHeight = document.getElementById("static-analysis").offsetHeight;
    document.getElementById("static-analysis").style.height = 0;
    document.getElementById("static-analysis").style.visibility = "hidden";
    document.getElementById('app-toggle').addEventListener('click', (e) => {
        if (sf) {
            document.getElementById('ready').style.visibility = "hidden";
            document.getElementById("use-siegfried").style.visibility = "hidden";
            document.getElementById("static-analysis").style.height = toggleHeight + "px";
            document.getElementById("static-analysis").style.visibility = "visible";
            toggleHeight = document.getElementById("use-siegfried").offsetHeight;
            document.getElementById("use-siegfried").style.height = "0";
            sf = false;
            return;
        }
        document.getElementById('ready').style.visibility = "visible";
        complete = '<div class="w3-panel w3-light-grey w3-border" id="ready"><h5>Ready to scan...</h5><p>Select values for Siegfried and then select a file or directory to create a report against.</p></div>'
        document.getElementById('ready').innerHTML = complete;
        document.getElementById("static-analysis").style.visibility = "hidden";
        document.getElementById("use-siegfried").style.height = toggleHeight + "px";
        document.getElementById("use-siegfried").style.visibility = "visible";
        toggleHeight = document.getElementById("static-analysis").offsetHeight;
        document.getElementById("static-analysis").style.height = "0";
        sf = true;
        return;
    });
}

window.onload = () => {
    toggleInit();
    document.getElementById('butOpen').addEventListener('click', () => {
        window.showOpenFilePicker().then(handles => {
            for (const idx in handles) {
                const args = getArgs();
                args.unshift(handles[idx]);
                identify.apply(null, args).then(result => {
                    document.getElementById('sf-results').value = result;
                }).catch((err) => {
                    console.log("file selection error: " + err);
                });
            };
        }).catch((err) => {
            console.log("file selection error: " + err);
        });
    });
    document.getElementById('butDirectory').addEventListener('click', () => {
        window.showDirectoryPicker().then(handle => {
            complete = '<div class="w3-panel w3-pale-green w3-border"><h4>Complete!</h4><p>Siegfried has finished scanning, \'run Demystify\' to show the results.</p></div>';
            const args = getArgs();
            args.unshift(handle);
            document.getElementById('ready').style.visibility = "hidden";
            document.getElementById('ready').style.height = "0px";
            document.getElementById('loader').style.visibility = "visible";
            document.getElementById('loader').style.height = "auto";
            identify.apply(null, args).then(result => {
                document.getElementById('sf-results').value = result;
                document.getElementById('loader').style.visibility = "hidden";
                document.getElementById('loader').style.height = "0px";
                document.getElementById('ready').innerHTML = complete;
                document.getElementById('ready').style.visibility = "visible";
                document.getElementById('ready').style.height = "auto";
            }).catch((err) => {
                console.log("directory selection error: " + err);
            });
        }).catch((err) => {
            console.log("directory selection error: " + err);
        });
    });
    document.getElementById('butDownload').addEventListener('click', (event) => {
        try {
            downloadResults()
        } catch (err) {
            console.log("download siegfrried error (ensure siegfried has been run): " + err)
        }
    });
}
