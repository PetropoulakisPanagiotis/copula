from scipy.stats import norm, expon
from scipy.optimize import minimize
from scipy.linalg import det, inv
from math import pi
import numpy as np
from allnorm import allnorm
from copulalib import Copula

def allgumbel(x, y):

    sample = len(x)

    # Convert to normall #
    result = allnorm(x, y)

    u = result["u"]
    v = result["v"]
    sigma = result["sigma"]
    hes_norm = result["hes_norm"]

    lu = -np.log(u)
    lv = -np.log(v)

    # x - mean, y - mean #
    xbar = x - sigma[2]
    ybar = y - sigma[3]

    # Calculate theta #
    theta = Copula(x.flatten(),y.flatten(), family='gumbel').theta

    # Find logLikelihood of theta #
    cop1 = logLikelihood(theta, lu, lv, sample, sigma, xbar, ybar, u, v) 

    # Calculate hessian of log-copula's density #
    hes = -np.sum(np.multiply((-2 * (theta ** (-2))) * (((lu ** theta) + (lv ** theta)) ** (-1)), np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))) - np.multiply((((lu ** theta) + (lv ** theta)) ** (-2)) * (-2 + (1/theta)), ((np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))) ** 2)) + (theta ** (-3))* np.multiply((2*((lu ** theta) + (lv * theta))) **(-1 + (1/theta)), (theta * (np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv)))) - np.multiply(((lu ** theta) + (lv ** theta)), np.log((lu ** theta) + (lv ** theta)))) + (theta ** (-4))*(np.multiply(np.multiply(((lu ** theta) + (lv * theta)) ** (-2 + (1/theta)), (theta * np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))) - np.multiply(((lu ** theta) + (lv ** theta)), np.log((lu ** theta) + (lv ** theta)))), ((-1 + theta) * theta) * (np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))) + np.multiply(((lu ** theta) + (lv * theta)), np.log((lu ** theta) + (lv ** theta))))) + np.multiply((-2 + (1/theta)) * (((lu ** theta) + (lv ** theta)) ** (-1)), np.multiply(lu ** theta, np.log(lu ** 2)) + np.multiply(lv ** theta, np.log(lv ** 2))) + (theta ** (-2)) * (np.multiply((((lu ** theta) + (lv * theta)) ** (-1 + (1/theta))), -theta *(np.multiply(lu ** theta, np.log(lu ** 2)) + np.multiply(lv ** theta, np.log(lv ** 2))) + np.multiply(np.log((lu ** theta) + (lv ** theta)),   np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))))) -np.divide(((np.multiply(np.multiply(theta *(lu ** theta), ((lu ** theta) + (lv ** theta)) ** (1/theta)), np.log(lu)) -np.multiply(((lu ** theta) + (lv ** theta)) ** (1 + (1/theta)), np.log((lu ** theta) + (lv ** theta))) + theta*(theta * ((lu ** theta) + (lv ** theta)) + np.multiply(np.multiply(((lu ** theta) + (lv ** theta)) ** (1/theta),lv ** theta), np.log(lv)))) ** (-2)),  np.multiply((theta ** 4) * ( -1 + theta + (((lu ** theta) + (lv ** theta)) ** (1/theta))), ((lu ** theta) + (lv ** theta)) ** 2)) + np.divide(np.multiply((((lu ** theta) + (lv ** theta)) ** (-2 + (1/theta))), np.multiply(np.multiply(np.multiply((theta ** 2) * (lu ** theta), (lu ** theta) + (lv ** theta)), np.log(lu ** 2)) + np.multiply((((lu ** theta) + (lv ** theta)) ** 2),  np.log((lu ** theta) + (lv ** theta)) ** 2) + np.multiply(np.multiply((theta ** 2) * (lv ** theta), np.log(lv)), -2 *((lu ** theta) + (lv ** theta)) + np.multiply((lu ** theta) + (lv ** theta), np.log(lv))) + np.multiply(np.multiply(2 * theta * ((lu ** theta) + (lv ** theta)), np.log((lu ** theta) + (lv ** theta))),(lu ** theta) + (lv ** theta) -(np.multiply(lv ** theta, np.log(lv)))) -np.multiply(2 * theta * (lu ** theta), np.log(lu)), np.multiply((lu ** theta) + (lv ** theta), np.log((lu ** theta) + (lv ** theta))) + theta * (((lu ** theta) + (lv ** theta)) + np.multiply((-1 + theta) * (lv ** theta), np.log(lv))))), (theta ** 4) * (-1 + theta + (((lu ** theta) + (lv ** theta)) ** (1/theta)))))

    hes_cop = - hes

    s = -sample / hes_cop
    hes_prior_cop = -1 / (s ** 2)

    log_prior = np.log(norm.pdf(theta, loc=0, scale=s)) + np.log(expon.pdf(sigma[0], scale=1)) + np.log(expon.pdf(sigma[1], scale=1))
    BF = 1
    BFu = cop1 + log_prior + 0.5 * np.log(-1/(det(hes_norm) * (hes_cop - hes_prior_cop)))
    hes = det(hes_norm) * (hes_cop - hes_prior_cop)

    result = {"theta": theta, "cop1": cop1, "hes": hes, "hes_prior_cor": hes_prior_cop, "BF": BF, "BFu": BFu}

    return result

