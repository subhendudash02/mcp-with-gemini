from google import genai
from google.genai import types
from dotenv import load_dotenv
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters, ListToolsResult
import os
import asyncio

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
server = StdioServerParameters(
    command="python",
    args=["server.py"],
    env=None
)

prompt = "Find number of students having marks1 between 40 to 70."

def create_gemini_tools(mcp_tools: ListToolsResult):
    tools = [
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )
                for tool in mcp_tools.tools
            ]
    return tools

async def run():
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = await session.list_tools()
            tools = create_gemini_tools(mcp_tools)

            response = client.models.generate_content(
                model="gemini-2.0-flash",   # choose appropriate model name
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    tools=tools,
                ),
            )

            if (response.candidates[0].content.parts[0].function_call):
                # if gemini correctly identifies the mcp server function declaration correctly
                function_call = response.candidates[0].content.parts[0].function_call

                result = await session.call_tool(
                    function_call.name, arguments=dict(function_call.args)
                )

                print(result.content[0].text)

            else:
                print("No function call was generated by the model.")
                if response.text:
                     print("Model response:")
                     print(response.text)



asyncio.run(run())