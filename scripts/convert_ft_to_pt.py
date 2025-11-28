from gensim.models import KeyedVectors
import torch

# Load .ft text vectors (change: using load_word2vec_format)
kv = KeyedVectors.load_word2vec_format("/cephyr/users/cleland/Alvis/stanza_resources/sv/pretrain/diachronic.ft")

# Convert to PyTorch tensor (change: using .vectors attribute)
emb = torch.tensor(kv.vectors)

# Save as .pt (final output)
torch.save(emb, "/cephyr/users/cleland/Alvis/stanza_resources/sv/pretrain/diachronic.pt")