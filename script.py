import csv
import hashlib
import hmac
import os
import argparse
import sys


class AddressHashMatcher:
    def __init__(self, secret_key: str = None):
        """
        Initialize address matcher with secret key
        Args:
            secret_key: Secret key string for HMAC. If not provided, will read from file or generate new one
        """
        if secret_key:
            self.secret_key = secret_key.encode()
        else:
            key_file = 'secret.key'
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    self.secret_key = f.read()
                print(f"Loaded existing secret key from: {key_file}")
            else:
                # Generate a random 32-byte key
                self.secret_key = os.urandom(32)
                with open(key_file, 'wb') as f:
                    f.write(self.secret_key)
                print(f"Generated and saved new secret key to: {key_file}")

    def _hash_address(self, address: str) -> str:
        """
        Hash address using HMAC-SHA256 with secret key
        Args:
            address: Original address to be hashed
        Returns:
            HMAC hash of the address
        """
        try:
            hmac_obj = hmac.new(self.secret_key, 
                              address.encode(), 
                              hashlib.sha256)
            return hmac_obj.hexdigest()
        except Exception as e:
            print(f"Error hashing address {address}: {str(e)}")
            return None

    def _verify_hash(self, address: str, hashed_address: str) -> bool:
        """
        Verify if address matches with its HMAC hash
        Args:
            address: Original address
            hashed_address: HMAC hash of the address
        Returns:
            Boolean indicating if the pair matches
        """
        try:
            current_hash = self._hash_address(address)
            return current_hash == hashed_address
        except Exception as e:
            print(f"Error verifying hash for address {address}: {str(e)}")
            return False

    def process_addresses(self, input_file: str, output_file: str):
        """
        Process address list and generate corresponding hashes
        Args:
            input_file: Input CSV file path (containing address column)
            output_file: Output CSV file path (will contain hashed_address column)
        """
        try:
            with open(input_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out:
                reader = csv.reader(f_in)
                writer = csv.writer(f_out)

                # Write header
                writer.writerow(['hashed_address'])

                # Skip header row
                next(reader)

                # Process each address
                for row in reader:
                    if row:  # Ensure row is not empty
                        address = row[0]
                        hashed = self._hash_address(address)
                        if hashed:
                            writer.writerow([hashed])

            print(f"Successfully processed addresses and saved to {output_file}")

        except Exception as e:
            print(f"Error processing addresses: {str(e)}")
            sys.exit(1)

    def match_addresses(self, addresses_file: str, hashed_file: str, output_file: str):
        """
        Match address and hash lists to find overlapping addresses
        Args:
            addresses_file: Path to original addresses CSV file
            hashed_file: Path to hashed addresses CSV file
            output_file: Path to output CSV file for matched addresses
        """
        try:
            # Read original addresses
            with open(addresses_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                addresses = [row[0] for row in reader if row]
                print(f"Loaded {len(addresses)} addresses from {addresses_file}")
            # Read hashed addresses
            with open(hashed_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                hashed_addresses = [row[0] for row in reader if row]
                print(f"Loaded {len(hashed_addresses)} hashed addresses from {hashed_file}")
            # Find matches and write to output
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['matched_address'])
                matched_addresses_count = 0
                for address in addresses:
                    current_hash = self._hash_address(address)
                    if current_hash in hashed_addresses:
                        matched_addresses_count += 1
                        writer.writerow([address])

            print(f"Successfully matched {matched_addresses_count} addresses and saved to {output_file}")

        except Exception as e:
            print(f"Error matching addresses: {str(e)}")
            sys.exit(1)


def setup_argparse():
    """
    Set up command line argument parser
    """
    parser = argparse.ArgumentParser(description='Address Hash Matcher Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Parser for hash generation
    hash_parser = subparsers.add_parser('hash', help='Generate hashed addresses')
    hash_parser.add_argument('-i', '--input', required=True, help='Input CSV file with addresses')
    hash_parser.add_argument('-o', '--output', required=True, help='Output CSV file for hashed addresses')
    hash_parser.add_argument('-k', '--key', help='Secret key string (optional)')

    # Parser for address matching
    match_parser = subparsers.add_parser('match', help='Match addresses with hashed addresses')
    match_parser.add_argument('-a', '--addresses', required=True, help='CSV file with original addresses')
    match_parser.add_argument('-s', '--hashed', required=True, help='CSV file with hashed addresses')
    match_parser.add_argument('-o', '--output', required=True, help='Output CSV file for matched addresses')
    match_parser.add_argument('-k', '--key', help='Secret key string (optional)')

    return parser


def main():
    """
    Main entry point for the CLI
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize matcher with provided key file (if any)
    matcher = AddressHashMatcher(args.key)

    try:
        if args.command == 'hash':
            matcher.process_addresses(args.input, args.output)
        elif args.command == 'match':
            matcher.match_addresses(args.addresses, args.hashed, args.output)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()