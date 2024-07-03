import numpy as np


def simulator():
    """Non-configurable simulator running with default settings."""
    prior_draws = prior()
    observables = observation_model(prior_draws)
    return dict(parameters=prior_draws, observables=observables)


def prior(D: int = 10, lower_bound: float = -1.0, upper_bound: float = 1.0, rng: np.random.Generator = None):
    """Generates a random draw from a D-dimensional uniform prior bounded between
    `lower_bound` and `upper_bound` which represents the location vector of
    a (conjugate) Gaussian likelihood.

    Parameters
    ----------
    D           : int, optional, default : 10
        The dimensionality of the Gaussian prior.
    lower_bound : float, optional, default : -1.
        The lower bound of the uniform prior.
    upper_bound : float, optional, default : 1.
        The upper bound of the uniform prior.
    rng         : np.random.Generator or None, default: None
        An optional random number generator to use.

    Returns
    -------
    params : np.ndarray of shape (D, )
        A single draw from the D-dimensional uniform prior.
    """

    if rng is None:
        rng = np.random.default_rng()
    return rng.uniform(low=lower_bound, high=upper_bound, size=D)


def observation_model(params: np.ndarray, n_obs: int = None, scale: float = 0.1, rng: np.random.Generator = None):
    """Generates batched draws from a D-dimenional Gaussian distributions given a batch of
    location (mean) parameters of D dimensions. Assumes a spherical convariance matrix given
    by scale * I_D.
    
    See Task T.2 from the paper https://arxiv.org/pdf/2101.04653.pdf
    NOTE: The paper description uses a variance of 0.1 for likelihood function
    but the implementation uses scale = 0.1 Our implmenetation uses a default scale
    of 0.1 for consistency with the implementation.
    
    Parameters
    ----------
    params : np.ndarray of shape (params, D)
        The location parameters of the Gaussian likelihood.
    n_obs  : int or None, optional, default: None
        The number of observations to draw from the likelihood given the location
        parameter `params`. If None, a single draw is produced.
    scale  : float, optional, default : 0.1
        The scale of the Gaussian likelihood.
    rng    : np.random.Generator or None, default: None
        An optional random number generator to use.

    Returns
    -------
    x : np.ndarray of shape (params.shape[0], params.shape[1]) if n_obs is None,
        else np.ndarray of shape (params.shape[0], n_obs, params.shape[1])
        A single draw or a sample from a batch of Gaussians.
    """

    # Use default RNG, if None provided
    if rng is None:
        rng = np.random.default_rng()
    # Generate prior predictive samples, possibly a single if n_obs is None
    if n_obs is None:
        return rng.normal(loc=params, scale=scale)
    x = rng.normal(loc=params, scale=scale, size=(n_obs, params.shape[0], params.shape[1]))
    return np.transpose(x, (1, 0, 2))
