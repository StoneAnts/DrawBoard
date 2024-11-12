import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import directed_hausdorff

# 3D绘图函数
def plot_3d_shape(points, ax, color='b', label='Shape'):
    points = np.array(points)
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color=color, label=label)
    ax.plot(points[:, 0], points[:, 1], points[:, 2], color=color)  # 可连接各点

# 计算Hausdorff距离函数
def hausdorff_distance(points1, points2):
    points1 = scale_to_target(align_points(points1)) # 中心对齐，统一缩放
    points2 = scale_to_target(align_points(points2)) # 中心对齐，统一缩放
    points2 = rotational_alignment(points2, points1) # points2相对于points1做旋转对齐
    plot_3d_shape(points1, ax, color='black', label='Shape 3')
    plot_3d_shape(points2, ax, color='yellow', label='Shape 4')
    #plot_3d_shape(points3, ax, color='blue', label='Shape 5')
    d1 = directed_hausdorff(points1, points2)[0]
    d2 = directed_hausdorff(points2, points1)[0]
    return max(d1, d2)

# 中心对齐
def align_points(points):
      # 计算中心
      center = np.mean(points, axis=0)
      # 平移中心到原点
      aligned_points = points - center
      return aligned_points

# 统一缩放
def scale_to_target(points, target_size=100):
  # 获取边界框
  min_x = min(point[0] for point in points)
  max_x = max(point[0] for point in points)
  min_y = min(point[1] for point in points)
  max_y = max(point[1] for point in points)
  min_z = min(point[2] for point in points)
  max_z = max(point[2] for point in points)
  
  # 计算边界框宽度和高度
  length = max_x - min_x
  width = max_y - min_y
  height = max_z - min_z
  
  # 计算缩放因子
  scale_factor_x = target_size / length
  scale_factor_y = target_size / width
  scale_factor_z = target_size / height
  scale_factor = min(scale_factor_x, scale_factor_y, scale_factor_z)  # 选择较小的因子以保持比例
  
  # 缩放点集   
  scaled_points = [(scale_factor * (x - min_x), scale_factor * (y - min_y), scale_factor * (z - min_z)) for x, y, z in points]
  return scaled_points

# 旋转对齐，使用Kabsch algorithm找到两个点集之间的最优旋转对齐
def rotational_alignment(source_points, target_points):
  # 计算质心
  centroid_source = np.mean(source_points, axis=0)
  centroid_target = np.mean(target_points, axis=0)

  # 去中心化
  source_centered = source_points - centroid_source
  target_centered = target_points - centroid_target

  # SVD 分解
  H = np.dot(source_centered.T, target_centered)
  U, S, Vt = np.linalg.svd(H)
  R_matrix = np.dot(Vt.T, U.T)

  # 将源点集旋转对齐
  aligned_points = np.dot(source_points - centroid_source, R_matrix) + centroid_target
  return aligned_points

# 样例输入两组3D坐标点
shape1 = 3 * np.array([[1, 2, 3], [4, 6, 5], [7, 3, 8], [1, 2, 3]])
shape2 = np.array([[1, 3, 4], [4, 5, 8], [7, 8, 5], [1, 3, 4]])

# 创建3D绘图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plot_3d_shape(shape1, ax, color='r', label='Shape 1')
plot_3d_shape(shape2, ax, color='g', label='Shape 2')

ax.legend()
plt.title("3D Shape Visualization")

# 计算并显示Hausdorff距离
distance = hausdorff_distance(shape1, shape2)
print(f"Hausdorff Distance between Shape 1 and Shape 2: {distance:.2f}")

plt.show()