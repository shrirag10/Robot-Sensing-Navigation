%% % Load data file
load('C:\Users\ragsh\Desktop\FALL 24\RSN\LAB4\data_going_in_circles.mat');

% Extract and convert magnetometer data from Tesla to milligauss
mag_x = imu.magnetometer_x * 1e7;  % Convert to milligauss
mag_y = imu.magnetometer_y * 1e7;  % Convert to milligauss
mag_z = imu.magnetometer_z * 1e7;  % Convert to milligauss

% Plot raw magnetometer data on the x-y plane
figure;
scatter(mag_x, mag_y, 10, 'filled');
xlabel('Magnetometer X (milligauss)');
ylabel('Magnetometer Y (milligauss)');
title('Raw Magnetometer Data (in milligauss)');
grid on;
%% % Hard-Iron Offset Calculation in milligauss
offset_x = (max(mag_x) + min(mag_x)) / 2;
offset_y = (max(mag_y) + min(mag_y)) / 2;

% Correct magnetometer readings for hard-iron effect
mag_x_corrected = mag_x - offset_x;
mag_y_corrected = mag_y - offset_y;

% Plot the magnetometer data after hard-iron correction
figure;
scatter(mag_x_corrected, mag_y_corrected, 10, 'filled');
xlabel('Magnetometer X (Corrected, milligauss)');
ylabel('Magnetometer Y (Corrected, milligauss)');
title('Magnetometer Data after Hard-Iron Correction');
grid on;
%% % Soft-Iron Scaling Calculation
scale_x = max(abs(mag_x_corrected));
scale_y = max(abs(mag_y_corrected));
scaling_factor = scale_x / scale_y;
mag_x_final = mag_x_corrected;
mag_y_final = mag_y_corrected * scaling_factor;

figure;
scatter(mag_x_final, mag_y_final, 10, 'filled');
xlabel('Magnetometer X (Soft-Iron Corrected, milligauss)');
ylabel('Magnetometer Y (Soft-Iron Corrected, milligauss)');
title('Magnetometer Data after Hard and Soft-Iron Correction');
grid on;
%% % Plot raw and corrected magnetometer data together in the same graph
figure;
hold on;
scatter(mag_x, mag_y, 10, 'filled', 'MarkerFaceColor', 'b');
scatter(mag_x_final, mag_y_final, 10, 'filled', 'MarkerFaceColor', 'r');

xlabel('Magnetometer X (milligauss)');
ylabel('Magnetometer Y (milligauss)');
title('Magnetometer Data: Raw (Blue) vs. Corrected (Red)');
legend('Raw Data', 'Corrected Data');
grid on;
hold off;
%% % Load the data from data_driving.mat
load('C:\Users\ragsh\Desktop\FALL 24\RSN\LAB4\data_driving.mat');
%% % Assuming data_driving.mat has a structure similar to data_going_in_circles.mat with magnetometer data:
mag_x_raw_driving = imu.magnetometer_x * 1e7; % Convert raw data from tesla to milligauss
mag_y_raw_driving = imu.magnetometer_y * 1e7; % Convert raw data from tesla to milligauss

% Apply previously obtained calibration (hard-iron correction using offsets)
mag_x_corrected_driving = mag_x_raw_driving - offset_x;
mag_y_corrected_driving = mag_y_raw_driving - offset_y * scaling_factor;

yaw_angle_raw = atan2(mag_y_raw_driving, mag_x_raw_driving); % Raw yaw in radians
yaw_angle_corrected = atan2(mag_y_corrected_driving, mag_x_corrected_driving); % Corrected yaw in radians
figure;
plot(yaw_angle_raw, 'b');
hold on;
plot(yaw_angle_corrected, 'r');
xlabel('Sample Index');
ylabel('Yaw Angle (Radians)');
title('Raw vs. Corrected Yaw Angle from Magnetometer Data');
legend('Raw Magnetometer Yaw', 'Corrected Magnetometer Yaw');
grid on;
hold off;

