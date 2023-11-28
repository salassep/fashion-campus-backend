import torch
# import cv2
import matplotlib.pyplot as plt
from io import BytesIO
import requests
import os
import numpy 
import torch.nn as nn
import torchvision.transforms 
import torch.nn.functional as F
from PIL import Image
from collections import OrderedDict
from .initialization_model import FashionCNN

from .preprocessing import *

## Inference
# Label

def load():
    PATH = "/app/AI/best_modell.pt"
    model =FashionCNN()
    model.load_state_dict(torch.load(PATH))
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    return  model