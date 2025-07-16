
# UserSpectre - Username Recon Tool

![UserSpectre](https://img.shields.io/badge/python-3.6%2B-blue)
![Threads](https://img.shields.io/badge/threads-25-green)

UserSpectre is a fast and concurrent username reconnaissance tool written in Python. It checks the availability or presence of a username across multiple websites, saving the results for further analysis.

---

## Features

- Concurrent scanning with configurable thread count
- Supports multiple site configuration JSON files
- Color-coded terminal output (using `colorama`)
- Saves results in JSON and TXT formats under a `scan` directory
- Can be run standalone or invoked programmatically from another Python script

---

## Requirements

- Python 3.6 or higher  
- Dependencies:
  
  A `requirements.txt` file is included for easy installation of dependencies. To install all required packages, run:

  ```bash
  pip install -r requirements.txt
```

* The `requirements.txt` should contain:

  ```
  requests
  colorama
  ```

---

## Usage

### Run standalone

```bash
python3 UserSpectre.py --username <username> --sites sites.json --workers 25
```

* `--username` — Username to search (prompts if not given)
* `--sites` — One or more JSON files with site URLs (default: `sites.json`)
* `--workers` — Number of concurrent threads (default: 25)

### Run via start script

Edit `start.py` to set parameters:

```python
from UserSpectre import main

if __name__ == "__main__":
    username = "exampleuser"
    sites_files = ["sites.json"]
    workers = 25

    main(username, sites_files, workers)
```

Then run:

```bash
python3 start.py
```

---

## Sites JSON Format

Each site entry should have:

* `name`: Friendly site name
* `url`: URL with `{}` as placeholder for the username
* Optional `error_type`: `"status_code"` or `"keyword"`
* Optional `error_msg`: Keyword indicating username absence if `error_type` is `"keyword"`

Example `sites.json`:

```json
[
  {
    "name": "GitHub",
    "url": "https://github.com/{}",
    "error_type": "status_code"
  },
  {
    "name": "Twitter",
    "url": "https://twitter.com/{}",
    "error_type": "keyword",
    "error_msg": "page not found"
  }
]
```

---

## Output

* Results saved in the `scan/` directory as:

  * `<username>_result.json` — JSON summary of found usernames
  * `<username>_result.txt` — Plain text summary of found usernames

* Console output colors:

  * **Green**: Username found
  * **Red**: Username not found
  * **Yellow**: Errors (timeouts, connection issues)

---



## 💰 Donations

Support the project with Bitcoin donations:

```
bc1qlpw590fkykfdd9v92g9snfmx8hc8vwxvkz5npm
```




## Contributing

Feel free to open issues or submit pull requests.
Ensure contributions follow ethical and legal guidelines.

---

## License

This project is for educational and authorized security testing only.
Do not use for unauthorized scanning or attacks.

---

*Happy Reconnaissance!*

```

---

If you want, I can also help you generate the actual `requirements.txt` file content or anything else!
```
