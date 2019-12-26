# git for-each: execute a command for each branch or directory
# Note that aliases are not expanded

# For each branch
git new one && echo one > one.txt && git add one && git commit -m one
git new two && echo two > two.txt && git add two && git commit -m two
git new three && echo three > three.txt && git add three && git commit -m three

git for-each - git log --oneline

# For each directory
mkdir dir_A && echo A > A/data.txt
mkdir dir_B && echo B > B/data.txt
mkdir dir_C && echo C > C/data.txt

git for-each dir_* - cat data.txt
