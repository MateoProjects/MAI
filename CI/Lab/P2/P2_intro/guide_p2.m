close all, clear all, clc

K = 30;
q = .6;
A = [rand(1,K)-q; rand(1,K)+q];
B = [rand(1,K)+q; rand(1,K)+q];
C = [rand(1,K)+q; rand(1,K)-q];
D = [rand(1,K)-q; rand(1,K)-q];

plot(A(1,:), A(2,:), 'bs')
hold on
grid on
plot(B(1,:), B(2,:), 'r+')
plot(C(1,:), C(2,:), 'go')
plot(D(1,:), D(2,:), 'm*')

text(.5-q, .5+2*q, 'Class A')
text(.5+q, .5+2*q, 'Class B')
text(.5+q, .5-2*q, 'Class C')
text(.5-q, .5-2*q, 'Class D')
a = [0 1]';
b = [1 1]';
c = [1 0]';
d = [0 0]';

P = [A B C D];
T = [repmat(a, 1 , length(A)) repmat(b,1, length(B))...
    repmat(c, 1 , length(C)) repmat(d, 1, length(D))];
plotpv(P,T);
net = perceptron;
E = 1;
net.adaptParam.passes = 1;
linehandle = plotpc(net.IW{1}, net.b{1});
n = 0;
while (sse(E) &  n < 1000)
    n = n+1;
    [net, Y, E] = adapt(net,P,T);
    linehandle = plotpc(net.IW{1}, net.b{1}, linehandle);
    drawnow;
    pause(0.001);
end
view(net);

% por use network

p = [0.7; 1.2]
y = net(p)

close all, clear all, clc
K = 100;
q = .6;
A1 = [rand(1,K)-q; rand(1,K)+q];
B1 = [rand(1,K)+q; rand(1,K)+q];
C1 = [rand(1,K)+q; rand(1,K)-q];
D1 = [rand(1,K)-q; rand(1,K)-q];

A = [A1 C1];
B = [B1 D1];

plot(A(1,:), A(2,:),'k+', B(1,:), B(2,:), 'b*')
xlim([-2,3]);
ylim([-2,3]);
grid on
hold on
a = 0;
b = 1;
P = [A B];
T = [repmat(a, 1, length(A)) repmat(b, 1, length(B))];
net = perceptron;
E = 1;
net.adaptParam.passes = 1;
linehandle = plotpc(net.IW{1}, net.b{1});
n = 0;
while (sse(E) & n < 20)
    n = n+1;
    [net, Y, E] = adapt(net, P,T);
    linehandle = plotpc(net.IW{1}, net.b{1}, linehandle);
    drawnow;
    pause(0.01);
end
view(net);

close all,clear all, clc 
K = 100;
% offset of clusters
q = .6;
% define 2 groups of input data
A1 = [rand(1,K)-q; rand(1,K)+q];
B1 = [rand(1,K)+q; rand(1,K)+q];
C1 = [rand(1,K)+q; rand(1,K)-q];
D1 = [rand(1,K)-q; rand(1,K)-q];
A = [A1 C1];
B = [B1 D1];

plot(A(1,:),A(2,:),'k+',B(1,:),B(2,:),'b*')
grid on
hold on

a = 0;
b = 1;
P = [A B];
T = [repmat(a,1,length(A)) repmat(b,1,length(B))]
net = feedforwardnet([20]);
%net

[net, tr, Y,E] = train(net, P,T);
view(net)
fprintf('Accuracy: %f\n',100-100*sum(abs((Y>0.5)-T))/length(T))
figure(2)
plot(T','linewidth',2)
hold on
plot(Y','r--')
grid on
legend('Targets','Network response','location','best')
ylim([-1.25 1.25])
% generate a grid
span = -1:.005:2;
[P1,P2] = meshgrid(span,span);
pp = [P1(:) P2(:)]';
% simulate neural network on a grid
aa = net(pp);
% plot classification regions
figure(1)
mesh(P1,P2,reshape(aa,length(span),length(span))-5);
colormap cool
view(2)
% show netwo
view(net)

close all, clear all, clc
% number of samples of each cluster
K = 100;
% offset of clusters
q = .6;
% define 2 groups of input data
A1 = [rand(1,K)-q; rand(1,K)+q];
B1 = [rand(1,K)+q; rand(1,K)+q];
C1 = [rand(1,K)+q; rand(1,K)-q];
D1 = [rand(1,K)-q; rand(1,K)-q];
A = [A1 C1];
B = [B1 D1];
% plot data
plot(A(1,:),A(2,:),'k+',B(1,:),B(2,:),'b*')
grid on
hold on
% Define output coding
% coding (+1/0) for 2-class XOR problem
a = 0;
b = 1;
% Prepare inputs and outputs for network training
% define inputs (combine samples from all two classes)
P = [A B];
% define targets
T = [repmat(a,1,length(A)) repmat(b,1,length(B))];
% create a neural network
net = feedforwardnet([20]);
% adjust the network for classification
for i =1:(length(net.layers)-1)
%net.layers{i}.transferFcn = 'logsig'; % you can use either logsig or tansig
 net.layers{i}.transferFcn = 'tansig';
end
net.layers{end}.transferFcn = 'softmax';
% Cost function: crossentropy
net.performFcn = 'crossentropy';
% Train function: Gradient descent with momentum
net.trainFcn = 'traingdm'; net.trainParam.lr = 0.5; net.trainParam.mc = 0.8; net.trainParam.epochs =2000;
% Train function: Scaled Conjugate Gradients. You can tried it instead of traingdm.
%net.trainFcn = 'trainscg'; net.trai

%net.trainFcn = 'trainscg'; net.trainParam.lr = 0.1; net.trainParam.mc = 0.8; %net.trainParam.epochs= 1000;
% The processFcns parameter is used when you want to perform certain preprocessing
% steps on the network inputs and targets. Be careful, Matlab perform the most common
% preprocessings automatically when you create a network. If you do not want any
% preprocessing you need to disable this parameter.
net.outputs{end}.processFcns = {};
% train the neural network
[net,tr,Y,E] = train(net,P,T);
% Notice that tr has the indices of the training, validation and test data sets:
% tr.trainInd
% tr.valInd
% tr.testInd
% show network
view(net)
% Accuracy
fprintf('Accuracy: %f\n',100-100*sum(abs((Y>0.5)-T))/length(T))
% Plot targets and network response to see how good the network learns the data
figure(2)
plot(T','linewidth',2)
hold on
plot(Y','r--')
grid on
legend('Targets','Network response','location','best')
ylim([-1.25 1.25])
% Plot classification result for the complete input space (separation by hyperplanes)
% generate a grid
span = -1:.005:2;
[P1,P2] = meshgrid(span,span);
pp = [P1(:) P2(:)]';
% simulate neural network on a grid
aa = net(pp);
% plot classification regions
figure(1)
mesh(P1,P2,reshape(aa,length(span),length(span))-5);
colormap cool
view(2)

%% ------------------------------------------ 
%% creating a personalized neural network
close all, clear all, clc
inputs = [1:6]; % input vector (6-dimensional pattern); i.e. 1 2 3 4 5 6
outputs = [7:12]; % corresponding target output vector; i.e. 7 8 9 10 11 12
