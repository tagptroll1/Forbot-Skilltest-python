def get_start_end(range_string: str) -> (int, int):
    if "-" in range_string:
        start, end = map(int, range_string.split("-"))
    else:
        if range_string:
            start = end = int(range_string)
        else:
            start = end = None
    return start, end

def build_string_ranges(set_of_numbers: set) -> str:
    # Since it's an iterator we can grab the first entry before looping to save a check inside the loop
    previous = next(set_of_numbers)
    final_result = [previous, '-']

    for i in set_of_numbers:
        if previous and i != previous+1:
            final_result.append(previous)
            final_result.append(',')
            final_result.append(i)
            final_result.append('-')
        previous = i
    else:
        # Make sure to include the last number
        final_result.append(previous)

    # Join the results together and remove any stray trailing -, which should not be an issue.
    return "".join(map(str, final_result)).rstrip('-')

def subtract_list_of_ranges_from_set(initial_set: set, ranges: list) -> set:
    for range_ in ranges:
        # Create a range of start to end of the excluded numbers
        start, end = get_start_end(range_.strip())

        # Handle Empty inputs
        if start is None:
            continue

        initial_set -= set(range(start, end + 1))
    return initial_set

def run() -> None:
    includes = input("Includes: ")
    excludes = input("Excludes: ")
    expected = None # used for hard-coded testing

    # Takes a few seconds
    # includes = "0-100000000"
    # excludes = "2500-5000000"

    # includes = "10-100"
    # excludes = "20-30"
    # expected = "10-19,31-100"

    # includes = "50-5000,10-100"
    # excludes = ""
    # expected = "10-5000"

    # includes = "10-100,200-300"
    # excludes = "95-205"
    # expected = "10-94,206-300"

    # includes = "10-100, 200-300, 400-500"
    # excludes = "95-205, 410-420"
    # expected = "10-94,206-300,400-409,421-500"

    # includes = "5-13, 2-8"
    # excludes = "4-10, 5-11"
    # expected = "2-3,12-13"


    inclue_ranges = includes.split(",")
    exclude_ranges = excludes.split(",")

    all_included = set()

    for include in inclue_ranges:
        # Create a range of start to end
        start, end = get_start_end(include.strip())
        include_range = set(range(start, end + 1))

        # Remove all excluded numbers from the range
        include_range = subtract_list_of_ranges_from_set(include_range, exclude_ranges)
        
        # Add all the new included numbers to the total set
        all_included = all_included.union(include_range)

    print("Included: ", includes)
    print("Excluded: ", excludes)

    if expected:
        print("Expected: ", expected)
    # Make the set a sorted iterator. In theory the set can be sorted and iterated over for more speed
    # But this ensures it's sorted
    include_range = iter(sorted(all_included))
    final_string = build_string_ranges(include_range)

    print(final_string)

if __name__ == "__main__":
    run()