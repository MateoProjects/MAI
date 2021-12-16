%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%             IMPORT DATA              %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
P = importdata("Input.mat"); % input
T = importdata("Output.mat");
K = 8671; % samples of Input

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%            GLOBAL SETTINGS           %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
doHyperparametersSearch = false;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%              PARAMETERS              %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
trainingRatio = [0.8 0.4 0.1];
validationRatio = [0.1 0.2 0.1];
testRatio = [0.1 0.4 0.8];
hiddenUnits = [50 200 500];
% Default hyperparameters
numEpochs = 1000;
learningRate = 0.001;
momentum = 0.2;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  HYPERPARAMETERS SEARCH WITH MODEL1  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if doHyperparametersSearch
    fprintf("-------------- Start of Hyperparameters search --------------\n")
    hiddenUnitsIdx = 1; % Set fixed number of hiddenUnits (minimum, for less computational cost)
    datasetRatiosIdx = 1; % Set fixed number of training/validation/test ratios
    numEpochsList = [500 1000 2000];
    learningRatesList = [0.1 0.01 0.001];
    mcRatesList = [0.1 0.2 0.3];
    
    bestNumEpochs = 0;
    bestLr = 0;
    bestMc = 0;
    bestAcc = 0;
    for i = 1:length(numEpochsList)
        for j = 1:length(learningRatesList)
            for k = 1:length(mcRatesList)
                fprintf("Testing using NumEpochs=%d LR=%f MC=%f\n", numEpochsList(i), learningRatesList(j), mcRatesList(k))
                [trainAcc, valAcc, testAcc] = model1(hiddenUnits(hiddenUnitsIdx), ...
                    trainingRatio(datasetRatiosIdx), validationRatio(datasetRatiosIdx), testRatio(datasetRatiosIdx), ...
                    P , T, ...
                    numEpochsList(i), learningRatesList(j), mcRatesList(k));
                fprintf("Obtained accuracy = %f\n", valAcc)
                if valAcc > bestAcc
                   bestAcc = valAcc;
                   bestNumEpochs = numEpochsList(i);
                   bestLr = learningRatesList(j);
                   bestMc = mcRatesList(k);
                end
            end
        end
    end
    fprintf("Best Hyperparamters: NumEpochs=%d LR=%f MC=%f. With %f accuracy\n", bestNumEpochs, bestLr, bestMc, bestAcc)
    numEpochs = bestNumEpochs;
    learningRate = bestLr;
    momentum = bestMc;
    fprintf("-------------- End of Hyperparameters search --------------\n")
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                MODEL1                %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf("-------------- Testing Model 1 --------------\n")
for i = 1:length(hiddenUnits)
    for j = 1:length(trainingRatio)
        fprintf("Testing using Hidden units=%d TrainDataRatio=%f ValDataRatio=%f TestDataRatio=%f \n", hiddenUnits(i), trainingRatio(j), validationRatio(j), testRatio(j))
        [trainAcc, valAcc, testAcc] = model1(hiddenUnits(i), trainingRatio(j), validationRatio(j), testRatio(j), P, T, numEpochs, learningRate, momentum);
        fprintf("Obtained accuracies: Train=%f Validation=%f Test=%f\n", trainAcc, valAcc, testAcc)
    end
end
fprintf("-------------- End of test --------------\n")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                MODEL2                %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf("-------------- Testing Model 2 --------------\n")
for i = 1:length(hiddenUnits)
    for j = 1:length(trainingRatio)
        fprintf("Testing using Hidden units=%d TrainDataRatio=%f ValDataRatio=%f TestDataRatio=%f \n", hiddenUnits(i), trainingRatio(j), validationRatio(j), testRatio(j))
        [trainAcc, valAcc, testAcc] = model2(hiddenUnits(i), trainingRatio(j), validationRatio(j), testRatio(j), P, T, numEpochs, learningRate, momentum);
        fprintf("Obtained accuracies: Train=%f Validation=%f Test=%f\n", trainAcc, valAcc, testAcc)
    end
end
fprintf("-------------- End of test --------------\n")

