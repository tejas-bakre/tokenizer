# Project 1: Build Your Own Tokenizer

A Byte Pair Encoding (BPE) tokenizer built from scratch — the same algorithm used by GPT-2, GPT-4, and LLaMA.

---

## What It Does

- Learns a vocabulary from raw text by iteratively merging frequent character pairs
- Encodes new text into integer token IDs
- Decodes integer IDs back into text
- Saves and loads the learned vocabulary and merge rules to disk

---

## File Structure

```
tokenizer/
├── tokenizer.py   ← core BPE logic (Tokenizer class)
├── vocab.json     ← saved vocabulary (token → id)
└── merges.txt     ← saved merge rules (in learned order)
```

---

## How to Use

```python
from tokenizer import Tokenizer

# Train
t = Tokenizer()
t.train("low low low lower lowest", vocab_size=20)

# Encode and decode
ids = t.encode("lowest slow")
print(ids)                # [12, 4, 8]
print(t.decode(ids))      # lowest s low

# Save
t.save("vocab.json", "merges.txt")

# Load into a fresh tokenizer
t2 = Tokenizer()
t2.load("vocab.json", "merges.txt")
print(t2.encode("lower"))  # [10]
```

---

## How It Works

### Training
1. Count the frequency of every word in the corpus
2. Split each word into individual characters
3. Repeatedly find the most frequent adjacent pair and merge it into a new token
4. Record every merge in order — this is the learned knowledge
5. Stop when the vocabulary reaches the target size

### Encoding
1. Split new text into characters
2. Replay the learned merge rules top to bottom, in order
3. Look up each remaining token in the vocabulary to get its integer ID

### Decoding
1. Reverse the vocabulary lookup (id → token)
2. Join tokens back into text

---

## Key Concepts

**Why sub-word tokenization?**
Word-level tokenization produces huge vocabularies and cannot handle unseen words. Character-level tokenization produces sequences that are too long and carries no meaning. BPE finds the middle ground — frequent patterns become single tokens, rare words fall back gracefully to smaller pieces.

**Why does merge order matter?**
The model trained on this tokenizer learned patterns based on specific token boundaries. Applying merges in a different order would produce different token IDs for the same text — breaking the model entirely.

**Why multiply pair counts by word frequency?**
A pair inside a word that appears 1000 times in the corpus should outweigh a pair inside a word that appears once. Frequency reflects real usage.

---

## Known Limitations

| Limitation | How production tokenizers solve it |
|---|---|
| Spaces appear between decoded tokens | Use `Ġ` marker to encode spaces as part of tokens |
| Splits only on whitespace | Regex pre-tokenization to handle punctuation |
| Case sensitive | Lowercasing or explicit case handling |
| Unknown characters possible | Byte-level BPE — start from 256 raw bytes, never unknown |

---

