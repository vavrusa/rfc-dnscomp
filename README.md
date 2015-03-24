## What it is

Draft proposal to use stream compression on DNS packets without
breaking backwards compatibility with DNS protocol.

## Building

Depends on [miekg/mmark][mmark] and [xml2rfc][xml2rfc].

```sh
$ go get github.com/miekg/mmark/mmark
$ pip install xml2rfc
$ make
```

[mmark]: http://github.com/miekg/mmark
[xml2rfc]: http://xml2rfc.ietf.org/
