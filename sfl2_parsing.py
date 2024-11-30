import sys

def parse_sfl2(sfl2_file):
    # read data
    with open(sfl2_file, 'rb') as file:
        data = file.read()

    # initialize buffer and contexts
    data_buffer = bytearray()
    name_header = "636F6D2E6170706C652E6170702D73616E64626F782E72656164"
    extracted_value = bytearray()
    extracted_data = []
    header_found = False
    reading = False
    find_uuid = False

    # loop through data
    for byte in data:
        data_buffer.append(byte)  # add each new byte to the buffer

        if header_found:
            if format(byte, '02x').upper() == "2F":
                reading = True

        if reading:
            if not find_uuid:
                if format(byte, '02x') != "00":
                    extracted_value.append(byte)
                else:
                    extracted_data.append(extracted_value.decode('utf-8', errors='ignore'))
                    extracted_value = bytearray()
                    reading = False
                    header_found = False

        # keep buffer at 26 bytes
        if len(data_buffer) > 26:
            data_buffer.pop(0)

        if data_buffer.hex().upper() == name_header:
            header_found = True

    return extracted_data

def main():
    # Check if enough arguments are provided
    if len(sys.argv) < 2:
        print("Usage: python sfl2_parsing.py <sfl2_file_path>")
        sys.exit(1)

    sfl2_file = sys.argv[1]

    # parse file
    parsed_data = parse_sfl2(sfl2_file)

    for value in parsed_data:
        print(value)


if __name__ == "__main__":
    main()
