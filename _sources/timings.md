# Timings

All timings have been measured on an NVIDIA GeForce RTX 5090.


## Timings

`y = alpha * x` and `y += alpha * x`

```{image} pictures/timing_copyvec.png
:width: 40%
:align: center
```


`C = A*B` (using cublas)

with $A$ is $m \times m$, and $B$ is $m \times n$.

```{image} pictures/timing_matmat.png
:width: 40%
:align: center
```

