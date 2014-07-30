# SOL Design

![Igor SOL Design](https://docs.google.com/drawings/d/1YiY9cBmCVGKoQG-12gxCHKqPBhJaLBg977aIyM7tgYs/pub?w=804&h=627 "Igor SOL Design")

*[Diagram source](https://docs.google.com/drawings/d/1YiY9cBmCVGKoQG-12gxCHKqPBhJaLBg977aIyM7tgYs/edit?usp=sharing)*

The SOL console is asynchronous and full-duplex by nature, whereas REST over HTTP is synchronous and half-duplex.
The proposed design bridges this limitation by maintaing a producer-consumer queue for each user on the Igor server,
containing commands and responses collected from the user and the IPMI controller.

An alternative idea to explore is [WebSockets](https://www.websocket.org/).
