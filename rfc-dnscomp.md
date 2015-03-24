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
from the first octet for the label length, and leaves the 2 most significant bits reserved for second meaning:

{#fig:compr_ptr type="ascii-art" align=center}
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    | 1  1|                OFFSET                   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
Figure: Domain name compression pointer format.

If both most significant bits have a value of '1', the following 14 bits represent a compression pointer, which denotes
a position in the message where the next label continues. This position may also be a compression pointer, as it points backwards
and the final name doesn't exceed the size limits [@RFC1035 section 2.3.4]. The method implies only the repetitive domain name labels
may be compressed.

Later, [@RFC6891 section 5.] defined an extended label type, where the most significant two bits have a value of '01',
and the remaining 6 bits are used for extended label type. [@RFC3363 section 3.] has shown that the extended label types
are rejected as malformed by unaware DNS implementations.

The proposed compression method introduces an extended label type to indicate that the remainder of the message is compressed,
and a and OPT RR option COMPRESS to declare compression support. To ensure compatibility with existing infrastructure, the new label type **SHOULD NOT** be used in a DNS query, and it **MAY** be used in DNS response only after the support is indicated by the presence of the COMPRESS option in the query.

# How the remainder compression works

The client proposes a compression algorithm via the COMPRESS OPT option, this mandates that the client supports [@RFC6891] EDNS.
A COMPRESS-aware server places compression indicator at any start of the label in the message, and then the compressed remainder of the message. If a client recognizes compression indicator, it decompresses the remainder of the message in its place.

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

The Algorithm field defines the compression algorithm proposed by the client.
A value of zero indicates the default proposed compression algorithm.

@TODO@

## Algorithms

a. DEFLATE, code 0x00, MANDATORY

   A lossless compressed data format that compresses data using a combination of the LZ77 algorithm and Huffman coding.
   As specified in the [@RFC1951], the format can be implemented readily in a manner not covered by patents.

b. LZ4, code 0x01

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

Note - a decompressed remainder of the message **MUST NOT** contain a compression pointer.

@TODO@

# Examples

# Client: declaring compression support

@TODO@

# Server: compressing message part

@TODO@

# Backward Compatibility

The proposed label format *MAY NOT* be correctly processed by existing software, so the following considerations
must be taken into account:

a. DNS header is never compressed, as it does not contain a domain name label.
b. The proposed remainder compression indicator **MUST NOT** be used in domain name query.
c. The proposed remainder compression **MUST NOT** be present in domain name response, unless proposed by the requestor.

Applications intercepting response messages **MAY** misinterpret the message as malformed.

# Performance considerations

@TODO@ Depends on algorithm and implementation, may be faster because of bandwidth savings, may be slower because of extra overhead.

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

