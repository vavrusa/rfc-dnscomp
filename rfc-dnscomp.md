% Title = "DNS Message Compression"
% abbrev = "dnsmsgcompr"
% category = "std"
% docName = "draft-vavrusa-dnscompr-00"
% ipr= "trust200902"
% area = "Internet"
% workgroup = ""
% keyword = ["DNS"]
%
% date = 2015-03-23T00:00:00Z
%
% [[author]]
% initials="M."
% surname="Vavrusa"
% fullname="Marek Vavrusa"
% #role="editor"
% organization = "CZ.NIC"
%   [author.address]
%   email = "marek.vavrusa@nic.cz"
%   [author.address.postal]
%   street = "Milesovska 1136/5"
%   city = "Praha"
%   code = "130 00"
%   country = "CZ"

.# Abstract

This document describes an application of data compression algorithms on DNS messages with the goal of
reducing message size of frequent responses. The client proposes compression protocol which the server may use
to compress an arbitrary part of the response.

{mainmatter}

# Introduction

## Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in [@RFC2119].

## Terminology

The reader is assumed to be familiar with the basic DNS and DNSSEC concepts described in [@RFC1034], [@RFC1035] and [@RFC6891].
The terms "compression", "decompression" are used as in [@RFC1951].

## Rationale

The domain name compression was introduced in [@RFC1035 section 4.1.4] with the intent of reducing message length by
avoiding repetitive sequences of domain name labels. This has proven useful especially for the the UDP-carried messages,
so the [@RFC1123 section 6.1.2.4] mandated the use of compression in responses.

A domain name is represented by a sequence of labels, where the first octet denotes the label length, excluding itself.
Each domain name is required to be terminated by a zero-length label representing the root domain name.
[@RFC1035 section 2.3.4] declares that a label length **MUST** be 63 bytes or less. This requires the least significant 6 bits
from the first octet for the label length, and leaves the 2 most significant bits reserved for second meaning.

If both most significant bits have a value of '1', the following 14 bits represent a compression pointer, which denotes
a position in the message where the next label continues. This position may also be a compression pointer, as it points backwards
and the final name doesn't exceed the size limits [@RFC1035 section 2.3.4]. The method implies only the repetitive domain name labels
may be compressed.

Later, [@RFC6891 section 5.] defined an extended label type, where the most significant two bits have a value of '01',
and the remaining 6 bits are used for extended label type. [@RFC3363 section 3.] has shown that the extended label types
are rejected as malformed by unaware DNS implementations.

The proposed compression method introduces an extended label type to indicate that the remainder of the message is compressed,
and an OPT RR option COMPRESS to negotiate compression support. To ensure compatibility with existing infrastructure, the new label type **MUST NOT** be used in a DNS query, and it **MAY** be used in DNS response only after the support is indicated by the presence of the COMPRESS option in the query.

# How the remainder compression works

The client proposes a compression algorithm via the COMPRESS OPT option, this mandates that the both client and the server support [@RFC6891] EDNS.
If the server doesn't support EDNS, no OPT RR is returned in the response and no compression occurs.
A COMPRESS-aware server **MAY** place a compression indicator at any start of the label in the message, followed by the compressed remainder of the message.
The server **SHOULD** use the client-proposed algorithm if it supports it, but it **MAY** use the mandatory algorithm as well.

If a client recognizes compression indicator, it decompresses the remainder of the message in its place.
If the server uses mandatory algorithm instead of negotiated, client **SHOULD** assume that the server doesn't support the negotiated algorithm,
and **SHOULD** try different algorithm next time. If the response isn't compressed, the client **MUST NOT** presume that the server doesn't support it.

# The COMPRESS OPT option

COMPRESS is an OPT RR [@RFC6891] option, that can be included once in the RDATA of an OPT RR in DNS messages.

The option is encoded in 5 bytes as shown below.

{#fig:compress_opt type="ascii-art" align=center}
                         1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |       OPTION-CODE TBD         |     OPTION-LENGTH = 1         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Algorithm   |
    +-+-+-+-+-+-+-+-+
Figure: OPT RR option COMPRESS format.

The Algorithm field defines the compression algorithm proposed by the client, denoted by an assigned number.
There are 256 possible combinations, including the mandatory compression algorithm. In the case of exhaustion,
a new OPT code should be proposed. A value of zero indicates the mandatory compression algorithm.

The COMPRESS option **MAY** be used in the query to indicate compression request and negotiated algorithm.
The use of COMPRESS option in the response is not defined.

@TODO@

## Algorithms

a. DEFLATE, code 0x00, MANDATORY

   A lossless compressed data format that compresses data using a combination of the LZ77 algorithm and Huffman coding.
   As specified in the [@RFC1951], the format can be implemented readily in a manner not covered by patents.

b. LZ4, code 0x01 OPTIONAL

   LZ4 is a lossless data compression algorithm that is focused on compression and decompression speed.
   BSD licensed implementation written by Yann Collet, no RFC available to date.

@TODO@ Needs further research, the compression algorithms are mine field of patents.

# The remainder compression indicator

This document proposes an alternative remainder compression indicator:

{#fig:compr_indicator type="ascii-art" align=center}
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    | 0  1| 0  0  0  0  0  1|       ALGORITHM       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
Figure: Compression indicator extended label type format.

The "01" denotes the extended label type, as defined in the [@RFC6891 section 5.].
The remaining part of the first octet "000001" defines a remainder compression indicator.
The next octet represent the used compression algorithm.

Note - a decompressed remainder of the message **MUST NOT** contain a compression indicator,
thus a message can only be compressed once.

@TODO@

# Examples

# Client: declaring compression support

@TODO@

# Server: compressing message part

@TODO@

# Backward Compatibility

The proposed label format may not be correctly processed by existing software, so the following considerations
must be taken into account:

a.  DNS header is never compressed, as it does not contain a domain name label.
b.  The proposed remainder compression indicator **MUST NOT** be used in domain name query.
c.  The proposed remainder compression **MUST NOT** be present in domain name response, unless proposed by the requestor.

Applications intercepting response messages may reject the message as malformed, but there is no legitimate application for
tampering with responses known to the author.

# Client considerations

Client **MUST** follow fallback procedure as in [@RFC6891 section 6.2.2.].

# Performance considerations

@TODO@
@REMARK@ Depends on algorithm and implementation, may be faster because of bandwidth savings, may be slower because of extra overhead.
@REMARK@ LZ4 for example shows over 480MB/s compression speed on a single core, this is almost equal to 1M 512B packets/sec per core.
@REMARK@ Response using this draft may not use label compression.
@REMARK@ TODO: measurements on performance (nr. cycles per compressed/uncompressed response)

# Security considerations

The compression library implementing used compression algorithm is a liability.
Corruption of the compressed data is likely to be more severe than for the uncompressed data,
the DNS implementation **MUST** parse the message after decompression, as it would with an uncompressed message,
even though the decompression algorithm may detect a corruption.

# Acknowledgements

@TODO@

<!-- reference we need to include -->

{backmatter}

# Appendix A. Evaluation on selected responses

@TODO@
@REMARK@ See https://github.com/vavrusa/rfc-dnscomp/tree/master/data
