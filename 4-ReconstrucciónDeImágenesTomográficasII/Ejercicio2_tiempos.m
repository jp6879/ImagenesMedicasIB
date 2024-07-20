% Ejercicio 2 - Medicion de tiempos

N = 256;                % Tamaño de la imagen

p = 360;                % Número de detectores paralelos

eta = 0.0001;           % Ruido relativo

k = 100;                % Número de iteraciones

theta = 0:0.5:179;      % Número de ángulos

% Create the test problem.
[A,b_ex,x_ex] = paralleltomo(N,theta,p);

% Noise level.
delta = eta*norm(b_ex);

% Add noise to the rhs.
randn('state',0);
e = randn(size(b_ex));
e = delta*e/norm(e);
b = b_ex + e;

% fprintf(1,'\n\n');
% fprintf(1,'Perform k = %2.0f iterations with Kaczmarz''s method.',k);
% fprintf(1,'\nThis takes a moment ...');

% Perform the kaczmarz iterations.
% tic
% Xkacz = kaczmarz(A,b,k);
% toc

fprintf(1,'\n\n');
fprintf(1,'Perform k = %2.0f iterations with the symmetric Kaczmarz method.',k);
fprintf(1,'\nThis takes a moment ...\n');

%Perform the symmetric kaczmarz iterations.
tic
Xsymk = symkaczmarz(A,b,k);
toc

fprintf(1,'\n\n');
fprintf(1,'Perform k = %2.0f iterations with the randomized Kaczmarz method.',k);
fprintf(1,'\nThis takes a moment ...\n');

% Perform the randomized kaczmarz iterations.
tic
Xrand = randkaczmarz(A,b,k);
toc

fprintf(1,'\n\n');
fprintf(1,'Perform k = %2.0f iterations with SART method.',k);
fprintf(1,'\nThis takes a moment ...');

% Perform SART
tic
Xsart = sart(A,b,k);
toc
