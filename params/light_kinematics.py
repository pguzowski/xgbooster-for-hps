class model_params:
    pass

model_params.treedef = 'light_kinematics'
import importlib.util
spec = importlib.util.spec_from_file_location("module_name", "treedefs/%s.py"%model_params.treedef)
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

model_params.getit = foo.getit
model_params.getit_df = foo.getit_df
model_params.featmap = foo.featmap
model_params.featmap_vars = foo.featmap_vars

model_params.name = 'light_kinematics'
model_params.param =  {'booster': 'dart',
        'max_depth':6,
        'eta':0.3,
        'objective':'binary:logistic',
        #'eval_metric':'auc',
        #'subsample':0.5,
        'tree_method':'hist',
        #'scale_pos_weight': float(len(data_nu_train))/float(len(data_sig_train)),
        'rate_drop': 0.1,
         'skip_drop': 0.5 }
#model_params.num_round = 600
