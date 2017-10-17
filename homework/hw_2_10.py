'''
Matthew Schaelling
Math 402
October 18, 2017
'''

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def problem57():
    # for the beta distribution
    alpha = .5
    beta = .5
    X = np.linspace(0,1,num=100)
    mean = stats.beta(alpha,beta).mean()
    sigma = stats.beta(alpha,beta).std()
    normal = stats.norm.pdf
    beta_pdf = lambda x: stats.beta(alpha, beta).pdf(x)
    beta = lambda x: stats.beta(alpha,beta).rvs(x)

    plt.figure(figsize=(15,10))
    plt.title('Beta Distribution')
    for n in [2**x for x in range(6)]:
        plt.subplot(2,3,int(np.log(n)) + 1)
        plt.title('n = {}'.format(n))
        pdf = beta_pdf(X)
        plt.plot(X,  pdf, label = 'Beta')
        plt.plot(X, normal(X,loc=mean,scale=sigma), label = 'Normal({},{})'.format(mean, str(sigma) + '/' + str(np.sqrt(n))))
        plt.hist(np.array([sample.mean for sample in beta((1000,n))]), normed=True)
    plt.show()

