%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%             IMPORT DATA              %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

P = importdata("Input.mat"); % input
T = importdata("Output.mat");
K = 8671; % samples of Input

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%            PUT PARAMETERS            %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

trainingRatio = [0.8 0.4 0.1];
validationRatio = [0.1 0.2 0.1];
testRatio = [0.1 0.4 0.8];
hiddenUnits = [50 200 500];
learningRate = [0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9];
mcRate = [0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9];
bestLr = 0;
bestMc= 0;
bestAcc = 0;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                MODEL1                %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for m = 1:3
    bestLr = 0;
    bestMc = 0;
    bestAcc = 0;
    for n = 1:9
        for i = 1:9
           acc = model1(hiddenUnits(m), trainingRatio(m), validationRatio(m), testRatio(m), P , T, 2000, learningRate(n), mcRate(i));
           if bestAcc < acc
               bestAcc = acc;
               bestLr = learningRate(m);
               bestMc = mcRate(n);
           end % end if
        end %enf for i
    end %end for n
    fprintf("Best Learning Rate and MC for %d hidden units: %f lr %f mc\n", hiddenUnits(m), bestLr, bestMc)
end %end for m
fprintf("-------------- End of training model --------------\n")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                MODEL2                %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i = 1:3
    model2(hiddenUnits(i), trainingRatio(i), validationRatio(i), testRatio(i), P , T, 2000, 0.5, 0.8)
end

