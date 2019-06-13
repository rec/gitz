🗜gitz - tiny useful git commands, some dangerous 🗜
-------------------------------------------------------------------

This is a collection of eight little git utilities, each of which does one
useful thing well.

Three of them come from scattered open source repositories which I grabbed,
and the other five only exist here.

Half of them are aimed at rapid development on private branches
because they rewrite history extensively.  These are marked as dangerous.

---

``git-amp``
  AMend the last commit message and force-Push, somewhat safely.
  (dangerous)

``git-infer``
  Commit your changes with an auto-generated message
  (from https://github.com/moondewio/git-infer)

``git-listall``
  List recent commits for multiple branches

``git-open``
  Opens the GitHub page for a repo/branch in your browser
  (from https://github.com/paulirish/git-open)

``git-rename``
  Renames a git branch _and_ its remote branch.
  (dangerous)

``git-snip``
  Delete one or more commits by commit id or position
  (dangerous)

``git-split``
  Split a commit into individual changes, one per file
  (dangerous)

``git-st``
  Pretty, compact alternative to ``git-status`` (from
  https://www.reddit.com/user/ex1c)
