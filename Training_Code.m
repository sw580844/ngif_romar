
% Appendix (Code)

% % Imapge Processing – Image Preperation
% %Load folder
% fls = dir('C:\Users\aalqatatsheh\Documents\MATLAB\Frames')
% toRemove = strcmp(fls(1).name, '.');
% fls(toRemove) = [];
% toRemove = strcmp(fls(1).name, '..');
% fls(toRemove) = [];

% for i = 1:length(fls)
%     % Read data from directory and store in 168 x 224 x number of files
%     str = strcat(' C:\Users\aalqatatsheh\Documents\MATLAB\Frames', int2str(i), '.dat');
%     data (:, :, i) = load(fls(i).name);
%     frame = tall(data);
% end

% % Transfer matrix into rgb photos
% figure('pos', [164 218 1000 800]);
% C = colormap;
% L = size(C, 1);

% for i = 1:length(fls)
%     D = gather(frame(:, :, i))
%     Ds = round(interp1(linspace(min(D(:)), max(D(:)), L), 1:L, D));
%     H = reshape(C(Ds, :), [size(Ds) 3]);
%     Y = imresize(H, [224, 224], 'Method', 'bilinear')
%     B = reshape(Y, [], 1)
%     RGB(:, :, i) = B

% end

% % Transfer RGB2Gray. For matching entities, RGB1=RGB(:,:,10:682)
% RGB1 = RGB(:, :, 6:681);
% B = [size(RGB1)];

% for i = 1:B(1, 3);
%     BB = reshape(RGB1(:, :, i), [224 224 3]);
%     GRY(:, i) = reshape(rgb2gray(BB), [], 1);
%     End
%     % Calculate mean average background of side tensors with sizes (3584 x 13) to identify background
%     iii = 1

%     for i = 1:52
%         ii = iii
%         iii = 13 * i
%         B2 = GRY(1:3584, ii:iii);
%         B3 = GRY(3585:7168, ii:iii);
%         B4 = GRY(7169:10752, ii:iii);
%         B5 = GRY(10753:14336, ii:iii);
%         B6 = GRY(14337:28672, ii:iii);
%         B7 = GRY(28673:32257, ii:iii);
%         B8 = GRY(32258:35841, ii:iii);
%         B9 = GRY(39426:43010, ii:iii);
%         B10 = GRY(43011:46593, ii:iii);
%         B11 = GRY(46594:50176, ii:iii);
%         BG(:, i) = max([mean(B2, 'all'), mean(B3, 'all'), mean(B4, 'all'), mean(B5, 'all'), mean(B6, 'all'), mean(B7, 'all'), mean(B8, 'all'), mean(B9, 'all'), mean(B10, 'all'), mean(B11, 'all')]);
%     end

%     % Remove background layer to ease calculating pixels
%     i = 0.0
%     aaa = 1

%     for i = 1:52
%         aa = aaa
%         aaa = 13 * i

%         for k = aa:aaa
%             b(:, k) = GRY(:, k);
%             b(b < BG(:, i)) = 0.0;
%         end

%     end

%     % Transfer Gray scale to jpeg photo and calculate properties
%     i = 0

%     for i = 1:676
%         filename = sprintf('MyGray_%d.jpeg', i)
%         imwrite(uint8(1000 * (reshape(b(:, i), [224 224]))), filename);
%         I = imread(filename);
%         II = logical(I)

%         properties = regionprops(II, {'Area', 'Eccentricity', 'EquivDiameter', 'EulerNumber', 'MajorAxisLength', 'MinorAxisLength', 'Orientation', 'Perimeter'})
%             sm = transpose(table2array(cell2table(struct2cell(properties))));
%             [m] = max(sm);
%             m(:, 1) = sum(sm(:, 1));
%             m(:, 8) = sum(sm(:, 8))
%             Property(:, i) = m
%         end

%         % Match table with images.
%         Data_File_new2(1, :) = mean(Data_File_new1(1:9, :))

%         for i = 1:258
%             ii = i * 10
%             Data_File_new2(i + 1, :) = mean(Data_File_new1(ii:ii + 9, :))
%         end

%         Data_File_new2(i + 2, :) = mean(Data_File_new1(ii + 10:ii + 17, :))
        
%       % Calculate estimation error
%         Property1 = transpose(Property)
%         Property1 = Property1(417:676, :)
        
