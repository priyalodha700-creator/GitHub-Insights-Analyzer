# GitHub-Insights-Analyzer
A Python CLI tool that fetches any public GitHub user's profile and repository data via the GitHub REST API, then auto-generates a visual report (language distribution + top repos by stars) and a clean Markdown summary — great for portfolios and quick GitHub analytics.
# 📊 GitHub Insights Analyzer

A Python CLI tool that fetches **any public GitHub user's data** via the GitHub REST API and auto-generates:

- 🥧 A **visual report** (PNG) — language distribution pie chart + top repos by stars bar chart
- 📝 A clean **Markdown summary report** — followers, total stars, top languages, top repos table

Perfect for portfolios, resumes, or quickly analyzing any developer's public GitHub footprint — including your own!

---

## ✨ Features

- Works with **any GitHub username** — no login required for basic usage
- Auto-generates a polished **matplotlib chart** (language split + top starred repos)
- Auto-generates a **Markdown report** ready to paste into a README or portfolio
- Optional GitHub token support for higher API rate limits (60/hr → 5000/hr)
- Handles pagination automatically for users with 100+ repositories
- Clean error handling (invalid username, rate limit, etc.)

---

## 📸 Example Output

Running the tool on a username produces two files:

```
<username>_report.png   # Visual chart
<username>_report.md    # Markdown report
```

Sample Markdown report snippet:

```markdown
# GitHub Insights Report — @torvalds

## Summary
- Followers: 250000+
- Public Repos: 8
- Total Stars Earned: 200000+

## Top Languages
- C: 4 repo(s)
- Shell: 2 repo(s)

## Top Repositories
| Repo    | Stars  | Forks | Language |
|---------|--------|-------|----------|
| linux   | 190000 | 55000 | C        |
```

---

## 🚀 Installation

```bash
git clone https://github.com/<your-username>/github-insights-analyzer.git
cd github-insights-analyzer
pip install -r requirements.txt
```

---

## 🛠️ Usage

```bash
python src/github_analyzer.py <github_username>
```

**Example:**

```bash
python src/github_analyzer.py torvalds
```

### Using a GitHub token (recommended, optional)

Unauthenticated requests are limited to 60/hour. For higher limits (5000/hour), pass a
[personal access token](https://github.com/settings/tokens):

```bash
python src/github_analyzer.py torvalds --token ghp_xxxxxxxxxxxx
```

or set it as an environment variable:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
python src/github_analyzer.py torvalds
```

---

## 🧱 Project Structure

```
github-insights-analyzer/
├── src/
│   └── github_analyzer.py   # Main script (GitHubAnalyzer class + CLI)
├── requirements.txt
└── README.md
```

---

## 🔧 How It Works

1. `GitHubAnalyzer` calls the GitHub REST API (`/users/{username}` and `/users/{username}/repos`)
2. Repository data is aggregated: stars, forks, languages
3. `matplotlib` renders a two-panel chart (pie + bar)
4. A Markdown report is generated with tables and summary stats

---

## 🌱 Possible Extensions (great for making this project even more impressive)

- Add a **Flask/Streamlit web dashboard** instead of CLI
- Add **commit activity heatmap** using the Events API
- Compare **two GitHub users side-by-side**
- Auto-post the generated chart to your GitHub profile README (GitHub Actions + cron)
- Add **unit tests** with `pytest` and a CI workflow (`.github/workflows/test.yml`)

---

## 📄 License

MIT License — free to use and modify.

---

## 🙋 Why this project stands out

Most beginner GitHub projects are to-do lists or calculators. This one:
- Uses a **real, external REST API**
- Does actual **data analysis + visualization**
- Produces a **tangible, shareable artifact** (chart + report)
- Is easy to explain in an interview, and easy to extend (dashboard, GitHub Actions, etc.)
