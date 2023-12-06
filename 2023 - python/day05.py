
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f9cd071425b0d21d57535630a0d32e44bb5c7fe32070a07aa9170e67bb82f54f3bb900290fd1cb879c94a1e1230f809a51bec010d7f706512"
import aocd
import re


USE_TEST_DATA = 0
TEST_DATA = 'seeds: 79 14 55 13\n\nseed-to-soil map:\n50 98 2\n52 50 48\n\nsoil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15\n\nfertilizer-to-water map:\n49 53 8\n0 11 42\n42 0 7\n57 7 4\n\nwater-to-light map:\n88 18 7\n18 25 70\n\nlight-to-temperature map:\n45 77 23\n81 45 19\n68 64 13\n\ntemperature-to-humidity map:\n0 69 1\n1 0 69\n\nhumidity-to-location map:\n60 56 37\n56 93 4'
# NUMBER_REGEX = r'^Card +(\d+): (.*) \| (.*)$'
NUMBER_REGEX = r'(\d+)'
MAP_REGEX = r'(.*) map:'

def part_1():
    if USE_TEST_DATA:
        input_list = TEST_DATA.splitlines()
    else:
        input_list = aocd.get_data(day=5).splitlines()

    seed_list_match = re.findall(NUMBER_REGEX, input_list[0])
    seed_list_match = list(map(int, seed_list_match))
    seed_range_list = []
    for seed in range(len(seed_list_match) // 2):
        seed_range_list.append((seed_list_match[2 * seed], seed_list_match[2 * seed] + seed_list_match[2 * seed + 1]))
    seed_range_list.sort(key=lambda x: x[0])

    # For every map, create a lambda function based on the numbers
    transformations_list = []
    current_map = []
    for line in input_list[2:]:
        if line == '':
            # Save the dict
            current_map.sort(key=lambda x: x[0])
            transformations_list.append(current_map)
            current_map = []
            continue

        if not line[0].isdigit():
            continue

        # Add to the current map
        conv = re.findall(NUMBER_REGEX, line)
        conv = tuple(map(int, conv))
        (soil_start_idx, seed_start_idx, both_range) = conv
        new_conv = (seed_start_idx, seed_start_idx + both_range, soil_start_idx - seed_start_idx)
        if current_map == []:
            current_map = [new_conv]
        else:
            current_map.append(new_conv)
    
    transformations_list.append(current_map)

    # Go through every stage from seed to location
    for transformations in transformations_list:
        # Do every seed range for every step
        new_seed_range_list = []
        for seed_range in seed_range_list:
            (seed_start, seed_stop) = seed_range
            copy_value_to_new = True
            for transformation in transformations:
                # For every tranformation range, see if the seed start idx is in range.
                # If yes, transform every object in transformation range
                # If no, check if seed end idx is in range. If so, transform every object there!
                (trans_start, trans_stop, modification_needed) = transformation

                if trans_start <= seed_start < trans_stop:
                    if seed_stop <= trans_stop:
                        # Seed:    |         |
                        # Trans: |               |
                        # If the whole seed range is in transformation range, make the transformation
                        new_seed_range_list.append((seed_start + modification_needed, seed_stop + modification_needed))
                        copy_value_to_new = False
                        break # next seed range
                    else:
                        # Seed:    |         |
                        # Trans: |        |
                        # Save whatever's outside the trans range for another conversion
                        untransformed_seed_range = (trans_stop, seed_stop)
                        seed_range_list.append(untransformed_seed_range)
                        # Add everything that is available in the trans range
                        seed_stop = trans_stop
                        new_seed_range_list.append((seed_start + modification_needed, seed_stop + modification_needed))
                        copy_value_to_new = False
                        break # next seed range
                elif trans_start < seed_stop <= trans_stop:
                    # Seed:    |         |
                    # Trans:       |                   |
                    # Save whatever's outside the trans range for another conversion
                    untransformed_seed_range = (seed_start, trans_start)
                    seed_range_list.append(untransformed_seed_range)
                    # Add everything that is available in the trans range
                    seed_start = trans_start
                    new_seed_range_list.append((seed_start + modification_needed, seed_stop + modification_needed))
                    copy_value_to_new = False
                    break # next seed range

            # If no match is found, the value should remain
            if copy_value_to_new:
                new_seed_range_list.append(seed_range)
        
        seed_range_list = new_seed_range_list
        # assert(27 == sum(map(lambda x: x[1] - x[0], seed_range_list)))
    seed_range_list.sort(key=lambda x: x[0])
    print("lowest of lowest = {}". format(seed_range_list[0][0]))
    # assert that the total number of seeds does not change
    #     minimum_location = min(minimum_location, current_value)
    #     print("original {} to {}".format(seed, current_value))
    # print(minimum_location)
part_1()