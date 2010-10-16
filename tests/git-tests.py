import unittest
import tempfile
import shutil
import os

from nose.tools import *
from git import Repo, Git

from srcstats.vcs_git import GitVcsWrapper
from srcstats.vcs import VcsWrapper

class GitVcsTests(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()


        g = Git(self.test_dir)
        g.init()

        open('%s/testfile.txt' % (self.test_dir, ), 'w').write('This is a test')
        g.add('testfile.txt')
        g.commit('-m', 'First commit')

        os.mkdir('%s/testdir' % (self.test_dir, ))
        open('%s/testdir/file2.txt' % (self.test_dir, ), 'w').write('This is another test')
        g.add('testdir/file2.txt')
        g.commit('-m', 'Second commit')

        self.vcs = VcsWrapper.vcs_for_path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_is_git_repo(self):
        assert isinstance(self.vcs, GitVcsWrapper)

    def test_commit_summary(self):
        c = self.vcs.head
        eq_(c.summary, 'Second commit')
        c = c.parent
        eq_(c.summary, 'First commit')
        c = c.parent
        eq_(c, None)

    def test_file_iterators(self):
        found_testfile = False
        fount_file2 = False

        for f in self.vcs.head.file_iter:
            if f.path == 'testfile.txt':
                found_testfile = True
                eq_(f.stream.read(), 'This is a test')
            elif f.path == 'testdir/file2.txt':
                found_file2 = True
                eq_(f.stream.read(), 'This is another test')

        assert found_testfile
        assert found_file2
