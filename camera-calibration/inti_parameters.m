clear; clc
load('cameraParams.mat');
cameraParams

IntrinsicMatrix = cameraParams.IntrinsicMatrix;
save('IntrinsicMatrix.mat', 'IntrinsicMatrix');

FocalLength = cameraParams.FocalLength;
save('FocalLength.mat', 'FocalLength');

PrincipalPoint = cameraParams.PrincipalPoint;
save('PrincipalPoint.mat', 'PrincipalPoint');

RadialDistortion = cameraParams.RadialDistortion;
save('RadialDistortion.mat', 'RadialDistortion');

RotationMatrices = cameraParams.RotationMatrices;
save('RotationMatrices.mat', 'RotationMatrices');

RotationVectors = cameraParams.RotationVectors;
save('RotationVectors.mat', 'RotationVectors');

TranslationVectors = cameraParams.TranslationVectors;
save('TranslationVectors.mat', 'TranslationVectors');

NumPatterns = cameraParams.NumPatterns;
save('NumPatterns.mat', 'NumPatterns');

WorldPoints = cameraParams.WorldPoints;
save('WorldPoints.mat', 'WorldPoints');

ReprojectedPoints = cameraParams.ReprojectedPoints;
save('ReprojectedPoints.mat', 'ReprojectedPoints');
