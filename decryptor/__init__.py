import logging
from enum import Enum
from zlib import decompress

from decryptor.qmc1 import qmc1_decrypt
from decryptor.tripledes import DECRYPT, tripledes_crypt, tripledes_key_setup


class QrcType(Enum):
    LOCAL = 0
    CLOUD = 1


def qrc_decrypt(encrypted_qrc: str | bytearray | bytes, qrc_type: int) -> tuple[str | None, str | None]:
    if encrypted_qrc is None or encrypted_qrc.strip() == "":
        logging.error("没有可解密的数据")
        return None, None
    try:
        key = bytearray(b"!@#)(*$%123ZXC!@!@#)(NHL")

        if isinstance(encrypted_qrc, str):
            encrypted_text_byte = bytearray.fromhex(encrypted_qrc)  # 将文本解析为字节数组
        elif isinstance(encrypted_qrc, bytearray):
            encrypted_text_byte = encrypted_qrc
        elif isinstance(encrypted_qrc, bytes):
            encrypted_text_byte = bytearray(encrypted_qrc)
        else:
            logging.error("无效的加密数据类型")
            return None, "无效的加密数据类型"

        if qrc_type == QrcType.LOCAL:
            qmc1_decrypt(encrypted_text_byte)
            encrypted_text_byte = encrypted_text_byte[11:]

        data = bytearray(len(encrypted_text_byte))
        schedule = [[[0] * 6 for _ in range(16)] for _ in range(3)]
        tripledes_key_setup(key, schedule, DECRYPT)

        # 以 8 字节为单位迭代 encrypted_text_byte
        for i in range(0, len(encrypted_text_byte), 8):
            temp = bytearray(8)

            tripledes_crypt(encrypted_text_byte[i:], temp, schedule)

            # 将结果复制到数据数组
            for j in range(8):
                data[i + j] = temp[j]

        decrypted_qrc = decompress(data).decode("utf-8")
    except Exception as e:
        logging.exception("解密失败")
        return None, str(e)
    return decrypted_qrc, None