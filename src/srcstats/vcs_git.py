import git

import vcs

class GitVcsWrapper(vcs.VcsWrapper):
    def __init__(self, path):
        try:
            self.repo = git.Repo(path)
        except git.exc.InvalidGitRepositoryError:
            raise vcs.IncorrectVcsError()

    @property
    def head(self):
        return GitCommit(self.repo.heads.master.object)

class GitCommit(vcs.Commit):
    def __init__(self, object):
        self.object = object

    @property
    def summary(self):
        return self.object.summary

    @property
    def parent(self):
        if self.object.parents:
            return GitCommit(self.object.parents[0])
        return None

    @property
    def file_iter(self):
        for blob in self._traverse_tree(self.object.tree):
            yield GitFile(blob)

    def _traverse_tree(self, tree):
        for blob in tree.blobs:
            yield blob

        for tree in tree.trees:
            for blob in self._traverse_tree(tree):
                yield blob

class GitFile(vcs.File):
    def __init__(self, blob):
        self.blob = blob

    @property
    def path(self):
        return self.blob.path

    @property
    def stream(self):
        return self.blob.data_stream
