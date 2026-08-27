from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitStatusEntry:
    """A single file entry from `git status --porcelain`."""

    index_state: str
    worktree_state: str
    path: str


class GitUnavailableError(RuntimeError):
    """Raised when the git executable cannot be located."""


class NotAGitRepositoryError(RuntimeError):
    """Raised when an operation is attempted outside a Git repository."""


class IndustryGitRepository:
    """Read-only, subprocess-safe Git repository introspection utility.

    All operations are non-destructive: this class never commits, pushes,
    resets, cleans, or otherwise mutates repository state. Every Git
    invocation uses an explicit argument list (never `shell=True`) to avoid
    shell-injection risk.
    """

    def __init__(self, working_directory: Path | None = None) -> None:
        self.working_directory: Path = (working_directory or Path.cwd()).resolve()

    def _run_git(self, *args: str) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                ["git", *args],
                cwd=self.working_directory,
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as error:
            raise GitUnavailableError(
                "git executable was not found on PATH. Install Git to enable repository introspection."
            ) from error
        except subprocess.CalledProcessError as error:
            stderr = error.stderr.strip() if error.stderr else "unknown git error"
            raise NotAGitRepositoryError(
                f"git command failed in {self.working_directory}: {stderr}"
            ) from error

    def is_git_available(self) -> bool:
        try:
            subprocess.run(
                ["git", "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def is_repository(self) -> bool:
        if not self.is_git_available():
            return False
        try:
            result = self._run_git("rev-parse", "--is-inside-work-tree")
        except (GitUnavailableError, NotAGitRepositoryError):
            return False
        return result.stdout.strip() == "true"

    def repository_root(self) -> Path:
        result = self._run_git("rev-parse", "--show-toplevel")
        return Path(result.stdout.strip())

    def current_branch(self) -> str:
        result = self._run_git("rev-parse", "--abbrev-ref", "HEAD")
        return result.stdout.strip()

    def commit_hash(self, short: bool = False) -> str:
        args = ["rev-parse"]
        if short:
            args.append("--short")
        args.append("HEAD")
        result = self._run_git(*args)
        return result.stdout.strip()

    def remote_url(self, remote_name: str = "origin") -> str | None:
        try:
            result = self._run_git("remote", "get-url", remote_name)
        except NotAGitRepositoryError:
            return None
        return result.stdout.strip()

    def status(self) -> list[GitStatusEntry]:
        result = self._run_git("status", "--porcelain")
        entries: list[GitStatusEntry] = []
        for line in result.stdout.splitlines():
            if not line:
                continue
            index_state, worktree_state = line[0], line[1]
            path = line[3:]
            entries.append(GitStatusEntry(index_state, worktree_state, path))
        return entries

    def is_clean(self) -> bool:
        return len(self.status()) == 0

    def metadata_summary(self) -> dict[str, str | bool | None]:
        if not self.is_repository():
            return {"is_repository": False}
        return {
            "is_repository": True,
            "root": str(self.repository_root()),
            "branch": self.current_branch(),
            "commit": self.commit_hash(short=True),
            "remote": self.remote_url(),
            "clean": self.is_clean(),
        }

    @staticmethod
    def run() -> None:
        repository = IndustryGitRepository()
        if not repository.is_git_available():
            print("Git is not installed on this system.")
            return
        if not repository.is_repository():
            print(f"{repository.working_directory} is not inside a Git repository.")
            return
        for key, value in repository.metadata_summary().items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    IndustryGitRepository.run()
