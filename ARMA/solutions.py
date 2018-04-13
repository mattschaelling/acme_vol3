# solutions.py
"""Volume 3: ARMA. Partial Solutions File."""

import numpy as np
from math import log, sqrt
from scipy.stats import norm
from scipy import linalg as la
from scipy import optimize as opt
from matplotlib import pyplot as plt


def arma_likelihood(time_series,
                    phis=np.array([]), thetas=np.array([]), mu=0.,sigma=1.):
    """Calculate the log-likelihood of the ARMA model parameters, given the time series.

    Parameters:
        time_series ((n,) ndarray): The time series in question, z_t.
        phis: ((p,) ndarray): The phi parameters.
        thetas ((q,) ndarray): The theta parameters.
        mu (float): The parameter mu.
        sigma (float): The standard deviation of the a_t random variables.

    Returns:
        (float): The log-likelihood of the model
    """
    # Get system dimensions.
    p,q = len(phis), len(thetas)
    r = max(p,q+1)
    d = time_series.ndim             # d = 1 for these problems.

    # Define the system.
    F = np.diag(np.ones(r-1), -1)    # F is rxr.
    F[0,:p] = phis

    Q = np.zeros((r,r))              # Q is rxr.
    Q[0,0] = sigma**2

    H = np.zeros((d,r))              # H is dxr. IT IS VERY IMPRORTANT that this is 2D!
    H[0,0] = 1
    H[0,1:q+1] = thetas

    # Get initial state estimates x_{1|0} and P_{1|0}.
    x = np.zeros(r)
    P = la.solve(np.eye(r**2) - np.kron(F, F), Q.flatten()).reshape((r,r))
    I = np.eye(r)

    # Do Kalman Filter (estimate/predict) to calculate the log likelihood.
    log_likelihood = 0
    for z in time_series - mu:
        mean = H@x
        y = z - mean
        S = H@P@H.T
        K = la.solve(S.T, H@P.T).T   # K = P @ H.T @ inv(S)
        x = F@(x + K@y)
        P = F@((I - K@H)@P)@F.T + Q

        log_likelihood += log(norm.pdf(z, mean, np.sqrt(S)))

    return log_likelihood


def arma_fit(time_series):
    """Return the ARMA model that minimizes AICc for the given time series, subject to p,q <= 3.

    Parameters:
        time_series ((n,) ndarray): The time series in question, z_t.

    Returns:
        phis ((p,) ndarray): The phi parameters.
        thetas ((q,) ndarray): The theta parameters.
        mu (float): The parameter mu.
        sigma (float): The standard deviation of the a_t random variables.
    """
    AICc = lambda k,n,l: 2*k*(1 + (k+1)/(n-k)) - 2*l

    best_aicc = np.inf
    best_params = [], [], 0, 0

    emp_mean = np.mean(time_series)
    emp_sigma = np.std(time_series)
    n = len(time_series)

    for p in range(4):
        for q in range(4):
            x0 = np.array([0]*p + [0]*q + [emp_mean] + [emp_sigma])
            k = len(x0)
            def f(x):
                return -arma_likelihood(time_series, phis=x[:p], thetas=x[p:p+q], mu=x[-2], sigma=x[-1])
            opt_x = opt.fmin(f, x0, maxiter=10000, maxfun=10000, disp=False)
            k = len(x0)
            new_aicc = AICc(k,n,-f(opt_x))
            if new_aicc < best_aicc:
                print("New best model found with p={}, q={}".format(p, q))
                best_aicc = new_aicc
                best_params = opt_x[:p], opt_x[p:p+q], opt_x[-2], opt_x[-1]
    return best_params


def arma_forecast(time_series,
                  phis=np.array([]), thetas=np.array([]), mu=0., sigma=1.,
                  future_periods=20):
    """Forecast a time series modeled with the given ARMA model.

    Parameters:
        time_series ((n,) ndarray): The time series in question, z_t.
        phis: ((p,) ndarray): The phi parameters.
        thetas ((q,) ndarray): The theta parameters.
        mu (float): The parameter mu.
        sigma (float): The standard deviation of the a_t random variables.
        future_periods (int): The number of future periods to return.

    Returns:
        e_vals ((future_periods,) ndarray): The expected values of z for times n+1, ..., n+future_periods
        sigs ((future_periods,) ndarray): The standard deviations of z for times n+1, ..., n+future_periods
    """
    # Get system dimensions.
    p,q = len(phis), len(thetas)
    r = max(p,q+1)
    d = time_series.ndim             # d = 1 for these problems.

    # Define the system.
    F = np.diag(np.ones(r-1), -1)    # F is rxr.
    F[0,:p] = phis

    Q = np.zeros((r,r))              # Q is rxr.
    Q[0,0] = sigma**2

    H = np.zeros((d,r))              # H is dxr. IT IS VERY IMPRORTANT that this is 2D!
    H[0,0] = 1
    H[0,1:q+1] = thetas

    # Get initial state estimates x_{1|0} and P_{1|0}.
    x = np.zeros(r)
    P = la.solve(np.eye(r**2) - np.kron(F, F), Q.flatten()).reshape((r,r))
    I = np.eye(r)

    # Do Kalman Filter (estimate/predict) for the first n periods.
    for z in time_series - mu:
        y = z - H@x
        S = H@P@H.T
        K = la.solve(S.T, H@P.T).T   # K = P @ H.T @ inv(S)
        x = F@(x + K@y)
        P = F@((I - K@H)@P)@F.T + Q

    means = []
    sigs = []
    # Forecast forward a few periods.
    for k in range(future_periods):
        x = F@x
        P = F@P@F.T + Q
        means.append(H@x + mu)
        sigs.append(sqrt(H@P@H.T))


    return np.array(means), np.array(sigs)
