"""Chinese subtitle rule shared by tests/docs: one cue = one line of <= 18 characters.
Python mirror of template/src/theme.ts splitCaption() (keep the two in sync)."""
import re

PUNCT = "，。、；：！？,.;:!?"
LATIN = re.compile(r"[A-Za-z0-9_]")


def count_chars(s):
    return sum(1 for c in s.replace("**", "") if c.strip())


def split_caption(text, max_chars=18):
    chars, hi = [], False
    for part in re.split(r"(\*\*)", text):
        if part == "**":
            hi = not hi
            continue
        chars += [(c, hi) for c in part]
    out, cur = [], []

    def n(a):
        return sum(1 for c, _ in a if c.strip())
    for i, (c, h) in enumerate(chars):
        cur.append((c, h))
        if c in PUNCT and n(cur) >= min(8, max_chars):
            out.append(cur)
            cur = []
            continue
        if n(cur) >= max_chars:
            cut = len(cur)
            for k in range(len(cur) - 1, 0, -1):
                a, b = cur[k - 1][0], cur[k][0]
                if a in PUNCT or a == " " or not (LATIN.match(a) and LATIN.match(b)):
                    cut = k
                    break
            if i + 1 < len(chars) and LATIN.match(c) and LATIN.match(chars[i + 1][0]):
                out.append(cur[:cut])
                cur = cur[cut:]
            else:
                out.append(cur)
                cur = []
    if n(cur):
        out.append(cur)
    res = []
    for seg in out:
        s, h = "", False
        for c, hh in seg:
            if hh != h:
                s += "**"
                h = hh
            s += c
        if h:
            s += "**"
        s = re.sub(r"[，。、；：,.;:]+(\*\*)?$", r"\1", s.strip())
        s = re.sub(r"^(\*\*)?[，。、；：！？,.;:!?\s]+", r"\1", s)
        if count_chars(s):
            res.append(s)
    return res
