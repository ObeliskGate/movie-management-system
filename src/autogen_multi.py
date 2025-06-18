from flask import render_template, request, jsonify
from sqlalchemy import (
    inspect,
    text,
)
import configparser

# 初始化AutoGen
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

from src.init import get_db

config = configparser.ConfigParser()
config.read('config.ini')

config_list = [
    {
        "model": config.get('agent', 'model'),
        "api_key": config.get('agent', 'api_key'),
        "base_url": config.get('agent', 'base_url')
    }
]

# 创建SQL代理
sql_agent = AssistantAgent(
    name="SQL_Agent",
    llm_config={
        "config_list": config_list,
        "tools": [{
            "type": "function",
            "function": {
                "name": "explore_database",
                "description": "Get database schema and sample data",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }, {
            "type": "function",
            "function": {
                "name": "query_database",
                "description": "Execute SQL queries after exploring the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query to execute"
                        }
                    },
                    "required": ["query"]
                }
            }
        }]
    },
    system_message="""You are a SQL expert that can query the FILMS database using SQLAlchemy.
    Before executing any query:
    1. First explore the database structure using explore_database, but pay attention the explore_database only provide sampled data instead of total data
    2. Analyze the available columns
    3. Then construct an appropriate SQL query
    4. Execute the query and explain results
    
    Always format your responses as follows:
    1. Show the SQL query you're using and explain the results together
    """
)

# 创建主助手代理
assistant = AssistantAgent(
    name="Assistant",
    llm_config={
        "config_list": config_list,
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "explore_database",
                    "description": "Get database schema and sample data",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_database",
                    "description": "Execute SQL queries after exploring the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The SQL query to execute",
                            }
                        },
                        "required": ["query"],
                    },
                },
            },
        ],
    },
    system_message="""You are a helpful assistant for querying film information.
    Always explore the database first using explore_database before executing any queries.
    Pay attention that the information you get through explore_database is limited, which just help you to understand the column of the schema.
    Make sure to understand the available data before constructing SQL queries.
    Only `SELECT `query operations are permitted, as other actions are unsafe."""
)

# 创建用户代理实例
user_proxy = UserProxyAgent(
    name="User_proxy",
    human_input_mode="NEVER",  
    is_termination_msg=lambda x: x.get("tool_calls") is None,
    code_execution_config=False,
    llm_config={"config_list": config_list},
)

MOVIE_TABLE_NAMES = [
    "production_company",
    "actor_info",
    "director_info",
    "movie_info",
    "role_info",
    "actor_movie_relation",
    "director_movie_relation"
]

# 注册工具函数
@user_proxy.register_for_execution()
@assistant.register_for_llm(name="explore_database")
def explore_database() -> str:
    """Get database schema and sample data"""
    engine = get_db().engine
    try:
        with engine.connect() as con:
            # 获取表结构
            inspector = inspect(engine)
            ret = ""
            for name in MOVIE_TABLE_NAMES:
                columns = inspector.get_columns(name)
                schema = f"Table name: {name}\nTable Schema:\n" + "\n".join([f"- {col['name']}: {col['type']}" for col in columns])
                
                # 获取样本数据
                result = con.execute(text(f"SELECT * FROM {name} LIMIT 3"))
                rows = result.fetchall()
                
                sample_data = f"\nSample Data from {name}:\n"
                if rows:
                    columns = result.keys()
                    sample_data += " | ".join(columns) + "\n"
                    sample_data += "-" * 50 + "\n"
                    for row in rows:
                        sample_data += " | ".join(str(value) for value in row) + "\n"

                ret += f"{schema}\n\n{sample_data}\n\n"
                
            return ret.strip()
    except Exception as e:
        return f"""
            异常类型: {type(e)}
            异常 args: {e.args}
            异常 repr: {repr(e)}
        """

@user_proxy.register_for_execution()
@assistant.register_for_llm(name="query_database")
def query_database(query: str) -> str:
    """Execute SQL query on the FILMS database"""
    try:
        db = get_db()
        engine = db.engine
        with engine.connect() as con:
            result = con.execute(text(query))
            rows = result.fetchall()
            if not rows:
                return "No results found."
            
            # 将结果格式化为更易读的形式
            columns = result.keys()
            output = "\nResults:\n"
            output += "-" * 50 + "\n"
            output += " | ".join(columns) + "\n"
            output += "-" * 50 + "\n"
            
            for row in rows:
                output += " | ".join(str(value) for value in row) + "\n"
            
            return output
    except Exception as e:
        return f"""
            异常类型: {type(e)}
            异常 args: {e.args}
            异常 repr: {repr(e)}
        """


async def get_reply(input: str, clear_history=False) -> str:
    try:    
        len_before = len(list(user_proxy.chat_messages.values())[0])
        await user_proxy.a_initiate_chat(
            assistant,
            message=input,
            clear_history=clear_history,
        )
        after_list = list(user_proxy.chat_messages.values())[0]
        get_content = lambda t: t.get("content", "No reply") if t else "No reply"
        
        contents = []
        for it in after_list[len_before:]:
            if it.get("role") != "user":
                continue
            current_content = get_content(it)
            if current_content:
                contents.append(current_content)
        return "\n --- \n".join(contents)

    except Exception as e:
        return f"Error: {str(e)}"


def set_chat_route(app):
    @app.route('/chat')
    async def chat():
        return render_template('chat.html')

    @app.route('/api/chat', methods=['POST'])
    async def _query():
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({'error': '查询不能为空'}), 400

        try:
            # 直接发送用户输入到现有对话

            result = await get_reply(user_input)
            return jsonify({'response': result})
        except Exception as e:
            return jsonify({'error': f"查询失败: {str(e)}"}), 500
        

    @app.route('/api/init_chat')
    async def _init_chat():
        # 单独处理初始化
        await user_proxy.a_initiate_chat(
            assistant,
            message="请预加载数据库中的数据",
            # max_turns=2,
            clear_history=True,
        )
        return jsonify({"status": "success"})
        