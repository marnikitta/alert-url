import logging
import os
import socket

logger = logging.getLogger(__name__)


def try_notify_systemd() -> None:
    systemd_socket = os.getenv("NOTIFY_SOCKET")
    if systemd_socket:
        logger.info("Notifying systemd")
        notify_systemd(systemd_socket)


def notify_systemd(notify_socket: str) -> None:
    # Ensure the socket path starts with a '@' if it's abstract
    if notify_socket.startswith("@"):
        notify_socket = "\0" + notify_socket[1:]

    # Create a socket and connect to the systemd notify socket
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as sock:
            sock.connect(notify_socket)
            sock.sendall(b"READY=1")
            logger.info("Notification sent: READY=1")
    except Exception as e:
        logger.exception("Failed to notify", e)
