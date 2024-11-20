# REXON
> An AI-powered reconnaissance tool that transforms natural language into powerful security commands. Streamline your recon workflow with intelligent automation and command generation.

Rexon is a command-line tool that helps security researchers and penetration testers automate their reconnaissance workflow using natural language processing.

## Features

- Natural language to command translation
- Single and multiple domain reconnaissance
- File processing with AI-powered filtering
- Built-in tool dependency checker
- Interactive CLI interface

## Installation

# Clone the repository
git clone https://github.com/rabbyt3s/Rexon.git

# Navigate to the directory
cd rexon

# Install dependencies
pip install -r requirements.txt

# Configure your environment
cp .env.example .env
# Edit .env with your API keys

## Usage

python app.py

### Basic Commands
- Single domain reconnaissance:
  example.com > Find all subdomains and check for alive hosts
  
- Process existing files:
  urls.txt > Extract all endpoints containing /api/

## Configuration

Create a `.env` file with the following variables:
OPENAI_API_KEY=your_key_here

## Requirements

- Python 3.8+
- GEMINI API key
- Common reconnaissance tools:
  - subfinder - Subdomain discovery tool
  - httpx - HTTP toolkit
  - nuclei - Vulnerability scanner
  - amass - Network mapping
  - naabu - Port scanner
  - waybackurls - Historical URL discovery
  - gau - Get All URLs
  - katana - Web crawler
  - ffuf - Web fuzzer
  - anew - Unique line filter

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Rabbytes** - [@Rabbyt3s](https://twitter.com/Rabbyt3s)
