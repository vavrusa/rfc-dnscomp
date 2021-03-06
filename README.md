## Abstract

This document describes an application of data compression algorithms on DNS messages with the goal of reducing message size of frequent responses.
The client proposes compression protocol which the server may use to compress an arbitrary part of the response.

*TL;DR* this:

* cuts the `NS .` *(already label-compressed)* response size by half
* is applicable to any message type
* is opt-in *(unlike label compression)*
* ...and hopefully doesn't break the protocol.

## See it

The `make publish` builds a HTML version, the branch `gh-pages` contains a built `index.html` for GitHub Pages.

* HTML at [vavrusa.github.io/rfc-dnscomp][ghpages]
* Measurements in [data](data) directory

## Build it

Depends on [miekg/mmark][mmark] and [xml2rfc][xml2rfc].

```sh
$ go get github.com/miekg/mmark/mmark
$ pip install xml2rfc
$ make
```

[mmark]: http://github.com/miekg/mmark
[xml2rfc]: http://xml2rfc.ietf.org/
[ghpages]: http://vavrusa.github.io/rfc-dnscomp
