"""
Funciones para leer datos binarios con diferentes encodings (endianness)
"""
import struct


def read_u16_be(data: bytes, offset: int) -> int:
    """
    Lee un uint16_t en Big Endian
    
    Args:
        data: Bytes a leer
        offset: Posición inicial
        
    Returns:
        Valor leído como entero
    """
    return struct.unpack('>H', data[offset:offset+2])[0]


def read_u32_le(data: bytes, offset: int) -> int:
    """
    Lee un uint32_t en Little Endian
    
    Args:
        data: Bytes a leer
        offset: Posición inicial
        
    Returns:
        Valor leído como entero
    """
    return struct.unpack('<I', data[offset:offset+4])[0]
