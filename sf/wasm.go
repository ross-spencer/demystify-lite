package main

import (
	"bytes"
	"fmt"
	"syscall/js"
	"time"

	"github.com/richardlehane/siegfried"
	"github.com/richardlehane/siegfried/pkg/config"
	"github.com/richardlehane/siegfried/pkg/static"
	"github.com/richardlehane/siegfried/pkg/writer"
)

func sfWrapper(sf *siegfried.Siegfried) js.Func {
	out := &bytes.Buffer{}
	w := writer.YAML(out)
	sfFunc := js.FuncOf(func(this js.Value, args []js.Value) any {
		if len(args) != 2 {
			return "Invalid number of arguments passed"
		}
		name := args[0].String()
		len := args[1].Length()
		data := make([]byte, len)
		js.CopyBytesToGo(data, args[1])
		in := bytes.NewReader(data)
		ids, err := sf.Identify(in, name, "")
		if err != nil {
			fmt.Printf("unable to identify %s\n", err)
			return err.Error()
		}
		w.Head(config.SignatureBase(), time.Now(), sf.C, config.Version(), sf.Identifiers(), sf.Fields(), "")
		w.File(name, int64(len), "", nil, nil, ids)
		w.Tail()
		return out.String()
	})
	return sfFunc
}

func main() {
	sf := static.New()
	js.Global().Set("identify", sfWrapper(sf))
	<-make(chan bool)
}