%         %PCA
%         % Data Cleansing and Preperation
%         DD = readtable('C:\Users\aalqatatsheh\Documents\MATLAB\Data.dat');
%         DD(1:43, :) = [];
%         DD = table2array(DD);
%         DD = cellfun(@str2num, DD, 'UniformOutput', false);
%         DD = cell2mat(DD);
%         DD(:, 19) = int16(DD(:, 4) / 0.53);
%         i = 1:1:length(DD);
%         % Speed calculation
%         DD(length(DD) + 1, 2) = 0;
%         DD(i, 20) = abs(((DD(i, 2) - DD(i + 1, 2)) * 600));
%         idx = []
%         % Indexes used to index parts of array to insert data from Steve (powder voltage, etc)
%         idx = any(DD(:, 19) < 60 | DD(:, 19) > 98, 2);
%         DD(idx, :) = [];
%         idx = []
%         idx = any(DD(:, 19) < 64 | DD(:, 19) > 67, 2);
%         DD(idx, 21) = 3.45;
%         idx = any(DD(:, 19) < 68 | DD(:, 19) > 87, 2);
%         DD(idx, 21) = 3.85;
%         idx = []
%         idx = any(DD(:, 19) > 88, 2);
%         DD(idx, 21) = 4.25;
%         idx = []
%         idx = any(DD(:, 19) < 64, 2);
%         DD(idx, 21) = 4.25;
%         DD(:, 5:6) = [];
%         DD(:, 8:10) = [];
%         DataFile1 = DD

%         % To average over every 9/10 columns ie. rolling window
%         DD1(1, :) = mean(DD(1:9, :))
%         for i = 1:265
%             DD1(1 + i, :) = mean(DD(i * 10:i * 10 + 9, :));
%         end

%         DD1(267, :) = mean(DD(2660:2668, :))
%         DataFile = DD1;
%         % Datafiler is a subset of DataFile with some columns removed DataFile_reduced
%         DataFile(:,14)=int16(DataFile(:,14))
%         Datafiler = DataFile
%         % Following lines delete multiple columns at a time, then the others take their place
%         Datafiler (:, 1:4) = [];
%         Datafiler (:, 3:8) = [];
%         Datafiler (:, 4:6) = [];
       
