# Plan: Add search and filter capabilities to book app

## Problem
The book app only supports exact author search (`find` command). Users need:
- Partial title search (case-insensitive)
- Filter by read/unread status
- Filter by year range

## Approach

### Phase 1: BookCollection methods (`books.py`)
Add three new methods:
- `search_by_title(query: str) -> List[Book]` — case-insensitive partial match
- `filter_by_status(read: bool) -> List[Book]` — filter by read/unread
- `filter_by_year(start: int, end: int) -> List[Book]` — filter by year range

### Phase 2: CLI handlers (`book_app.py`)
- `handle_search()` — prompts for partial title, calls `search_by_title()`
- `handle_filter()` — prompts for filter type (read/unread/year), delegates to appropriate method
- Wire `"search"` and `"filter"` commands in `main()` dispatch
- Update `show_help()` to document both commands

### Phase 3: Tests (`tests/test_books.py`)
Add tests for all three new methods covering happy path and edge cases.

## Files to Change

| File | Change |
|------|--------|
| `books.py` | Add `search_by_title()`, `filter_by_status()`, `filter_by_year()` |
| `book_app.py` | Add `handle_search()`, `handle_filter()`, wire commands, update help |
| `tests/test_books.py` | Add tests for all three new methods |

## Notes
- All new functions get type hints
- Reuse existing `show_books()` for display
- `filter` command prompts user to choose: read / unread / year range
