from enum import Enum

RestMethod = Enum(
    "RestMethod",
    ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE", "CONNECT"],
    start=0
)
