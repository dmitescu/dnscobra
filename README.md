# Motivation

There's no script that performs DNS bruteforcing AND uses `getaddrinfo` such that torsocks may proxy
the DNS requests. In conclusion, to avoid DNS leaks, use this script instead.

In case there's a need for a dictionary, there are plenty (may I recommend the `dnsrecon` one?).

# Synopsis

```
./dnscobra.py --threads 3 -D dictionary.txt -o output.csv example.com
```
