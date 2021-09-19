.DELETE_ON_ERROR:

MODNAME := $(shell python get_info.py --model_name)
SPLITEXTNU := $(shell python get_info.py --split)
ifeq ($(SPLITEXTNU),1)
  SPLIT := --split_ext_nu
  FMAPS := $(shell python get_info.py --featmap --split_ext_nu)
  FMAP_EXT := $(filter %ext.txt,$(FMAPS))
  FMAP_NU := $(filter %nu.txt,$(FMAPS))
else
  FMAPS := $(shell python get_info.py --featmap)
  FMAP_EXT := $(FMAPS)
  FMAP_NU := $(FMAPS)
endif

SOUTPUTS := $(patsubst ../signals/fulltree/%,%,$(wildcard ../signals/fulltree/r*.root))
BOUTPUTS := $(patsubst ../backgrounds/fulltree/%,%,$(wildcard ../backgrounds/fulltree/*.root))

BDT_SDIR := ../signals/bdt_out/$(MODNAME)
BDT_BDIR := ../backgrounds/bdt_out/$(MODNAME)

OUTPUTS_R1 := $(foreach BN,$(filter-out %r3.root,$(BOUTPUTS)),$(BDT_BDIR)/$(BN)) \
	      $(foreach BN,$(filter-out r3%,$(SOUTPUTS)),$(BDT_SDIR)/$(BN))
OUTPUTS_R3 := $(foreach BN,$(filter-out %r1.root,$(BOUTPUTS)),$(BDT_BDIR)/$(BN)) \
	      $(foreach BN,$(filter-out r1%,$(SOUTPUTS)),$(BDT_SDIR)/$(BN))

OUTPUTS_R1 := $(foreach BN,$(filter-out %r3.root,$(BOUTPUTS)),$(BDT_BDIR)/$(BN)) \
	      $(foreach BN,$(filter-out r3%,$(SOUTPUTS)),$(BDT_SDIR)/$(BN))
OUTPUTS_R3 := $(foreach BN,$(filter-out %r1.root,$(BOUTPUTS)),$(BDT_BDIR)/$(BN)) \
	      $(foreach BN,$(filter-out r1%,$(SOUTPUTS)),$(BDT_SDIR)/$(BN))


MODELDIR := models/$(MODNAME)
MODEL_E_R1 := $(MODELDIR)/model_r1.json
MODEL_N_R1 := $(MODELDIR)/nu_model_r1.json
MODEL_E_R3 := $(MODELDIR)/model_r3.json
MODEL_N_R3 := $(MODELDIR)/nu_model_r3.json
MODELS_R1 := $(MODEL_E_R1) $(MODEL_N_R1)
MODELS_R3 := $(MODEL_E_R3) $(MODEL_N_R3)

TRAIN_R1 := ../signals/to_bdt/training_fhc.root ../backgrounds/to_bdt/ana_ext_r1_train.root ../backgrounds/to_bdt/ana_ext_r1_test.root ../backgrounds/to_bdt/ana_nu_fhc_r1_train.root
TRAIN_R3 :=  ../signals/to_bdt/training_rhc.root ../backgrounds/to_bdt/ana_ext_r3_train.root ../backgrounds/to_bdt/ana_ext_r3_test.root ../backgrounds/to_bdt/ana_nu_rhc_r3_train.root

PARAMS := params/$(MODNAME).py

NUMROUNDDIR := numbers/$(MODNAME)
ifneq ("$(wildcard $(NUMROUNDDIR)/e_r1.txt)","")
  NUMROUND_E_R1_FILE := $(NUMROUNDDIR)/e_r1.txt
  NUMROUND_E_R1 := -n $(shell cat $(NUMROUND_E_R1_FILE))
endif
ifneq ("$(wildcard $(NUMROUNDDIR)/n_r1.txt)","")
  NUMROUND_N_R1_FILE := $(NUMROUNDDIR)/n_r1.txt
  NUMROUND_N_R1 := -n $(shell cat $(NUMROUND_N_R1_FILE))
endif
ifneq ("$(wildcard $(NUMROUNDDIR)/e_r3.txt)","")
  NUMROUND_E_R3_FILE := $(NUMROUNDDIR)/e_r3.txt
  NUMROUND_E_R3 := -n $(shell cat $(NUMROUND_E_R3_FILE))
endif
ifneq ("$(wildcard $(NUMROUNDDIR)/n_r3.txt)","")
  NUMROUND_N_R3_FILE := $(NUMROUNDDIR)/n_r3.txt
  NUMROUND_N_R3 := -n $(shell cat $(NUMROUND_N_R3_FILE))
endif


test:
	@#echo $(MODNAME)
	@#echo $(FMAP)
	@#echo $(OUTPUTS_R3)
	echo "$(OUTPUTS_R3)"
.PHONY: test

# only need to remake feature maps if output_tree_format.h has changed
ifeq ($(SPLITEXTNU),1)
$(FMAP_EXT): ../scripts/output_tree_format.h 
	python make_featmap.py -m $(MODNAME) --split_ext_nu ext > $@
$(FMAP_NU): ../scripts/output_tree_format.h 
	python make_featmap.py -m $(MODNAME) --split_ext_nu nu > $@
else
$(FMAPS): ../scripts/output_tree_format.h 
	python make_featmap.py -m $(MODNAME) > $@
endif

$(MODELDIR)/:
	mkdir -p $@
$(BDT_SDIR)/:
	mkdir -p $@
$(BDT_BDIR)/:
	mkdir -p $@

$(MODEL_E_R1): $(TRAIN_R1) $(PARAMS) $(FMAP_EXT) $(NUMROUND_E_R1_FILE) | $(MODELDIR)/
	( time nice python train.py --run 1 --model $(MODNAME) $(NUMROUND_E_R1) $(SPLIT); ) > $(MODELDIR)/log_train_r1.log 2>&1 
	
$(MODEL_N_R1): $(TRAIN_R1) $(PARAMS) $(FMAP_NU) $(NUMROUND_N_R1_FILE) | $(MODELDIR)/
	( time nice python train_v_nu.py --run 1 --model $(MODNAME) $(NUMROUND_B_R1) $(SPLIT); ) > $(MODELDIR)/log_nu_train_r1.log 2>&1
	
$(MODEL_E_R3): $(TRAIN_R3) $(PARAMS) $(FMAP_EXT) $(NUMROUND_E_R3_FILE) | $(MODELDIR)/
	( time nice python train.py --run 3 --model $(MODNAME) $(NUMROUND_E_R3) $(SPLIT); ) > $(MODELDIR)/log_train_r3.log 2>&1
	
$(MODEL_N_R3): $(TRAIN_R3) $(PARAMS) $(FMAP_NU) $(NUMROUND_N_R3_FILE) | $(MODELDIR)/
	( time nice python train_v_nu.py --run 3 --model $(MODNAME) $(NUMROUND_N_R3) $(SPLIT); ) > $(MODELDIR)/log_nu_train_r3.log 2>&1

$(OUTPUTS_R1): $(MODELS_R1) | $(BDT_SDIR)/ $(BDT_BDIR)/
	python eval_tree.py --run 1 --model $(MODNAME) -i $(subst /bdt_out/$(MODNAME)/,,$(dir $@))/to_bdt/$(notdir $@) -o $@ $(SPLIT)

$(OUTPUTS_R3): $(MODELS_R3) | $(BDT_SDIR)/ $(BDT_BDIR)/
	python eval_tree.py --run 3 --model $(MODNAME) -i $(subst /bdt_out/$(MODNAME)/,,$(dir $@))/to_bdt/$(notdir $@) -o $@ $(SPLIT)

run1: $(OUTPUTS_R1)
.PHONY: run1

run3: $(OUTPUTS_R3)
.PHONY: run3

all: run1 run3
.PHONY: all
