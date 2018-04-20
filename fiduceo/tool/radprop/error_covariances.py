import numpy as np


class ErrorCovariances():

    def calculate(self, uncertainty_vector, correlation_matrix):
        unc_matrix = np.diag(uncertainty_vector)
        covariance_matrix = np.dot(unc_matrix, correlation_matrix)
        covariance_matrix = np.dot(covariance_matrix, unc_matrix)

        return covariance_matrix
