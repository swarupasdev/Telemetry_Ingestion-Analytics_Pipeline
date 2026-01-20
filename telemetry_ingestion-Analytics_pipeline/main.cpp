#include <iostream>
#include <chrono>
#include <thread>
#include <random>

struct DataSample {
    long long timestamp;
    float cpu;
    float ram;
    float sensorA;
};

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dist(0.0f, 100.0f);

    const auto interval = std::chrono::milliseconds(500);

    while (true) {
        auto now = std::chrono::system_clock::now().time_since_epoch();
        long long ts = std::chrono::duration_cast<std::chrono::milliseconds>(now).count();

        DataSample s{
            ts,
            dist(gen),
            dist(gen),
            dist(gen)
        };

        std::cout << "ts=" << s.timestamp << " "
            << "cpu=" << s.cpu << "% "
            << "ram=" << s.ram << "% "
            << "sensorA=" << s.sensorA << "\n";

        std::this_thread::sleep_for(interval);
    }

    return 0;
}
