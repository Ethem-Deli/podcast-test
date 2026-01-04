import yaml
import xml.etree.ElementTree as ET

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"

ET.register_namespace("itunes", ITUNES_NS)
ET.register_namespace("content", CONTENT_NS)

with open("feed.yaml", "r", encoding="utf-8") as file:
    yaml_data = yaml.safe_load(file)

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

link_prefix = yaml_data["link"]

ET.SubElement(channel, "title").text = yaml_data["title"]
ET.SubElement(channel, "subtitle").text = yaml_data["subtitle"]
ET.SubElement(channel, f"{{{ITUNES_NS}}}author").text = yaml_data["author"]
ET.SubElement(channel, "description").text = yaml_data["description"]
ET.SubElement(channel, "language").text = yaml_data["language"]
ET.SubElement(channel, "link").text = link_prefix

ET.SubElement(
    channel,
    f"{{{ITUNES_NS}}}image",
    href=link_prefix + yaml_data["image"]
)

ET.SubElement(
    channel,
    f"{{{ITUNES_NS}}}category",
    text=yaml_data["category"]
)

for item in yaml_data["item"]:
    item_el = ET.SubElement(channel, "item")

    ET.SubElement(item_el, "title").text = item["title"]
    ET.SubElement(item_el, f"{{{ITUNES_NS}}}author").text = yaml_data["author"]
    ET.SubElement(item_el, "description").text = item["description"]
    ET.SubElement(item_el, f"{{{ITUNES_NS}}}duration").text = item["duration"]
    ET.SubElement(item_el, "pubDate").text = item["published"]

    ET.SubElement(
        item_el,
        "enclosure",
        url=link_prefix + item["file"],
        length=str(item["length"]),
        type="audio/mpeg",
    )

tree = ET.ElementTree(rss)
tree.write("podcast.xml", encoding="utf-8", xml_declaration=True)