%% % Extract relevant data from the IMU structure

gyro_z = imu.angular_velocity_z;  % Gyro z-axis data in radians/sec
timestamps = imu.timestamps;      % Timestamps in seconds
yaw_mag_unwrapped = unwrap(yaw_angle_corrected);
% Call the custom integration function
yaw_angle_gyro = custom_integration(gyro_z, timestamps);

figure;
plot(yaw_angle_corrected, 'r');  % Corrected magnetometer yaw (from previous step)
hold on;
plot(yaw_angle_gyro, 'g');       % Integrated yaw from gyro (custom integration)
xlabel('Sample Index');
ylabel('Yaw Angle (Radians)');
title('Comparison of Magnetometer and Gyroscope Yaw Angles');
legend('Magnetometer Yaw (Corrected)', 'Gyroscope Yaw (Integrated - Custom)');
grid on;
hold off;
function yaw_angle = custom_integration(gyro_z, timestamps)
    % Custom trapezoidal integration of yaw rate (gyro_z) over time.
    n = length(gyro_z);  % Number of data points
    yaw_angle = zeros(n, 1);  % Pre-allocate yaw angle array

    % Loop through data points and apply trapezoidal rule
    for i = 2:n
        dt = timestamps(i) - timestamps(i - 1);  % Time difference
        yaw_angle(i) = yaw_angle(i - 1) + 0.5 * (gyro_z(i) + gyro_z(i - 1)) * dt;
    end
end
%% % Low-pass filter parameters- Plotting Comparison of Filters
low_cutoff_frequency = 0.08;  % Define a cutoff frequency (adjust as needed)
Fs = 1 / mean(diff(timestamps));  % Sample frequency

mag_yaw_low_pass = lowpass(yaw_angle_corrected, low_cutoff_frequency, Fs);
high_cutoff_frequency = 0.03;  % Define a cutoff frequency (adjust as needed)
gyro_yaw_high_pass = highpass(yaw_angle_gyro, high_cutoff_frequency, Fs);

alpha = 0.90;  % Weighting factor (0 < alpha < 1)
n = length(yaw_mag_unwrapped);
yaw_fused = zeros(n, 1);  % Pre-allocate for performance
yaw_fused(1) = mag_yaw_low_pass(1);  % Start with the first low-pass value

for i = 2:n
    % High-pass filter on gyro (yaw rate integration)
    gyro_term = yaw_fused(i-1) + gyro_yaw_high_pass(i) * mean(diff(timestamps));
    
    % Low-pass filter on magnetometer
    mag_term = mag_yaw_low_pass(i);
    
    % Fuse the estimates
    yaw_fused(i) = alpha * gyro_term + (1 - alpha) * mag_term;
end

figure;
plot(timestamps, mag_yaw_low_pass, 'b', 'LineWidth', 1.5); hold on;
plot(timestamps, gyro_yaw_high_pass, 'g', 'LineWidth', 1.5);
plot(timestamps, yaw_fused, 'r', 'LineWidth', 2);
xlabel('Time (s)');
ylabel('Yaw Angle (Radians)');
legend('Low-pass Filter (Magnetometer)', ...
       'High-pass Filter (Gyroscope)', ...
       'Complementary Filter (Fused)');
title('Comparison of Low-pass, High-pass, and Complementary Filters');
grid on;
hold off;

%%  Assuming mag_x_final and mag_y_final are defined
% Calculate yaw from corrected magnetometer data
imu_yaw = atan2(mag_y_final, mag_x_final);  
imu_yaw = imu_yaw(:);  
window_size = 5;  
num_timestamps = length(timestamps);
num_imu_yaw = length(imu_yaw);
if num_imu_yaw > num_timestamps
    imu_yaw = imu_yaw(1:num_timestamps);
elseif num_imu_yaw < num_timestamps
  
    imu_yaw = [imu_yaw; repmat(imu_yaw(end), num_timestamps - num_imu_yaw, 1)];
