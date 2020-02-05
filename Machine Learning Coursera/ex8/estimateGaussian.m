function [mu sigma2] = estimateGaussian(X)
%ESTIMATEGAUSSIAN This function estimates the parameters of a 
%Gaussian distribution using the data in X
%   [mu sigma2] = estimateGaussian(X), 
%   The input X is the dataset with each n-dimensional data point in one row
%   The output is an n-dimensional vector mu, the mean of the data set
%   and the variances sigma^2, an n x 1 vector
% 

% Useful variables
[m, n] = size(X);

% You should return these values correctly
mu = zeros(n, 1);
sigma2 = zeros(n, 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the mean of the data and the variances
%               In particular, mu(i) should contain the mean of
%               the data for the i-th feature and sigma2(i)
%               should contain variance of the i-th feature.
%

mu = 1/m * sum(X);
rep = repmat(mu, m, 1); 
% repmat全称是Replicate Matrix ，
% 意思是复制和平铺矩阵，是MATLAB里面的一个函数。
% 语法有B = repmat(A,m,n)，将矩阵 A 复制 m×n 块，
% 即把 A 作为 B 的元素，B 由 m×n 个 A 平铺而成。
sigma2 = 1/m * sum((X - rep).^2);







% =============================================================


end
