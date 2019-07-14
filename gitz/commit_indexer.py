from gitz import git


class CommitIndexer:
    def __init__(self):
        self.commit_ids = [git.commit_id()]

    def index(self, commit_id):
        if commit_id.isnumeric() and len(commit_id) < git.COMMIT_ID_LENGTH:
            commit_id = 'HEAD~' + commit_id

        commit_id = git.commit_id(commit_id)
        for i, id in enumerate(self.commit_ids):
            if id.startswith(commit_id) or commit_id.startswith(id):
                return i

        commits = '%s~..%s~' % (commit_id, self.commit_ids[-1])
        for line in git.GIT_SILENT.log('--oneline', commits):
            if line.strip():
                commit, *_ = line.split(maxsplit=1)
                self.commit_ids.append(commit.lower())
        return len(self.commit_ids) - 1
