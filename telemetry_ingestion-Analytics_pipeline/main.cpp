#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <chrono>
#include <random>
#include <fstream>

struct DataSample {
    long long timestamp;
    float cpu;
    float ram;
    float sensorA;
};

std::queue<DataSample> buffer;
std::mutex mtx;
std::condition_variable cv;
bool running = true;

void producer() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dist(0.0f, 100.0f);

    while (running) {
        auto now = std::chrono::system_clock::now().time_since_epoch();
        long long ts = std::chrono::duration_cast<std::chrono::milliseconds>(now).count();

        DataSample s{ ts, dist(gen), dist(gen), dist(gen) };

        {
            std::lock_guard<std::mutex> lock(mtx);
            buffer.push(s);
        }

        cv.notify_one();
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
}

void consumer() {
    std::ofstream file("telemetry.csv", std::ios::app);

    if (!file.is_open()) {
        std::cerr << "Failed to open telemetry.csv\n";
        return;
    }

    file << "timestamp,cpu,ram,sensorA\n";
    file.flush();

    while (running) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [] { return !buffer.empty(); });

        DataSample s = buffer.front();
        buffer.pop();
        lock.unlock();

        file << s.timestamp << ","
            << s.cpu << ","
            << s.ram << ","
            << s.sensorA << "\n";

        file.flush();
    }
}

int main() {
    std::thread t1(producer);
    std::thread t2(consumer);

    t1.join();
    t2.join();
    return 0;
}
