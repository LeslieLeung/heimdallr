from typing import Dict

from heimdallr.webhook.base import WebhookBase


class GithubStarWebhook(WebhookBase):
    def __init__(self, message: Dict):
        super().__init__(message)

    def parse(self) -> (str, str, str):
        action = self.message["action"]
        repo_name = self.message["repository"]["full_name"]
        from_user = self.message["sender"]["login"]
        stars = self.message["repository"]["stargazers_count"]
        title = f"Activity on {repo_name}"
        if action == "created":
            body = f"{from_user} starred {repo_name}\nStars: {stars}"
        elif action == "deleted":
            body = f"{from_user} removed star on {repo_name}\nStars: {stars}"
        else:
            body = f"{from_user} {action} {repo_name}\nStars: {stars}"
        jump_url = self.message["repository"]["html_url"]
        return title, body, jump_url
