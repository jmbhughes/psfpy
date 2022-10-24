import inspect
from numbers import Real
from typing import Any

import numpy as np
import matplotlib.pyplot as plt

from psfpy import simple_psf, varied_psf, FunctionalCorrector, ArrayCorrector
from psfpy.corrector import calculate_covering


@simple_psf
def gaussian(x, y, x0, y0, sigma_x, sigma_y):
    return np.exp(-(np.square(x-x0)/(2*np.square(sigma_x)) + np.square(y-y0)/(2*np.square(sigma_y))))


@simple_psf
def target_model(x, y):
    x0 = 16
    y0 = 16
    sigma_x = 3
    sigma_y = 3
    return np.exp(-(np.square(x-x0)/(2*np.square(sigma_x)) + np.square(y-y0)/(2*np.square(sigma_y))))


@varied_psf(gaussian)
def my_psf(x: Real | np.ndarray, y: Real | np.ndarray) -> dict[str, Any]:
    return {
        "x0": 16,
        "y0": 16,
        "sigma_x": (x+1)*3,
        "sigma_y": (y+1)*4
    }


if __name__ == "__main__":
    show_steps = True

    uncorrected_image = np.zeros((1048, 1048))

    my_model = FunctionalCorrector(my_psf, target_model)
    if show_steps:
        corners = calculate_covering(uncorrected_image.shape, 250)
        array_corrector = my_model.evaluate_to_array_form(corners[:, 0], corners[:, 1], 250)
        corrected_image = array_corrector.correct_image(uncorrected_image)
    else:
        corrected_image = my_model.correct_image(uncorrected_image, 250)

    fig, axs = plt.subplots(ncols=2, sharex=True, sharey=True)
    axs[0].imshow(uncorrected_image)
    axs[1].imshow(uncorrected_image)
    plt.show()

    #array_corrector = my_model.evaluate_to_array_form(np.arange(10), np.arange(10), 10)
    # array_corrector.save("array_corrector.corr")
    # loaded = ArrayCorrector.load("array_corrector.corr")
    # print(type(loaded))
    # evaluated_model = my_model.evaluate(np.arange(100), np.arange(100), 100)
    # print(evaluated_model[0, 0])
    # corrected_image = evaluated_model.correct_image(uncorrected_image)
