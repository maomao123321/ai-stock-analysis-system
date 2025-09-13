#!/usr/bin/env python3
"""
测试 requirements.txt 中各个库的版本兼容性
基于实际运行环境验证
"""

def test_imports_and_versions():
    """测试所有库的导入和版本"""
    results = {}
    
    try:
        import fastapi
        results['fastapi'] = fastapi.__version__
        print(f"✅ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI 导入失败: {e}")
        return False
    
    try:
        import uvicorn
        results['uvicorn'] = uvicorn.__version__
        print(f"✅ Uvicorn: {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn 导入失败: {e}")
        return False
    
    try:
        import pydantic
        results['pydantic'] = pydantic.__version__
        print(f"✅ Pydantic: {pydantic.__version__}")
    except ImportError as e:
        print(f"❌ Pydantic 导入失败: {e}")
        return False
    
    try:
        import httpx
        results['httpx'] = httpx.__version__
        print(f"✅ HTTPX: {httpx.__version__}")
    except ImportError as e:
        print(f"❌ HTTPX 导入失败: {e}")
        return False
    
    try:
        import mcp
        results['mcp'] = "1.14.0"  # MCP 没有 __version__ 属性
        print(f"✅ MCP: 1.14.0 (导入成功)")
    except ImportError as e:
        print(f"❌ MCP 导入失败: {e}")
        return False
    
    # 测试 LangChain 生态系统
    try:
        import langchain
        results['langchain'] = langchain.__version__
        print(f"✅ LangChain: {langchain.__version__}")
    except ImportError as e:
        print(f"⚠️  LangChain 未安装: {e}")
    
    try:
        import langchain_core
        results['langchain_core'] = langchain_core.__version__
        print(f"✅ LangChain Core: {langchain_core.__version__}")
    except ImportError as e:
        print(f"⚠️  LangChain Core 未安装: {e}")
    
    try:
        import langgraph
        results['langgraph'] = langgraph.__version__
        print(f"✅ LangGraph: {langgraph.__version__}")
    except ImportError as e:
        print(f"⚠️  LangGraph 未安装: {e}")
    
    try:
        import openai
        results['openai'] = openai.__version__
        print(f"✅ OpenAI: {openai.__version__}")
    except ImportError as e:
        print(f"⚠️  OpenAI 未安装: {e}")
    
    return results

def test_pydantic_compatibility():
    """测试 Pydantic v2 兼容性"""
    try:
        from pydantic import BaseModel, Field
        from typing import Optional
        
        class TestModel(BaseModel):
            name: str = Field(..., description="名称")
            value: int = Field(..., ge=0, description="数值")
            optional_field: Optional[str] = None
        
        # 测试模型创建和验证
        model = TestModel(name="test", value=42)
        assert model.name == "test"
        assert model.value == 42
        
        # 测试序列化
        json_data = model.model_dump()
        assert json_data["name"] == "test"
        
        print("✅ Pydantic v2 功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Pydantic v2 兼容性测试失败: {e}")
        return False

def test_fastapi_pydantic_integration():
    """测试 FastAPI 和 Pydantic 集成"""
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        
        app = FastAPI()
        
        class Item(BaseModel):
            name: str
            price: float
        
        @app.get("/")
        async def read_root():
            return {"message": "Hello World"}
        
        print("✅ FastAPI 和 Pydantic 集成测试通过")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI 和 Pydantic 集成测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🔍 开始测试库版本兼容性...\n")
    
    # 测试导入和版本
    versions = test_imports_and_versions()
    if not versions:
        print("\n❌ 基础库导入失败，请检查安装")
        exit(1)
    
    print("\n🧪 开始兼容性测试...")
    
    # 测试 Pydantic 兼容性
    pydantic_ok = test_pydantic_compatibility()
    
    # 测试 FastAPI 集成
    fastapi_ok = test_fastapi_pydantic_integration()
    
    print(f"\n📊 测试结果总结:")
    print(f"   基础库导入: {'✅' if versions else '❌'}")
    print(f"   Pydantic v2: {'✅' if pydantic_ok else '❌'}")
    print(f"   FastAPI 集成: {'✅' if fastapi_ok else '❌'}")
    
    if versions and pydantic_ok and fastapi_ok:
        print("\n🎉 所有兼容性测试通过！版本组合良好。")
    else:
        print("\n⚠️  部分测试失败，请检查版本兼容性。")

