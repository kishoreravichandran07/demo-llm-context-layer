"""Demo configuration. Plain Python so the demo stays dependency-free."""

# Work-relevance rules: an item counts as work context if it mentions a known
# project marker or one of these keywords. Everything else is personal/noise.
WORK_KEYWORDS = ["project", "pricing", "legal", "security", "deployment", "customer"]

# Access control: which coworker may receive which owner's context.
# Mirrors the "designated coworkers only" control from the case study.
ACCESS_LIST = {
    "alex": ["priya", "sam"],
    "priya": ["alex"],
}
