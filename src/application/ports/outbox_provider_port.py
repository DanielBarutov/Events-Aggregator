import typing


class OutboxProviderPort(typing.Protocol):
    async def execute(self, payload): ...
