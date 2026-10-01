"""Extract class signatures, never method bodies, for preprocessing metadata.

Run this only when updating the pinned mapping inputs. The Gradle build uses
the checked-in .api.gz files and does not need Python or Minecraft jars.
"""

import gzip
import io
import struct
import sys
import zipfile


def signatures(data):
    stream = io.BytesIO(data)

    def u1():
        return stream.read(1)[0]

    def u2():
        return struct.unpack(">H", stream.read(2))[0]

    def u4():
        return struct.unpack(">I", stream.read(4))[0]

    def skip_attributes():
        for _ in range(u2()):
            u2()
            stream.seek(u4(), 1)

    if u4() != 0xCAFEBABE:
        raise ValueError("not a class file")
    u2()
    u2()
    pool = [None] * u2()
    index = 1
    while index < len(pool):
        tag = u1()
        if tag == 1:
            pool[index] = stream.read(u2()).decode("utf-8", "replace")
        elif tag in (3, 4, 9, 10, 11, 12, 17, 18):
            stream.seek(4, 1)
        elif tag in (5, 6):
            stream.seek(8, 1)
            index += 1
        elif tag in (7, 8, 16, 19, 20):
            pool[index] = u2()
        elif tag == 15:
            stream.seek(3, 1)
        else:
            raise ValueError("unknown constant pool tag %s" % tag)
        index += 1

    def classname(index):
        return pool[pool[index]] if index else ""

    access = u2()
    name = classname(u2())
    parent = classname(u2())
    interfaces = [classname(u2()) for _ in range(u2())]
    lines = ["C\t%s\t%d\t%s\t%s\n" % (name, access, parent, ",".join(interfaces))]
    for kind in ("F", "M"):
        for _ in range(u2()):
            member_access = u2()
            member_name = pool[u2()]
            descriptor = pool[u2()]
            skip_attributes()
            if member_name != "<clinit>":
                lines.append("%s\t%s\t%d\t%s\t%s\n" %
                             (kind, name, member_access, member_name, descriptor))
    return lines


def main(jar_path, output_path, prefix=""):
    with zipfile.ZipFile(jar_path) as jar, open(output_path, "wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as output:
            for name in sorted(jar.namelist()):
                if name.endswith(".class") and name.startswith(prefix) and not name.startswith("META-INF/"):
                    output.write("".join(signatures(jar.read(name))).encode("utf-8"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
