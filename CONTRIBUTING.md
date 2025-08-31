# Contributing to `ossm-lab`

The `ossm-lab` package provides the **analysis lab** of the OSSM ecosystem and will implement standardized methods 
for model evaluation.

## How to Contribute
- **Issues**: Use GitHub Issues to report bugs, request features, or propose new analysis methods.  
- **Pull Requests**: Fork the repo, create a feature branch, and open a PR. Keep PRs focused and provide a clear description.  
- **Discussions**: Use GitHub Discussions for design proposals or standards questions.

## Adding an Analysis Method
When contributing a new method:
1. Implement it under `ossm_lab/` following the existing pipeline structure.  
2. Register it using the provided decorator/registry system.  
3. Add minimal tests to `tests/`.  
4. Document the method with usage examples where possible.  

## Code Style
- Follow **PEP 8** for Python code.  
- Keep APIs consistent with the existing analysis pipeline.  

## Tests & Validation
- Ensure all tests pass locally before submitting a PR.  
- Add unit tests covering new functionality.  

## Licensing
All contributions are released under **GPL-3.0**. By contributing, you agree to this license.

## Code of Conduct
All contributors must follow the project’s [Code of Conduct](../CODE_OF_CONDUCT.md).
