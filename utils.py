#utils.py

import requests
import os
from dotenv import load_dotenv
from groq import Groq
from collections import Counter

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {GITHUB_TOKEN}"}


# -----------------------------
# FETCH GITHUB DATA
# -----------------------------
def fetch_github_data(username):
    url = f"https://api.github.com/users/{username}/repos"
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return None

    repos = res.json()
    data = []

    for repo in repos:
        repo_name = repo["name"]

        repo_data = {
            "name": repo_name,
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "description": repo["description"],
            "has_readme": False,
            "commits": []
        }

        # README check
        r = requests.get(
            f"https://api.github.com/repos/{username}/{repo_name}/readme",
            headers=headers
        )
        repo_data["has_readme"] = r.status_code == 200

        # commits
        c = requests.get(
            f"https://api.github.com/repos/{username}/{repo_name}/commits",
            headers=headers
        )

        if c.status_code == 200:
            commits = []
            for commit in c.json()[:10]:
                msg = commit["commit"]["message"].lower().strip()
                commits.append(msg)
            repo_data["commits"] = commits

        data.append(repo_data)

    return data


# -----------------------------
# BUILD INTELLIGENT SUMMARY
# -----------------------------
def build_summary(username, data):
    all_commits = []
    language_counter = Counter()
    repo_names = []
    empty_or_dead_repos = 0
    no_readme = 0

    summary = f"""
USER: {username}
TOTAL REPOSITORIES: {len(data)}

REPOSITORY BREAKDOWN:
"""

    for r in data:
        repo_names.append(r["name"])

        if not r["commits"]:
            empty_or_dead_repos += 1

        if not r["has_readme"]:
            no_readme += 1

        lang = r["language"] or "Unknown"
        language_counter[lang] += 1

        all_commits.extend(r["commits"])

        summary += f"""
- Repo: {r['name']}
  Stars: {r['stars']}
  Language: {lang}
  README: {r['has_readme']}
  Commits: {r['commits']}
"""

    # commit pattern analysis
    commit_patterns = Counter(all_commits).most_common(10)

    summary += f"""

GLOBAL SIGNALS:
- Total commits analyzed: {len(all_commits)}
- Empty or dead repos: {empty_or_dead_repos}
- Repos without README: {no_readme}

MOST COMMON COMMIT MESSAGES:
{commit_patterns}

LANGUAGE DISTRIBUTION:
{dict(language_counter)}

REPO NAMES SAMPLE:
{repo_names[:10]}
"""

    return summary


def get_user_stats(username, data):
    # Fetch user profile for followers
    user_url = f"https://api.github.com/users/{username}"
    user_res = requests.get(user_url, headers=headers)
    followers = 0
    following = 0
    if user_res.status_code == 200:
        user_info = user_res.json()
        followers = user_info.get('followers', 0)
        following = user_info.get('following', 0)

    # Compute detailed from data
    all_commits = []
    empty_repos = 0
    no_readme_repos = 0
    total_stars = 0
    langs = Counter()
    for repo in data:
        if not repo["commits"]:
            empty_repos += 1
        if not repo["has_readme"]:
            no_readme_repos += 1
        total_stars += repo["stars"]
        lang = repo["language"] or "Unknown"
        langs[lang] += 1
        all_commits.extend(repo["commits"])

    total_repos = len(data)
    total_commits = len(all_commits)
    commit_patterns = Counter(all_commits).most_common(5)
    primary_lang = langs.most_common(1)[0][0] if langs else "None"
    readme_pct = round((1 - no_readme_repos / total_repos) * 100, 1) if total_repos else 0

    # Professional conclusion + improvements
    analysis = []
    improvements = []

    if total_repos < 5:
        analysis.append("Low repository count limits visibility.")
        improvements.append("Start 2-3 focused projects to build portfolio.")
    if empty_repos / total_repos > 0.5:
        analysis.append("High empty repos suggest abandoned projects.")
        improvements.append("Archive inactive repos or add MVP code.")
    if no_readme_repos / total_repos > 0.5:
        analysis.append(f"Only {readme_pct}% repos have READMEs.")
        improvements.append("Add README to all repos - boosts stars 20-30%.")
    if total_commits < 50:
        analysis.append("Low commit volume indicates infrequent activity.")
        improvements.append("Aim for 3-5 commits/week on active projects.")
    if 'fix' in str(commit_patterns).lower() and commit_patterns[0][1] > total_commits * 0.25:
        analysis.append("Reactive coding (fixes dominate commits).")
        analysis.append("Shift to TDD or planning for fewer bugs.")
    follower_ratio = followers / max(following, 1)
    if follower_ratio < 0.5:
        analysis.append(f"Follower ratio {follower_ratio:.1f}x suggests outbound networking.")
        improvements.append("Engage in issues/PRs, share on X/Reddit.")

    conclusion = " ".join(analysis[:3]) if analysis else "Solid GitHub presence - room for polish."

    tips = " | ".join(improvements[:3]) if improvements else "Maintain momentum, focus on quality."

    return {
        "total_repos": total_repos,
        "total_commits": total_commits,
        "followers": followers,
        "following": following,
        "total_stars": total_stars,
        "readme_pct": readme_pct,
        "primary_lang": primary_lang,
        "commit_patterns": [f"{pat[0]} ({pat[1]}x)" for pat in commit_patterns],
        "analysis": analysis,
        "improvements": improvements,
        "conclusion": conclusion,
        "tips": tips
    }


def generate_roast_original(data, username):
    if not data:
        return "User not found."

    summary = build_summary(username, data)

    prompt = f"""
Roast this GitHub profile brutally in a funny, savage, meme-like way.

Use ALL the data provided. Do NOT ignore commit patterns, repo behavior, or languages.

Rules:
- ONLY English
- No headings or structured report format
- Mix real data + insults in every sentence
- Be extremely funny and disrespectful (comedy roast style)
- Make it feel like you're stalking their GitHub and judging their entire life

You MUST incorporate:
- repo count behavior
- empty / dead repos
- commit message patterns
- language obsession or confusion
- README laziness
- naming style of repos

DATA:
{summary}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a savage, funny GitHub roast comedian who uses real data to insult developers in a hilarious way."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1.1,
            max_tokens=1200
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return str(e)


def generate_roast(data, username):
    if not data:
        return {"roast": "User not found.", "summary": {}}

    roast_text = generate_roast_original(data, username)
    stats = get_user_stats(username, data)
    return {"roast": roast_text, "summary": stats}
