from scipy.stats import norm, expon
from scipy.optimize import minimize
from scipy.linalg import det, inv
from math import pi
import numpy as np
from allnorm import allnorm
from copulalib.copulalib import Copula
from pandas import read_excel

def allfrank(x, y):

    sample = len(x)

    # Convert to normall #
    result = allnorm(x, y)

    u = result["u"]
    v = result["v"]
    sigma = result["sigma"]
    hes_norm = result["hes_norm"]

    # x - mean, y - mean #
    xbar = x - sigma[2]
    ybar = y - sigma[3]

    # Calculate theta #
    theta = Copula(x.flatten(),y.flatten(), family='frank').theta

    # Find logLikelihood of theta #
    cop1 = logLikelihood(theta, sample, sigma, xbar, ybar, u, v)

    # Calculate hessian of log-copula's density #
    hes_cop = (-sample / (theta ** 2)) - (sample * np.exp(-theta) / ((2 - np.exp(-theta)) ** 2)) + 2 * np.sum(np.divide(((-np.exp(-theta)) - (np.multiply((u + v) ** 2,   np.exp(-theta * (u+v)))) + (np.multiply(u ** 2, np.exp(-theta * u))) + (np.multiply(v ** 2, np.exp(-theta * v)))), np.exp(-theta) - 1 + np.multiply(np.exp(-theta * u) - 1, np.exp(-theta*v) - 1))) + 2 * np.sum((np.divide(((-np.exp(-theta)) + (np.multiply(u + v,   np.exp(-theta * (u+v)))) - (np.multiply(u, np.exp(-theta * u))) - (np.multiply(v, np.exp(-theta * v)))), np.exp(-theta) - 1 + np.multiply(np.exp(-theta * u) - 1, np.exp((-theta*v) - 1)))) ** 2)

    s = -sample / hes_cop
    hes_prior_cop = -1 / (s ** 2)

    if norm.pdf(theta, loc=0, scale=s) != 0:
        log_prior = np.log(norm.pdf(theta, loc=0, scale=s)) + np.log(expon.pdf(sigma[0], scale=1)) + np.log(expon.pdf(sigma[1], scale=1))
        BFu = cop1 + log_prior + 0.5 * np.log(-1/(det(hes_norm) * (hes_cop - hes_prior_cop)))
        hes = det(hes_norm) * (hes_cop - hes_prior_cop)
    else:
        theta = 0
        cop1 = 0
        log_prior = np.log(10 **(-300)) + np.log(expon.pdf(sigma[0], scale=1)) + np.log(expon.pdf(sigma[1], scale=1))
        BFu = cop1 = log_prior + 0.5 * np.log(inv(hes_norm))
        hes = det(hes_norm)

    BF = 1

    result = {"theta": theta, "cop1": cop1, "hes": hes, "hes_prior_cor": hes_prior_cop, "BF": BF, "BFu": BFu}

    return result

# Log-likelihood #
def logLikelihood(theta, sample, sigma, xbar, ybar, u, v):

    lLikelihood = (0.5 * sample * np.log(theta ** 2)) + (0.5 * sample * np.log((1 - np.exp(-theta)) ** 2)) - (theta * np.sum(u + v)) - (np.sum(np.log((np.exp(-theta) - 1 +  np.multiply(np.exp(-theta*u) - 1, np.exp(-theta*v) - 1)) ** 2))) - (0.5 * sample * np.log(2 * pi * (sigma[0] ** 2))) - (0.5 * np.sum(xbar ** 2) / (sigma[0] ** 2)) - (0.5 * sample * np.log(2 * pi * (sigma[1] ** 2))) - (0.5 * np.sum(ybar ** 2) / (sigma[1] ** 2))

    return lLikelihood

# Test #
if __name__ == "__main__":
    df = read_excel("/home/petropoulakis/Desktop/artificial_data_iosif.xlsx", sheet_name='Sheet1')
    x = []
    y = []

    for index, row in df.iterrows():
        x.append([float(row['x'])])
        y.append([float(row['y'])])

    x = np.asarray(x, dtype=np.float32)
    y = np.asarray(y, dtype=np.float32)


    result = allfrank(x, y)

    print(result)
