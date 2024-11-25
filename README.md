# Address Hash Matcher Tool

A Python tool for secure address hashing and matching using RSA encryption. This tool provides two main functionalities:

1. Generate encrypted hashes for a list of addresses
2. Match original addresses against a list of encrypted hashes

## Features

- RSA encryption-based address hashing
- Command-line interface for easy usage
- CSV file support for input and output
- Persistent key storage
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

2. Install required dependencies:

```bash
pip install pycryptodome
```

## Usage

The tool provides two main commands: `hash` and `match`.

### File Format Requirements

All input CSV files should:

- Contain a header row
- Have only one column
- For addresses: column should contain the plain addresses
- For hashed addresses: column should contain the encrypted hashes

# Address Hash Matcher Tool

## Private Key Management

### Generating a Private Key

There are several ways to generate a private key:

1. **Using the Tool Automatically**

```bash
# The tool will automatically generate a private key if none is provided
python script.py hash -i addresses.csv -o hashed.csv
```

2. **Using OpenSSL (Recommended for Production)**

```bash
# Generate a 2048-bit RSA private key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Optional: Extract public key if needed
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

Key Management Tips:

- If no key file is specified, a new key pair will be generated for each run
- For consistent results across multiple runs, use the same key file
- Keep your private key secure and backed up
- The key file will be automatically created if it doesn't exist
- Recommended key size is 2048 bits or larger

### Command: Generate Hashed Addresses

Use this command to generate encrypted hashes for a list of addresses.

```bash
python script.py hash -i <input_file> -o <output_file> [-k <key_file>]
```

Parameters:

- `-i, --input`: Input CSV file containing addresses
- `-o, --output`: Output CSV file for hashed addresses
- `-k, --key`: (Optional) Private key file path

Example:

```bash
python script.py hash -i addresses.csv -o hashed_addresses.csv -k private_key.pem
```

### Command: Match Addresses with Hashes

Use this command to find matching addresses between an original address list and a hashed address list.

```bash
python script.py match -a <addresses_file> -s <hashed_file> -o <output_file> [-k <key_file>]
```

Parameters:

- `-a, --addresses`: CSV file with original addresses
- `-s, --hashed`: CSV file with hashed addresses
- `-o, --output`: Output CSV file for matched addresses
- `-k, --key`: (Optional) Private key file path

Example:

```bash
python script.py match -a original_addresses.csv -s hashed_addresses.csv -o matched_addresses.csv -k private_key.pem
```

### Private Key Management

- If no key file is specified, a new key pair will be generated for each run
- For consistent results across multiple runs, use the same key file
- Keep your private key secure and backed up
- The key file will be automatically created if it doesn't exist

## Example Files

### input_addresses.csv

```csv
address
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
```

### hashed_addresses.csv (output)

```csv
hashed_address
<base64_encoded_hash_1>
<base64_encoded_hash_2>
<base64_encoded_hash_3>
```

### matched_addresses.csv (output)

```csv
matched_address
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
0x64e5c44a6f1276ac2ff623ac54e63e5a61a576906b3ec427ac87fe8bf5615d2952
```
