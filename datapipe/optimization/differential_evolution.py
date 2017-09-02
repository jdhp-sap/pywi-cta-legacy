#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__all__ = []

import json
from scipy import optimize
from datapipe.optimization.objectivefunc.wavelets_mrfilter_delta_psi_sigma_scipy import ObjectiveFunction

import datapipe.denoising.cdf
from datapipe.denoising.inverse_transform_sampling import EmpiricalDistribution

def main():

    instrument = "astri"
    #instrument = "astri_konrad"
    #instrument = "flashcam"
    #instrument = "lstcam"
    #instrument = "nectarcam"

    if instrument == "astri":

        noise_distribution = EmpiricalDistribution(datapipe.denoising.cdf.ASTRI_CDF_FILE)
        input_files = ["/dev/shm/.jd/astri/gamma/"]

    elif instrument == "astri_konrad":

        noise_distribution = EmpiricalDistribution(datapipe.denoising.cdf.ASTRI_CDF_FILE)
        input_files = ["/dev/shm/.jd/astri_konrad/gamma/"]

    elif instrument == "flashcam":

        noise_distribution = EmpiricalDistribution(datapipe.denoising.cdf.FLASHCAM_CDF_FILE)
        input_files = ["/dev/shm/.jd/flashcam/gamma/"]

    elif instrument == "lstcam":

        noise_distribution = EmpiricalDistribution(datapipe.denoising.cdf.LSTCAM_CDF_FILE)
        input_files = ["/dev/shm/.jd/lstcam/gamma/"]

    elif instrument == "nectarcam":

        noise_distribution = EmpiricalDistribution(datapipe.denoising.cdf.NECTARCAM_CDF_FILE)
        input_files = ["/dev/shm/.jd/nectarcam/gamma/"]

    else:

        raise Exception("Unknown instrument", instrument)

    func = ObjectiveFunction(input_files=input_files,
                             noise_distribution=noise_distribution,
                             max_num_img=None)

    bounds = ((0.5, 6), (0.5, 6), (0.5, 6), (0.5, 6))

    x_list = []
    fx_list = []

    def callback(xk, convergence):
        x_list.append(xk.tolist())
        fx_list.append(float(func(xk)))

        fx_best = min(fx_list)
        fx_best_index = fx_list.index(fx_best)
        x_best = x_list[fx_best_index]

        print("{}: f({})={} ({}) ; best ({}): f({})={}".format(len(x_list), x_list[-1], fx_list[-1], convergence, fx_best_index, x_best, fx_best))

        res_dict = {
                    "best_solution": x_best,
                    "best_score": float(fx_best),
                    "solutions": x_list,
                    "scores": fx_list
                   }

        with open("optimize_sigma_diff_evo.json", "w") as fd:
            json.dump(res_dict, fd, sort_keys=True, indent=4)  # pretty print format

    res = optimize.differential_evolution(func,
                                          bounds,
                                          maxiter=50,         # The number of iterations
                                          popsize=10,
                                          callback=callback,
                                          #polish=False,
                                          disp=False)          # Print status messages

    print("x* =", res.x)
    print("f(x*) =", res.fun)
    print("Cause of the termination:", res.message)
    print("Number of evaluations of the objective functions:", res.nfev)
    print("Number of iterations performed by the optimizer:", res.nit)

    # SAVE RESULTS ############################################################

    res_dict = {
                "best_solution": res.x.tolist(),
                "best_score": float(res.fun),
                "solutions": x_list,
                "scores": fx_list
               }

    with open("optimize_sigma_diff_evo.json", "w") as fd:
        json.dump(res_dict, fd, sort_keys=True, indent=4)  # pretty print format


if __name__ == "__main__":
    main()

