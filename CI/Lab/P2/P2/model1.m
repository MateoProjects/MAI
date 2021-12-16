function [trainAcc, valAcc, testAcc] =  model1(hiddenUnits, trainingRatio, validationRatio, testRatio, P, T, epochs, lr, mc)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %         1.1 LOGSIG LOGSIG MSE        %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    trainAcc = 0;
    valAcc = 0;
    testAcc = 0;
    numTests = 3;
    for j = 1:numTests
        net = feedforwardnet([hiddenUnits]); % select hidden units
        for i =1:(length(net.layers)-1)
            net.layers{i}.transferFcn = 'logsig'; % you can use either logsig or tansig
        %net.layers{i}.transferFcn = 'tansig';
        end
        net.layers{end}.transferFcn = 'logsig';
        % Cost function: mese
        net.performFcn = 'mse';
        % Train function: Gradient descent with momentum
        net.trainFcn = 'traingdx'; 
        net.trainParam.lr = lr; 
        net.trainParam.mc = mc; 
        net.trainParam.epochs = epochs;
        %net.trainFcn = 'trainscg'; net.trainParam.lr = 0.1; net.trainParam.mc = 0.8; %net.trainParam.epochs= 1000;
        net.outputs{:}.processFcns = {};
        net.divideFcn = 'dividerand';% divideFCN allow to change the way the data is
        % divided into training, validation and test
        % data sets.
        net.divideParam.trainRatio = trainingRatio; % Ratio of data used as training set
        net.divideParam.valRatio = validationRatio; % Ratio of data used as validation set
        net.divideParam.testRatio = testRatio; % Ratio of data used as test set
        net.trainParam.max_fail = 40; % validation check parameter
        net.trainParam.min_grad = 1e-5; % minimum performance gradient
        [net,tr,Y,E] = train(net,P,T);
        [argvalueT, argmaxT] = max(T);
        [argvalueY, argmaxY] = max(Y);
        trainAcc = trainAcc + (sum(argmaxT(tr.trainInd)==argmaxY(tr.trainInd)) / length(tr.trainInd))/numTests;
        valAcc = valAcc + (sum(argmaxT(tr.valInd)==argmaxY(tr.valInd)) / length(tr.valInd))/numTests;
        testAcc = testAcc + (sum(argmaxT(tr.testInd)==argmaxY(tr.testInd)) / length(tr.testInd))/numTests;
    end
end

