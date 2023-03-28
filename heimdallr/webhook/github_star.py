from typing import Dict

from heimdallr.webhook.base import WebhookBase


class GithubStarWebhook(WebhookBase):
    def __init__(self, message: Dict):
        super().__init__(message)

    def parse(self) -> (str, str):
        action = self.message["action"]
        repo_name = self.message["repository"]["full_name"]
        from_user = self.message["sender"]["login"]
        stars = self.message["repository"]["stargazers_count"]
        if action == "created":
            title = f"{from_user} starred {repo_name}"
            body = f"Stars: {stars}"
        elif action == "deleted":
            title = f"{from_user} unstarred {repo_name}"
            body = f"Stars: {stars}"
        else:
            title = f"{from_user} {action} {repo_name}"
            body = f"Stars: {stars}"
        return title, body
