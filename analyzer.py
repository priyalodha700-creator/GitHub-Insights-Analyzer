"""
GitHub Insights Analyzer
=========================
Fetches public data for any GitHub user/organization and generates:
  1. A visual report (language distribution + top repos by stars) as PNG
  2. A clean Markdown summary report

Author: You :)
"""

import os
import sys
import requests
from collections import Counter
from datetime import datetime

import matplotlib
matplotlib.use("Agg")  # no GUI backend needed
import matplotlib.pyplot as plt

API_BASE = "https://api.github.com"


class GitHubAnalyzer:
    def __init__(self, username: str, token: str | None = None):
        self.username = username
        self.session = requests.Session()
        headers = {"Accept": "application/vnd.github+json"}
        # Optional token -> higher rate limit (60/hr -> 5000/hr)
        token = token or os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.session.headers.update(headers)

        self.profile = {}
        self.repos = []

    # ---------- Data fetching ----------
    def fetch_profile(self):
        url = f"{API_BASE}/users/{self.username}"
        resp = self.session.get(url, timeout=15)
        self._check_response(resp)
        self.profile = resp.json()
        return self.profile

    def fetch_repos(self):
        repos = []
        page = 1
        while True:
            url = f"{API_BASE}/users/{self.username}/repos"
            params = {"per_page": 100, "page": page, "type": "owner", "sort": "updated"}
            resp = self.session.get(url, params=params, timeout=15)
            self._check_response(resp)
            batch = resp.json()
            if not batch:
                break
            repos.extend(batch)
            page += 1
        self.repos = [r for r in repos if not r.get("fork")]
        return self.repos

    @staticmethod
    def _check_response(resp):
        if resp.status_code == 404:
            print("Error: GitHub user not found.")
            sys.exit(1)
        if resp.status_code == 403:
            print("Error: GitHub API rate limit exceeded. "
                  "Set a GITHUB_TOKEN environment variable to raise the limit.")
            sys.exit(1)
        resp.raise_for_status()

    # ---------- Analysis ----------
    def language_distribution(self) -> Counter:
        return Counter(r["language"] for r in self.repos if r.get("language"))

    def top_repos_by_stars(self, n=5):
        return sorted(self.repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:n]

    def totals(self):
        return {
            "total_repos": len(self.repos),
            "total_stars": sum(r.get("stargazers_count", 0) for r in self.repos),
            "total_forks": sum(r.get("forks_count", 0) for r in self.repos),
            "total_watchers": sum(r.get("watchers_count", 0) for r in self.repos),
        }

    # ---------- Output ----------
    def generate_chart(self, output_path="github_report.png"):
        lang_counts = self.language_distribution()
        top_repos = self.top_repos_by_stars()

        fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

        # Pie chart: language distribution
        if lang_counts:
            labels, sizes = zip(*lang_counts.most_common(8))
            axes[0].pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90)
            axes[0].set_title("Language Distribution (by repo count)")
        else:
            axes[0].text(0.5, 0.5, "No language data", ha="center")
            axes[0].axis("off")

        # Bar chart: top repos by stars
        if top_repos:
            names = [r["name"] for r in top_repos]
            stars = [r.get("stargazers_count", 0) for r in top_repos]
            axes[1].barh(names[::-1], stars[::-1], color="#6e40c9")
            axes[1].set_xlabel("Stars")
            axes[1].set_title("Top Repositories by Stars")
        else:
            axes[1].text(0.5, 0.5, "No repos found", ha="center")
            axes[1].axis("off")

        fig.suptitle(f"GitHub Insights — @{self.username}", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close(fig)
        return output_path

    def generate_markdown_report(self, output_path="github_report.md"):
        totals = self.totals()
        lang_counts = self.language_distribution()
        top_repos = self.top_repos_by_stars()

        lines = []
        lines.append(f"# GitHub Insights Report — @{self.username}")
        lines.append(f"_Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")

        if self.profile.get("bio"):
            lines.append(f"> {self.profile['bio']}\n")

        lines.append("## Summary\n")
        lines.append(f"- **Followers:** {self.profile.get('followers', 0)}")
        lines.append(f"- **Following:** {self.profile.get('following', 0)}")
        lines.append(f"- **Public Repos:** {totals['total_repos']}")
        lines.append(f"- **Total Stars Earned:** {totals['total_stars']}")
        lines.append(f"- **Total Forks:** {totals['total_forks']}\n")

        lines.append("## Top Languages\n")
        for lang, count in lang_counts.most_common(8):
            lines.append(f"- {lang}: {count} repo(s)")

        lines.append("\n## Top Repositories\n")
        lines.append("| Repo | Stars | Forks | Language |")
        lines.append("|------|-------|-------|----------|")
        for r in top_repos:
            lines.append(
                f"| [{r['name']}]({r['html_url']}) | {r.get('stargazers_count', 0)} "
                f"| {r.get('forks_count', 0)} | {r.get('language') or '—'} |"
            )

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python github_analyzer.py <github_username> [--token TOKEN]")
        sys.exit(1)

    username = sys.argv[1]
    token = None
    if "--token" in sys.argv:
        token = sys.argv[sys.argv.index("--token") + 1]

    print(f"Fetching data for @{username} ...")
    analyzer = GitHubAnalyzer(username, token=token)
    analyzer.fetch_profile()
    analyzer.fetch_repos()

    chart_path = analyzer.generate_chart(f"{username}_report.png")
    md_path = analyzer.generate_markdown_report(f"{username}_report.md")

    print(f"Done!")
    print(f" - Chart saved to: {chart_path}")
    print(f" - Markdown report saved to: {md_path}")


if __name__ == "__main__":
    main()
