from typing import override

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value

        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
