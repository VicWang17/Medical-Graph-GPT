# Medical-Graph-GPT

Medical-Graph-GPT 是一个医疗知识图谱构建工具。

## 功能特点

- 🔍 自动从医疗文本中提取实体和关系
- 🤖 利用 ChatGPT 进行智能文本分析
- 📊 将提取的知识存储到 Neo4j 图数据库
- 🔄 支持批量处理医疗文本数据
- 📝 详细的日志记录功能

## 系统要求

- Python 3.6+
- Neo4j 数据库
- ChatGPT API 访问权限

## 安装步骤

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/Medical-Graph-GPT.git
cd Medical-Graph-GPT
```

2. 安装依赖包：
```bash
pip install flask py2neo requests
```

3. 配置 Neo4j 数据库：
   - 确保 Neo4j 数据库已安装并运行
   - 默认连接配置：
     - URL: bolt://localhost:7687
     - 用户名: xxxx
     - 密码: xxxxxxxx

4. 配置 ChatGPT API：
   - 在 `api.py` 中设置正确的 ChatGPT API URL

## 使用方法

1. 准备医疗文本数据：
   - 将需要处理的医疗文本放入 `data.txt` 文件中
   - 每行一条文本记录

2. 启动服务器：
```bash
python run_server.py
```

3. 发送处理请求：
   - 向 `http://localhost:5000/re` 发送 POST 请求
   - 系统将自动处理文本并构建知识图谱

## 项目结构

- `api.py`: 主要的 API 实现，包含文本处理和 ChatGPT 调用逻辑
- `data2neo.py`: Neo4j 数据库操作相关代码
- `run_server.py`: 服务器启动脚本
- `data.txt`: 待处理的医疗文本数据
- `info.log`: 运行日志文件

## 注意事项

- 确保 Neo4j 数据库正常运行
- 检查 ChatGPT API 的可用性和配置
- 处理大量数据时注意 API 调用频率限制
- 定期备份 Neo4j 数据库

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License
