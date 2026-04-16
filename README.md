# Repo Roast Machine

## Overview

Repo Roast Machine is a GitHub analysis tool that takes a username, pulls their public repository data, and converts it into a brutally honest AI-generated roast.

It is built on a simple principle: your GitHub history is a personality test you did not consent to.

---

## What it does

It analyzes a developer’s GitHub footprint using real data:

* Repository names (creative genius or “test123” syndrome)
* README quality (present, empty, or emotionally abandoned)
* Commit messages (professional or psychological breakdown)
* Activity timeline (consistent developer or seasonal coder)
* Language usage (polyglot engineer or one-language survival mode)
* Stars, forks, and engagement metrics

This structured data is sent to a language model which generates a contextual roast based entirely on observable behavior.

---

## Example output

“24 repositories detected. 18 of them are either called ‘final’, ‘final2’, or ‘final_really_final’. None of them are final.

Your commit history reads like a panic attack logged in Git form: ‘fix’, ‘fix bug’, ‘working now’, ‘pls don’t break’.

Your most recent activity is old enough to apply for historical classification.

At this point, your GitHub is not a portfolio. It is a digital graveyard of good intentions.”

---

## Why this exists

Most developer tools reward activity.

This one rewards honesty.

It highlights:

* Abandoned projects
* Inconsistent coding habits
* Placeholder repos that never evolved
* Commit messages that reveal emotional states

It turns GitHub into a behavioral mirror with commentary.

---

## Tech stack

* GitHub REST API for data extraction
* Python for backend processing
* OpenAI / Gemini API for roast generation
* Flask / Streamlit for UI
* HTML, CSS, JavaScript for frontend presentation

---

## System flow

1. User enters GitHub username
2. GitHub API fetches repository metadata
3. Data is cleaned and structured
4. Prompt is engineered with behavioral context
5. LLM generates roast response
6. UI displays output with dramatic formatting

---

## Environment variables

Create a `.env` file:

GITHUB_TOKEN=your_github_token
GEMINI_API_KEY=your_llm_api_key

Do not commit this file.

---

## Installation

git clone [https://github.com/Rucha-1111/Repo-Roast-Machine.git](https://github.com/Rucha-1111/Repo-Roast-Machine.git)
cd Repo-Roast-Machine
pip install -r requirements.txt
python app.py

---

## Security note

This project only uses public GitHub data.

However, API keys must never be exposed or pushed to GitHub.

If you did, the internet already judged you before this tool did.

---

## License

Educational use only.

Not responsible for:

* emotional damage
* sudden repository renaming
* existential developer crises
