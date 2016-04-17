clear; clc; close all;

% Distance to calculate over
%
m = 0:.1:100;

% Attenuation Source: 
% http://www.timesmicrowave.com/calculator/?productId=71&frequency=2400&runLength=200&mode=calculate#form
%
y = 39.4/100*m; % RG-213
y1 = 14.2/100*m; % LMR-600

% Plot Results
%
semilogx(m,y,m,y1);
grid on;
ylabel('Attenuation (dB)');
xlabel('Distance (m)');
legend('RG-213','LMR-600')
title('Coaxial Attenuation')
hold on
str1 = 'Distance of 60m\rightarrow';
plot([1 1]*60, ylim,'--r');
ylimits = ylim();
text(60, ylimits(2)/2, str1, 'Color', 'red', 'HorizontalAlignment', ...
    'right');


