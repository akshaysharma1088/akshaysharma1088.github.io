# Updating the site

- **Papers, talks, jobs, reviews, articles in other publications:** edit `data.json`. Each section is a list of placards (`research_cards`, `outlet_cards`, `speaking_cards`, `service_cards`): a card has `kind`, `name`, `meta`, `status`, optional `url` and `wide`, and `items` (title, url, note). A new HackerNoon article goes into the HackerNoon card's `items`. Then run `python3 scripts/build_static.py` so the static copy in `index.html` matches, and commit both files.
- **Newsletter issues:** nothing to do. A GitHub Action (`.github/workflows/update-newsletter.yml`) reads the Substack feed once a day and updates `posts.json`. To run it right away, open the repo's Actions tab, pick "Update newsletter posts" and click "Run workflow".
- **GitHub stars and forks** on the benchmark cards load live from GitHub's public API.
- `profile_pic.jpg` and `projects.html` stay as they are.
