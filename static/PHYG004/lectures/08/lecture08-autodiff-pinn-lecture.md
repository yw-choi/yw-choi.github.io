# Lecture 08: Automatic Differentiation & Physics-Informed Neural Networks

---

## Part 1: Automatic Differentiation (10 min)

### Derivatives in Physics

Forces from potentials. Equations of motion from Lagrangians. Response functions from free energies:

$$\mathbf{F} = -\nabla V, \qquad \frac{d}{dt}\frac{\partial L}{\partial \dot{q}} = \frac{\partial L}{\partial q}, \qquad \chi = -\frac{\partial^2 F}{\partial h^2}$$

How do we compute these on a computer?

| Method | Exact? | Cost | Limitation |
|--------|--------|------|------------|
| Symbolic | Yes | High | Expression swell — grows exponentially |
| Finite difference | No | Low | Step-size dilemma |
| **Autodiff** | **Yes** | **Low** | Needs a framework |

### Why Not Finite Differences?

$$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$$

Large $h$ gives truncation error $O(h^2)$. Small $h$ triggers floating-point cancellation. There is no universally good $h$:

![Finite difference error vs step size](https://upload.wikimedia.org/wikipedia/commons/4/41/AbsoluteErrorNumericalDifferentiationExample.png)
*Fig 1. Error of numerical differentiation vs step size. Truncation error dominates at large $h$ (right), cancellation error at small $h$ (left). Autodiff avoids this entirely. [Wikipedia, CC-BY-SA]*

### Autodiff: A Worked Example

Consider computing $e = (a + b) \times (b + 1)$. We break it into elementary steps:

$$c = a + b, \qquad d = b + 1, \qquad e = c \times d$$

This defines a **computational graph**. Each edge carries a local partial derivative:

$$\frac{\partial c}{\partial a} = 1, \quad \frac{\partial c}{\partial b} = 1, \quad \frac{\partial d}{\partial b} = 1, \quad \frac{\partial e}{\partial c} = d, \quad \frac{\partial e}{\partial d} = c$$

The chain rule gives the end-to-end derivative by **multiplying along paths** and **summing over paths**:

$$\frac{\partial e}{\partial b} = \frac{\partial e}{\partial c}\frac{\partial c}{\partial b} + \frac{\partial e}{\partial d}\frac{\partial d}{\partial b} = d \cdot 1 + c \cdot 1$$

The question is: in which **order** do we evaluate this? Two strategies:

**Forward mode** — fix one input (here $b$), push its derivative forward through the graph:

$$\frac{\partial c}{\partial b} = 1 \;\to\; \frac{\partial d}{\partial b} = 1 \;\to\; \frac{\partial e}{\partial b} = d \cdot 1 + c \cdot 1$$

One pass gives $\partial e / \partial b$. To get $\partial e / \partial a$, we need a separate pass.

![Forward-mode autodiff](https://colah.github.io/posts/2015-08-Backprop/img/tree-forwradmode.png)
*Fig 2a. Forward mode computing $\partial e / \partial b$ on the graph $e = (a+b)(b+1)$. Each node accumulates the derivative of that node w.r.t. $b$, propagating left to right. [7]*

**Reverse mode** — start from the output $e$, pull derivatives backward:

$$\frac{\partial e}{\partial e} = 1 \;\to\; \frac{\partial e}{\partial c} = d, \;\; \frac{\partial e}{\partial d} = c \;\to\; \frac{\partial e}{\partial a} = d, \;\; \frac{\partial e}{\partial b} = d + c$$

One pass gives derivatives w.r.t. **all inputs at once**.

![Reverse-mode autodiff](https://colah.github.io/posts/2015-08-Backprop/img/tree-backprop.png)
*Fig 2b. Reverse mode on the same graph. Each node accumulates the derivative of $e$ w.r.t. that node, propagating right to left. One pass yields both $\partial e / \partial a$ and $\partial e / \partial b$. [7]*

| | Forward mode | Reverse mode |
|--|-------------|-------------|
| One pass gives | $\partial(\text{all outputs}) / \partial(\text{one input})$ | $\partial(\text{one output}) / \partial(\text{all inputs})$ |
| Efficient when | Few inputs (e.g., Jacobian column) | Few outputs (e.g., scalar loss) |

> Training a neural network = minimize a scalar loss $L(\theta_1, \dots, \theta_n)$ with $n \sim 10^6$ parameters. Reverse mode gives all $n$ gradients in one backward pass — this is backpropagation. [1]

### Autodiff in JAX

```python
import jax

jax.grad(f)                    # first derivative
jax.grad(jax.grad(f))         # second derivative
jax.hessian(f)                 # full Hessian matrix
jax.vmap(jax.grad(f))         # gradient at many points (batched)
```

Physics example — force and curvature from a potential:

```python
def V(r):
    return 4 * ((1/r)**12 - (1/r)**6)   # Lennard-Jones

force    = lambda r: -jax.grad(V)(r)             # F = -dV/dr
curv     = jax.grad(jax.grad(V))                 # V''(r) = curvature
forces   = jax.vmap(lambda r: -jax.grad(V)(r))   # forces at many r
```

For a multi-dimensional potential, `jax.hessian(V)` at a minimum gives the dynamical matrix — its eigenvalues are the squared normal mode frequencies $\omega_i^2$. This generalizes to phonon calculations in crystals.

We've used autodiff to compute forces from a **known** potential. But what if we don't know the solution — only the equation it must satisfy?

---

## Part 2: Physics-Informed Neural Networks (15 min)

### From Autodiff to PDE Solving

Autodiff can differentiate any function w.r.t. its inputs — including a neural network. If a network takes coordinates $x$ as input and outputs $u_\theta(x)$, then autodiff gives $\frac{\partial u_\theta}{\partial x}$, $\frac{\partial^2 u_\theta}{\partial x^2}$, etc. These are exactly the terms that appear in a PDE.

This is the key idea behind Physics-Informed Neural Networks [2]: use a neural network as a **trial solution**, and train it so that the PDE is satisfied. If you've seen the Ritz variational method — where you minimize energy over a family of trial functions — PINNs are the same idea, but the trial function is a neural network instead of a linear combination of basis functions.

### How PINNs Work

Given a boundary-value problem:

$$\mathcal{D}[u](x) = f(x), \quad x \in \Omega; \qquad u(x) = g(x), \quad x \in \partial\Omega$$

PINNs [2] proceed in four steps:

1. Parametrize the solution as a neural network $u_\theta(x)$
2. Autodiff computes $\frac{\partial u_\theta}{\partial x}$, $\frac{\partial^2 u_\theta}{\partial x^2}$, ... (w.r.t. **input** $x$)
3. Define a loss measuring how well the PDE and BCs are satisfied
4. Minimize the loss via gradient descent (w.r.t. **weights** $\theta$, via backprop)

Note the dual role of autodiff: step 2 differentiates w.r.t. the network *input* $x$; step 4 differentiates w.r.t. the network *weights* $\theta$.

![PINN architecture](https://ar5iv.labs.arxiv.org/html/2201.05624/assets/info_pinn.png)
*Fig 3. PINN schematic. The network maps coordinates to the solution. Autodiff (w.r.t. $x$) provides the PDE derivatives. The loss combines the PDE residual, boundary conditions, and optional data. Backprop (w.r.t. $\theta$) updates the weights. [3]*

### Loss Function

$$\mathcal{L} = \underbrace{\frac{1}{N}\sum_{i=1}^{N}\left(\mathcal{D}[u_\theta](x_i) - f(x_i)\right)^2}_{\mathcal{L}_{\text{pde}}} + \; w_{\text{bc}} \underbrace{\frac{1}{M}\sum_{j=1}^{M}\left(u_\theta(x_j) - g(x_j)\right)^2}_{\mathcal{L}_{\text{bc}}}$$

- **Collocation points** $\{x_i\}_{i=1}^N$: sampled inside the domain — no mesh needed
- **Unsupervised**: the equation itself is the training signal
- **Flexible**: change the PDE, add data, solve inverse problems — just modify the loss

### Example: Poisson Equation

$$u''(x) = -\sin(x), \qquad u(0) = 0, \quad u(\pi) = 0$$

```python
# pseudocode — in real JAX, use argnums to select which argument to differentiate
def pinn_loss(params, x_colloc):
    u    = network(params, x_colloc)         # u_θ(x)
    u_xx = d2_dx2(network)(params, x_colloc) # autodiff w.r.t. x
    L_pde = mean((u_xx + sin(x_colloc))**2)
    L_bc  = network(params, 0.0)**2 + network(params, pi)**2
    return L_pde + 10.0 * L_bc
```

### Limitations

PINNs are not a silver bullet:

- **Convergence**: slower than finite elements for standard well-posed problems
- **Loss balancing**: PDE and BC gradients can differ by orders of magnitude, causing one term to dominate training [4]
- **Spectral bias**: networks learn low-frequency components first; sharp features converge slowly [5]

### Today's Hands-on: Quantum Harmonic Oscillator

We apply PINNs to the time-independent Schrödinger equation [6] in atomic units:

$$-\frac{1}{2}\psi''(x) + \frac{1}{2}x^2\,\psi(x) = E\,\psi(x)$$

| Component | Role |
|-----------|------|
| $\psi_\theta(x)$ | Network output (wavefunction) |
| $\psi''(x)$ | Autodiff w.r.t. $x$: `jax.grad(jax.grad(psi_fn, argnums=1), argnums=1)` |
| $E$ | Trainable scalar (energy eigenvalue) |
| $\mathcal{L}_{\text{pde}}$ | Schrödinger equation residual |
| $\mathcal{L}_{\text{norm}}$ | $\left(\int\psi^2\,dx - 1\right)^2$ — normalization |
| $\mathcal{L}_{\text{bc}}$ | $\psi(x_{\min})^2 + \psi(x_{\max})^2$ — bound-state decay |

**Expected result**: $E \to 0.5$, $\;\psi(x) \to \pi^{-1/4}\exp(-x^2/2)$

We pick this problem because the exact answer is known — you can verify the PINN works before applying it where analytic solutions don't exist.

---

## References

[1] A. G. Baydin, B. A. Pearlmutter, A. A. Radul, J. M. Siskind. "Automatic Differentiation in Machine Learning: a Survey." *J. Mach. Learn. Res.* **18**(153):1–43, 2018. [arXiv:1502.05767](https://arxiv.org/abs/1502.05767)

[2] M. Raissi, P. Perdikaris, G. E. Karniadakis. "Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations." *J. Comput. Phys.* **378**:686–707, 2019. [DOI:10.1016/j.jcp.2018.10.045](https://doi.org/10.1016/j.jcp.2018.10.045)

[3] S. Cuomo, V. S. di Cola, F. Giampaolo, G. Rozza, M. Raissi, F. Piccialli. "Scientific Machine Learning through Physics-Informed Neural Networks: Where we are and What's Next." *J. Sci. Comput.* **92**:88, 2022. [arXiv:2201.05624](https://arxiv.org/abs/2201.05624)

[4] S. Wang, Y. Teng, P. Perdikaris. "Understanding and mitigating gradient flow pathologies in physics-informed neural networks." *SIAM J. Sci. Comput.* **43**(5):A3055–A3081, 2021. [arXiv:2001.04536](https://arxiv.org/abs/2001.04536)

[5] N. Rahaman et al. "On the Spectral Bias of Neural Networks." *ICML*, 2019. [arXiv:1806.08734](https://arxiv.org/abs/1806.08734)

[6] P. Jin, S. Mattheakis, P. Protopapas. "Physics-Informed Neural Networks for Quantum Eigenvalue Problems." 2022. [arXiv:2203.00451](https://arxiv.org/abs/2203.00451)

[7] C. Olah. "Calculus on Computational Graphs: Backpropagation." 2015. [colah.github.io](https://colah.github.io/posts/2015-08-Backprop/)

### Figure Sources

- Fig 1: [Wikipedia: Numerical differentiation](https://en.wikipedia.org/wiki/Numerical_differentiation), CC-BY-SA
- Fig 2a, 2b: Olah [7], computational graph for $e = (a+b)(b+1)$
- Fig 3: Cuomo et al. [3], arXiv open access
