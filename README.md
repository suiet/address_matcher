# Address Hash Matcher Tool

A Python tool for secure address hashing and matching using HMAC-SHA256. This tool provides two main functionalities:

1. Generate secure hashes for a list of addresses
2. Match original addresses against a list of hashed addresses

## Features

- HMAC-SHA256 based secure hashing
- Command-line interface for easy usage
- CSV file support for input and output
- Persistent secret key storage
- Error handling and logging
- Support for large address lists

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. Clone the repository or download the script:

```bash
git clone <repository-url>
# or download script.py directly
```

2. No additional dependencies required (uses Python standard library)

## Usage

The tool provides two main commands: `hash` and `match`.

### File Format Requirements

All input CSV files should:

- Contain a header row
- Have only one column
- For addresses: column should contain the plain addresses
- For hashed addresses: column should contain the hashed addresses

## Secret Key Management

The tool uses a secret key for generating secure hashes. There are several ways to provide the secret key:

1. **Using Command Line**

```bash
# Provide secret key directly
python script.py hash -i addresses.csv -o hashed.csv -k "your-secret-key"
```

2. **Using Automatic Key Management**

```bash
# The tool will automatically generate and save a secret key if none is provided
python script.py hash -i addresses.csv -o hashed.csv
```

Key Management Tips:

- If no key is specified, a random 32-byte key will be generated and saved to `secret.key`
- For consistent results across multiple runs, use the same secret key
- Keep your secret key secure and backed up
- The key file will be automatically created if it doesn't exist

### Command: Generate Hashed Addresses

Use this command to generate secure hashes for a list of addresses.

```bash
python script.py hash -i <input_file> -o <output_file> [-k <secret_key>]
```

Parameters:

- `-i, --input`: Input CSV file containing addresses
- `-o, --output`: Output CSV file for hashed addresses
- `-k, --key`: (Optional) Secret key string

Example:

```bash
python script.py hash -i addresses.csv -o hashed_addresses.csv -k "my-secret-key"
```

### Command: Match Addresses with Hashes

Use this command to find matching addresses between an original address list and a hashed address list.

```bash
python script.py match -a <addresses_file> -s <hashed_file> -o <output_file> [-k <secret_key>]
```

Parameters:

- `-a, --addresses`: CSV file with original addresses
- `-s, --hashed`: CSV file with hashed addresses
- `-o, --output`: Output CSV file for matched addresses
- `-k, --key`: (Optional) Secret key string

Example:

```bash
python script.py match -a original_addresses.csv -s hashed_addresses.csv -o matched_addresses.csv -k "my-secret-key"
```

## Example Files

### input_addresses.csv

```csv
address
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
```

### hashed_addresses.csv (output)

```csv
hashed_address
7f8b82ca2c9a8d89e6dfb4510916a72b4dfd0d8f8b7a84b831c0470e3b01a801
7f8b82ca2c9a8d89e6dfb4510916a72b4dfd0d8f8b7a84b831c0470e3b01a801
```

### matched_addresses.csv (output)

```csv
matched_address
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
```
