# demystify lite

Demystify-lite is a WASM-based implementation of [demystify][demystify-1].

It is powered by [pyscript][pyscript-1] and Siegfried's recent WASM
implementation.

These two features allow for Demystify to be run completely in the browser
from format identification to demystify report. Do data from your file
collections is passed over the network.

Demystify is also a static analysis engine for existing DROID and Siegfried
reports and these can be analysed in the browser too.

## Running demystify lite

Demystify lite can be run from its [home on github][github-1]. If you are
running it locally, you can download these files and from the root directory
the following command will start a web server which can then be accessed in
the browser by following the web-server prompts.

```sh
python -m http.server
```

## Branding demystify-lite

The customize folder contains the application's `favicon.ico` and `header.png`.

This can be used to customize the appearance of this site if you are hosting
it for yourself. The ideal size of the header.png file is 1000px x 200px.

## Siegfried and demystify lite

The `sf/` folder contains all the files needed to run Siegfried with
demystify-lite.

For more information on the Siegfried components, take a look at the Siegfried
[README.md for WASM][sf-1].

The files for demystify-lite are taken from the Siegfried official release pages
e.g. https://github.com/richardlehane/siegfried/releases/tag/v1.11.1 under:
`siegfried_<version>_wasm.zip`.

Specifically we need:

* `sf.wasm`
* `wasm_exec.js`

With `app.js` being a modified version of Richard's `example.js` which sets
some defaults for the demystify-lite app and helps provide some basic user
experience.

[github-1]: https://ross-spencer.github.io/demystify-lite/
[pyscript-1]: https://pyscript.net/
[demystify-1]: https://github.com/exponential-decay/demystify
[sf-1]: https://github.com/richardlehane/siegfried/blob/main/wasm/README.md
