from typing import override

from components.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")

        if not self.children:
            raise ValueError("All parent nodes must have children")

        parent_opening = ""

        if self.props:
            parent_opening = f"<{self.tag}{self.props_to_html()}>"
        else:
            parent_opening = f"<{self.tag}>"

        for child in self.children:
            parent_opening += child.to_html()

        parent_closing = f"</{self.tag}>"

        return parent_opening + parent_closing
