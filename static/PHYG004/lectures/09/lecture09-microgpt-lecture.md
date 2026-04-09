# Lecture 09 — microgpt: a GPT in 200 lines

**PHYG004 — 2026 Spring — Sogang University**
**Wed Apr 8 & Fri Apr 10, 2026**

## Pre-reading (do this before Wednesday)

Read Karpathy's blog post in full. It is short.

→ **https://karpathy.ai/microgpt.html**

This lecture is a guided walkthrough of that post and the code it points to.
We will not re-derive the post in slides. We will read the code together.

## What we are doing

Karpathy released `microgpt.py`: a 200-line, dependency-free Python file that
trains and samples from a GPT. It contains exactly the algorithmic content of
a modern LLM and nothing else. Our job for the next two classes is to
understand every line of it.

We will not look at the final 200-line file directly. We will look at the
**six versions** that build up to it, one idea at a time:

```
train0 → train1 → train2 → train3 → train4 → train5
counts   MLP+SGD  autograd  attention multihead  Adam
```

Each step adds one new concept on top of the previous file. The diff between
two consecutive files is small enough to read in one sitting.

## Schedule

| Day  | Date         | Steps                | Focus                            |
|------|--------------|----------------------|----------------------------------|
| Wed  | Apr 8, 2026  | train0, train1, train2 | counting → MLP → autograd       |
| Fri  | Apr 10, 2026 | train3, train4, train5 | attention → multi-head → Adam   |

## Day 1 — counts, gradients, autograd

### train0 — bigram by counting

A bigram language model predicts the next character from the previous one.
For this model class there is a closed-form maximum-likelihood solution: count
how often each pair `(prev, next)` appears, normalize, done. No gradients
required.

This is the **baseline**. Every later step is "the same task, but with a more
expressive model and a more general training procedure." The final loss for
train0 is the floor that any model with the same Markov assumption can hit.

Why start here? Because it makes the rest of the lecture honest. When we add
a neural net in train1 and the loss does not improve, that is not a bug —
that is the model class telling us it has the same expressive power as the
count table.

### train1 — MLP with manual gradients

Replace the count table with a one-layer MLP. The model is now a
differentiable function `token_id → logits`. To train it we need gradients,
which we compute two ways:

1. **Numerical**: perturb each parameter by ε, measure how the loss changes.
   `O(P)` forward passes. Slow but unmistakable.
2. **Analytic**: chain rule, by hand. `O(1)` backward passes. Fast but
   error-prone.

The two should agree to many digits. They do. This is the only sanity check
that protects you from a wrong analytic derivation.

Loss does not improve over train0. That is expected: a bigram MLP and a
bigram count table are the same model class. We are paying the cost of
differentiability and getting nothing for it yet.

The reason to do it anyway is that the count-table trick **stops working** as
soon as the model is more expressive than a lookup. Gradient descent is the
general-purpose hammer. From train1 onward we never count again.

### train2 — autograd with the `Value` class

Hand-deriving gradients for one MLP layer is annoying. For a transformer it
is unthinkable. We need autograd.

`Value` is a scalar wrapper that records every operation it participates in.
After the forward pass we have a DAG of `Value` nodes. `loss.backward()`
walks the DAG in reverse topological order and applies the chain rule
locally at each node. This is identical in algorithm to PyTorch's autograd —
the only difference is that PyTorch operates on tensors and ours operates on
single numbers.

Read at least one `_backward` closure carefully (try `__mul__`). Convince
yourself it implements the local derivative of that op. Once you believe one
of them, the rest follow the same pattern.

After train2 the training loop is the one we will use forever:

```
forward → loss.backward() → step → zero_grad → repeat
```

The model still has the same expressive power as train0. We have not added
intelligence, only a way to add intelligence.

## Day 2 — attention, depth, Adam

### train3 — single-head attention, position embeddings, RMSNorm, residual

This is the lecture. Everything before this was infrastructure. This is where
the model becomes a transformer.

Four ideas land in this file at once:

- **Position embeddings.** A pure attention layer is permutation-invariant.
  Sequences are not. We add a learned vector per position so the model can
  tell "first token" from "third token."
- **Single-head attention.** For each position, build a query, look at the
  keys of all earlier positions, softmax to get weights, take a weighted sum
  of values. This is the **only** mechanism in the transformer that lets
  positions talk to each other. Everything else is per-position.
- **Causal mask.** A language model must not look at the future. The
  attention only attends to positions ≤ current. Find this in the code and
  understand exactly which line enforces it.
- **RMSNorm + residual.** Standard transformer plumbing. RMSNorm keeps
  activations at a stable scale; residuals make the network trainable when
  it gets deep.

Loss drops below train2 for the first time. The model now uses context
beyond the previous character. This is the first step where adding
parameters actually buys you something.

### train4 — multi-head attention and a layer loop

Two changes:

1. **Multi-head**: split the embedding into `n_head` chunks, run a separate
   attention on each, concatenate. Why? Each head can specialize. One head
   might track "vowel after consonant," another "what was the first letter."
   Empirically this helps; the parameter count stays the same as one big
   head.
2. **Layer loop**: stack the transformer block `n_layer` times, with
   layer-prefixed parameter names so the optimizer can find them.

After this file the **architecture** is identical to the final `train.py`.
The only thing left is the optimizer.

### train5 — Adam

SGD takes the same step size for every parameter and has no memory. Adam
keeps two running averages per parameter:

- **First moment** (mean of gradients) — momentum. Smooths out noise and
  keeps moving in directions that have been consistent.
- **Second moment** (mean of squared gradients) — per-parameter learning
  rate. Parameters with consistently large gradients get smaller effective
  steps.

The result is faster convergence and less hyperparameter babysitting. Same
model, lower loss in the same number of steps. This is `train.py`. We are
done.

## What microgpt is not

microgpt is the **algorithmic** core of an LLM. It is not the **engineering**
core. To go from microgpt to a frontier model you would add:

- A subword tokenizer (BPE) instead of single characters.
- Tensors and a GPU. The `Value` class is a few thousand times slower than
  PyTorch on the same algorithm.
- Trillions of tokens of training data instead of 32k names.
- Hundreds of layers, billions of parameters.
- Mixed precision, distributed training, gradient checkpointing, FlashAttention,
  and a thousand other tricks that buy speed but not new ideas.
- Post-training: supervised fine-tuning, RLHF / RLAIF, tool use.

None of these change the algorithm. They change what scale the algorithm can
run at. The fact that you can write the algorithm in 200 lines of pure Python
is the point of this lecture.

## Resources

- Karpathy, *microgpt* blog post — https://karpathy.ai/microgpt.html
- Final single-file gist (`microgpt.py`) — https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95
- Build progression gist (`build_microgpt.py`) — https://gist.github.com/karpathy/561ac2de12a47cc06a23691e1be9543a
- Predecessors worth knowing: **micrograd** (autograd in 100 lines), **makemore**
  (the names dataset and the bigram → MLP → transformer progression on it),
  **nanoGPT** (the same idea at scale, in PyTorch).

## Hands-on

See `handson/README_en.md`. Six files, six steps, in order. Read, run, diff.
