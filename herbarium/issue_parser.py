from dataclasses import dataclass
from typing import Protocol

from .issue_service import Issue
from .parse_issue_title import sanitise_text_for_bash


@dataclass(frozen=True)
class IssueInfo:
    branch_title: str
    first_commit_str: str


class IssueParser(Protocol):
    def get_issue_info(self, issue: Issue) -> IssueInfo:
        ...


class DefaultIssueParser(IssueParser):
    def get_issue_info(self, issue: Issue) -> IssueInfo:
        branch_title = self._get_branch_title(issue=issue)
        first_commit_str = self._get_first_commit_str(issue=issue)

        return IssueInfo(branch_title=branch_title, first_commit_str=first_commit_str)

    def _get_branch_title(self, issue: Issue) -> str:
        entity_id_section = "" if issue.entity_id is None else f"/{issue.entity_id}"
        return f"{issue.prefix}{entity_id_section}/{issue.description}"

    def _get_first_commit_str(self, issue: Issue) -> str:
        if issue.entity_id is None:
            first_commit_str = f"{issue.prefix}: {issue.description}"
        else:
            first_commit_str = f"""{issue.prefix}(#{issue.entity_id}): {issue.description}

Fixes #{issue.entity_id}"""

        return sanitise_text_for_bash(first_commit_str)