# Log-likelihood #
def logLikelihood(theta, lu, lv, sample, sigma, xbar, ybar, u, v):

    lLikelihood = np.sum(np.log(np.exp(np.multiply(-(lu * theta) + (lv * theta), 1/theta)))) - np.sum(np.log(u) + np.log(v)) + ((-2 + (1/theta)) * np.sum(np.log((lu * theta) + (lv * theta)))) + ((theta - 1) * np.sum(np.log(lu) + np.log(lv))) + np.sum(np.log((theta - 1) + np.multiply((lu * theta) + (lv * theta), 1/theta))) - (0.5 * sample * np.log(2* pi * (sigma[1] ** 2))) - (0.5 * np.sum(xbar ** 2) / (sigma[1] ** 2)) - (0.5 * sample * np.log(2* pi * (sigma[2] ** 2))) - (0.5 * np.sum(ybar ** 2) / (sigma[2] ** 2))

    return lLikelihood

# Test #
if __name__ == "__main__":

    x = np.array([[1.17908773759908],
[1.26305581625269],
[0.771849836437448],
[1.27236806158374],
[1.06762167816921],
[0.740861130762702],
[0.882538271488752],
[1.02355726590734],
[1.34449188249146],
[1.36209400380002],
[0.79913673334245],
[1.37791557805622],
[1.34374319306538],
[0.992666794725612],
[1.1685246934324],
[0.785623440283714],
[0.960522053861197],
[1.27538919621894],
[1.16282081176698],
[1.34896521647506],
[1.08017324936976],
[0.639444744416241],
[1.20654124980114],
[1.30124181971394],
[1.09283295665557],
[1.13981033453647],
[1.13060658152297],
[0.945296134939529],
[1.08003049407135],
[0.810102755359703],
[1.10837406990635],
[0.629097247078773],
[0.881598620596058],
[0.663366614549803],
[0.740386163226934],
[1.18572465966165],
[1.10191685180286],
[0.90483497262863],
[1.32940208571446],
[0.63617473676465],
[0.969169303511085],
[0.939721946309485],
[1.14483235472524],
[1.16491948009672],
[0.822104015609906],
[0.994868065910367],
[0.972635829673485],
[1.07507704817901],
[1.11030602011362],
[1.13786249916409],
[0.881061834425424],
[1.09337350910347],
[1.07982421557545],
[0.803243908632791],
[0.763997560217006],
[0.999179854989943],
[1.34954450901568],
[0.917717872007627],
[1.04307768389809],
[0.84812353347176],
[1.13569647934816],
[0.868291697373892],
[1.00298653381559],
[1.10434938308107],
[1.24626919429533],
[1.34850439507716],
[1.02372588805625],
[0.782695949475133],
[0.792106777783728],
[0.869790711712901],
[1.1994820211648],
[0.867785043967833],
[1.17875946232039],
[0.86099828810776],
[1.29406573854451],
[0.922927140953954],
[0.82923086417587],
[0.865783418792146],
[1.05902179136753],
[0.986598993739827],
[0.92383120166892],
[1.19148898026997],
[1.04307580607798],
[1.02499261489963],
[1.27728794569314],
[0.886883620803755],
[1.13946496300102],
[1.13725433362607],
[0.939137991240478],
[1.03416618329783],
[0.713295503874875],
[0.678459396443872],
[1.01545497097545],
[1.15387674752142],
[1.30126900021867],
[0.774633079202016],
[1.03467601691077],
[0.984639655923675],
[0.547944840146526],
[0.91593424417459]])

    y = np.array([
[1.14684481952685],
[3.18504817062711],
[-0.812498965381792],
[2.38075608550868],
[0.74876576621871],
[-0.718414010468814],
[-0.101673682231141],
[1.6690246598243],
[2.93160510793243],
[3.1411064977521],
[-0.441769420402504],
[1.09251726915322],
[1.66551539344568],
[2.5694659017669],
[1.08106410039058],
[0.048338106141192],
[0.935759194840204],
[5.5315853687035],
[0.734760835378463],
[2.26186510344098],
[0.593305744008014],
[-0.797186977639064],
[-0.147886329630428],
[3.1718448528123],
[2.68440473779584],
[3.17914234379166],
[0.67309200310982],
[0.5652896134949],
[1.06677867202545],
[0.210352807664453],
[1.61407768631101],
[-1.1461056315907],
[-0.256694972660073],
[-1.6514748776315],
[-1.26397238665474],
[1.06695345469542],
[3.00439512250057],
[0.58142834914681],
[2.52031063618567],
[-1.98654881604522],
[1.95065953609182],
[0.94823171973042],
[1.57358592390263],
[2.05257365128711],
[-0.330013247325689],
[0.076715084924791],
[0.435492532364579],
[0.637915280581112],
[0.986553606194684],
[1.25661190083814],
[0.13047333332139],
[0.335842724675321],
[3.10862955175974],
[0.803979505542531],
[-0.664415953916064],
[1.11146669160805],
[1.98644333723867],
[1.73116740596053],
[1.13053221766067],
[-0.6294541095164],
[2.74035250788574],
[-0.004819572212223],
[0.618244670610043],
[1.52980911671684],
[1.0194592325218],
[1.31522674967639],
[3.11918966524197],
[0.683592347825198],
[-0.339253712432552],
[-0.669782516904158],
[1.43715509009995],
[-0.062659220458819],
[3.08230951684405],
[-1.03861479744284],
[0.719712791648805],
[-0.024856057737549],
[0.076199592945625],
[0.557049867573171],
[1.88737158618073],
[0.94752757421864],
[0.671671801208617],
[1.58855211204886],
[2.08338855762971],
[0.608245482279323],
[2.83415205755296],
[-0.21933165066182],
[1.5962115809904],
[2.23985501634217],
[1.36586873899521],
[0.284728922668134],
[-0.277385475450303],
[-1.00406952005183],
[1.2150149873182],
[1.81797779010685],
[2.21623120211885],
[-0.798319543491166],
[1.38679478212643],
[1.05522630882211],
[-2.02722095851983],
[1.20082525320018]])


    result = allgumbel(x, y)

    print(result)