end
imu_yaw_interp = interp1(1:length(imu_yaw), imu_yaw, linspace(1, length(imu_yaw), num_timestamps), 'linear', 'extrap');
fused_yaw_smoothed = movmean(yaw_fused, window_size);

figure;
plot(timestamps, yaw_fused, 'r', 'LineWidth', 1.5); hold on;  % Fused yaw
plot(timestamps, imu_yaw_interp, 'k--', 'LineWidth', 1.5);   % IMU yaw in dashed black
xlabel('Time (s)');
ylabel('Yaw Angle (Radians)');
legend('Fused Yaw (Complementary Filter)', 'IMU Yaw (From Magnetometer)');
title('Comparison of Fused Yaw vs IMU Yaw');
grid on;
hold off;
%% Part-2 Velocity Estimation 
R = 6371000;
% Extract latitude, longitude, and timestamps from GPS data
latitudes = gps.latitude;
longitudes = gps.longitude;
time_g = gps.timestamps;
timevector_g = time_g - time_g(1);
num_points = length(latitudes);
velocity_g = zeros(1, num_points - 1);
for i = 2:num_points
    % Convert lat-long to radians
    lat1 = deg2rad(latitudes(i-1));
    lon1 = deg2rad(longitudes(i-1));
    lat2 = deg2rad(latitudes(i));
    lon2 = deg2rad(longitudes(i));
      
    dlat = lat2 - lat1;
    dlon = lon2 - lon1;
    a = sin(dlat/2)^2 + cos(lat1) * cos(lat2) * sin(dlon/2)^2;
    c = 2 * atan2(sqrt(a), sqrt(1-a));
    distance = R * c;
    dt = timevector_g(i) - timevector_g(i-1);
    
    if dt > 0
        velocity_g(i-1) = distance / dt;
    else
        velocity_g(i-1) = 0;
    end
end

velocity_g(end+1) = velocity_g(end);

[unique_timevector_g, ~, ic] = unique(timevector_g);
unique_velocity_g = zeros(size(unique_timevector_g));
for i = 1:length(unique_timevector_g)
    unique_velocity_g(i) = mean(velocity_g(ic == i));
end
assert(length(unique_timevector_g) == length(unique_velocity_g), 'Lengths must match after uniquification');
assert(issorted(unique_timevector_g), 'Timestamps must be sorted');


forward_acceleration = imu.linear_acceleration_x;
timestamps = imu.timestamps;
timevector_imu = timestamps - timestamps(1);

velocity_g_interp = interp1(unique_timevector_g, unique_velocity_g, timevector_imu, 'linear', 'extrap');

stationary_indices = timestamps <= timestamps(1) + 10;
offset_x = mean(forward_acceleration(stationary_indices)); %Offesetting IMU Velocity
corrected_accel_x = forward_acceleration - offset_x;

velocity_x = cumtrapz(timevector_imu, corrected_accel_x);

figure;
hold on;
plot(timevector_imu, velocity_x, 'b-', 'LineWidth', 1.5); % Corrected IMU velocity
plot(timevector_imu, velocity_g_interp, 'r-', 'LineWidth', 1.5); % Interpolated GPS velocity
title('Comparison of  IMU Velocity and Interpolated GPS Velocity-Before Adjustment');
xlabel('Time (s)');
ylabel('Velocity (m/s)');
legend('IMU Velocity', 'GPS Velocity');
grid on;
hold off;
%% Filtering of IMU Velocity
% High-pass filter specifications for IMU velocity adjustment
fs = 1 / mean(diff(timevector_imu)); % Sampling frequency
cutoff_freq = 0.1; 
[b, a] = butter(2, cutoff_freq / (fs / 2), 'high'); 
velocity_x_filtered = filtfilt(b, a, velocity_x);
velocity_x_filtered(velocity_x_filtered < 0) = 0; %--For eliminating the negative values
% --- Plot 1: GPS Velocity vs. IMU Velocity (Before Adjustment) ---
figure;
hold on;
plot(timevector_imu, velocity_x, 'b-', 'LineWidth', 1.5); % Original offset-corrected IMU velocity
plot(timevector_imu, velocity_g_interp, 'r-', 'LineWidth', 1.5); % Interpolated GPS velocity
title('Comparison of GPS Velocity with IMU Velocity (Before Adjustment)');
xlabel('Time (s)');
ylabel('Velocity (m/s)');
legend(' IMU Velocity', 'GPS Velocity');
grid on;
hold off;

