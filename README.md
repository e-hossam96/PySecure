# PySecure

Packages Vulnerability Check for Python using OSS Index Public API from Sona Type.

## Overview

This package provides a simple way to scan Python dependencies for known security vulnerabilities. It leverages the [Sonatype OSS Index](https://ossindex.sonatype.org/) to retrieve vulnerability information.

## Features

- Check vulnerabilities in multiple Python packages at once.
- Support for authentication with Sonatype OSS Index API.
- Batch processing to handle large dependency lists.
- Environment variable configuration.
- Detailed vulnerability reports.

## Setup

- Clone the repository.

```bash
git clone https://github.com/e-hossam96/PySecure.git
```

- Install [UV](https://docs.astral.sh/uv/) using the following command.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Create the Python environment.

```bash
uv sync
```

## Usage

### Basic Example

- Create the packages json file in a file named `sample_packages.json` in the following format.

```json
[
    {
        "name": "transformers",
        "version": "4.51.2"
    }
]
```

- Run the script.

```bash
python main.py
```

### Using Environment Variables

Create a `.env` file with your Sonatype OSS Index credentials:

```text
OSSINDEX_API_USERNAME=your_username
OSSINDEX_API_TOKEN=your_token
```

### Command-line Usage

```bash
python main.py
```

This will read package information from `sample_packages.json` and write vulnerability data to `sample_packages_info.json`.

## Authentication

While the API can be used without authentication, it has rate limits. For higher limits:

1. Create an account at [OSS Index](https://ossindex.sonatype.org/)
2. Generate an API token in your account settings
3. Set the following environment variables:
   - `OSSINDEX_API_USERNAME`: Your OSS Index username
   - `OSSINDEX_API_TOKEN`: Your OSS Index API token

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
