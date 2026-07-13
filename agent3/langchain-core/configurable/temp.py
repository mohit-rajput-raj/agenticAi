from langchain_core.runnables import ConfigurableField, RunnableSerializable


class EchoWithTemperature(RunnableSerializable[str, str]):
    """Tiny runnable that shows how configurable fields work."""

    temperature: float = 0.7

    def invoke(self, input: str, config=None, **kwargs) -> str:
        return f"Generated with temp={self.temperature}: {input}"


runnable = EchoWithTemperature().configurable_fields(
    temperature=ConfigurableField(
        id="temperature",
        name="Temperature",
        description="Controls randomness in the output",
    )
)

print(runnable.invoke("Hello"))
print(runnable.with_config(configurable={"temperature": 0.9}).invoke("Hello"))
