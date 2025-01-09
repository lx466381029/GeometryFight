import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入所有测试
from tests.test_scenes import TestScenes

def run_tests():
    """运行所有测试"""
    # 创建测试加载器
    loader = unittest.TestLoader()
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestScenes))
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    # 如果测试失败，使用非零状态码退出
    sys.exit(0 if success else 1) 