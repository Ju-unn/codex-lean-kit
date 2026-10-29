# Over-engineering checklist

A part is over-engineered when no R-n needs it.

Report each one with:
- the part
- the R-n it serves (none)
- what to delete or simplify
- what is lost

## Look for
- Abstractions with one implementation: interfaces, factories, base classes, generic repositories, DI containers.
- Options, flags, and config nobody asked for. Code paths "for later".
- Guards for operations the system does not have. Examples: write-conflict handling on a read-only API, retries around a local function call.
- Layers that only pass data through. The same validation repeated in every layer.
- A dependency added for a few lines of standard-library work.
- Caching, queues, pagination, background jobs, or i18n without a stated need.
- Tests that re-implement the code, or that test the framework instead of our behaviour.

## Keep
These are never over-engineering:
- input validation at trust boundaries
- error handling that prevents data loss
- security controls
- tests for required behaviour