%         % Columns present: meltpool size, temp, and protection glas temp 
%         %PCA
%         C = (Datafiler' * Datafiler)
%         % Eigenvalues and eigenvectors
%         [W Lambda] = eig(C);
%         W = W(:, end:-1:1);
%         Lambda = Lambda(:, end:-1:1);
%         [U, Sig, V] = svd(Datafiler);
%         V = -V;
%         V_r = V(:, 1:2);
%         Datafilerr = Datafiler * V_r;

%         figure; plot(Datafilerr(:, 1), Datafilerr(:, 2), 'o');
%         xlabel('PCA1'); ylabel('PCA2');
%         SV = diag(Sig);
%         % Plotting the staircase showing cumulative variance given by each variable
%         figure:stairs(cumsum(SV) / sum(SV));
%         xlabel('Principal Components'); ylable('Comulitive Sum/Sum')
%         [coeff, score, latent, tsquared, explained, mu] = pca(Datafiler);
        
%         T2 = transpose(reshape(tsquared(1:266, :), 7, []));
%         TT = controlchart(T2, 'rules', 'we2')
%         x = TT.mean;
%         cl = TT.mu;
%         se = TT.sigma ./ sqrt(TT.n);
%         hold on
%         plot(cl + 2 * se, 'm')
%         RR = controlrules('we2', x, cl, se);
%         Rule = find(RR)
        
%         Temp_D = int16(Datafiler(:, 2))
%         i = 0;

%         for i = 1:length(Rule);
%             Defect(i) = Temp_D(Rule(i))
%         End

% % CNN Deep Learning
% % prepare labelled data for training and testing 
% i=0
% for i=1:688
% filename = sprintf('%d_MyRGB.jpeg', i)
% imwrite((reshape(RGB(:,i),[224 224 3])),filename);
% end
% Temp=int16(Datafiler(:,1))
% imagefiles = dir(fullfile('C:\Users\aalqatatsheh\Documents\MATLAB\Frames', '*.jpeg'));

% [~, reindex] = sort( str2double( regexp( {imagefiles.name},'\d+\.?\d*', 'match', 'once' )));
% imagefiles = imagefiles(reindex);

% %Label images with temperature for CNN
% [uTemp,ia,ic] = unique(Temp);
% mkdir('imageFolder');
% folder='C:\Users\aalqatatsheh\Documents\MATLAB\Frames\imageFolder\file';
% [parentFolder,deepestFolder] = fileparts(folder);

% %Create subfolders
% i=0
% for i=1:length(uTemp);
% newSubFolder = fullfile(parentFolder,sprintf(strcat(num2str(uTemp(i))), deepestFolder))
% mkdir(newSubFolder)
% end
% images = dir(fullfile('C:\Users\aalqatatsheh\Documents\MATLAB\Frames\imageFolder'));
% toRemove = strcmp(images(1).name,'.');
% images (toRemove) = [];
% toRemove = strcmp(images(1).name, '..');
% images (toRemove) = [];

% ImTemp=cell(267,2);
% files = dir('C:\Users\aalqatatsheh\Documents\MATLAB\Frames\imageFolder')
% dirFlags = [files.isdir]

% % Extract only those that are directories.
% subFolders = files(dirFlags)
% toRemove = strcmp(subFolders(1).name,'.');
% subFolders (toRemove) = [];
% toRemove = strcmp(subFolders (1).name, '..');
% subFolders (toRemove) = [];

% id=0
% k=0
% for id = 417:683
% k=id-416 
% ImTemp(k,1)=cellstr(imagefiles(id).name)
% ImTemp(k,2)=cellstr(num2str(Temp(k)))
% end

% for id = 417:683
% k=id-416 
% path=fullfile('C:\Users\aalqatatsheh\Documents\MATLAB\Frames\imageFolder',cell2mat(ImTemp(k,2)), '\')
% source=fullfile('C:\Users\aalqatatsheh\Documents\MATLAB\Frames',cell2mat(ImTemp(k,1)))
% movefile(source,path) 
% end

% del=tbl.Label(find(tbl.Count < 3));

% i=0;
% for i=1:length(del)
% delete(fullfile('C:\Users\aalqatatsheh\Documents\MATLAB\Frames\imageFolder',cell2mat(string(del(i))),'*.*'))
% rmdir (fullfile('C:\Users\aalqatatsheh\Documents\MATLAB\Frames\imageFolder',cell2mat(string(del(i)))))  
% end

% % Define imageDatastore
% imds=imageDatastore('C:\Users\aalqatatsheh\Documents\MATLAB\Frames\imageFolder1','IncludeSubfolders',true,'FileExtensions','.jpeg','LabelSource','foldernames');

% % split the labelled data between trained and validated
% [imdsTrain,imdsValidation] = splitEachLabel(imds,0.7, 'randomized');

% % Load pretrained network
% net=googlenet()

% % Inspect first and last layers of the net
% net.Layers(1);
% net.Layers(end);
% inputSize = net.Layers(1).InputSize;


% % Number of class names for ImageNet classification task
% numel(net.Layers(end).ClassNames);

% % Number of class names for ImageNet classification task
% numel(net.Layers(end).ClassNames);


% %Convert the trained network to a layer graph 
% lgraph = layerGraph(net);
% % find layer to replace
% [learnableLayer,classLayer] = findLayersToReplace(lgraph)

% % Speed up learning
% numClasses = numel(categories(imdsTrain.Labels));

% if isa(learnableLayer,'nnet.cnn.layer.FullyConnectedLayer')
%     newLearnableLayer = fullyConnectedLayer(numClasses, ...
%         'Name','new_fc', ...
%         'WeightLearnRateFactor',10, ...
%         'BiasLearnRateFactor',10);
    
% elseif isa(learnableLayer,'nnet.cnn.layer.Convolution2DLayer')
%     newLearnableLayer = convolution2dLayer(1,numClasses, ...
%         'Name','new_conv', ...
%         'WeightLearnRateFactor',10, ...
%         'BiasLearnRateFactor',10);
% end

% lgraph = replaceLayer(lgraph,learnableLayer.Name,newLearnableLayer);

% % Replace the classification layer with a new one without class labels. Train Network automatically sets the output classes of the layer at training time
% newClassLayer = classificationLayer('Name','new_classoutput');
% lgraph = replaceLayer(lgraph,classLayer.Name,newClassLayer);

% % Graph
% figure('Units','normalized','Position',[0.3 0.3 0.4 0.4]);
% plot(lgraph)
% ylim([0,10])


% % Freeze Initial Layers
% layers = lgraph.Layers;
% connections = lgraph.Connections;
% addpath 'C:\Users\aalqatatsheh\Documents\MATLAB\Examples\R2020a\nnet\TransferLearningUsingGoogLeNetExample'
% layers(1:10) = freezeWeights(layers(1:10));
% lgraph = createLgraphUsingConnections(layers,connections);

% %Train Network Using ImageDataAugmenter
% pixelRange = [-30 30];
% scaleRange = [0.9 1.1];
% imageAugmenter = imageDataAugmenter('RandXReflection',true,'RandXTranslation',pixelRange,'RandYTranslation',pixelRange, 'RandXScale',scaleRange,'RandYScale',scaleRange);
% augimdsTrain = augmentedImageDatastore(inputSize(1:2),imdsTrain,'DataAugmentation',imageAugmenter);

% %Automatically resize validation images 
% augimdsValidation = augmentedImageDatastore(inputSize(1:2),imdsValidation);

% %number of Epochs to train and batch sizes
% miniBatchSize = 5;
% valFrequency = floor(numel(augimdsTrain.Files)/miniBatchSize);
% options = trainingOptions('sgdm', ...
%     'MiniBatchSize',miniBatchSize, ...
%     'MaxEpochs',8, ...
%     'InitialLearnRate',0.5e-4, ...
%     'Shuffle','every-epoch', ...
%     'ValidationData',augimdsValidation, ...
%     'ValidationFrequency',valFrequency, ...
%     'Verbose',false, ...
%     'Plots','training-progress');

% % train the network
% net = trainNetwork(augimdsTrain,lgraph,options);

% [YPred,probs] = classify(net,augimdsValidation);
% accuracy = mean(YPred == imdsValidation.Labels)
% idx = randperm(numel(imdsValidation.Files),4);
% figure
% for i = 1:4
%     subplot(2,2,i)
%     I = readimage(imdsValidation,idx(i));
%     imshow(I)
%     label = YPred(idx(i));
%     title(string(label) + ", " + num2str(100*max(probs(idx(i),:)),3) + "%");
% end
