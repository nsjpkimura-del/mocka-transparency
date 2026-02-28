import sys
import hashlib
from rfc3161ng import RemoteTimestamper

DEFAULT_TSA_URL = "http://timestamp.digicert.com"

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main():
    if len(sys.argv) < 3:
        print("usage: python tools\\rfc3161_stamp.py <infile> <outfile> [tsa_url]")
        sys.exit(2)

    infile = sys.argv[1]
    outfile = sys.argv[2]
    tsa_url = sys.argv[3] if len(sys.argv) >= 4 else DEFAULT_TSA_URL

    with open(infile, "rb") as f:
        data = f.read()

    ts = RemoteTimestamper(tsa_url, hashname="sha256")
    token = ts.timestamp(data)

    with open(outfile, "wb") as f:
        f.write(token)

    print("INFILE=" + infile)
    print("INFILE_SHA256=" + sha256_file(infile))
    print("TSR_OUT=" + outfile)
    print("TSR_SHA256=" + sha256_file(outfile))
    print("TSA_URL=" + tsa_url)

if __name__ == "__main__":
    main()
