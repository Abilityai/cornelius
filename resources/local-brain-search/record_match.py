"""Ranking helpers shared by search.py and daemon.py (stdlib only - keep in lockstep).

1. q_adjust_chunks - the learned Q-value boost is per NOTE, but results are per
   CHUNK. The boost used to be keyed {note_id: similarity}, so when a note had
   several chunks in the result list the LAST (weakest) one won and every chunk of
   that note was re-scored to it: a record whose decision line matched at 0.58 was
   ranked by its Change Log chunk at 0.21. Now each chunk keeps its own score and
   only the note's boost factor is applied to it.

2. record_word_hits - records (reference-kind scopes, e.g. Company/) are short,
   dated facts named by their words: "the weekly sync", a person, a product. A
   question phrased in plain language ("what decisions were made in the weekly
   sync?") lands far below the similarity threshold against a one-line decision,
   so a records read could come back empty while the record sits in scope. This
   pass matches the question's content words against IN-SCOPE RECORD chunks only
   (never cognitive notes - their ranking is unchanged) and adds the chunks that
   carry most of them. Each added hit says `match: "words"` and keeps its real
   cosine in `raw_similarity`.
"""
import re

from memory_config import in_read_scope, is_reference_scope, scope_of

_STOP = frozenset("""
a about above after again all also am an and any are as at be been before being
below between both but by can could did do does doing done during each few for
from further had has have having he her here hers him his how i if in into is it
its just me more most my no nor not of off on once only or other our ours out over
own per please same she should so some such than that the their them then there
these they this those through to too under until up us very was we were what when
where which while who whom why will with would you your yours tell show give find
list know any anything something according brain company notes note record records
say says said said made make makes get got
""".split())


def _terms(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 1]


def _stem(t):
    return t[:5] if len(t) > 5 else t


def query_terms(query):
    """Content words of a question, stemmed, in order, de-duplicated."""
    seen, out = set(), []
    for t in _terms(query):
        if t in _STOP:
            continue
        s = _stem(t)
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def word_coverage(terms, text):
    """Share of the query's content words present in text (prefix-stemmed)."""
    if not terms:
        return 0.0
    have = {_stem(t) for t in _terms(text)}
    return sum(1 for t in terms if t in have) / len(terms)


def q_adjust_chunks(results, adjust_fn, read_scope=None, key="similarity"):
    """Apply the per-note Q boost to every chunk's OWN score, then re-sort."""
    if not results:
        return results
    best = {}
    for r in results:
        nid = r["note_id"]
        best[nid] = max(best.get(nid, float("-inf")), r[key])
    adjusted = adjust_fn(dict(best), read_scope=read_scope)
    for r in results:
        base = best[r["note_id"]]
        new = adjusted.get(r["note_id"], base)
        factor = (new / base) if base else 1.0
        r[key] = r[key] * factor
    results.sort(key=lambda x: x[key], reverse=True)
    return results


MIN_COVERAGE = 0.6   # most of the question's content words must be in the record chunk


def record_word_hits(query, metadata, read_scope, threshold, limit, cosine_of, taken=()):
    """Record chunks (reference-kind, in scope) that carry most of the query's words.

    cosine_of(idx) -> the chunk's real cosine to the query (for raw_similarity).
    taken: (note_id, heading) pairs already in the results - not added twice.
    Ranking score sits just above the threshold and grows with coverage, so a
    word-matched record shows up without outranking a strong semantic hit.
    """
    terms = query_terms(query)
    need = 1 if len(terms) == 1 else 2
    if not terms:
        return []
    taken = set(taken)
    hits = []
    for idx, meta in enumerate(metadata):
        nid = meta.get("note_id", "")
        if not is_reference_scope(scope_of(nid)) or not in_read_scope(nid, read_scope):
            continue
        if (nid, meta.get("heading")) in taken:
            continue
        text = " ".join(str(meta.get(k) or "") for k in ("title", "heading", "content"))
        cov = word_coverage(terms, text)
        if cov < MIN_COVERAGE or round(cov * len(terms)) < need:
            continue
        raw = float(cosine_of(idx))
        hits.append({
            "similarity": max(raw, threshold + (1.0 - threshold) * 0.5 * cov),
            "raw_similarity": raw,
            "word_coverage": round(cov, 2),
            "match": "words",
            "title": meta["title"],
            "heading": meta["heading"],
            "filepath": meta["filepath"],
            "note_id": nid,
            "content": meta["content"],
        })
    hits.sort(key=lambda h: (h["word_coverage"], h["raw_similarity"]), reverse=True)
    return hits[:limit]
