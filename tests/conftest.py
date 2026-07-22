"""Test bootstrap: if the compiled dynare_preprocessor is absent
(pure-python environments), stub it so importing the dyno package
does not fail. When the real extension is installed, it is used."""

import sys
import types

try:  # pragma: no cover - environment-dependent
    import dynare_preprocessor  # noqa: F401
except ImportError:
    stub = types.ModuleType("dynare_preprocessor")

    class _PreprocessorException(Exception):
        pass

    stub.PreprocessorException = _PreprocessorException
    stub.UnsupportedFeatureException = _PreprocessorException
    stub.DynareModel = object
    sys.modules["dynare_preprocessor"] = stub
