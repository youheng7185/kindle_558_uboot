import re
import sys

pattern = re.compile(
    r"setmem\s*/\d+\s+(0x[0-9a-fA-F]+)\s*=\s*(0x[0-9a-fA-F]+)",
    re.IGNORECASE
)

def convert_line(line):
    # remove inline comments
    line = line.split("//")[0].strip()
    if not line:
        return None

    match = pattern.search(line)
    if not match:
        return None

    addr, value = match.groups()
    return f"DATA 4 {addr} {value}"

def convert_file(input_path, output_path=None):
    output_lines = []

    with open(input_path, "r") as f:
        for line in f:
            converted = convert_line(line)
            if converted:
                output_lines.append(converted)

    output_text = "\n".join(output_lines)

    if output_path:
        with open(output_path, "w") as f:
            f.write(output_text + "\n")
    else:
        print(output_text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py input.txt [output.txt]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    convert_file(input_file, output_file)