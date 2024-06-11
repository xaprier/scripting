from instaloader import Instaloader, Profile

L = Instaloader()
PROFILE = "ringwitdahoodie"
profile = Profile.from_username(L.context, PROFILE)

posts_sorted_by_likes = sorted(
    profile.get_posts(), key=lambda post: post.likes, reverse=True
)

for post in posts_sorted_by_likes:
    L.download_post(post, PROFILE)
