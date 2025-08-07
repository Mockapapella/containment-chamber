# What is this?

Containment Chamber makes AI agents code without breaking things.

When agents adds features to your codebase, it often breaks existing code. Containment Chamber prevents this by surrounding the AI-generated code with so many deterministic verifiers that the LLM has no choice but to do it right.

Built for agents, not humans. Currently in alpha.

# Use

Since this is in the early stages, the recommended way to use this is to clone the repo, delete some folders, and run:

```
rm -rf .git/
rm -rf .github/
rm -rf .stubs/
rm -rf .tests/*
git init
uv sync
source .venv/bin/activate
pre-commit install
```

Yeah, it's jank, but this is the worst it will ever be™. From there you can run your coding agent (i.e. `claude`, `opencode`, etc.) and start building features. Before each commit, the pre-commit runs a litany of curated tests to make sure there haven't been any regressions. Doing this before every commit ensures that every subsequent feature request has solid ground to stand on.

Only Python for now but other languages planned once the theory proves out.

# Features

- [x] 100% test coverage
    - [ ] Auto-detection of over-defined tests (i.e. multiple tests that test the same thing)
- [x] Property-based testing
    - [ ] Auto-discovery of valid signatures for property tests (currently no library for this)
- [x] Mutation testing
- [x] Enforce all type hints
- [x] Enforce all linting rules
- [x] Set and enforce complexity thresholds
    - [x] Cyclomatic Complexity
    - [x] Cognitive Complexity
- [x] Security Audits
    - [x] Source code
    - [x] Dependencies
    - [x] Secrets analysis
- [x] Enforce consistent code formatting
- [ ] High quality auto-documentation
- [ ] Reproducible builds
- [ ] Memory profiler
- [ ] TestContainers for external services
- [ ] Post-receive hook that monitors github CI build
- [ ] Remove all dead code (currently no reliable method)

PRs welcome :)
