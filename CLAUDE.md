# CLAUDE.md

Guidance for Claude Code working in this repository.

## Project

NLP analysis of Reddit discussion of *Frieren: Beyond Journey's End* Season 2 on r/Frieren and r/anime. The research questions are in `README.md`: how opinion about the show changes episode by episode, how the two subreddits differ, and which themes dominate. This is a from-scratch rebuild of an earlier notebook-only project (`btduyforwork/analysing-frieren-season-2-reddit`, reference only), done as a learning project.

## Working agreement

- The owner is new to AI and NLP and is learning NLP, software engineering and AI-assisted development. Explain terms in plain words, explain *why*, offer options with trade-offs, and let the owner make the key technical decisions (methods, thresholds, number of topics, labels, model choice). Never pick them silently.
- Work in the loop **Explore → Plan → Code → Review → Commit**. Show the plan before writing code for anything beyond a small fix.
- Keep changes small and scoped to the current stage of `docs/PLAN.md`. One pull request per stage; tick the stage's status in the plan when it merges.
- Ask before pushing, opening a pull request, or rewriting git history.
- Write code, comments and docs in English.

## Study decisions (do not change without the owner)

- Posts created 2026-01-01 to 2026-04-01 UTC in r/Frieren and r/anime; keep every comment on those posts. Each post gets a `post_type`: episode discussion thread or keyword post.
- Data source: Arctic Shift only. Fetch once into a dated raw snapshot with a manifest; every later stage reads the snapshot, never the API.
- "Sentiment" means **opinion about the show**, not emotional tone. Story words (demon, kill, death) are not negative opinion.
- Sentiment: VADER baseline vs a transformer model, both scored against about 300 hand labels (accuracy, macro-F1, confusion matrix).
- Topics: TF-IDF + NMF vs BERTopic; choose the number of topics by NPMI coherence, diversity, stability over 5 seeds, and human reading. One topic per comment, with a minimum weight, otherwise "unassigned".
- Statistics: chi-square + Cramér's V for proportions; cluster bootstrap (resample whole posts) for confidence intervals on means.
- Deliverables: `README.md` + `report/report.md`.

## Data rules

- **Never commit comment text, post text or usernames.** `data/` is gitignored. Only code, aggregate tables, metrics, figures, and hand labels as `comment_id,label` are committed.
- Tests never call the network; they use small hand-made fixtures in `tests/fixtures/`.
- All randomness is seeded from the study config.

## Commands

```bash
uv sync                                          # install everything, including dev tools
uv run pytest                                    # run the tests
uv run ruff check . && uv run ruff format --check .   # lint and format check (CI runs these)
uv run ruff format .                             # auto-format
uv add <package>                                 # add a runtime dependency
uv run frieren --help                            # pipeline CLI; stages are added as they are built
```

## Layout

- `src/frieren_nlp/`: all pipeline logic, importable and tested. Notebooks import from here and never define pipeline functions.
- `src/frieren_nlp/cli.py`: the `frieren` command; each stage becomes a subcommand.
- `tests/`: pytest, one test file per module.
- `.github/workflows/ci.yml`: runs lint, format check and tests on every pull request.
- Added in later stages: `config/` (study settings), `notebooks/`, `outputs/` (aggregates and figures), `report/`.

## Code style

- Python 3.12, type hints on public functions, small pure functions where possible.
- Paths and settings come from config, not hard-coded strings.
- Join tables on ids, never by row position.
- Topic labels are stored keyed to a model fingerprint, so a refit cannot silently mislabel topics.
