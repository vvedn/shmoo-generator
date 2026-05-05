# AutoShmoo CI

Automatic generation of shmoo plots from hardware sweep reports, with full CI/CD integration.

<!-- CI Badge: replace YOUR_USERNAME/autoshmoo-ci with your actual GitHub path -->
![CI](https://github.com/vvedn/shmoo-generator/actions/workflows/ci.yml/badge.svg)

## What It Does

AutoShmoo reads `.rpt` files from hardware sweep tools, extracts voltage/frequency/pass-fail data, and generates:

- A summary table (CSV + Markdown)
- Shmoo plots (pass/fail by voltage vs. frequency)
- Power summary charts

Everything runs automatically in GitHub Actions on every push.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/vvedn/shmoo-generator.git
cd autoshmoo-ci

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the project and dev dependencies
pip install .[dev]

# Run the tool on sample data
python -m autoshmoo generate examples/sample_project/reports --out outputs

# Run tests
pytest
```

## Project Structure

```
autoshmoo-ci/
├── autoshmoo/          # Main Python package
│   ├── parser.py       # Parse .rpt files into records
│   ├── matcher.py      # Group records by signal generator
│   ├── plots.py        # Generate shmoo and power plots
├── examples/           # Sample report data for demos
├── tests/              # Unit tests (pytest)
├── outputs/            # Generated artifacts (gitignored except .gitkeep)
└── .github/workflows/  # CI pipeline
```

## Branching & PR Strategy


1. **`main`** branch is always stable and CI-passing.
2. **Feature branches** (e.g., `feat/siggen-random-results`) are created for each signal generator's code and sweep results.
3. When a feature branch is merged into `main` via pull request, the CI pipeline:
   - Runs linting and tests
   - Parses all report files
   - Generates shmoo plots
   - Uploads artifacts

**Example workflow:**

```bash
# Create a branch for new siggen results
git checkout -b feat/siggen-random-results

# Add report files and any parser updates
git add examples/sample_project/reports/siggen_random.rpt
git commit -m "feat(data): add siggen_random sweep results"

# Push and open a PR
git push -u origin feat/siggen-random-results
# Open PR on GitHub -> merge -> CI generates plots
```
`

## Requirements

- Python 3.11+
- pandas
- matplotlib
- tabulate
- pytest (dev)
- ruff (dev)
