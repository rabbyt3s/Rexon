import os
import google.generativeai as genai
from dotenv import load_dotenv 
from rich.console import Console

console = Console()

class CommandGenerator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandGenerator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        try:
            load_dotenv()
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        except KeyError:
            console.print("[error][-][/error] GEMINI_API_KEY not found in .env file")
            raise

        self.available_tools = {
            "subfinder": "Tool for discovering subdomains",
            "httpx": "Tool for HTTP/HTTPS probe and analyzer",
            "nuclei": "Vulnerability scanner",
            "naabu": "Port scanner",
            "katana": "Web crawler and spider",
            "gau": "Get All URLs from AlienVault, Wayback, Common Crawl",
            "grep": "Filter output using patterns",
            "sort": "Sort and remove duplicates with -u",
            "tee": "Save output to file while displaying it",
            "awk": "Text processing and pattern scanning",
            "sed": "Stream editor for text manipulation",
            "anew": "Append lines to a file if they don't exist",
            "uniq": "Remove duplicate lines",
            "cut": "Remove sections from lines of files",
            "tr": "Translate or delete characters",
            "wget": "Download files from the web",
            "curl": "Transfer data from/to servers",
            "ffuf": "Web fuzzer for content discovery",
            "feroxbuster": "Fast content discovery tool",
            "gobuster": "Directory/file & DNS busting tool",
            "dirsearch": "Web path scanner",
            "arjun": "HTTP parameter discovery suite",
            "binwalk": "Firmware analysis tool",
            "exiftool": "Read and write meta information",
            "strings": "Extract readable characters from files",
            "file": "Determine file type",
            "jq": "JSON processor and filter",
            "yq": "YAML/XML processor and filter",
        }

        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }

        # Initialize model only when needed
        self._model = None
        self._initialized = True

    @property
    def model(self):
        if self._model is None:
            self._model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-002",
                generation_config=self.generation_config,
            )
        return self._model
    
    def reformulate_query_with_gemini(self, query: str) -> str:
        try:
            chat = self.model.start_chat(history=[
                {"role": "user", "parts": [f"Reformulate this query for clarity in the context of web security reconnaissance: {query}"]},
                {"role": "model", "parts": ["Provide only the reformulated query, raw, without any explanation."]},
            ])

            response = chat.send_message(query)
            return response.text.strip()

        except Exception as e:
            console.print(f"[error][-][/error] Error reformulating query: {str(e)}")
            return query  

    def generate_command(self, query: str, target: str) -> str:
        try:
            query = self.reformulate_query_with_gemini(query)

            chat = self.model.start_chat(history=[
                {"role": "user", "parts": [self.initial_context]},
                {"role": "model", "parts": ["I will generate only raw commands using the available tools."]}
            ])

            prompt = f"Generate a command to {query} for the target {target}. Use the most appropriate tools for web security reconnaissance."
            response = chat.send_message(prompt)

            return response.text.strip()

        except Exception as e:
            console.print(f"[error][-][/error] Error generating command: {str(e)}")
            return None

    def process_file(self, query: str, file_path: str) -> str:
        try:
            chat = self.model.start_chat(history=[
                {"role": "user", "parts": [self.initial_context]},
                {"role": "model", "parts": ["I will generate only raw commands using the available tools."]}
            ])

            prompt = f"Generate a command to {query} using the file {file_path}"
            response = chat.send_message(prompt)

            return response.text.strip()

        except Exception as e:
            console.print(f"[error][-][/error] Error processing file: {str(e)}")
            return None

    @property
    def initial_context(self):
        return """You are a **command generator**. **Output ONLY the raw command**, nothing else. **ALWAYS save results in the `output/` directory**—this is mandatory for every command. **Do NOT include any commands to create directories** (e.g., `mkdir`). **Use ONLY these tools with their correct flags**:

- **sqlmap**: `-u` for URL, `--batch` for non-interactive mode, `--dbs` to enumerate databases
- **subfinder**: `-d` for domain, `-silent` for clean output, `-all` for all sources
- **httpx**: `-silent`, `-sc`, `-title`
- **nuclei**: `-t` for templates, `-target` for single target
- **naabu**: `-host` for target, `-p` for ports
- **katana**: `-u` for URL
- **gau**: (just domain)
- **grep**: `-i` for case insensitive, `-E` for regex, `-F` for fixed strings
- **sort**: `-u` for unique
- **tee**: (just filename, **MUST be in `output/` directory)
- **sed**: (standard syntax)
- **anew**: (just filename in `output/` directory, no flags)
- **uniq**: (no special flags needed)
- **cut**: `-d` for delimiter, `-f` for fields
- **tr**: (standard syntax)

**Additional Tools (if needed):**
- **wget**: `-q` for quiet, `-O` for output file
- **curl**: `-sL` for silent and location, `-o` for output file
- **jq**: For JSON processing
- **ffuf**: `-u` for URL, `-w` for wordlist
- **feroxbuster**: `-u` for URL, `-w` for wordlist
- **gobuster**: `dir` mode with `-u` for URL and `-w` for wordlist
- **arjun**: `-u` for URL, `-t` for threads
- **binwalk**: `-e` for extraction
- **exiftool**: For metadata extraction
- **strings**: For searching strings in binary files

**Guidelines:**

1. **All pipeline outputs must be directed to the `output/` directory using `tee`.**
2. **Use `awk '/200/ {print $1}'` for filtering status codes instead of `grep -F '[200]'` to avoid escaping issues.**
3. **Commands should be syntactically correct and executable without errors.**
4. **Do NOT include any commands to create the `output/` directory. Assume it already exists.**
5. **When the query asks for URLs/links and does not explicitly mention subdomains, it means archived links using `gau`. You can combine both, like "archived links of subdomains", etc.**

**Examples (note how ALL results MUST go to `output/`):**

# Extract URLs with parameters for SQL injection or XSS testing
grep -E '\?.*=[^&]*(?:&.*=[^&]*)*' output/example.txt | tee output/injectable_parameters.txt

# SQL Injection Testing
sqlmap -u "http://example.com/page?param=value" --batch --dbs | tee output/sql_injection_results.txt

# Links gathering
gau domain.com | tee output/links.txt

# Basic enumeration
subfinder -d domain.com -silent | httpx -silent -sc -title | tee output/results.txt
gau domain.com | grep -i api | sort -u | tee output/api_endpoints.txt
subfinder -d domain.com -silent | tee output/subdomains.txt

# Status code filtering using awk
subfinder -d domain.com -silent -all | httpx -silent -sc -title | awk '/200/ {print $1}' | tee output/domain_live_domains.txt

# Status code filtering with titles
subfinder -d acme.com -silent -all | httpx -silent -sc -title | awk '/200/ {print $1","substr($0, index($0,$3))}' | tee output/acme_200.txt

# Another status code example
httpx -silent -sc -title -l domains.txt | awk '/403/ {print $1}' | tee output/forbidden.txt

# File downloads
wget -q https://target.com/file.pdf -O output/downloaded.pdf
curl -sL https://api.target.com | jq '.data' | tee output/api_data.txt

# Content discovery
ffuf -u https://target.com/FUZZ -w wordlist.txt | tee output/dirs.txt
feroxbuster -u https://target.com -w wordlist.txt | tee output/ferox_results.txt
gobuster dir -u https://target.com -w wordlist.txt | tee output/gobuster_results.txt

# Parameter discovery
arjun -u https://target.com -t 10 | tee output/params.txt

# File analysis
binwalk -e firmware.bin | tee output/binwalk_results.txt
exiftool image.jpg | tee output/metadata.txt
strings binary_file | grep -i "api_key" | tee output/strings_results.txt

# Multiple tools combination
subfinder -d domain.com -silent | httpx -silent | nuclei -t cves/ -target - | tee output/vulns.txt
naabu -host domain.com -p 80,443,8080,8443 | httpx -silent | tee output/open_ports.txt
"""
