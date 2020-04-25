#!/bin/python

import socket
import argparse
import csv
import sys

from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="bruteforces dns")

parser.add_argument("--threads", type=int, help="number of threads")
parser.add_argument("-D", metavar="dictionary", type=str, help="dictionary file", required=True)
parser.add_argument("-o", metavar="output", type=str, help="csv output file")
parser.add_argument("hostname", type=str, help="hostname to bruteforce")

args = parser.parse_args()

dictionary_filename = args.D
output_filename = args.o
thread_no = 1
if args.threads is not None:
    thread_no = args.threads
hostname = args.hostname

try:
    dictionary = open(dictionary_filename, "r")
except FileNotFoundError:
    print("dictionary file not found")
    exit(1)

if output_filename is not None:
    try:
        output = open(output_filename, "w")
        output_writer = csv.writer(output)
    except:
        print("cannot open file for writing")
        exit(1)

def resolve_host(subdomain):
    addrinfo = set()
    subdomain = subdomain.strip()
    try:
        addrinfo = socket.getaddrinfo(subdomain + "." + hostname, None)
    except socket.gaierror:
        pass
    except:
        print("unexpected error:", sys.exc_info()[1])
        
    return (subdomain + "." + hostname, set(map(lambda i: i[4][0], addrinfo)))
    
executor = ThreadPoolExecutor(max_workers=thread_no)

for result in executor.map(resolve_host, dictionary):
    if len(result[1]) > 0:
        print(result[0] + " => " + str(result[1]))
        if output_filename is not None:
            for ip in result[1]:
                output_writer.writerow([result[0], ip])
        
if output_filename is not None:
    output.close()
dictionary.close()
