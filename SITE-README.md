# Updating the site

- **Papers, talks, jobs, reviews, articles in other publications:** edit `data.json`, commit. The page updates on the next load. Add a published DZone or HackerNoon article to `articles` (title, url, outlet, date, summary).
- **Newsletter issues:** nothing to do. A GitHub Action (`.github/workflows/update-newsletter.yml`) reads the Substack feed once a day and updates `posts.json`. To run it right away, open the repo's Actions tab, pick "Update newsletter posts" and click "Run workflow".
- **GitHub stars and forks** on the benchmark cards load live from GitHub's public API.
- `profile_pic.jpg` and `projects.html` stay as they are.
