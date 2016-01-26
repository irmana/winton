
res= ones(size(y,1),1); %25%

for i = 1 : size(y,2) %179%

yy = loaded_y(: , i:i);
x1 = loaded_x\yy;
norm(loaded_x*x1-yy);

res = [res x1];

end

res(:, 1) = [];


csvwrite('extrafeatures.csv',res)