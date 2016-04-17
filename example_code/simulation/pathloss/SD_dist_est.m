% script to calculate simulated distance and output power
% Author: Robert Irwin
clear; clc; clf;
d_act = 20; %km

path_loss = 32.45 + 20*log10(2400*d_act) - 26; %dB

rx_pow = 27-path_loss;

%tx_pow = 1;
sim_dist = .0628;
const = log10(2400*sim_dist); 
% const = (tx_pow-rx_pow - 32.45)/20;
tx_pow = 20*const+rx_pow+32.45;
%sim_dist = (10^const)/2400;
const = log10(2400*sim_dist); 
% results
rb = [571 800 1e3 1.9e3 2.6e3]; %kB/sec 
rb = rb.*8; %kb/sec
SNR = [16 20 22 26 32]; %dB
d = [25 20 16 10 3.1]; %km

figure(1)
plot(d,rb./1000)
grid on
xlabel('distance (km)')
ylabel('Data Rate (Mbps)')
title('Effective Data Rate as a Function of Distance')

figure(2)
plot(d, SNR)
grid on
xlabel('distance (km)')
ylabel('Signal to Noise Ratio (dB)')
title('SNR as a Function of Distance')
