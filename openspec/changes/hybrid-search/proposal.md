# hybrid-search Proposal

## Why
Users need a flexible search endpoint that can find subjects by name or by whether they have overdue tasks. This improves discoverability and helps students quickly locate relevant subjects that require attention.

## What Changes
- Add a new API endpoint for hybrid search on subjects.
- Support filtering subjects by:
  - subject name (partial match)
  - overdue tasks count or presence of overdue tasks
- Integrate Python logic to compute overdue task status and combine it with subject search criteria.
- Ensure the endpoint returns only subjects accessible to the authenticated user.

## Impact
- Frontend can use a single search endpoint for both name-based and overdue-task-based filtering.
- Backend adds Python integration to compute overdue status and return secure, user-specific search results.