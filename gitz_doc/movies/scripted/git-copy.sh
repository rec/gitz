# git-copy: Copy branches, both locally and remotely!

git branch -a
git copy master monster

git branch -a

git copy master monster

# Force push over an existing branch
git copy -f master monster

# develop is a "protected branch" (defaults are master:develop), so you
# need the --protected option to overwrite it.
git copy master develop
git copy --protected master develop
