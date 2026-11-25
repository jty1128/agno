from agno.agent import Agent, RunEvent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools


def test_streaming():
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        show_tool_calls=True,
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = agent.run("Hi, my name is John", stream=True)

    chunks: list[RunResponse] = list(response)

    assert len(chunks) > 0
    assert chunks[0].content is not None
    assert chunks[-1].content is not None
    assert chunks[0].content != chunks[-1].content


async def test_async_streaming():
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        show_tool_calls=True,
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = await agent.arun("Hi, my name is John", stream=True)

    chunks: list[RunResponse] = [chunk async for chunk in response]

    assert len(chunks) > 0
    assert chunks[0].content is not None
    assert chunks[-1].content is not None
    assert chunks[0].content != chunks[-1].content


def test_tool_streaming():
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools(cache_results=True)],
        show_tool_calls=True,
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = agent.run("Tell me the latest news in France", stream=True)

    chunks: list[RunResponse] = list(response)
    tool_calls: bool = any(chunk.tools for chunk in chunks)

    assert len(chunks) > 0
    assert tool_calls


async def test_async_tool_streaming():
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools(cache_results=True)],
        show_tool_calls=True,
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = await agent.arun("Tell me the latest news in France", stream=True)

    chunks: list[RunResponse] = [chunk async for chunk in response]
    tool_calls: bool = any(chunk.tools for chunk in chunks)

    assert len(chunks) > 0
    assert tool_calls


def test_streaming_with_intermediate_steps():
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        show_tool_calls=True,
        stream_intermediate_steps=True,
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = agent.run("Tell me the latest news in France", stream=True)

    chunks: list[RunResponse] = list(response)
    run_started: bool = any(chunk.event == RunEvent.run_started.value for chunk in chunks)
    run_response: bool = any(chunk.event == RunEvent.run_response.value for chunk in chunks)
    run_completed: bool = any(chunk.event == RunEvent.run_completed.value for chunk in chunks)

    assert len(chunks) > 0
    assert run_started
    assert run_completed
    assert run_response


async def test_async_streaming_with_intermediate_steps():
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        show_tool_calls=True,
        stream_intermediate_steps=True,
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = await agent.arun("Tell me the latest news in France", stream=True)

    chunks: list[RunResponse] = [chunk async for chunk in response]
    run_started: bool = any(chunk.event == RunEvent.run_started.value for chunk in chunks)
    run_completed: bool = any(chunk.event == RunEvent.run_completed.value for chunk in chunks)
    run_response: bool = any(chunk.event == RunEvent.run_response.value for chunk in chunks)

    assert len(chunks) > 0
    assert run_started
    assert run_completed
    assert run_response


def test_tool_call_streaming_with_intermediate_steps():
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools(cache_results=True)],
        show_tool_calls=True,
        stream_intermediate_steps=True,
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = agent.run("Tell me the latest news in France", stream=True)

    chunks: list[RunResponse] = list(response)
    run_started: bool = any(chunk.event == RunEvent.run_started.value for chunk in chunks)
    run_completed: bool = any(chunk.event == RunEvent.run_completed.value for chunk in chunks)
    run_response: bool = any(chunk.event == RunEvent.run_response.value for chunk in chunks)
    tool_call_started: bool = any(chunk.event == RunEvent.tool_call_started.value for chunk in chunks)
    tool_call_completed: bool = any(chunk.event == RunEvent.tool_call_completed.value for chunk in chunks)

    assert len(chunks) > 0
    assert run_started
    assert run_completed
    assert run_response
    assert tool_call_started
    assert tool_call_completed


async def test_async_tool_call_streaming_with_intermediate_steps():
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools(cache_results=True)],
        show_tool_calls=True,
        stream_intermediate_steps=True,
        markdown=True,
        telemetry=False,
        monitoring=False,
    )

    response = await agent.arun("Tell me the latest news in France", stream=True)

    chunks: list[RunResponse] = [chunk async for chunk in response]
    run_started: bool = any(chunk.event == RunEvent.run_started.value for chunk in chunks)
    run_completed: bool = any(chunk.event == RunEvent.run_completed.value for chunk in chunks)
    run_response: bool = any(chunk.event == RunEvent.run_response.value for chunk in chunks)
    tool_call_started: bool = any(chunk.event == RunEvent.tool_call_started.value for chunk in chunks)
    tool_call_completed: bool = any(chunk.event == RunEvent.tool_call_completed.value for chunk in chunks)

    assert len(chunks) > 0
    assert run_started
    assert run_completed
    assert run_response
    assert tool_call_started
    assert tool_call_completed
