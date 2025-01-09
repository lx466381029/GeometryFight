import subprocess
import sys

def install_dev():
    try:
        # 使用pip安装项目（开发模式）
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("开发模式安装成功！")
    except subprocess.CalledProcessError as e:
        print(f"安装失败：{e}")
        sys.exit(1)

if __name__ == "__main__":
    install_dev() 