fs_gps = 1 / mean(diff(timevector_imu)); % Sampling frequency for GPS (assuming aligned with IMU time vector)
cutoff_freq_gps = 0.6; % Cutoff frequency in Hz (adjust as needed to control smoothing)
[b_gps, a_gps] = butter(2, cutoff_freq_gps / (fs_gps / 2), 'low'); % 2nd order Butterworth low-pass filter
velocity_g_smooth_adjusted = filtfilt(b_gps, a_gps, velocity_g_interp); % Smoothed GPS velocity
imu_start_value = velocity_x_filtered(1); % Starting value of IMU after high-pass filtering
gps_start_value = velocity_g_smooth_adjusted(1); % Starting value of GPS after low-pass filtering
velocity_g_smooth_adjusted = velocity_g_smooth_adjusted - gps_start_value + imu_start_value;
figure;
hold on;
velocity_x_filtered= velocity_x_filtered*2.5;%Scaling factor
plot(timevector_imu, velocity_x_filtered, 'b-', 'LineWidth', 1.5); % High-pass filtered IMU velocity
plot(timevector_imu,smoothdata(velocity_g_smooth_adjusted,'gaussian',10), 'r-', 'LineWidth', 2); % Adjusted and smoothed GPS velocity
title('Comparison of GPS Velocity with IMU Velocity (After Adjustments)');
xlabel('Time (s)');
ylabel('Velocity (m/s)');
legend(' IMU Velocity', ' GPS Velocity');
grid on;
hold off;
%% Dead reckoning
% Define parameters for low-pass filter
lp_fc = 0.2;  % Low-pass cutoff frequency
order = 4;    % Filter order
fs = 1 / mean(diff(timevector_imu));  % Sampling frequency based on IMU timestamps
nyq = 0.5 * fs;
lp_fc_norm = lp_fc / nyq;
[b, a] = butter(order, lp_fc_norm, 'low');

forward_velocity = velocity_x;  % Forward velocity (X_dot)
angular_velocity_z = imu.angular_velocity_z;  % Angular velocity ω about z-axis
lateral_acceleration_y = imu.linear_acceleration_y;  % Lateral acceleration (Ÿ_obs)
wX_dot = angular_velocity_z .* forward_velocity;
Y_dot_dot_filtered = filtfilt(b, a, lateral_acceleration_y);

figure;
hold on;
plot(timevector_imu, wX_dot, 'b-', 'LineWidth', 1.5);  % wX_dot
plot(timevector_imu, detrend(Y_dot_dot_filtered), 'r-', 'LineWidth', 1.5);  % Filtered Ÿ_obs (detrended)
xlabel('Time (s)');
ylabel('Acceleration (m/s^2)');
title('Dead Reckoning using IMU and GPS Data');
legend('ωẊ (wX\_dot)', 'Filtered Ÿ\_obs (Y\_dot\_dot)');
grid on;
hold off;

% Plot difference
figure;
plot(timevector_imu, difference, 'k-', 'LineWidth', 1.5);
xlabel('Time (s)');
ylabel('Difference (m/s^2)');
title('Difference between ωẊ and Filtered Ÿ\_obs');
grid on;

%% % Extract complementary filter yaw (in radians) and forward velocity
% Data Extraction and Preprocessing
% Extract time data and normalize start time to zero
time_driving = imu.timestamps(~any(isnan(yaw_mag_unwrapped), 2), :);
time_driving = time_driving - time_driving(1);

