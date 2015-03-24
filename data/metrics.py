#!/usr/bin/env python

import sys
import zlib
import lz4
from pcapfile import savefile

for arg in sys.argv[1:]:
	pcap = savefile.load_savefile(open(arg, 'r'))
	for i in range(0, len(pcap.packets)):
		# strip IP/UDP
		pkt = pcap.packets[i].raw()[42:]
		# do not compress header
		zlib_len = len(zlib.compress(pkt[12:])) + 12
		lz4_len = len(lz4.compress(pkt[12:])) + 12
		print('[%d] base: %4dB, zlib: %4dB, lz4: %4dB' % \
		      (i, len(pkt), zlib_len, lz4_len))

