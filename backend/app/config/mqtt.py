from __future__ import annotations

import logging
import threading
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

_mqtt_client: Any | None = None
_mqtt_thread: threading.Thread | None = None


def _handle_message(_: Any, __: Any, msg: Any) -> None:
    logger.info("Received MQTT message on %s: %s", msg.topic, msg.payload.decode(errors="ignore"))


def start_mqtt() -> None:
    global _mqtt_client, _mqtt_thread

    if _mqtt_client is not None:
        return

    try:
        import paho.mqtt.client as mqtt
    except ImportError:
        logger.warning("paho-mqtt is unavailable; skipping MQTT startup")
        return

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if settings.MQTT_USERNAME:
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    def on_connect(client: mqtt.Client, *_: Any) -> None:
        logger.info("Connected to MQTT broker")
        client.subscribe(settings.MQTT_TOPIC)

    client.on_connect = on_connect
    client.on_message = _handle_message
    client.connect_async(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)

    thread = threading.Thread(
        target=lambda: client.loop_forever(retry_first_connection=True),
        name="mqtt-listener",
        daemon=True,
    )
    thread.start()

    _mqtt_client = client
    _mqtt_thread = thread


def stop_mqtt() -> None:
    global _mqtt_client, _mqtt_thread

    if _mqtt_client is None:
        return

    try:
        _mqtt_client.disconnect()
    except Exception:
        logger.exception("Failed to disconnect MQTT client cleanly")

    if _mqtt_thread is not None:
        _mqtt_thread.join(timeout=2)

    _mqtt_client = None
    _mqtt_thread = None
