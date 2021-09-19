import argparse
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--model_name", help="",action="store_true")
group.add_argument("--featmap", help="", action="store_true")
group.add_argument("--split", help="", action="store_true")
parser.add_argument("--split_ext_nu",help="",action="store_true")
args = parser.parse_args()
if args.model_name:
    from model_params import model_params
    print(model_params.name)
elif args.featmap:
    from model_params import model_params
    if args.split_ext_nu:
        from getit_getter import featmap_getter
        print(featmap_getter(model_params.name,'ext'),featmap_getter(model_params.name,'nu'))
    else:
        print(model_params.featmap)
elif args.split:
    from model_params import model_params
    try:
        print(model_params.split)
    except:
        print(0)
else:
    raise
