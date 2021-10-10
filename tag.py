from motor.motor_asyncio import AsyncIOMotorClient
import json

client = AsyncIOMotorClient("", tls=True, tlsAllowInvalidCertificates=True)

col = client.hitomi.info


async def female_male_tag():
    female_tags = []
    male_tags = []
    raw_tags = []

    mapping = {"female": female_tags, "male": male_tags, "tag": raw_tags}

    async for i in col.find({}, {"tags": 1}):
        for tag_info in i["tags"]:
            value = tag_info["value"]
            if "♀" in value:
                replaced = value.replace(" ♀", "")
                if replaced not in female_tags:
                    female_tags.append(replaced)
            elif "♂" in value:
                replaced = value.replace(" ♂", "")
                if replaced not in male_tags:
                    male_tags.append(replaced)
            else:
                if value not in raw_tags:
                    raw_tags.append(value)

    for tag_type in ["female", "male", "tag"]:
        with open(f"./tags/{tag_type}.json", "w+", encoding="UTF-8") as f:
            f.write(json.dumps(mapping[tag_type]))


async def main():
    tag_list = []

    for tag_type in [
        "group",
        "series",
        "artist",
        "characters",
    ]:
        async for i in col.find({}, {tag_type: 1}):
            for tag_info in i[tag_type]:
                if tag_info["value"] not in tag_list:
                    tag_list.append(tag_info["value"])

        with open(f"./tags/{tag_type}.json", "w+", encoding="UTF-8") as f:
            f.write(json.dumps(tag_list))

        tag_list.clear()

    await female_male_tag()


import asyncio

asyncio.get_event_loop().run_until_complete(female_male_tag())