% Use filtered velocity data
corrected_velocity_x = velocity_x_filtered;

% Calculate displacement from velocity using trapezoidal integration
accel_displacement = trapz(time_driving, corrected_velocity_x);

% Extract GPS eastings and northings, ignoring NaNs
gps_indices = ~isnan(gps.utm_easting) & ~isnan(gps.utm_northing);
eastings = gps.utm_easting(gps_indices);
northings = gps.utm_northing(gps_indices);

% Normalize GPS data to align with the start point
eastings_zeroed = eastings - eastings(1);
northings_zeroed = northings - northings(1);

%% IMU Trajectory Calculation
% Extract and normalize yaw from gyro data
yaw_gyro = yaw_angle_gyro - yaw_angle_gyro(1);
vn = corrected_velocity_x .* cos(yaw_gyro);  % Northing velocity
ve = corrected_velocity_x .* sin(yaw_gyro);  % Easting velocity
xe = cumtrapz(time_driving, ve);  % Easting displacement
xn = cumtrapz(time_driving, vn);  % Northing displacement

%% Align IMU Trajectory with GPS
% Compute initial heading angles
gps_heading_o = atan2(northings(2) - northings(1), eastings(2) - eastings(1));
imu_heading_o = yaw_gyro(1);

% Calculate rotation angle to align IMU with GPS
rotation_angle = gps_heading_o - imu_heading_o;

% Rotate IMU-derived trajectory for alignment
xe_rotated = xe * cos(rotation_angle) - xn * sin(rotation_angle);
xn_rotated = xe * sin(rotation_angle) + xn * cos(rotation_angle);

%% Plotting the Trajectories
figure;
cla;  % Clear current axes to prevent multiple plots
hold on;

% Plot IMU Trajectory (Blue) - Only once
plot(xe_rotated, xn_rotated, 'b-', 'DisplayName', 'IMU Trajectory', 'LineWidth', 1.5);

% Plot GPS Trajectory (Red) - Only once
plot(eastings_zeroed, northings_zeroed, 'r-', 'DisplayName', 'GPS Trajectory', 'LineWidth', 1.5);

% Formatting the Plot
xlabel('Easting Position (m)');
ylabel('Northing Position (m)');
title('Estimated Vehicle Trajectory');
legend('show');
grid on;
axis equal;
hold off;
%% % Assuming the following variables are already in your workspace:
% Define downsampling factor

downsample_factor = 2;
forward_acceleration = - forward_acceleration;
time_ds = downsample(time_driving, downsample_factor);
ax_ds = downsample(forward_acceleration, downsample_factor);
omega_ds = downsample(yaw_gyro, downsample_factor);
dt = diff(time_ds);
omega_dot = [0; diff(omega_ds)./dt];
omega_squared = omega_ds.^2;
min_omega = 0.1; 
min_omega_dot = 0.05;  

valid_points = abs(omega_ds) > min_omega & abs(omega_dot) > min_omega_dot;
xc_estimates = ax_ds ./ omega_squared;

valid_estimates = xc_estimates(valid_points);
valid_estimates = valid_estimates(~isinf(valid_estimates) & ~isnan(valid_estimates));
median_est = median(valid_estimates);
mad = median(abs(valid_estimates - median_est));
inliers = abs(valid_estimates - median_est) < 3 * mad;
xc_final = mean(valid_estimates(inliers));

fprintf('Estimated xc: %.4f meters\n', xc_final);
fprintf('Number of valid estimates: %d\n', sum(inliers));
fprintf('Standard deviation: %.4f\n', std(valid_estimates(inliers)));
figure;
plot(time_ds(valid_points), xc_estimates(valid_points), 'b.', 'MarkerSize', 2);
hold on;
yline(xc_final, 'r-', 'LineWidth', 2);
xlabel('Time (s)');
ylabel('xc estimates (m)');
title('xc Estimates Over Time');
legend('Individual estimates', 'Final estimate');
grid on;