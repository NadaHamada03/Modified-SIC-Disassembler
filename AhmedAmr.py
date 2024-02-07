# creating the instruction set dictionary for format 3 without modification
instruction_set_for3 = {
    0x18: 'ADD', 0x40: 'AND', 0x28: 'COMP',
    0x24: 'DIV', 0x3C: 'J', 0x30: 'JEQ',
    0x34: 'JGT', 0x38: 'JLT', 0x48: 'JSUB',
    0x00: 'LDA', 0x50: 'LDCH', 0x08: 'LDL',
    0x04: 'LDX', 0x20: 'MUL', 0x44: 'OR',
    0xD8: 'RD', 0x4C: 'RSUB', 0x0C: 'STA',
    0x54: 'STCH', 0x14: 'STL', 0xE8: 'STSW',
    0x10: 'STX', 0x1C: 'SUB', 0xE0: 'TD',
    0x2C: 'TIX', 0xDC: 'WD',
}

# creating the instruction set dictionary for format 3 with modification
instruction_set_modi = {
    0x19: 'ADD', 0x41: 'AND', 0x29: 'COMP',
    0x25: 'DIV', 0x3D: 'J', 0x31: 'JEQ',
    0x35: 'JGT', 0x39: 'JLT', 0x49: 'JSUB',
    0x01: 'LDA', 0x51: 'LDCH', 0x09: 'LDL',
    0x05: 'LDX', 0x21: 'MUL', 0x45: 'OR',
    0xD9: 'RD', 0x0D: 'STA',
    0x55: 'STCH', 0x15: 'STL', 0xE9: 'STSW',
    0x11: 'STX', 0x1D: 'SUB', 0xE1: 'TD',
    0x2D: 'TIX', 0xDD: 'WD',
}

# creating the instruction set dictionary for format 1
instruction_set_for1 = {
    0xC4: 'FIX', 0xC0: 'FLOAT',
    0xF4: 'HIO', 0xC8: 'NORM',
    0xF0: 'SIO', 0xF8: 'TIO',
}

# create the assembly text file, output will be without line labels
assembly_code = f'/Users/nadahamada/Desktop/assembly_code.txt'

# create the assembly text file, output will be with line labels
assembly = f'/Users/nadahamada/Desktop/assembly.txt'

# read the hte_record.txt file
hte_record = f'/Users/nadahamada/Desktop/HTE.txt'

# Create a symbol table txt file
symbol_table_file = open('/Users/nadahamada/Desktop/symbol_table.txt', 'w')

# Dictionary of unique labels and their corresponding address
label_dict = {}

# Checks whether the hte has a valid structure
with open(hte_record, 'r') as input_file:
    input_lines = input_file.readlines()

    # Check the file structure (validation)
    # Minimum number of lines is 2 (H & E records, assuming that the code is just a RESB/RESW)
    if len(input_lines) < 2:
        print("File does not contain enough lines.")

    # Checks for 1 H record, 1 E record, T records in the middle
    elif input_lines[0].startswith('H') and all(line.startswith('T') for line in input_lines[1:-1]) and input_lines[-1].startswith('E'):
        print("File structure is valid.")
    else:
        print("File structure is not valid.")
input_file.close()

# Counts the number of lines in the file
with open(hte_record, 'r') as input_file:
    line_count = 0

    # Iterate through each line in the file
    for line in input_file:
        line_count += 1

    # Print the total number of lines
    print("Total number of lines in the file:", line_count)
input_file.close()

try:
    with open(hte_record, 'r') as input_file, open(assembly_code, 'w') as output_file:
        # Read the file line by line
        for line in input_file:
            # Extract the first letter of each line
            first_letter = line[0] if line.strip() else None

            # Check if the line starts with 'h'
            if first_letter == 'H':
                # Check if the line has exactly 18 digits + H letter
                if len(line.strip()) == 19:
                    output_file.write('LOCATION  LINE_LABEL  INSTRUC  TARGET_LABEL  OPCODE\n')

                    # Read and write the first 6 characters (name of programme)
                    output_file.write('          ' + line[1:7].strip() + '      ')

                    # Read and write the next 6 characters with a space (starting address of programme)
                    output_file.write('START    ' + line[9:13].strip() + '\n')
                    start_loc = hex(int(line[9:13], 16))
                    print("Start Location Counter:", start_loc)

                    # Read the next 6 characters, for looping (length of programme)
                    end_loc = hex(int(line[15:19], 16) + int(line[9:13], 16))
                    print("End Location Counter:", end_loc)

                    # Variables to store values
                    t_start_loc_hex = "0x"  # Starting location counter of the current text record
                    t_end_loc_hex = "0x"  # Ending location counter of the current text record
                    instruct = ""  # Possible instruction
                    target_label = "0x"  # Possible label

                    # Loop through lines and enumerate to get the line number
                    for line_number, line in enumerate(input_file, start=1):

                        # Strip newline characters from the line
                        line = line.strip()

                        #beginning of T record processing

                        #end of T record Processing

    #checking for labels and regenrating the assembly code
    for key, value in label_dict.items():
        print(f'{key}: {value}')

    with open(assembly_code, 'r') as input_file, open(assembly, 'w') as output_file:
        output_file.write(input_file.readline())
        output_file.write(input_file.readline())

        # Process the rest of the lines
        for line in input_file:

            # Extract the first 4 characters (location counters) from the line
            # Search for the location counter in the label dictionary
            label_value = label_dict.get(int(line[0:4], 16))
            print('in if')
            print(f'Label from mapping: {line[0:4]}')
            print(f'Label from assembly code: {label_value}')

            # this line has a label
            if label_value is not None:
                # Write to the output file
                output_file.write(f'{line[0:4]}        {label_value}      {line[22:]}')
                print('in if')

            # this line does not have a label
            else:
                output_file.write(line)
                print(f'in else')

    output_file.close()
    input_file.close()

except FileNotFoundError:
    print(f"Error: The file '{hte_record}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")