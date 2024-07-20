% Ejercicio 2 - ART, Simetric ART, Random ART, SART
close all

% Set the parameters for the test problem.

for step = [5, 3, 1, 0.5]
    
    N = 256;            % The discretization points. 

    p = 360;            % No. of parallel rays.
   
    eta = 0.0001;       % Relative noise level.

    k = 100;            % No. of iterations.
    
    theta = 0:step:179;   % No. of used angles.
    
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
    %fantomaname = ['fantoma' num2str(step) '.mat'];
    %save(fantomaname, 'fantoma'); % Save the matrix to a .mat file
    
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
    
    ART = reshape(Xkacz,N,N);
    ARTname = ['ART_angles' num2str(step) '.mat'];
    save(ARTname, 'ART'); % Save the matrix to a .mat file

    fprintf(1,'\n\n');
    fprintf(1,'Perform k = %2.0f iterations with the symmetric Kaczmarz method.',k);
    fprintf(1,'\nThis takes a moment ...\n');

    % Perform the symmetric kaczmarz iterations.
    Xsymk = symkaczmarz(A,b,k);

    % Show the symmetric kaczmarz solution.
    figure
    imagesc(reshape(Xsymk,N,N)), colormap gray,
    axis image off
    caxis(c);
    title('Symmetric Kaczmarz reconstruction')

    symART = reshape(Xsymk,N,N);
    symARTname = ['symART_angles' num2str(step) '.mat'];
    save(symARTname, 'symART'); % Save the matrix to a .mat file

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
    
    randART = reshape(Xrand,N,N);
    randARTname = ['randART_angles' num2str(step) '.mat'];
    save(randARTname, 'randART'); % Save the matrix to a .mat file

    fprintf(1,'\n\n');
    fprintf(1,'Perform k = %2.0f iterations with the SART method.',k);
    fprintf(1,'\nThis takes a moment ...\n');

    % Perform SART
    Xsart = sart(A,b,k);

    % Show the SART solution.
    figure
    imagesc(reshape(Xsart,N,N)), colormap gray,
    axis image off
    caxis(c);
    title('SART reconstruction')

    SART = reshape(Xsart,N,N);
    SARTname = ['SART_angles' num2str(step) '.mat'];
    save(SARTname, 'SART');
end

for p = [30, 60, 90, 180, 360]
    
    N = 256;             % The discretization points
    
    %p = 360;            % No. of parallel rays.
   
    eta = 0.0001;       % Relative noise level.

    k = 100;            % No. of iterations.
    
    theta = 0:0.5:179;   % No. of used angles.
  
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
    %fantomaname = ['fantoma' num2str(step) '.mat'];
    %save(fantomaname, 'fantoma'); % Save the matrix to a .mat file
    
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
    
    ART = reshape(Xkacz,N,N);
    ARTname = ['ART_detectorsv2' num2str(p) '.mat'];
    save(ARTname, 'ART'); % Save the matrix to a .mat file

    fprintf(1,'\n\n');
    fprintf(1,'Perform k = %2.0f iterations with the symmetric Kaczmarz method.',k);
    fprintf(1,'\nThis takes a moment ...\n');

    % Perform the symmetric kaczmarz iterations.
    Xsymk = symkaczmarz(A,b,k);

    % Show the symmetric kaczmarz solution.
    figure
    imagesc(reshape(Xsymk,N,N)), colormap gray,
    axis image off
    caxis(c);
    title('Symmetric Kaczmarz reconstruction')

    symART = reshape(Xsymk,N,N);
    symARTname = ['symART_detectorsv2' num2str(p) '.mat'];
    save(symARTname, 'symART'); % Save the matrix to a .mat file

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
    
    randART = reshape(Xrand,N,N);
    randARTname = ['randART_detectorsv2' num2str(p) '.mat'];
    save(randARTname, 'randART'); % Save the matrix to a .mat file

    fprintf(1,'\n\n');
    fprintf(1,'Perform k = %2.0f iterations with the SART method.',k);
    fprintf(1,'\nThis takes a moment ...\n');

    % Perform SART
    Xsart = sart(A,b,k);

    % Show the SART solution.
    figure
    imagesc(reshape(Xsart,N,N)), colormap gray,
    axis image off
    caxis(c);
    title('SART reconstruction')

    SART = reshape(Xsart,N,N);
    SARTname = ['SART_detectorsv2' num2str(p) '.mat'];
    save(SARTname, 'SART');
end

for eta = [0.1, 0.01, 0.001, 0.0001, 0.00001]
    
    N = 256;
    
    p = 360;            % No. of parallel rays.
 
    k = 100;            % No. of iterations.
    
    theta = 0:0.5:179;   % No. of used angles.
  
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
    %fantomaname = ['fantoma' num2str(step) '.mat'];
    %save(fantomaname, 'fantoma'); % Save the matrix to a .mat file
    
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
    
    ART = reshape(Xkacz,N,N);
    ARTname = ['ART_rnoise' num2str(eta) '.mat'];
    save(ARTname, 'ART'); % Save the matrix to a .mat file

    fprintf(1,'\n\n');
    fprintf(1,'Perform k = %2.0f iterations with the symmetric Kaczmarz method.',k);
    fprintf(1,'\nThis takes a moment ...\n');

    % Perform the symmetric kaczmarz iterations.
    Xsymk = symkaczmarz(A,b,k);

    % Show the symmetric kaczmarz solution.
    figure
    imagesc(reshape(Xsymk,N,N)), colormap gray,
    axis image off
    caxis(c);
    title('Symmetric Kaczmarz reconstruction')

    symART = reshape(Xsymk,N,N);
    symARTname = ['symART_rnoise' num2str(eta) '.mat'];
    save(symARTname, 'symART'); % Save the matrix to a .mat file

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
    
    randART = reshape(Xrand,N,N);
    randARTname = ['randART_rnoise' num2str(eta) '.mat'];
    save(randARTname, 'randART'); % Save the matrix to a .mat file

    fprintf(1,'\n\n');
    fprintf(1,'Perform k = %2.0f iterations with the SART method.',k);
    fprintf(1,'\nThis takes a moment ...\n');

    % Perform SART
    Xsart = sart(A,b,k);

    % Show the SART solution.
    figure
    imagesc(reshape(Xsart,N,N)), colormap gray,
    axis image off
    caxis(c);
    title('SART reconstruction')

    SART = reshape(Xsart,N,N);
    SARTname = ['SART_rnoise' num2str(eta) '.mat'];
    save(SARTname, 'SART');
end
    

y = 10:10:1000;

N = 256;            % Tamaño de imagen

p = 360;            % No. of parallel rays.

theta = 0:0.5:179;   % No. of used angles.

eta = 0.0001;         % Error relativo

% Create the test problem.
[A,b_ex,x_ex] = paralleltomo(N,theta,p);

% Noise level.
delta = eta*norm(b_ex);

% Add noise to the rhs.
randn('state',0);
e = randn(size(b_ex));
e = delta*e/norm(e);
b = b_ex + e;

for k = y

   
    fprintf(1,'\n\n');
    fprintf(1,'Perform k = %2.0f iterations with the expectation maximization method.',k);
    fprintf(1,'\nThis takes a moment ...\n');

    % Perform Expectation Maximization
    XEM = em(A,b,k);
    
    figure
    imagesc(reshape(XEM,N,N)), colormap gray,
    axis image off
    caxis(c);
    
    title('Expectation maximization recontruct')
    
    EMr = reshape(XEM,N,N);
    
    EMname = ['EM_k' num2str(k) '.mat'];
    save(EMname, 'EMr');
end
