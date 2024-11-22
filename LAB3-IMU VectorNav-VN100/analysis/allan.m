% Load CSV data
data = readtable('/home/shrirag10/LAB3/src/imu_data.csv');  % Replace with your actual file path

% Extract accelerometer and gyroscope data
accel_x = data.accel_x;  % Adjust column names as per your CSV
accel_y = data.accel_y;  % Adjust column names as per your CSV
accel_z = data.accel_z;  % Adjust column names as per your CSV
gyro_x = data.gyro_x;    % Adjust column names as per your CSV
gyro_y = data.gyro_y;    % Adjust column names as per your CSV
gyro_z = data.gyro_z;    % Adjust column names as per your CSV

% Combine the accelerometer and gyroscope axes data
accel_combined = sqrt(accel_x.^2 + accel_y.^2 + accel_z.^2);
gyro_combined = sqrt(gyro_x.^2 + gyro_y.^2 + gyro_z.^2);

% Sampling time interval (assuming uniform sampling)
dt = 1 / 100;  % Adjust based on your actual sampling rate

% Function to compute Allan deviation
function [taus, allan_deviation] = compute_allan_deviation(data, dt)
    N = length(data);   % Number of data points
    max_tau = floor(N / 2);  % Maximum tau is half the data length
    taus = logspace(log10(1), log10(max_tau), 50);  % Tau values spaced logarithmically
    
    allan_deviation = zeros(size(taus));  % Initialize Allan deviation array
    
    for i = 1:length(taus)
        tau = round(taus(i));  % Ensure tau is an integer
        num_averages = floor(N / tau);  % Number of averages for this tau
        
        if num_averages < 2
            allan_deviation(i) = NaN;  % Skip computation for invalid values
            continue;
        end

        % Compute the averages of the data over non-overlapping windows of size tau
        avg_values = arrayfun(@(j) mean(data((j-1)*tau + 1 : j*tau)), 1:num_averages);
        
        % Compute the Allan variance
        allan_var = 0.5 * mean(diff(avg_values).^2);
        
        % Store Allan deviation (sqrt of variance)
        allan_deviation(i) = sqrt(allan_var);
    end
end

% Calculate Allan deviation for combined accelerometer and gyroscope data
[tau_accel, allan_dev_accel] = compute_allan_deviation(accel_combined, dt);
[tau_gyro, allan_dev_gyro] = compute_allan_deviation(gyro_combined, dt);

% Filter valid tau and Allan deviation values for accelerometer
valid_idx_accel = ~isnan(allan_dev_accel) & allan_dev_accel > 0;

% Plot Allan deviation for Accelerometer
figure;
loglog(tau_accel(valid_idx_accel), allan_dev_accel(valid_idx_accel), 'b', 'LineWidth', 2);
xlabel('\tau (s)');
ylabel('\sigma(\tau) (m/s^2)');
title('Allan Deviation for Accelerometer');
grid on;

% Filter valid tau and Allan deviation values for gyroscope
valid_idx_gyro = ~isnan(allan_dev_gyro) & allan_dev_gyro > 0;

% Plot Allan deviation for Gyroscope
figure;
loglog(tau_gyro(valid_idx_gyro), allan_dev_gyro(valid_idx_gyro), 'g', 'LineWidth', 2);
xlabel('\tau (s)');
ylabel('\sigma(\tau) (rad/s)');
title('Allan Deviation for Gyroscope');
grid on;


%Debbugging
disp('First 5 rows of accelerometer combined data:');
disp(accel_combined(1:5));

disp('First 5 rows of gyroscope combined data:');
disp(gyro_combined(1:5));

disp('Tau values for accelerometer:');
disp(tau_accel(1:5));

disp('Allan deviation for accelerometer:');
disp(allan_dev_accel(1:5));

disp('Tau values for gyroscope:');
disp(tau_gyro(1:5));

disp('Allan deviation for gyroscope:');
disp(allan_dev_gyro(1:5));
% Plot raw combined accelerometer data
figure;
plot(accel_combined);
title('Raw Accelerometer Data');
xlabel('Sample Index');
ylabel('Acceleration (m/s^2)');
grid on;

% Plot raw combined gyroscope data
figure;
plot(gyro_combined);
title('Raw Gyroscope Data');
xlabel('Sample Index');
ylabel('Angular Velocity (rad/s)');
grid on;
