import matplotlib.pyplot as plt

# Khai báo danh sách lưu trữ dữ liệu từ tệp
conflict = []
temperature = []

# Đọc dữ liệu từ tệp
with open('sa_step_print.txt', 'r') as file:
    for line in file:
        data = line.split()
        temperature.append(float(data[1]))
        conflict.append(float(data[0]))

# Đảo ngược dữ liệu trên trục x để có trục giảm dần từ 1000 về 0 từ trái sang phải
temperature.reverse()
conflict.reverse()

# Số lượng điểm bạn muốn hiển thị (ví dụ: mỗi 2 điểm)
step = 10

# Chọn một số điểm để hiển thị
temperature_thinned = temperature[::step]
conflict_thinned = conflict[::step]

# Vẽ biểu đồ
plt.plot(temperature_thinned, conflict_thinned, marker='o', linestyle='-')
plt.xlabel('Temperature')
plt.ylabel('Conflict')
plt.title('Biểu đồ Conflict và Temperature')
plt.grid(True)

# Đảo ngược trục x để đánh số từ 1000 về 0 từ trái sang phải
plt.gca().invert_xaxis()

# Hiển thị đồ thị
plt.show()
