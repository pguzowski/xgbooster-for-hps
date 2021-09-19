import importlib.util
spec = importlib.util.spec_from_file_location("module_name", "params/no_scale_eta_0.3.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

model_params = foo.model_params

