#%% Imports

try:
    from models.model_embed import *
except Exception:
    from model_embed import *

import torch
import torch.nn as nn
from performer_pytorch import Performer

import math
import torch.nn.functional as F
import copy

#%% Tranformer Reconfiguration

def transConfig(cfg):
    cfg_layer = copy.deepcopy(cfg.transformer)
    num_layers = cfg_layer.pop('num_layers')
    cfg_trans = {
        'encoder_layer' : nn.TransformerEncoderLayer(**cfg_layer),
        'num_layers'    : num_layers,  
    }
    return cfg_trans

#%% BottleNeck Class

class BottleNeck(nn.Module):
    def __init__(self, cfg):
        self.idFlag = False
        super(BottleNeck, self).__init__()
        if hasattr(cfg, 'performer'):
            self.embedder = Embedder(**cfg.embedder)
            self.transformer = Performer(**cfg.performer)
        elif hasattr(cfg, 'transformer'):
            self.embedder = Embedder(**cfg.embedder)
            self.transformer = nn.TransformerEncoder(**transConfig(cfg))
        else:
            self.idFlag = True
        
    def forward(self, x):
        if self.idFlag == True:
            y = x
        else:
            z = self.embedder(x)
            t = self.transformer(z)
            y = depatcher(t, self.embedder.unfold_shape)
        return y