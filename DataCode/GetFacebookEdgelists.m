function GetFacebookEdgelists(Network)
    path = strcat(MATLAB_Path(),'facebook100\');
    NetworkFile = strcat(path,Network,'.mat');
    SavePath = 'NetworkSimulations\SimulationCode\';
    SaveFile = strcat(MATLAB_Path(),SavePath,Network,'_Edgelist.csv');

    load(char(NetworkFile))

    [row col v] = find(A);

    dlmwrite(char(SaveFile),[col,row],'delimiter',',');
end