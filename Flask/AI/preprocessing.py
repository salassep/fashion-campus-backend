import torch
import numpy
from PIL import Image
from .initialization_model import FashionCNN
from .image_helpers import encode, decode


def prepro(base64):
    img = decode(base64)

    with torch.no_grad():
    #Choose folder with numbers 1/ You can change this to any numbers folder
        path = Image.open("image.jpg").convert(mode="L")
        img = path.resize((28, 28))

    #Prepare image for model
        img = numpy.array(img)
        img = numpy.expand_dims(img, axis=0)
        g = (img / 255.0).astype(numpy.float32)
        g = numpy.expand_dims(g, axis=0)
        y = torch.from_numpy(g)

        return y

