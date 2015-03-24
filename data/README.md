# Captured responses

There is a pcap file and a (k)dig output log for captured responses.

## Queries

* `+dnssec @a.root-servers.net NS .`
* `+dnssec @a.root-servers.net NS cz`
* `+dnssec @a.ns.nic.cz. AAAA a.ns.nic.cz.`
* `+dnssec @a.ns.nic.cz. A non-existent-name.cz.`
* `+edns=0 @a.root-servers.net NS .`       
* `+edns=0 @a.root-servers.net NS cz`
* `+edns=0 @a.ns.nic.cz. AAAA a.ns.nic.cz.`
* `+edns=0 @a.ns.nic.cz. A non-existent-name.cz.`

## Metrics

```sh
$ pip install pypcapfile lz4
$ ./metrics.py responses.pcap
[0] base:  913B, zlib:  465B, lz4:  532B
[1] base:  485B, zlib:  335B, lz4:  364B
[2] base: 1214B, zlib: 1015B, lz4: 1010B
[3] base: 1010B, zlib:  936B, lz4:  931B
[4] base:  755B, zlib:  302B, lz4:  394B
[5] base:  278B, zlib:  127B, lz4:  159B
[6] base:  218B, zlib:  116B, lz4:  144B
[7] base:  105B, zlib:  100B, lz4:  106B
```
