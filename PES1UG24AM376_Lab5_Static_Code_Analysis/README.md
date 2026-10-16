# PES1UG24AM376 Lab 5 – Static Code Analysis

Script analysed: `student_grade_system.py`

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.51/10 | 10.00/10 |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | 0 issues |
| Flake8 | 8 issues | 0 issues |

Reports: `*_report_before.txt` and `*_report_after.txt`.

## Issues found and fixed

| Issue | Tool / Code | Line(s) | Description | Fix Approach |
|-------|-------------|---------|-------------|--------------|
| Shell injection | Bandit B605 (High) | 60 | `os.system("echo ... " + filename)` runs a shell with user-controlled input | Replaced with `print()` |
| Weak hash | Bandit B324 (High) | 49 | `hashlib.md5` is cryptographically broken | Switched to `hashlib.sha256` |
| Use of eval | Bandit B307 (Medium), Pylint W0123 | 44 | `eval(gpa_expr)` can execute arbitrary code | Replaced with plain arithmetic `avg_score / scale` |
| Insecure random | Bandit B311 (Low) | 53 | `random.randint` is not suitable for PINs | Used `secrets.randbelow` |
| Hardcoded secret | Bandit B105 (Low) | 64 | Portal token hardcoded in source | Read from `PORTAL_TOKEN` environment variable |
| Try/except/pass | Bandit B110, Pylint W0702, Flake8 E722 | 26 | Bare `except: pass` silently hides all errors | Catch `KeyError` only, report it and return `False` |
| Mutable default arg | Pylint W0102 | 15 | `grade_list=[]` shared across calls | Default to `None` and initialise inside the function |
| Unused import | Pylint W0611, Flake8 F401 | 6 | `json` imported but never used | Removed import |
| Unused variables | Pylint W0612, Flake8 F841 | 31, 43 | `grace_marks`, `avg_score` assigned but never used | Removed / used in the GPA calculation |
| None comparison | Pylint C0121, Flake8 E711 | 32 | `== None` instead of `is None` | Changed to `is None` |
| Line too long | Flake8 E501 | 19, 34 | Lines over 79 characters | Split into shorter lines |
| Missing final newline | Pylint C0304, Flake8 W292 | 75 | File did not end with a newline | Added final newline |
| Unsafe file handling | Pylint R1732, W1514 | 57 | `open()` without `with` or encoding | Used `with open(..., encoding="utf-8")` |
| Naming / docstrings / style | Pylint C0103, C0116, C0209, R1703, R1705 | various | `addGrade` not snake_case, missing docstrings, `%` formatting, redundant if/else | Renamed to `add_grade`, added docstrings, used f-string, `return avg >= threshold` |

## Commits

1. Original script and before reports
2. Bandit fixes
3. Flake8 fixes
4. Pylint fixes
5. After reports and this table
