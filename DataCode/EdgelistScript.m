Nets = {'Haverford76','Hamilton46','Amherst41','Williams40','Caltech36','Reed98','Simmons81'};

for i = 1:numel(Nets)
    GetFacebookEdgelists(Nets(i))
end