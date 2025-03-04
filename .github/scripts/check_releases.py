import requests
import json
from datetime import datetime, timedelta
from pathlib import Path


def get_latest_release():
    url = "https://api.github.com/repos/propromo-software/propromo.php/tags"
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y.%m.%d")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch tags: {response.status_code}")
        return None

    tags = response.json()

    # Get all tags from yesterday
    yesterday_tags = []
    for tag in tags:
        tag_name = tag["name"]
        # Check if tag starts with "v" followed by yesterday's date
        if tag_name.startswith(f"v{yesterday}."):
            try:
                # Extract the increment part
                increment = int(tag_name.split(".")[-1])
                yesterday_tags.append((tag_name, increment, tag))
            except (ValueError, IndexError):
                continue

    if not yesterday_tags:
        print(f"No tags found for {yesterday}")
        return None

    # Get the tag with highest increment
    latest_tag = max(yesterday_tags, key=lambda x: x[1])
    print(f"Found latest tag: {latest_tag[0]} with increment {latest_tag[1]}")
    return latest_tag[2]


def create_hugo_post(release_data):
    posts_dir = Path("content/posts")
    posts_dir.mkdir(parents=True, exist_ok=True)

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tag_name = release_data["name"]

    # Create a formatted date for the post front matter
    post_date = f"{yesterday}T12:00:00+00:00"

    post_file = posts_dir / f"release-{tag_name}.md"
    if post_file.exists():
        print(f"Post already exists for {tag_name}: {post_file}")
        return False

    # Save release data as JSON
    data_dir = Path("data/releases")
    data_dir.mkdir(parents=True, exist_ok=True)

    json_file = data_dir / f"{tag_name}.json"
    if not json_file.exists():
        with open(json_file, "w") as f:
            json.dump(release_data, f, indent=2)

    # Create Hugo post content
    post_content = f"""---
title: "Release {tag_name}"
date: {post_date}
tags: ["website"]
author: "Propromo"
showToc: true
TocOpen: false
draft: false
---

## New Release: {tag_name}

A new version of the Propromo website has been released!

### Release Details

- **Version**: {tag_name}
- **Release Date**: {yesterday}
- **Download URL**: [GitHub Release]({release_data['tarball_url']})
- **Release URL**: [GitHub Release](https://github.com/propromo-software/propromo.php/releases/tag/{tag_name})

For more information, visit the [Propromo GitHub repository](https://github.com/propromo-software/propromo.php).
"""

    with open(post_file, "w") as f:
        f.write(post_content)

    print(f"Created new post: {post_file}")
    return True


def main():
    latest_release = get_latest_release()
    if latest_release:
        post_created = create_hugo_post(latest_release)
        if post_created:
            print("Post successfully created")
        else:
            print("No new post created")


if __name__ == "__main__":
    main()
