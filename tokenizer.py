import json 
class Tokenizer:

    def __init__(self):
        self.vocab = {}      # token string → integer id
        self.merges = []     # list of (str, str) tuples, in learned order

    def get_pair_counts(self, splits, word_freqs):
        pair_counts = {}
        for word, freq in word_freqs.items():
            chars = splits[word]
            for i in range(len(chars) - 1):
                pair = (chars[i], chars[i + 1])
                if pair not in pair_counts:
                    pair_counts[pair] = 0
                pair_counts[pair] += freq
        return pair_counts

    def merge_pair(self, pair, splits):
        a, b = pair
        merged = a + b
        for word in splits:
            chars = splits[word]
            new_chars = []
            i = 0
            while i < len(chars):
                if i < len(chars) - 1 and chars[i] == a and chars[i + 1] == b:
                    new_chars.append(merged)
                    i += 2
                else:
                    new_chars.append(chars[i])
                    i += 1
            splits[word] = new_chars
        return splits

    def train(self, corpus: str, vocab_size: int):
        # Step 1: Count word frequencies
        word_freqs = {}
        for word in corpus.split():
            if word not in word_freqs:
                word_freqs[word] = 0
            word_freqs[word] += 1

        # Step 2: Split each word into characters
        splits = {}
        for word in word_freqs:
            splits[word] = list(word)

        # Step 3: Build initial vocabulary from all unique characters
        all_chars = set()
        for chars in splits.values():
            for c in chars:
                all_chars.add(c)
        self.vocab = {ch: i for i, ch in enumerate(sorted(all_chars))}

        # Step 4: Iteratively merge until we reach vocab_size
        while len(self.vocab) < vocab_size:
            pair_counts = self.get_pair_counts(splits, word_freqs)
            if not pair_counts:
                break
            best_pair = max(pair_counts, key=lambda p: pair_counts[p])
            splits = self.merge_pair(best_pair, splits)
            new_token = best_pair[0] + best_pair[1]
            self.vocab[new_token] = len(self.vocab)
            self.merges.append(best_pair)

        print("Merges learned:", self.merges)
        print("Vocabulary:", self.vocab)

        #print(word_freqs)
        #print(splits)
        #pair_counts = self.get_pair_counts(splits, word_freqs)
        #print(pair_counts)

    def encode(self, text: str) -> list:
        ids = []
        for word in text.split():
            chars = list(word)
            for pair in self.merges:
                a, b = pair
                merged = a + b
                i = 0
                new_chars = []
                while i < len(chars):
                    if i < len(chars) - 1 and chars[i] == a and chars[i + 1] == b:
                        new_chars.append(merged)
                        i += 2
                    else:
                        new_chars.append(chars[i])
                        i += 1
                chars = new_chars
            for token in chars:
                ids.append(self.vocab[token])
        return ids

    def decode(self, ids: list) -> str:
        reverse_vocab = {i: token for token, i in self.vocab.items()}
        tokens = [reverse_vocab[i] for i in ids]
        return " ".join(tokens)

    def save(self, vocab_path: str, merges_path: str):
        with open(vocab_path, "w") as f:
            json.dump(self.vocab, f)
        with open(merges_path, "w") as f:
            for a, b in self.merges:
                f.write(f"{a} {b}\n")

    def load(self, vocab_path: str, merges_path: str):
        with open(vocab_path, "r") as f:
            self.vocab = json.load(f)
        with open(merges_path, "r") as f:
            for line in f:
                a, b = line.strip().split(" ")
                self.merges.append((a, b))


if __name__ == "__main__":
    t = Tokenizer()
    corpus = "low low low lower lowest"
    t.train(corpus, vocab_size=20)
    t.save("vocab.json", "merges.txt")

    t2 = Tokenizer()
    t2.load("vocab.json", "merges.txt")

    text = "lowest slow lower"
    ids = t2.encode(text)
    print("Encoded:", ids)
    print("Decoded:", t2.decode(ids))
    #print(t.encode("lowest"))
    #print(t.encode("low"))
    #print(t.encode("lower"))
    #print(t.encode("slow"))
    #print(t.encode("lowest lower low"))
    #print(t.decode([12]))
    #print(t.decode([8]))
    #print(t.decode([4, 8]))