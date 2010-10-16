class IncorrectVcsError(RuntimeError):
    pass

class VcsWrapper(object):
    """A class for abstracting certain operations in different version
    control systems."""

    @staticmethod
    def vcs_for_path(path):
        import vcs_git

        vcs_list = [vcs_git.GitVcsWrapper]

        for vcs in vcs_list:
            try:
                return vcs(path)
            except IncorrectVcsError:
                continue

        return None
    
    def __init__(self, path):
        """Initializes a VCS from a given path.

        Raises IncorrectVcsError if there isn't a repository of the
        correct type there."""
        pass

    @property
    def head(self):
        """Returns a Commit object corresponding to the head"""
        pass

class Commit(object):
    @property
    def summary(self):
        """Returns a summary of the commit."""
        pass

    @property
    def parent(self):
        """Returns the parent commit (if many parents, an arbitrarily
        chosen one), or None if this is the first in its branch."""
        pass

    @property
    def file_iter(self):
        """Returns an iterator of File objects in the repository at
        this commit."""
        pass

class File(object):
    @property
    def path():
        """The relative path to this file"""
        pass

    @property
    def stream():
        """A file-like object representing the contents of this file."""
        pass
    
