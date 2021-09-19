import importlib.util

def getit_getter(name, split_ext_nu=None):
    if split_ext_nu is None:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s.py"%name)
    else:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s/%s.py"%(split_ext_nu,name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.model_params.getit

def getit_featmapvars_getter(name, split_ext_nu=None):
    if split_ext_nu is None:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s.py"%name)
    else:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s/%s.py"%(split_ext_nu,name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.model_params.getit, mod.model_params.featmap_vars


def featmap_getter(name, split_ext_nu=None):
    if split_ext_nu is None:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s.py"%name)
    else:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s/%s.py"%(split_ext_nu,name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.model_params.featmap


def params_getter(name, split_ext_nu=None):
    if split_ext_nu is None:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s.py"%name)
    else:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s/%s.py"%(split_ext_nu,name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.model_params


def getit_getter_df(name, df, split_ext_nu=None):
    if split_ext_nu is None:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s.py"%name)
    else:
        spec = importlib.util.spec_from_file_location("module_name", "params/%s/%s.py"%(split_ext_nu,name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    df = mod.model_params.getit_df(df)
    cols = [c for c in df.columns]
    allowed_cols = [l.split()[1].strip() for l in open(mod.model_params.featmap).readlines()]
    cols_to_drop = []
    for col in cols:
        if col not in allowed_cols:
            cols_to_drop.append(col)
    if len(cols_to_drop) > 0:
        df.drop(columns=cols_to_drop,inplace=True)
    return df[allowed_cols]
