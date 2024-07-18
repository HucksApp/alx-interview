#!/usr/bin/python3
'''A script for parsing HTTP request logs.
'''
import sys
import re
from collections import defaultdict


def print_stats(total_size, status_code_counts):
    '''Prints the accumulated statistics of the HTTP request log.
    '''
    print(f"File size: {total_size}")
    for code in sorted(status_code_counts):
        if status_code_counts[code] > 0:
            print(f"{code}: {status_code_counts[code]}")


def main():
    '''the log parser.
    '''
    total_size = 0
    line_count = 0
    status_code_counts = defaultdict(int)

    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<date>[^\]]+)\] "GET /projects/260 HTTP/1.1" (?P<status_code>\d{3}) (?P<file_size>\d+)'
    )

    try:
        for line in sys.stdin:
            match = log_pattern.match(line)
            if match:
                data = match.groupdict()
                status_code = int(data['status_code'])
                file_size = int(data['file_size'])

                total_size += file_size
                status_code_counts[status_code] += 1
                line_count += 1

                if line_count % 10 == 0:
                    print_stats(total_size, status_code_counts)
    except KeyboardInterrupt:
        print_stats(total_size, status_code_counts)
        sys.exit(0)

    # Print final stats after processing all lines
    print_stats(total_size, status_code_counts)


if __name__ == "__main__":
    main()
