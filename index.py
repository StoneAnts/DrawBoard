import tkinter as tk
from scipy.spatial.distance import directed_hausdorff
import numpy as np

class DrawBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("画板")
        
        # 创建画布
        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=400)
        self.canvas.pack()
        
        # 初始化坐标列表
        self.coordinates = []
        self.point1 = []
        self.point2 = []
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-2>", self.save)
    
    def start_drawing(self, event):
        # 记录起始点
        self.last_x, self.last_y = event.x, event.y
        self.coordinates.append((self.last_x, self.last_y))
    
    def draw(self, event):
        # 获取当前坐标点
        x, y = event.x, event.y
        self.coordinates.append((x, y))
        
        # 在画布上绘制线条
        self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=2)
        
        # 更新上一个点为当前点
        self.last_x, self.last_y = x, y

    def save(self, event):
        self.point1 = self.coordinates
        self.coordinates = []
        #self.drawPoint(self.point1)

    def drawPoint(self, points):        
        # 创建主窗口
        root = tk.Tk()
        root.title("绘制坐标点")
        # 创建Canvas画布，设置尺寸
        canvas = tk.Canvas(root, width=600, height=400, bg="white")
        canvas.pack()

        # 绘制坐标点
        for x, y in points:
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", width=2)  # 画点，直径为10
            # 连接点（可选），绘制线段
        for i in range(len(points) - 1):
            canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill="blue", width=2)
          
        # 启动主循环
        root.mainloop()

    def hausdorff_similarity(self, shape1_points, shape2_points, threshold):
        # 中心对齐
        shape1_aligned = self.align_points(np.array(shape1_points))
        shape2_aligned = self.align_points(np.array(shape2_points))
        # 计算双向Hausdorff距离
        distance1 = directed_hausdorff(shape1_aligned, shape2_aligned)[0]
        distance2 = directed_hausdorff(shape2_aligned, shape1_aligned)[0]
        hausdorff_distance = max(distance1, distance2)
    
        # 判断是否相似
        if hausdorff_distance < threshold:
            return True, hausdorff_distance
        else:
            return False, hausdorff_distance

    def align_points(self, points):
      # 计算中心
      center = np.mean(points, axis=0)
      # 平移中心到原点
      aligned_points = points - center
      return aligned_points
# 创建主窗口并运行
root = tk.Tk()
app = DrawBoard(root)
root.mainloop()
print('point1: ', app.point1)
print('point2: ', app.coordinates)
res = app.hausdorff_similarity(app.point1, app.coordinates, 20)
print(res)
#app.drawPoint(app.point1)
#app.drawPoint(app.coordinates)