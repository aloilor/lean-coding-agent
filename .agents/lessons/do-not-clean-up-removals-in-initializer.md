# Do Not Clean Up Removals In The Initializer

## Mistake Pattern

Removing a baseline feature and then adding initializer logic that deletes its old files or configuration from existing projects makes initialization unexpectedly destructive.

## Rule

When something is removed from this baseline, stop generating or copying it. Do not add deletion or migration cleanup to the initializer; leave existing initialized-project artifacts untouched and document any optional manual cleanup.
