# Copula
This is the official implementation in Python for: 

[[Paper](https://arxiv.org)]

If you find this code useful, please consider citing:

```
@article{doi:10.1080/14697688.2018.1562197,
author = {Veni Arakelian and Petros Dellaportas and Roberto Savona and Marika Vezzoli},
title = {Sovereign risk zones in Europe during and after the debt crisis},
journal = {Quantitative Finance},
volume = {19},
number = {6},
pages = {961-980},
year  = {2019},
publisher = {Routledge},
doi = {10.1080/14697688.2018.1562197},
URL = {https://doi.org/10.1080/14697688.2018.1562197},
eprint = {https://doi.org/10.1080/14697688.2018.1562197}
```

## Installation
```
git clone https://github.com/PetropoulakisPanagiotis/copula.git
cd copula
pip install .
```

## Run an artificial example 
```
cd copula/copula
change the path in laplacetest_volatility.py line 10: 
df = read_excel("/home/petropoulakis/Desktop/copula-master/data/artificial_data_iosif.xlsx", sheet_name='Sheet1')  
python laplacetest_volatility.py
```
### Contributors 
* Petropoulakis Panagiotis petropoulakispanagiotis@gmail.com

###### Acknowledgements
* [ambhas](https://github.com/neel9102/ambhas/blob/master/ambhas/copula.py) repository for the parameter estimation of copula
