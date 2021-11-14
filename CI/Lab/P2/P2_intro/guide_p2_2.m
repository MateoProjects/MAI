inputs = [1:6]; % input vector (6-dimensional pattern); i.e. 1 2 3 4 5 6
outputs = [7:12]; % corresponding target output vector; i.e. 7 8 9 10 11 12
net = network( ...
1, ... % numInputs (number of inputs)
2, ... % numLayers (number of layers)
[1; 0], ... % biasConnect (numLayers-by-1 Boolean vector)
[1; 0], ... % inputConnect (numLayers-by-numInputs Boolean matrix)
[0 0; 1 0], ... % layerConnect (numLayers-by-numLayers Boolean matrix); [a b; c d]
... % a: 1st-layer with itself, b: 2nd-layer with 1st-layer,
... % c: 1st-layer with 2nd-layer, d: 2nd-layer with itself
[0 1] ... % outputConnect (1-by-numLayers Boolean vector)
);
% View network structure
%view(net);

net.layers{1}.size = 5;
% hidden layer transfer function
net.layers{1}.transferFcn = 'logsig';
%view(net);
net = configure(net,inputs,outputs);
%view(net);
initial_output = net(inputs);

net.trainFcn = 'trainlm';
net.performFcn = 'mse'; 
net = train(net,inputs,outputs);
net(1) % For 1 as input the outputs should be close to 7
 net(2) % For 1 as input the outputs should be close to 8
 net(3) % For 1 as input the outputs should be close to 9
 net(4) % For 1 as input the outputs should be close to 10
 net(5) % For 1 as input the outputs should be close to 11
 net(6) % For 1 as input the outputs should be close to 12