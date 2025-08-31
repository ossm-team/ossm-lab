# OSSM Lab

`ossm-lab` provides the **analysis lab** of the OSSM ecosystem.  
It implements standardized pipelines and methods to evaluate models on tasks, ensuring results are comparable and reproducible.  
It is one of the core packages of the [OSSM ecosystem](https://github.com/ossm-team), supported by the [NWO Open Science Fund](https://www.nwo.nl/en/researchprogrammes/open-science/open-science-fund).

## Vision

This package is part of an **open, community-driven ecosystem** for computational sensorimotor neuroscience. By standardizing evaluation methods, benchmarks, and metrics, `ossm-lab` allows researchers to **systematically compare models** and build cumulative scientific knowledge. The long-term goal is a community lab of analysis tools that grows alongside the model and task catalogues.

## Features

Please note that `ossm-lab` is under early development. Features are incomplete.

- **Standardized pipelines**: Consistent analysis structure inspired.  
- **Benchmark metrics**: Compare models on performance, mechanisms, and data alignment.  
- **Extensible**: Easy to add new analysis methods using a registry/decorator system.  

## Install

Requires **Python 3.11+**.

```bash
pip install -e .
```

## Related Packages

- [`ossm-base`](https://github.com/ossm-team/ossm-base) – shared types and utilities  
- [`ossm-models`](https://github.com/ossm-team/ossm-models) – model catalogue & SMS standard  
- [`ossm-tasks`](https://github.com/ossm-team/ossm-tasks) – task catalogue & STEF standard  

## Contribution

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md).  

## License

GPL-3.0. See [LICENSE](./LICENSE).
