close all
FitnessFunction = @(x)(1-x(1))^2+100*(x(2)-x(1)^2)^2;
popSize = [20,40,60,80,100,200, 500];
generations = [100,200,300,400,500];
selection = {@selectionstochunif, @selectionremainder, @selectionuniform, @selectionroulette, @selectiontournament};
selectionString = ["selectionstochunif" "selectionremainder" "selectionuniform" "selectionroulette" "selectiontournament"];
popInitRange = [1, 2, 3, 4, 5];
minFval = 1000;
popInitRangeVal = 1;
generationsVal = 1;
popSizeVal = 1;
crossOverVal = 1000;
minX = 0;
for t = 1: length(selection)
    for k = 1:length(popInitRange)
        for j = 1:length(generations)
            opts = gaoptimset('Generations',generations(j),'Display','none');
            opts = gaoptimset('SelectionFcn', selection(t),'Display', 'none');
            for i=1:length(popSize)
                opts = gaoptimset(opts,'PopulationSize',popSize(i));
                opts = gaoptimset(opts, 'PopInitRange',[-popInitRange(k) -popInitRange(k); popInitRange(k) popInitRange(k)]);
                rng default % rng (random number generation) for reproducibility it takes the same random number
                record=[];
                for n=0:.05:1
                    opts = gaoptimset(opts,'CrossoverFraction',n);
                    [x fval]=ga(FitnessFunction,2,[],[],[],[],[],[],[],opts);
                    record = [record; fval];
                    if fval < minFval
                       minFval = fval;
                       generationsVal = generations(j);
                       popInitRangeVal = popInitRange(k);
                       popSizeVal = popSize(i);
                       crossOverVal = n;
                       minX = x;
                       selectionBest = selectionString(t);
                    end
                end   
            end
        end
    end
end 
fprintf("MinFval: %E \n", minFval)
fprintf("PopInitRange: %d \n" , popInitRangeVal)
fprintf("Population Size: %d \n" , popSizeVal)
fprintf("Generations Val: %d \n", generationsVal)
fprintf("CrossOverVal: %f \n", crossOverVal)
fprintf("Best Selection: %s \n", selectionBest)


