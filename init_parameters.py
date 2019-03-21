import scipy.io as sio
import numpy as np


path = "camera-calibration/"


def init_parameter():
    parameters = dict()
    parameters['FocalLength'] = sio.loadmat(path+"FocalLength.mat")['FocalLength'][0]
    parameters['IntrinsicMatrix'] = sio.loadmat(path+"IntrinsicMatrix.mat")['IntrinsicMatrix']
    parameters['NumPatterns'] = sio.loadmat(path+"NumPatterns.mat")['NumPatterns'][0][0]
    parameters['PrincipalPoint'] = sio.loadmat(path+"PrincipalPoint.mat")['PrincipalPoint'][0]
    parameters['RadialDistortion'] = sio.loadmat(path+"RadialDistortion.mat")['RadialDistortion'][0]
    parameters['RotationMatrices'] = sio.loadmat(path+"RotationMatrices.mat")['RotationMatrices']
    parameters['RotationVectors'] = sio.loadmat(path+"RotationVectors.mat")['RotationVectors']
    parameters['TranslationVectors'] = sio.loadmat(path+"TranslationVectors.mat")['TranslationVectors']
    parameters['ImageSize'] = (3888, 5152)
    dist_coeffs = np.zeros((5, 1), np.float64)
    dist_coeffs[0] = parameters['RadialDistortion'][0]  # k1
    dist_coeffs[1] = parameters['RadialDistortion'][1]  # k2
    parameters['DistCoeffs'] = dist_coeffs
    return parameters


def get_points():
    points = dict()
    points['WorldPoints'] = sio.loadmat(path+"WorldPoints.mat")['WorldPoints']
    points['ReprojectedPoints'] = sio.loadmat(path+"ReprojectedPoints.mat")['ReprojectedPoints']
    return points


if __name__ == "__main__":
    print(init_parameter())

