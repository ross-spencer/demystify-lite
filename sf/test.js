window.onload = () => {
    document.getElementById('butOpen').addEventListener('click', () => {
        window.showOpenFilePicker().then(handles => {
            for (const idx in handles) {
                handles[idx].getFile().then(file => {
                    file.arrayBuffer().then(buff => {
                        let data = new Uint8Array(buff);
                        let res = identify(file.name, data);
                        results = document.getElementById("sf-results");
                        results.innerHTML = res;
                        console.log("sf complete");
                        //console.log(res)
                    });
                });
            }
        }
        );
    });

    /*
    const butDir = document.getElementById('butDirectory');
    butDir.addEventListener('click', async () => {
        const dirHandle = await window.showDirectoryPicker();
        for await (const entry of dirHandle.values()) {
            console.log(entry.kind, entry.name);
            if (entry.kind == "directory") {
                for await (const [key, value] of dirHandle.entries()) {
                    console.log({ key, value });
                }
            }
        }
    });
    */
}



