%ARTdemo (script) Demonstrates the use of, and the results from, the ART methods.
%
% This script illustrates the use of the ART methods kaczmarz, symmetric
% kaczmarz, and randomized kaczmarz.
%
% The script creates a parallel-beam test problem, adds noise, and solves
% the problems with the ART methods.  The exact solution and the results
% from the methods are shown.
%
% See also: nonnegdemo, SIRTdemo, trainingdemo.

% Maria Saxild-Hansen and Per Chr. Hansen, Mar 11, 2011, DTU Compute.

close all
fprintf(1,'\nStarting ARTdemo:\n\n');

% Set the parameters for the test problem.
N = 512;           % The discretization points.
%N = 512;
theta = 0:1:179;  % No. of used angles.
%theta = 0:1:179;
p = 75;           % No. of parallel rays.
%p = 360;
eta = 0.05;       % Relative noise level.

fprintf(1,'Creating a parallel-bema tomography test problem\n');
fprintf(1,'with N = %2.0f, theta = %1.0f:%1.0f:%3.0f, and p = %2.0f.',...
    [N,theta(1),theta(2)-theta(1),theta(end),p]);

% Create the test problem.
[A,b_ex,x_ex] = paralleltomo(N,theta,p);

% Noise level.
delta = eta*norm(b_ex);

% Add noise to the rhs.
randn('state',0);
e = randn(size(b_ex));
e = delta*e/norm(e);
b = b_ex + e;

% Show the exact solution.
figure
imagesc(reshape(x_ex,N,N)), colormap gray,
axis image off
c = caxis;
title('Exact phantom')

fantoma = reshape(x_ex,N,N);
save('fantoma.mat', 'fantoma'); % Save the matrix to a .mat file

% No. of iterations.
k = 10;

fprintf(1,'\n\n');
fprintf(1,'Perform k = %2.0f iterations with Kaczmarz''s method.',k);
fprintf(1,'\nThis takes a moment ...');

% Perform the kaczmarz iterations.
Xkacz = kaczmarz(A,b,k);

% Show the kaczmarz solution.
figure
imagesc(reshape(Xkacz,N,N)), colormap gray,
axis image off
caxis(c);
title('Kaczmarz reconstruction')

fprintf(1,'\n\n');
fprintf(1,'Perform k = %2.0f iterations with the symmetric Kaczmarz method.',k);
fprintf(1,'\nThis takes a moment ...');

% Perform the EM iterations.
XEm = ex_max(A,b,k);

% Show the EM solution.
figure
imagesc(reshape(XEm,N,N)), colormap gray,
axis image off
caxis(c);
title('EM reconstruction')

fprintf(1,'\n\n');
fprintf(1,'Perform k = %2.0f iterations with the EM method.',k);
fprintf(1,'\nThis takes a moment ...\n');

% Perform the symmetric kaczmarz iterations.
Xsymk = symkaczmarz(A,b,k);

% Show the symmetric kaczmarz solution.
figure
imagesc(reshape(Xsymk,N,N)), colormap gray,
axis image off
caxis(c);
title('Symmetric Kaczmarz reconstruction')

fprintf(1,'\n\n');
fprintf(1,'Perform k = %2.0f iterations with the randomized Kaczmarz method.',k);
fprintf(1,'\nThis takes a moment ...\n');

% Perform the randomized kaczmarz iterations.
Xrand = randkaczmarz(A,b,k);

% Show the randomized kaczmarz solution.
figure
imagesc(reshape(Xrand,N,N)), colormap gray,
axis image off
caxis(c);
title('Randomized Kaczmarz reconstruction')


function mse_value = mse_2d(array1, array2)
    % Check if the input arrays have the same size
    if ~isequal(size(array1), size(array2))
        error('Input arrays must have the same size.');
    end

    % Calculate MSE
    squared_error = (array1 - array2).^2;
    mse_value = mean(squared_error(:));
end

function psnr_value = psnr(image1, image2, max_intensity)
    % Convert images to double precision
    image1 = im2double(image1);
    image2 = im2double(image2);

    % Calculate MSE
    mse = sum((image1(:) - image2(:)).^2) / numel(image1);

    % Calculate PSNR
    psnr_value = 10 * log10((max_intensity^2) / mse);
end

function ssim_value = ssim_index(image1, image2, K, window_size)
    % Convert images to double precision
    image1 = double(image1);
    image2 = double(image2);

    % Constants for SSIM calculation
    C1 = (K(1))^2;
    C2 = (K(2))^2;

    % Gaussian filter for window
    gaussian = fspecial('gaussian', window_size, 1.5);

    % Compute means
    mu1 = conv2(image1, gaussian, 'same');
    mu2 = conv2(image2, gaussian, 'same');

    % Compute variances and covariance
    mu1_sq = mu1.^2;
    mu2_sq = mu2.^2;
    mu1_mu2 = mu1 .* mu2;

    sigma1_sq = conv2(image1.^2, gaussian, 'same') - mu1_sq;
    sigma2_sq = conv2(image2.^2, gaussian, 'same') - mu2_sq;
    sigma12 = conv2(image1 .* image2, gaussian, 'same') - mu1_mu2;

    % SSIM formula
    num = (2 * mu1_mu2 + C1) .* (2 * sigma12 + C2);
    den = (mu1_sq + mu2_sq + C1) .* (sigma1_sq + sigma2_sq + C2);

    ssim_map = num ./ den;

    % Compute SSIM index
    ssim_value = mean2(ssim_map);
end