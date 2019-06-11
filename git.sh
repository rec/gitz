# Git aliases

alias g=git
alias go='g open'

alias gb='git branch'
alias gbr='git symbolic-ref --short HEAD'

alias gc='git checkout'
alias gcb='git checkout -b'

alias gi='git infer -a && git push'

# alias gl='git l upstream/dev..'
alias glm='git l master..'
alias gl='git l'

alias gri='git rebase -i upstream/dev'
alias gs='git st'
alias gst='git st'

alias gcp='git cherry-pick'

alias gp='git push'
alias gpf='git push --force-with-lease'
alias gps='git push --set-upstream origin'

alias gsh='git show > /tmp/git.diff'
alias gdiff='git diff > /tmp/git.diff'

alias grs='g reset --soft HEAD~'
alias greb='git fetch upstream && git rebase upstream/dev'
alias gdam='gc master && git merge dev && git push && gc dev'

alias gia='git infer -a'

alias grev='greset HEAD~ && gcopy'
alias gclean='gdelete one two three four five six'
alias gclean2='gdelete seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen'

# Amend the previous change to include all the changes you have currently.
# Slightly dangerous, don't use this on master.
alias gcam='git commit --amend -a --no-edit'

#
# Git functions.
#
# Many of these are "slightly dangerous" so use with care.
#

function gcom() {
    git commit -am "$*"
}

# Commit everything with a message and push it.
function gcomp() {
    gcom $* && gp
}

function gcomp-f() {
    gcom $* && gpf
}

# Check out a copy of the current branch under a new name and push it to your
# origin directory.
function gcopy() {
    gcb $1 && gps $1
}

function gbs() {
    for i in $@ ; do
        gcb $i && greset HEAD~ && gps $i
    done
}

alias gbss='gbs one two three four five six'
alias gbsss='gbss seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen'

function gnew() {
    echo "ERROR: Use gcopy"
}

function greset() {
    if [ $1 ] ; then
        NAME=$1
    else
        NAME=HEAD
    fi
    git reset --hard $NAME
}

# Back up the current branch.
function gback() {
    branch=`git symbolic-ref --short HEAD`
    back=b-$branch

    gdelete $back && gc $branch && gcopy $back && gc $branch
}

# Amend the previous commit to include all the changes you have currently,
# and force push. gcap is "git commit, amend, push"
# Slightly dangerous, don't use this on master.
function gcap() {
    if [[ $1 ]] ; then
        echo "ERROR: gcap doesn't take any commands"
        return 1
    fi
    gcam && gpf
}

# Check out a fresh copy of master under a new name and push it to your origin
# directory.
function gfresh-f() {
    if [[ -z $1 ]] ; then
        echo "ERROR: gfresh needs an argument"
        return 1
    fi
    base=`/code/dotfiles/python/base_branch.py`

    git checkout -b $1 && \
        git fetch upstream && \
        git reset --hard upstream/$base && \
        git push --set-upstream origin $1
}

# Check out a fresh copy of master under a new name and push it to your origin
# directory.  Fail if there are changes in the workspace.
function gfresh() {
    if git diff-index --quiet HEAD -- ; then
        gfresh-f "$1"
    else
        echo "ERROR: Changes in your workspace would be overwritten."
        return 1
    fi
}

function gunused() {
    gc `/code/dotfiles/python/unused_branch.py $@`
}

# Delete branches that have been merged to master.
function gdelete-safe() {
    branch=`gbr`

    for i in $@ ; do
        gunused $@ && gb -d $i && gp --delete origin $i
    done

    gc $branch
}

# Delete branches that might not have been merged to master.
function gdelete() {
    branch=`gbr`

    for i in $@ ; do
        gunused $@ && ( gb -D $i ; gp --delete origin $i )
    done

    gc $branch
    return 0
}

# Move an existing branch to a new name.
function gmove() {
    if [[ -z "$1" ]] ; then
        echo "Usage: gmove [from] to"
        return 1
    fi

    branch=`gbr`
    if [[ "$2" ]] ; then
        from=$1
        to=$2
    else
        from=$branch
        to=$1
    fi

    git checkout $from && \
        git pull && \
        git branch -m $from $to && \
        git push origin :$from && \
        git push --set-upstream origin $to && \
        git checkout $branch
}

function gr() {
    if [ -z "$1" ] ; then
        commits=12
    else
        commits="$1"
    fi
    git rebase -i HEAD~$commits
}

function gfix() {
    git commit -a --fixup $1 && git push
}

function gmaf() {
    if git diff-index --quiet HEAD -- ; then
        git commit -a --amend -m "$*" && git push --force-with-lease
    else
        echo "ERROR: Changes in your workspace would be overwritten."
     fi
}

function gbase-f() {
    BASE=`/code/dotfiles/python/base_branch.py`

    git fetch upstream && git rebase upstream/$BASE
}

function gbase() {
    if git diff-index --quiet HEAD -- ; then
        gbase-f
    else
        echo "ERROR: Changes in your workspace would be overwritten."
     fi
}

function gversion() {
    gfresh release
    gl -100 | sed -n '1,/v3./ p'
    echo
    /code/BiblioPixel/scripts/new_version
    gop
}

function gexplode() {
    grs && git split
}

# List branches
function _glist() {
    branch=`gbr`

    for i in $@ ; do
        gc $i 1> /dev/null && gl -8 && echo
    done

    gc $branch
}

# List branches
function glist() {
    if [[ $1 ]] ; then
        _glist $@
    else
        branches=`gb | sed -e 's/*//' | xargs echo`
        echo "branches=$branches"
        _glist $branches
    fi
}

function gupdate() {
    if [[ "$1" ]] ; then
        branch=`gbr`
        for i in $@ ; do
            echo "gupdating: $i"
            gc "$i" && greb && gpf
            if [[ -z "$?" ]] ; then
                return 1
            fi
            sleep 0.5
        done
        gc $branch
    else
        greb && gpf
    fi
}

# See https://www.reddit.com/r/git/comments/ah1euu

gsnip() {
    python - <<EOF
import os

for i in reversed(sorted(map(int, "$@".split()))):
    os.system("git rebase HEAD~%d --onto HEAD~%d" % (i, i + 1))
EOF
}
