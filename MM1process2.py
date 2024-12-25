import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# 参数设置
lambda_rates = [5, 7, 9, 11]  # 不同的到达率 λ
mu_rates = [8, 10, 12, 15]  # 不同的服务率 μ
simulation_time = 10000  # 仿真总时间
pkCount = 500  # 随机时间点的数量

# 计算理论值
def calculate_theoretical_values(lambda_rate, mu_rate):
    rho = lambda_rate / mu_rate
    Lq_theoretical = rho / (1 - rho)  # 理论排队长度
    Wq_theoretical = rho / (1 - rho) * (1 / mu_rate)  # 理论等待时间
    W_theoretical = 1 / (mu_rate * (1 - rho))  # 理论系统内停留时间
    return Lq_theoretical, Wq_theoretical, W_theoretical

# M/M/1 排队系统
def customer(env, server, queue_length, wait_times, system_times, random_times, random_queue_lengths,
             queue_length_after_service):
    arrival_time = env.now
    queue_length.append(len(server.queue))  # 记录顾客到达时的队列长度

    if int(env.now) in random_times:
        random_queue_lengths.append(len(server.queue))

    with server.request() as request:
        yield request
        wait_time = env.now - arrival_time  # 等待时间
        wait_times.append(wait_time)
        service_time = random.expovariate(mu_rate)  # 服务时间服从负指数分布
        yield env.timeout(service_time)

        queue_length_after_service.append(len(server.queue))  # 服务完毕后记录队列长度
        system_time = env.now - arrival_time  # 系统停留时间
        system_times.append(system_time)

# 随机选择时间点观察队列长度
def generate_random_times(total_time, num_points):
    return sorted(random.sample(range(1, total_time), num_points))

# 仿真函数
def run_simulation(lambda_rate, mu_rate):
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)  # 单服务员
    queue_length = []  # 用于记录顾客到达时队列长度
    wait_times = []  # 等待时间
    system_times = []  # 系统内停留时间
    random_queue_lengths = []  # 随机时间点观察到的队列长度
    queue_length_after_service = []  # 顾客服务完毕后观察到的队列长度

    random_times = generate_random_times(simulation_time, pkCount)

    def generate_customers():
        while True:
            inter_arrival_time = random.expovariate(lambda_rate)  # 到达时间服从泊松分布
            yield env.timeout(inter_arrival_time)
            env.process(
                customer(env, server, queue_length, wait_times, system_times, random_times, random_queue_lengths,
                         queue_length_after_service))

    env.process(generate_customers())
    env.run(until=simulation_time)

    # 返回仿真结果
    return np.mean(queue_length), np.mean(wait_times), np.mean(system_times), \
           np.mean(random_queue_lengths), np.mean(queue_length_after_service)

# 保存结果
results = []

# 对多个lambda和mu值进行循环
for lambda_rate in lambda_rates:
    for mu_rate in mu_rates:
        avg_queue_length, avg_wait_time, avg_system_time, avg_random_queue_length, avg_queue_length_after_service = run_simulation(lambda_rate, mu_rate)
        results.append({
            "lambda": lambda_rate,
            "mu": mu_rate,
            "avg_queue_length": avg_queue_length,
            "avg_wait_time": avg_wait_time,
            "avg_system_time": avg_system_time
        })

# 输出计算结果
for result in results:
    print(f"λ={result['lambda']}, μ={result['mu']} -> 平均排队长度: {result['avg_queue_length']:.2f}, "
          f"平均等待时间: {result['avg_wait_time']:.2f}, 平均系统停留时间: {result['avg_system_time']:.2f}")

# 绘制不同λ和μ下的仿真结果
lambdas = [result['lambda'] for result in results]
mus = [result['mu'] for result in results]
avg_queue_lengths = [result['avg_queue_length'] for result in results]
avg_wait_times = [result['avg_wait_time'] for result in results]
avg_system_times = [result['avg_system_time'] for result in results]

# 绘制平均排队长度
plt.figure(figsize=(10, 6))
plt.scatter(lambdas, avg_queue_lengths, c=mus, cmap='viridis', label='Average Queue Length', s=100)
plt.colorbar(label='Service Rate μ')
plt.title("Average Queue Length vs. Arrival Rate (λ) and Service Rate (μ)")
plt.xlabel('Arrival Rate λ')
plt.ylabel('Average Queue Length')
plt.grid(True)
plt.show()

# 绘制平均等待时间
plt.figure(figsize=(10, 6))
plt.scatter(lambdas, avg_wait_times, c=mus, cmap='viridis', label='Average Wait Time', s=100)
plt.colorbar(label='Service Rate μ')
plt.title("Average Wait Time vs. Arrival Rate (λ) and Service Rate (μ)")
plt.xlabel('Arrival Rate λ')
plt.ylabel('Average Wait Time')
plt.grid(True)
plt.show()

# 绘制平均系统内停留时间
plt.figure(figsize=(10, 6))
plt.scatter(lambdas, avg_system_times, c=mus, cmap='viridis', label='Average System Time', s=100)
plt.colorbar(label='Service Rate μ')
plt.title("Average System Time vs. Arrival Rate (λ) and Service Rate (μ)")
plt.xlabel('Arrival Rate λ')
plt.ylabel('Average System Time')
plt.grid(True)
plt.show()
