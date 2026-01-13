# Quick Reference

Common configuration settings organized by category for quick lookup.

## Quick Reference Table

| Category | Setting | Command | Purpose |
| --- | --- | --- | --- |
| **Performance** | fsmonitor | `git config --global core.fsmonitor true` | Monitor filesystem for changes (speeds up status) |
| **Performance** | untrackedCache | `git config --global core.untrackedCache true` | Cache untracked files list |
| **Performance** | fetch.parallel | `git config --global fetch.parallel 8` | Parallel fetch connections |
| **Performance** | checkout.workers | `git config --global checkout.workers 8` | Parallel checkout operations |
| **Pull/Rebase** | pull.rebase | `git config --global pull.rebase true` | Use rebase instead of merge on pull |
| **Pull/Rebase** | rebase.autoStash | `git config --global rebase.autoStash true` | Auto-stash uncommitted changes |
| **Pull/Rebase** | rebase.updateRefs | `git config --global rebase.updateRefs true` | Keep branch stack clean |
| **Fetch** | fetch.prune | `git config --global fetch.prune true` | Auto-prune deleted remote branches |
| **Fetch** | fetch.pruneTags | `git config --global fetch.pruneTags true` | Auto-prune deleted tags |
| **Push** | push.autoSetupRemote | `git config --global push.autoSetupRemote true` | Auto-setup tracking on first push |
| **Diff** | diff.algorithm | `git config --global diff.algorithm histogram` | Better diff accuracy |
| **Diff** | diff.colorMoved | `git config --global diff.colorMoved zebra` | Highlight moved code |
| **Merge** | merge.conflictstyle | `git config --global merge.conflictstyle zdiff3` | Show merge base in conflicts |
| **Merge** | rerere.enabled | `git config --global rerere.enabled true` | Remember conflict resolutions |
| **Line Endings** | core.safecrlf | `git config --global core.safecrlf warn` | Warn about line ending issues |
| **Sorting** | branch.sort | `git config --global branch.sort -committerdate` | Sort branches by date (newest first) |
| **Sorting** | tag.sort | `git config --global tag.sort -taggerdate` | Sort tags by date (newest first) |
| **Maintenance** | - | `git maintenance start` | Enable background maintenance |

For detailed explanations and platform-specific guidance, see the main [config SKILL.md](../SKILL.md).
