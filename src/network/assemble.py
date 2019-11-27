"""
Create bitmessage protocol command packets
"""

import struct

import addresses
from network.constants import MAX_ADDR_COUNT
from network.node import Peer
from protocol import CreatePacket, encodeHost


def assemble_addr(peerList):
    """Create address command"""
    if isinstance(peerList, Peer):
        peerList = (peerList)
    if not peerList:
        return b''
    retval = b''
    for i in range(0, len(peerList), MAX_ADDR_COUNT):
        payload = addresses.encodeVarint(
            len(peerList[i:i + MAX_ADDR_COUNT]))
        for stream, peer, timestamp in peerList[i:i + MAX_ADDR_COUNT]:
            payload += struct.pack(
                '>Q', timestamp)  # 64-bit time
            payload += struct.pack('>I', stream)
            payload += struct.pack(
                '>q', 1)  # service bit flags offered by this node
            payload += encodeHost(peer.host)
            payload += struct.pack('>H', peer.port)  # remote port
        retval += CreatePacket('addr', payload)
    return retval
