# git-delete: Delete branches, both locally and remotely

git new one two three
git branch -a

git delete one two
git branch -a

# You need the -p option to overwrite protected branches
git new -p develop
git branch -a

git delete develop
git delete -p develop
git branch -a
