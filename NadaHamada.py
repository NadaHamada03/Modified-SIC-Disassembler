#T Record processing
#symbol table generation
#assembly code output

if line.startswith('T') and line[1] != 'T':

    # Extract the first six characters and convert to hex
    t_start_loc = hex(int(line[3:7], 16))
    print("t_start_loc:", t_start_loc)

    # Extract the next two characters and convert to hex, then add to t_start_loc
    t_end_loc = hex(int(t_start_loc, 16) + int(line[7:9], 16))
    print("t_end_loc:", t_end_loc)

    # prints in console, helps keep track of any errors
    print("line_number:", line_number)
    print("line:", line)

    # cursor starts at 9th position, after Txxxxxxxx|-->, starting address and length of record
    counter = 9

    # equate the starting location of the text record to the location counter
    loc = int(t_start_loc, 16)

    # loop through the text record as long as the end location hasn't been reached
    while loc < int(t_end_loc, 16):

        # read the first 2 characters of the instruction bits
        opcode_hex_str = line[counter:counter + 2]

        if opcode_hex_str:
            opcode_hex = int(opcode_hex_str, 16)
            print("Opcode:", hex(opcode_hex))

            # assume the instruction is format 1 and map it
            instruct = instruction_set_for1.get(opcode_hex)

            # check the result of the successful mapping
            if instruct is not None:
                print("Mapped to instruction_set_for1:", instruct)

                output_file.write(f'{loc:04X}                  {instruct}                {opcode_hex:02X}           \n')

                # increment cursor counter by 2, format 1 is 2 hex chartacters
                counter += 2
                # increment location counter by 1 for the next instruction
                loc += 1

            # check the result of the unsuccessful mapping
            else:

                # try mapping to format 3 dictionary without modification
                instruct = instruction_set_for3.get(opcode_hex)

                # check the result of the successful mapping
                if instruct is not None:
                    print("Mapped to instruction_set_for3:", instruct)
                    label_hex = line[counter + 2:counter + 6]
                    label = int(label_hex, 16)

                    # check if instruction is RSUB because it has a default label
                    if instruct == 'RSUB':

                        print("RSUB instruction")

                        if label == 0x0000:
                            print("0000 label")
                            output_file.write(
                                f'{loc:04X}                  {instruct}                  {opcode_hex:02X}{label_hex}\n')

                            # increment location counter by 3
                            loc += 3

                    # process the instruction if it is not RSUB
                    else:

                        # check whether the scanned label is valid
                        if int(start_loc, 16) <= label <= int(end_loc, 16):
                            print(f"The scanned value {hex(label)} is within the range.")

                            # Adding a key-value pair with a unique "Var" number (label name) if they are not already in the dictionary
                            if label not in label_dict:
                                var_number = len(label_dict) + 1
                                label_dict[label] = f"Var{var_number}"
                                symbol_table_file.write(f'{hex(label)} : {label_dict.get(label)}\n')

                            output_file.write(
                                f'{loc:04X}                  {instruct}      {label_dict.get(label)}      {opcode_hex:02X}{label_hex}\n')

                            loc += 3

                        # label might have an indexing register
                        else:
                            print(f"The scanned value {hex(label)} is not within the range.")

                        # check if the new label after deducting 8000 in hex is a valid label
                        if int(start_loc, 16) <= label - 0x8000 <= int(end_loc, 16):

                            print(f"The scanned value {hex(label)} is within the range and has an indexing register.")

                            # Adding a key-value pair with a unique "Var" number
                            if label - 0x8000 not in label_dict:
                                var_number = len(label_dict) + 1
                                label_dict[label - 0x8000] = f"Var{var_number}"
                                symbol_table_file.write(f'{hex(label - 0x8000)} : {label_dict.get(label - 0x8000)}\n')

                            output_file.write(
                                f'{loc:04X}                  {instruct}     {label_dict.get(label - 0x8000)},x    {opcode_hex:02X}{label_hex}\n')

                            loc += 3

                # check the result of the unsuccessful mapping
                else:
                    instruct_modi = instruction_set_modi.get(opcode_hex)
                    if instruct_modi is not None:
                        print("Mapped to instruction_set_modi:", instruct_modi)
                        label_hex = line[counter + 2:counter + 6]
                        label = int(label_hex, 16)

                        if int(start_loc, 16) <= label <= int(end_loc, 16):
                            print(f"The scanned value {hex(label)} is within the range.")

                            # Adding a key-value pair with a unique "Var" number (label name) if they are not already in the dictionary
                            if label not in label_dict:
                                var_number = len(label_dict) + 1
                                label_dict[label] = f"Var{var_number}"
                                symbol_table_file.write(f'{hex(label)} : {label_dict.get(label)}\n')

                            output_file.write(
                                f'{loc:04X}                  {instruct_modi}      {label_dict.get(label)},4  {opcode_hex:02X}{label_hex}\n')

                            loc += 3

                        # label might have an indexing register
                        else:
                            print(f"The scanned value {hex(label)} is not within the range.")

                            # check if the new label after deducting 8000 in hex is a valid label
                            if int(start_loc, 16) <= label - 0x8000 <= int(end_loc):
                                print(
                                    f"The scanned value {hex(label)} is within the range and has an indexing register.")

                                # Adding a key-value pair with a unique "Var" number
                                if (label) - 0x8000 not in label_dict:
                                    var_number = len(label_dict) + 1
                                    label_dict[label - 0x8000] = f"Var{var_number}"
                                    symbol_table_file.write(
                                        f'{hex(label - 0x8000)} : {label_dict.get(label - 0x8000)}\n')

                                output_file.write(
                                    f'{loc:04X}                  {instruct_modi}     {label_dict.get(label - 0x8000)},x,4   {opcode_hex:02X}{label - 0x8000}\n')

                                loc += 3
                # increment counter by 6 for all format 3 (modified and not) instructions
                counter += 6

    # check if there is a gap between the locations, if there is then there is a reserve instruction
    next_line = next(input_file, None)
    if next_line is not None:
        next_t_start = hex(int(next_line[1:7], 16))

        if int(next_t_start, 16) - int(t_end_loc, 16) > 0x3:
            # calculating the reserve amount in decimal
            res_amt = int(next_t_start, 16) - int(t_end_loc, 16)

            # assume it is a RESB for simplicity as there is no way to determine whether it is a RESW/RESB
            output_file.write(f'{loc:04X}                  RESB     {res_amt}\n')

            loc = loc + res_amt

# print line end location
output_file.write(f'{loc:04X}                  END\n')

else:
# If the line is not exactly 18 characters, print an error message
output_file.write(f"Error: Line does not have 18 characters")

output_file.close()
input_file.close()