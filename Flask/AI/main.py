from .preprocessing import prepro
from .inferences import load
from .postprocessing import predict

# * Define image
path_image = "jury_test/mnist_358.png"

def input_image(base64_str):
    # * PREPROCESSING
    result_image = prepro(base64_str)

    # * INFERENCE
    model = load()

    # * POSTPROCESSING
    category_res = predict(model, result_image)

    return category_res

if __name__ == "__main__":
    # * PREPROCESSING
    result_image = prepro(path_image)

    # * INFERENCE
    model = load()

    # * POSTPROCESSING
    predict(model, result_image)



