#include <iostream>
#include <chrono>
#include <thread>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dist(0.0f, 100.0f);

    while (true) {
        auto now = std::chrono::system_clock::now();
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
            now.time_since_epoch()
        ).count();

        float cpu = dist(gen);
        float ram = dist(gen);

        std::cout << "timestamp=" << ms
            << " cpu=" << cpu
            << " ram=" << ram
            << std::endl;

        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    return 0;
}
