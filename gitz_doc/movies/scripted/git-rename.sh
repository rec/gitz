# git-rename: Rename branches, both locally and remotely!

git new one two
git branch -a
git rename one won
git branch -a

# You need force-push/-f to copy over an existing branch
git rename won two
git rename -f won two

# develop is a "protected branch" (default protected branches are
# master:develop), so you need the --protected option to overwrite it.
git rename two develop
git rename --protected two develop
