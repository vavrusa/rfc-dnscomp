## What it is

Draft proposal to use stream compression on DNS packets without
breaking backwards compatibility with DNS protocol.

## See it

The `make publish` builds a HTML version of the draft in the branch `gh-pages`,
so it can be viewed at [vavrusa.github.io/rfc-dnscomp][ghpages].

## Building

Depends on [miekg/mmark][mmark] and [xml2rfc][xml2rfc].

```sh
$ go get github.com/miekg/mmark/mmark
$ pip install xml2rfc
$ make
```

[mmark]: http://github.com/miekg/mmark
[xml2rfc]: http://xml2rfc.ietf.org/
[ghpages]: http://vavrusa.github.io/rfc-dnscomp
