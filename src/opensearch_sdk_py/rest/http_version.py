from enum import Enum

HttpVersion = Enum(
    "HttpVersion",
    ["HTTP_1_0", "HTTP_1_1"],
    start=0
)
