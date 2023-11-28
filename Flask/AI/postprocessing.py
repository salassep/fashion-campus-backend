import torch
import numpy as numpy
from .inferences import load


def predict(model, y ):
   
    with torch.no_grad():
        y_pred = model(y)
        #Get prediction
        y_pred = torch.argmax(y_pred, dim=1)
        # class_names= a
        a =  y_pred.detach().numpy()[0]
        name = {
            0: "Tshirt top",
            1: "Trouser", 
            2: "Pullover",
            3: "Dress",
            4: "Coat",
            5: "Sandal",
            6: "Shirt",
            7: "Sneaker",
            8: "Bag",
            9: "Ankle Boot", 
        }

        # print("Predicted as -" , name[a])
        return name[a]
