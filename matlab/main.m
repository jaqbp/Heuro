%_________________________________________________________________________
% Gazelle Optimization Algorithm source code 
%
%  
% paper:
% Jeffrey O. Agushaka, Absalom E. Ezugwu and Laith Abualigah
% Gazelle Optimization Algorithm: A Nature-inspired Metaheuristic
%  
%  
% E-mails: 218088307@stu.ukzn.ac.za            Jeffrey O. Agushaka 
%           ezugwuA@ukzn.ac.za                 Absalom E. Ezugwu
%           aligah@ammanu.edu.jo               Laith Abualigah
%_________________________________________________________________________

clear all
clc
format long
SearchAgents_no=50; % Number of search agents

Function_name='F5';
   
Max_iteration=1000; % Maximum number of iterations

[lb,ub,dim,fobj]=Get_Functions_details(Function_name);

[Best_score,Best_pos,Convergence_curve]=GOA2(SearchAgents_no,Max_iteration,lb,ub,dim,fobj);

% function topology
figure('Position',[500 400 700 290])
subplot(1,2,1);
func_plot(Function_name);
title('Function Topology')
xlabel('x_1');
ylabel('x_2');
zlabel([Function_name,'( x_1 , x_2 )'])

% Convergence curve
subplot(1,2,2);
semilogy(Convergence_curve,'Color','r')
title('Objective space')
xlabel('Iteration');
ylabel('Best score obtained so far');


display(['The best solution obtained by GOA is : ', num2str(Best_pos,10)]);
display(['The best optimal value of the objective function found by GOA is : ', num2str(Best_score,10)]);
disp(sprintf('--------------------------------------'));
