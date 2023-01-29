import os
import json
from datetime import datetime

data = json.load(open("outbox.json"))

# Copy media files into /static/{instance} where {instance} is:
instance = "mastodon.social"

# Output directory for markdownfiles:
out_dir = "toots"
os.makedirs(out_dir, exist_ok=True)

for post in data["orderedItems"]:

    # Ignore boosts, which are type "Announce"
    if post["type"] == "Create":

        toot_url = post["object"]["id"]
        date = post['published']  # 2018-09-17T13:53:48Z

        date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        title_format = "%a %d %b %Y %H:%M"
        title = date_object.strftime(title_format)

        in_reply_to_url = post["object"]["inReplyTo"]

        # boosts just have the original post URL as content
        if type(post["object"]) == str:
            content = post["object"]
        else:
            content = post["object"]["content"]

         # Filename example: 2006-12-12-tweet-996943.md
        parts = toot_url.split('/')
        id = parts[-1]
        ymd = date_object.strftime("%Y-%m-%d")
        filename = f"{out_dir}/{ymd}-toot-{id}.md"

        with open(filename, "w") as file:

            file.write("---\n")
            file.write(f"title: {title}\n")
            file.write(f"instance: {instance}\n")
            file.write(f"toot_url: {toot_url}\n")
            file.write(f"date: {date}\n")
            file.write("---\n")
            file.write("\n")

            if in_reply_to_url:
                parts = in_reply_to_url.split('/')
                name = parts[4]
                file.write(f"In reply to [{name}]({in_reply_to_url}):\n\n")

            file.write(content)
            file.write("\n\n")

            atts = post['object']['attachment']
            for att in atts:
                name = att['name']
                media_path = att['url']
                media_type = att['mediaType']
                full_media_path = f"/{instance}/{media_path}"
                
                if "video" in media_type:
                    w = att['width']
                    h = att['height']
                    file.write(f"<video width='{w}' height='{h}' controls>\n")
                    file.write(f"<source src='{full_media_path}' type='{media_type}'>\n")
                    file.write(f"</video>\n")
                else:
                    file.write(f"![{name}]({full_media_path})\n\n")

