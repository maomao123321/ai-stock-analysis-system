#!/usr/bin/env python3
"""
测试 requirements.txt 中各个库的兼容性
"""

def test_imports():
    """测试所有库的导入"""
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
        
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__}")
        
        import langchain
        print(f"✅ LangChain {langchain.__version__}")
        
        import langchain_core
        print(f"✅ LangChain Core {langchain_core.__version__}")
        
        import langgraph
        print(f"✅ LangGraph {langgraph.__version__}")
        
        import openai
        print(f"✅ OpenAI {openai.__version__}")
        
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__}")
        
        import httpx
        print(f"✅ HTTPX {httpx.__version__}")
        
        import mcp
        print(f"✅ MCP {mcp.__version__}")
        
        print("\n🎉 所有库导入成功！版本兼容性良好。")
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_pydantic_langgraph_compatibility():
    """测试 Pydantic 和 LangGraph 的兼容性"""
    try:
        from pydantic import BaseModel
        from langgraph.graph import StateGraph
        
        # 创建一个简单的 Pydantic 模型
        class TestModel(BaseModel):
            name: str
            value: int
        
        # 测试 LangGraph 是否能使用 Pydantic 模型
        def test_node(state: TestModel) -> TestModel:
            return state
        
        # 创建状态图
        graph = StateGraph(TestModel)
        graph.add_node("test", test_node)
        
        print("✅ Pydantic 和 LangGraph 兼容性测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Pydantic 和 LangGraph 兼容性测试失败: {e}")
        return False

def test_fastapi_openai_compatibility():
    """测试 FastAPI 和 OpenAI 的兼容性"""
    try:
        from fastapi import FastAPI
        from openai import OpenAI
        
        app = FastAPI()
        client = OpenAI()
        
        print("✅ FastAPI 和 OpenAI 兼容性测试通过")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI 和 OpenAI 兼容性测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🔍 开始测试库兼容性...\n")
    
    success = True
    success &= test_imports()
    success &= test_pydantic_langgraph_compatibility()
    success &= test_fastapi_openai_compatibility()
    
    if success:
        print("\n🎉 所有兼容性测试通过！")
    else:
        print("\n❌ 部分测试失败，请检查版本兼容性。")

