# Project plan: Frieren Season 2 on Reddit

A step-by-step plan for this project, written for someone new to NLP. It follows the same stages a real data-science project would.

## What we are trying to find out

1. How does opinion about the show change from episode to episode across the season?
2. Do r/Frieren and r/anime differ in how positive people are and in what they talk about?
3. Which themes dominate (animation, pacing, characters, adaptation, music), and do they rise or fall around particular episodes?

## How every stage works

Each stage follows the same loop: **Explore → Plan → Code → Review → Commit**.

- **Explore:** look at the data or the problem before deciding anything.
- **Plan:** agree on what to build. You make the key choices; Claude explains the options.
- **Code:** Claude writes the code with you, with tests (small scripts that check the code does what it should).
- **Review:** Claude opens a pull request (a proposed change on GitHub). You read it, ask questions, and CI (GitHub's automatic checker) runs the tests.
- **Commit:** you click Merge. The stage is done.

One stage means one pull request, so the project history reads like a story.

## Glossary

| Term | Plain meaning |
|---|---|
| NLP | Natural Language Processing: getting computers to work with human text. |
| Sentiment analysis | Deciding whether a text is positive, negative or neutral. Here: the commenter's **opinion about the show**. |
| Topic modelling | Automatically grouping comments by what they talk about. |
| Token | One unit of text, usually a word. |
| Hand labels | Comments you read and label yourself. They are the "answer key" used to check the models. |
| Snapshot | A saved copy of the downloaded data, so every later step uses exactly the same data. |
| Language detection | A small model that guesses which language a text is written in. Used to keep only English comments, because VADER and most sentiment models only understand English. |
| Data funnel | A table showing how many comments are left after each cleaning step, so every number in the report can be traced back. |
| Stakeholder | A person or organisation who could act on the findings, for example the studio, the streaming service or subreddit moderators. |

## The stages

| # | Stage | Status |
|---|---|---|
| 0 | Set up the project | ✅ Done (PR #1) |
| 1 | Write the study settings | Next |
| 2 | Collect the Reddit data | |
| 3 | Check and explore the data | |
| 4 | Clean the text | |
| 5 | Find the topics | |
| 6 | Hand-label comments | |
| 7 | Measure sentiment | |
| 8 | Combine and test the results | |
| 9 | Figures, report and README | |

### Stage 0: Set up the project ✅
**What:** an empty but working project: the package folder, tests, the uv installer, CI and `CLAUDE.md`.
**Done when:** `uv sync` installs it and the tests pass on GitHub. *(Merged.)*

### Stage 1: Write the study settings
**What:** put the scope decisions into one settings file (`config/study.toml`): dates, subreddits, keywords, how to recognise an episode discussion thread, and random seeds. Code reads this file instead of having numbers scattered around.
**You decide:** the keyword list; how an episode thread is recognised; **how a non-episode post gets an episode number** (from its title, the nearest episode by air date, or left out of episode analysis). Research question 1 needs this.
**Claude does:** writes the file, a small loader and tests.
**Done when:** the settings load in a test, and every value in them is one you agreed on.

### Stage 2: Collect the Reddit data
**What:** download posts and comments from Arctic Shift (a Reddit archive) and save them once as a dated snapshot, plus a manifest (a small file saying exactly what was fetched and when).
**You decide:** the open collection questions, for example whether usernames are dropped or replaced by a code, and whether r/Frieren posts are keyword-filtered too.
**Claude does:** writes the downloader with retries and polite pacing, and tests that use saved example responses, not the internet.
**Done when:** one command rebuilds the snapshot, and the manifest explains it.

### Stage 3: Check and explore the data
**What:** make sure the data is sound before trusting it: no duplicates, no missing ids, comments linked to their posts. Then take a first look: how many posts and comments per subreddit, per episode, per post type.
**Claude does:** writes the checks and a short exploration notebook.
**Done when:** the counts match the manifest, the raw counts are saved as the first row of the data funnel (`outputs/funnel.csv`), and you have a feel for the data.

### Stage 4: Clean the text
**What:** remove deleted comments, bots, moderator messages and duplicates, then keep only English comments using a language detector. Then prepare two versions of each comment: a lightly cleaned one for sentiment (keeps punctuation, emoji, capitals and words like "not", which VADER uses to judge feeling) and a heavily cleaned one for topics (lowercase, common filler words removed). Each step adds a row to the data funnel: raw → deleted → bots/moderators → duplicates → non-English → too short → final.
**You decide:** which language detector to use (`lingua`: accurate on short text but slow; fastText `lid.176`: fast and good; `langdetect`: simple but unreliable on short text); what to do with comments too short to detect reliably ("lol", "10/10"); whether to reduce words to their base form ("episodes" to "episode"); and how short a comment can be before it is dropped for topics.
**Done when:** every cleaning rule has a test, the language filter is checked by reading a sample of removed comments, and `outputs/funnel.csv` has a row for every step.

### Stage 5: Find the topics
**What:** try two topic methods, NMF (groups comments by shared words) and BERTopic (groups comments by meaning), with different numbers of topics. Score them on coherence (do the top words belong together?), diversity (are topics different from each other?) and stability (do the same topics come back with a different random seed?). Then read example comments yourself.
**You decide:** the method, the number of topics, the topic names, and the minimum weight for a comment to count as belonging to a topic.
**Done when:** each comment has one topic (or "unassigned"), and you can defend every topic name with example comments.

### Stage 6: Hand-label comments
**What:** you read about 300 comments, chosen evenly across subreddits, post types and topics, and label each as positive, negative or neutral **opinion about the show**. A short labelling guide keeps you consistent. For example, "the demon fight was brutal, best episode yet" is positive.
**Claude does:** writes the guide draft, picks the sample, and builds a simple labelling notebook. Only comment ids and labels are saved to git.
**Done when:** all ~300 are labelled, **before** you look at what any model says, so the answer key isn't influenced by the models.

### Stage 7: Measure sentiment
**What:** compare VADER (a fast word-list method, the baseline) with a transformer (a neural network that reads words in context). Score both against your labels with accuracy, macro-F1 (a score that treats all three classes fairly) and a confusion matrix (a table of which labels get mixed up). Then run the better one on all comments.
**You decide:** which transformer model to try, and which method wins.
**Done when:** you can show, with numbers, why the chosen method is the better one.

### Stage 8: Combine and test the results
**What:** answer the three research questions: opinion per episode, r/Frieren vs r/anime, and themes over the season. Statistical tests tell you whether a difference is real or just noise: chi-square (are the label shares different?), Cramér's V (how big is the difference?), and bootstrap confidence intervals (the likely range of an average). The bootstrap resamples whole posts, because comments in the same thread influence each other.
**Done when:** every claim you plan to make has a table in `outputs/` with its test and effect size.

### Stage 9: Figures, report and README
**What:** charts, a written report (`report/report.md`: question, data including the data funnel, methods, how the models were checked, results, recommendations for stakeholders, limitations, ethics) and a README explaining how to rerun everything.
**Recommendations for stakeholders:** each main finding is linked to a decision someone could make. For example: "negative opinion rises when pacing is discussed around episode X, so the studio could review how chapters are split across episodes." Each recommendation says how strong its evidence is (the test and effect size from Stage 8).
**You decide:** which stakeholders to write for (for example the studio Madhouse, the streaming service Crunchyroll, or subreddit moderators).
**Done when:** a stranger could read the report, trust it, and reproduce it, and every recommendation points to a result table in `outputs/`. A final code review and a check that no comment text or usernames are in git.

## Rules that apply everywhere

- No comment text or usernames are ever committed to git. Only code, counts, scores, figures, and hand labels stored as comment id plus label.
- Tests never use the internet.
- Every random step uses a fixed seed from the settings file, so results repeat exactly.
- Claude asks before pushing or opening a pull request.

The study decisions behind this plan are summarised in `CLAUDE.md`.
