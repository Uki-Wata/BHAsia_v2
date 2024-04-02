from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI

def create_agent(input):
    tools = [PythonREPLTool()]
    instructions = """You are an agent designed to write and execute python code to answer questions. You have access to a python REPL, which you can use to execute python code. If you get an error, debug your code and try again. Only use the output of your code to answer the question. You might know the answer without running any code, but you should still run the code to get the answer. If it does not seem like you can write code to answer the question, just return "I don't know" as the answer. """
    base_prompt = hub.pull("hwchase17/openai-functions-agent")
    prompt = base_prompt.partial(instructions=instructions)
    agent = create_openai_functions_agent(ChatOpenAI(temperature=0), tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    input_text = f"""
    Run the code below with python diagrams and save the output to the current path.
    {input}
    """

    result = agent_executor.invoke({"input": input_text})
    return result

if __name__ == "__main__":
    input_text = ""
    result = create_agent(input_text)
    print(result)

