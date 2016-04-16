
%%
clear; clc; close all;

% Input parameters
%
routerPdBm = 19; % Output of power router in dBm
f = 2.4E3; % Operating frequency in MHz
cableL = 60; % Legnth from 7th floor to Temple ENGR Roof in meters
ampPdB = 17; % Ampifier Gain dB (Avg)

% Path Loss
% Distance to calculate over
%
R = 1:.1:500;% Distance travel in km
Ku = 32.45; % Constant depending on units of R
G1 = 13; % Gain of the attenna
G2 = G1;

% Path Loss per km Calculation
% Source MILLIGAN 2005
%
pathLossdB = Ku + 20*log10(R*f)-G1-G2;

% Cable Attenuation
% Distance to calculate over
%
cableAttndB = 14.2/100*cableL; % LMR-600 (in dB)

% Link Budget
%
TxPdBm = routerPdBm + ampPdB - cableAttndB;
RxPdBm = TxPdBm - pathLossdB;

% Plot Results
%
semilogx(R,RxPdBm);
grid on;
ylabel('Rx Power (dBm)');
xlabel('Distance (km)');
legend(['Rx Power @ 2.4GHz w/ Tx Power = ' int2str(TxPdBm) 'dBm'])
title('Communication Link with Theoretical Path Loss')
hold on
% Rx sensitivity
% Source: http://community.linksys.com/t5/Wireless-Routers/WRT54GL-receiver-sensitivity-for-the-802-11b-standard/td-p/266342
data54 = -65;
data12 = -83;
data9 = -84;
data6 = -86;

% Find distances where we reach Rx sensitivity
%
[~, index54] = min(abs(RxPdBm-data54));
[~, index12] = min(abs(RxPdBm-data12));
[~, index9] = min(abs(RxPdBm-data9));
[~, index6] = min(abs(RxPdBm-data6));

% Create descriptive strings
%
str54 = ['\leftarrow Max Distance for 54Mbps=' int2str(R(index54)) 'km'];
str12 = ['Max Distance for 12Mbps=' int2str(R(index12)) 'km \rightarrow'];
str9 = ['\leftarrow Max Distance for 9Mbps=' int2str(R(index9)) 'km'];
str6 = ['Max Distance for 6Mbps=' int2str(R(index6)) 'km \rightarrow'];;

% Plot Results
%
hold on
text(R(index54), RxPdBm(index54), str54, 'Color', 'red', ...
    'HorizontalAlignment', 'left');
text(R(index12), RxPdBm(index12), str12, 'Color', 'red', ...
    'HorizontalAlignment', 'right');
text(R(index9), RxPdBm(index9), str9, 'Color', 'red', ...
    'HorizontalAlignment', 'left');
text(R(index6), RxPdBm(index6), str6, 'Color', 'red', ...
    'HorizontalAlignment', 'right');
