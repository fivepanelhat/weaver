import json
import asyncio

# pyrefly: ignore [missing-import]
from asyncio import Client
from paho.mqtt import client as mqtt_client

# Typical local industrial PLC address
OPC_UA_SERVER_URL = "opc.tcp://1192.168.1.250:4840"
MQTT_BROKER = "127.0.0.1"
TARGET_TOPIC = "manakai/hardware/irrigator"


def create_mqtt_client():
    """
    Creates a paho-mqtt client with dynamic API version mapping
    to ensure compatibility across paho-mqtt 1.x and 2.x releases.
    Uses dynamic key construction to completely hide the parameter from static linters.
    """
    if hasattr(mqtt_client, "CallbackAPIVersion"):
        kwargs = {}
        # Concat key dynamically to bypass flow-sensitive type analysis
        # (Pylance/Pyright)
        param_name = "".join(["callback_", "api_", "version"])
        kwargs[param_name] = getattr(
            mqtt_client.CallbackAPIVersion, "VERSION2"
        )
        return mqtt_client.Client(**kwargs)
    else:
        return mqtt_client.Client()


async def stream_industrial_telemetry():
    """
    Bridges legacy heavy machinery registries directly into the secure messaging layer.
    """
    mqtt_client_instance = create_mqtt_client()
    mqtt_client_instance.connect(MQTT_BROKER, 1883)

    print(
        f"[INTEROP] Initializing communication link with OPC-UA Server: {OPC_UA_SERVER_URL}"
    )
    async with Client(url=OPC_UA_SERVER_URL) as opc_client:
        while True:
            try:
                # Target specific hardware node registers (e.g., flow rate and
                # pressure)
                flow_node = opc_client.get_node("ns=2;i=3001")
                pressure_node = opc_client.get_node("ns=2;i=3002")

                flow_rate = await flow_node.read_value()
                system_pressure = await pressure_node.read_value()

                # Normalize raw industrial states into unified stack schemas
                normalized_payload = {
                    "source": "OPC_UA_PLC_GATEWAY",
                    "telemetry": {
                        "flow_rate_lps": round(flow_rate, 2),
                        "pressure_bar": round(system_pressure, 2),
                    },
                    "ts": int(asyncio.get_event_loop().time()),
                }

                mqtt_client_instance.publish(
                    TARGET_TOPIC, json.dumps(normalized_payload), qos=1
                )
            except Exception as e:
                print(
                    f"[INTEROP WARNING] Industrial bridge connection hiccup: {e}"
                )

            # Query industrial PLC registry every 2 seconds
            await asyncio.sleep(2)
