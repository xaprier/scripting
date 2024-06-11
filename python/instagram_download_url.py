import argparse
from instaloader import Instaloader, Post
import re


def download_instagram_post(url_or_shortcode, target_folder):
    # Create an Instaloader instance
    L = Instaloader()

    # Extract the shortcode from the URL or shortcode
    shortcode_match = re.search(
        r"(?:https?://www.instagram.com/p/)?([A-Za-z0-9-_]{11})/?", url_or_shortcode
    )

    if not shortcode_match:
        print("Invalid URL or shortcode.")
        return

    shortcode = shortcode_match.group(1)

    # Create a Post instance
    post = Post.from_shortcode(L.context, shortcode)

    # Download the post
    L.download_post(post, target=target_folder)
    print(f"Post {shortcode} successfully downloaded.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download an Instagram post by URL or shortcode."
    )
    parser.add_argument(
        "url_or_shortcode", type=str, help="URL or shortcode of the Instagram post"
    )
    parser.add_argument(
        "target_folder", type=str, help="Folder to save the downloaded post"
    )

    args = parser.parse_args()

    download_instagram_post(args.url_or_shortcode, args.target_folder)
