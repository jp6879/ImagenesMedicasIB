% Generación de FANTOMA shepp-logan    
N = 256;            % The discretization points. 

%p = 360;            % No. of parallel rays.

eta = 0.0001;       % Relative noise level.

k = 100;            % No. of iterations.

theta = 0:0.5:179;   % No. of used angles.

% % Create the test problem.
% [A,b_ex,x_ex] = paralleltomo(N,theta,p);
% 
% % Noise level.
% delta = eta*norm(b_ex);
% 
% % Add noise to the rhs.
% randn('state',0);
% e = randn(size(b_ex));
% e = delta*e/norm(e);
% b = b_ex + e;
% 
% % Show the exact solution.
% figure
% imagesc(reshape(x_ex,N,N)), colormap gray,
% axis image off
% c = caxis;
% title('Exact phantom')
% 
% fantoma = reshape(x_ex,N,N);
% fantomaname = ['fantoma512.mat'];
% save(fantomaname, 'fantoma'); % Save the matrix to a .mat file

% Testeamos que es el número de detectores. Voy a dejar N en 256 y cambiar
% p en los valores 50, 100, 200, 300

for p = [50, 100, 200, 300]
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
end