# git-rename: Rename branches, both locally and remotely!

git new one two

git branch -a

git rename one won

git branch -a

git rename won two

# Force push over an existing branch
git rename -f won two

# develop is a "protected branch" (defaults are master:develop), so you
# need the -p option to overwrite it.
git rename two develop
git rename -p two develop
