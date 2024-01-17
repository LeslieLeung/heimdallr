from typing import Dict

from heimdallr.config.config import get_config_list
from heimdallr.config.definition import ENABLED_GROUPS
from heimdallr.exception.auth import AuthException
from heimdallr.group.group import Group


class Config:
    token_to_group_map: Dict[str, Group] = {}

    def __init__(self) -> None:
        # get enabled groups
        enabled_groups = get_config_list(ENABLED_GROUPS, "", [])

        for name in enabled_groups:
            group = Group(name)
            self.token_to_group_map[group.token] = group

    def get_group(self, token: str) -> Group:
        if token not in self.token_to_group_map:
            raise AuthException("key is invalid")
        group = self.token_to_group_map[token]
        group.activate()
        return group


config = Config()
