clear; clc; close all;

% Distance to calculate over
%
R = 0:.1:20;% Distance travel in km
f = 2.4E9; % Operating frequency
Ku = 32.45; % Constant depending on units of R
G1 = 13; % Gain of the attenna
G2 = G1;
TxP = 6 % 6db Router Power + 


% Path Loss Source MILLIGAN 2005
%
ydB = Ku+mag2db(R*f)-G1-G2; % RG-213
ydBm = ydB - 30;

% Plot Results
%
semilogx(R,ydBm);
grid on;
ylabel('Path Loss (dB)');
xlabel('Distance (km)');
legend('Path Loss at 2.4GHz')


